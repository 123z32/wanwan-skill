/**
 * ESP8266 Modbus RTU ↔ TCP 透明透传网关
 * 
 * 功能：
 *   - TCP Server（端口 502），监听上位机连接
 *   - 双向透明转发：TCP ↔ UART（115200 8N1）
 *   - 不解析 Modbus 协议，纯字节流桥接
 *   - 支持单客户端连接（Modbus RTU 半总线特性决定）
 *   - 断线自动清理，支持重连
 * 
 * 硬件接线：
 *   - ESP8266 TX (GPIO1) → STM32F407 RX (PA3/USART2)
 *   - ESP8266 RX (GPIO3) → STM32F407 TX (PA2/USART2)
 *   - 共地！
 * 
 * 网络配置：
 *   - 修改下方 WiFi SSID/密码
 *   - 建议路由器固定 IP 或使用静态 IP
 * 
 * 作者：绾绾
 * 日期：2026-04-11
 */

#include <ESP8266WiFi.h>
#include <ESP8266mDNS.h>

// ================= 配置区 =================

// WiFi 配置
const char* WIFI_SSID = "Your_WiFi_SSID";
const char* WIFI_PASSWORD = "Your_WiFi_Password";

// 网关配置
const uint16_t TCP_PORT = 502;          // Modbus TCP 默认端口
const uint32_t SERIAL_BAUD = 115200;    // 与 STM32F407 USART2 一致
const uint16_t SERIAL_RX_BUF_SIZE = 512; // 串口接收缓冲区
const uint32_t CLIENT_TIMEOUT_MS = 30000; // 客户端超时断开（30s）
const uint16_t WATCHDOG_TIMEOUT_MS = 500; // 看门狗喂狗间隔

// ================= 全局变量 =================

WiFiServer tcpServer(TCP_PORT);
WiFiClient tcpClient;

unsigned long lastClientActivity = 0;
unsigned long lastWatchdogFeed = 0;
bool clientConnected = false;

// 串口接收缓冲（软件环形缓冲）
uint8_t serialRxBuf[SERIAL_RX_BUF_SIZE];
volatile uint16_t serialWriteIdx = 0;
volatile uint16_t serialReadIdx = 0;
volatile uint16_t serialBufCount = 0;

// ================= 中断服务函数 =================

/**
 * UART 接收中断回调
 * 将接收到的字节存入环形缓冲区
 */
void ICACHE_RAM_ATTR onSerialRx() {
  while (Serial.available()) {
    uint8_t byte = Serial.read();
    if (serialBufCount < SERIAL_RX_BUF_SIZE) {
      serialRxBuf[serialWriteIdx] = byte;
      serialWriteIdx = (serialWriteIdx + 1) % SERIAL_RX_BUF_SIZE;
      serialBufCount++;
    }
    // 缓冲区满时丢弃旧数据（不应该发生，正常 Modbus 帧很小）
  }
}

// ================= 辅助函数 =================

/**
 * 从环形缓冲区读取数据到 TCP
 */
void flushSerialToTcp() {
  if (serialBufCount == 0 || !clientConnected) return;

  noInterrupts();
  uint16_t count = serialBufCount;
  uint16_t readIdx = serialReadIdx;
  interrupts();

  // 批量发送，避免逐字节
  uint8_t chunk[64];
  while (count > 0) {
    uint16_t toRead = min(count, (uint16_t)sizeof(chunk));
    for (uint16_t i = 0; i < toRead; i++) {
      chunk[i] = serialRxBuf[readIdx];
      readIdx = (readIdx + 1) % SERIAL_RX_BUF_SIZE;
    }

    if (tcpClient.write(chunk, toRead) > 0) {
      noInterrupts();
      serialReadIdx = readIdx;
      serialBufCount -= toRead;
      count -= toRead;
      interrupts();
    } else {
      // TCP 发送失败，断开连接
      return;
    }
  }
}

/**
 * 从 TCP 读取数据写入串口
 */
void flushTcpToSerial() {
  if (!clientConnected || !tcpClient.available()) return;

  uint8_t buf[128];
  int len = tcpClient.read(buf, sizeof(buf));
  if (len > 0) {
    Serial.write(buf, len);
    Serial.flush();  // 等待发送完成，确保字节已发出
    lastClientActivity = millis();
  }
}

/**
 * 检查客户端超时
 */
void checkClientTimeout() {
  if (clientConnected && (millis() - lastClientActivity > CLIENT_TIMEOUT_MS)) {
    tcpClient.stop();
    clientConnected = false;
    Serial.println(F("[INFO] Client timeout, disconnected"));
  }
}

/**
 * 清理串口接收缓冲区（客户端断开时）
 */
void clearSerialBuffer() {
  noInterrupts();
  serialWriteIdx = 0;
  serialReadIdx = 0;
  serialBufCount = 0;
  interrupts();
}

// ================= 初始化 =================

void setup() {
  // 串口初始化（与 STM32F407 USART2 参数一致）
  Serial.begin(SERIAL_BAUD, SERIAL_8N1);
  Serial.setRxBufferSize(SERIAL_RX_BUF_SIZE);
  attachInterrupt(digitalPinToInterrupt(3), onSerialRx, CHANGE);  // GPIO3 = RX

  // LED 指示（GPIO2 板载 LED）
  pinMode(2, OUTPUT);
  digitalWrite(2, HIGH);  // 熄灭（低电平点亮）

  Serial.println();
  Serial.println(F("==============================="));
  Serial.println(F("ESP8266 Modbus RTU/TCP Gateway"));
  Serial.println(F("Transparent Bridge Mode"));
  Serial.println(F("==============================="));

  // WiFi 连接
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  Serial.print(F("[INFO] Connecting to WiFi"));
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(F("."));
    // 闪烁 LED 表示正在连接
    digitalWrite(2, !digitalRead(2));
  }
  digitalWrite(2, HIGH);  // 连接成功，熄灭

  Serial.println();
  Serial.print(F("[INFO] WiFi connected. IP: "));
  Serial.println(WiFi.localIP());

  // mDNS（可选，方便通过主机名访问）
  if (MDNS.begin("modbus-gw")) {
    Serial.println(F("[INFO] mDNS responder started: modbus-gw.local"));
  }

  // 启动 TCP Server
  tcpServer.begin();
  tcpServer.setNoDelay(true);  // 禁用 Nagle 算法，降低延迟
  Serial.print(F("[INFO] TCP server started on port "));
  Serial.println(TCP_PORT);

  // 清除可能残留的串口数据
  clearSerialBuffer();

  Serial.println(F("[INFO] Gateway ready, waiting for client..."));
  Serial.println(F("==============================="));
}

// ================= 主循环 =================

void loop() {
  // 喂狗（ESP8266 软件看门狗）
  if (millis() - lastWatchdogFeed > WATCHDOG_TIMEOUT_MS) {
    ESP.wdtFeed();
    lastWatchdogFeed = millis();
  }

  // 处理新客户端连接
  if (!clientConnected) {
    tcpClient = tcpServer.available();
    if (tcpClient && tcpClient.connected()) {
      clientConnected = true;
      lastClientActivity = millis();
      clearSerialBuffer();  // 新连接，清空旧数据
      digitalWrite(2, LOW);  // LED 点亮，表示有连接
      Serial.print(F("[INFO] Client connected: "));
      Serial.println(tcpClient.remoteIP());
    }
  } else {
    // 检查客户端是否断开
    if (!tcpClient.connected()) {
      tcpClient.stop();
      clientConnected = false;
      digitalWrite(2, HIGH);  // LED 熄灭
      Serial.println(F("[INFO] Client disconnected"));
      clearSerialBuffer();
    } else {
      // 双向数据转发
      flushTcpToSerial();   // TCP → UART
      flushSerialToTcp();   // UART → TCP
      checkClientTimeout(); // 超时检查
    }
  }

  // 处理 mDNS
  MDNS.update();

  yield();  // ESP8266 系统任务
}
