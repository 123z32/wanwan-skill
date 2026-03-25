#!/usr/bin/env node
/**
 * 消息心跳监控
 * =============
 * 每 10 分钟检查是否有未回复的消息，如果有则重新思考并发送
 * 
 * 配置：
 * - 检查间隔：10 分钟
 * - 超时阈值：5 分钟（用户发消息后 5 分钟未回复则触发）
 * - 日志：memory/message-heartbeat.log
 */

const fs = require('fs');
const path = require('path');
const https = require('https');

// 配置
const CHECK_INTERVAL_MS = 10 * 60 * 1000;  // 10 分钟
const TIMEOUT_THRESHOLD_MS = 5 * 60 * 1000; // 5 分钟
const STATE_FILE = path.join(__dirname, '../memory/message-heartbeat-state.json');
const LOG_FILE = path.join(__dirname, '../memory/message-heartbeat.log');

// 飞书配置
const appId = 'cli_a93b96d250391bd4';
const appSecret = 'v4Clks3h8xwSNUZoNARFoZCIgXS8vgq0';

// 日志函数
function log(message) {
  const timestamp = new Date().toISOString();
  const line = `[${timestamp}] ${message}\n`;
  console.log(line.trim());
  fs.appendFileSync(LOG_FILE, line);
}

// 读取状态
function loadState() {
  try {
    if (fs.existsSync(STATE_FILE)) {
      return JSON.parse(fs.readFileSync(STATE_FILE, 'utf-8'));
    }
  } catch (e) {
    log(`读取状态失败：${e.message}`);
  }
  return {
    lastCheck: null,
    lastUserMessage: null,
    lastBotReply: null,
    missedReplies: 0
  };
}

// 保存状态
function saveState(state) {
  fs.writeFileSync(STATE_FILE, JSON.stringify(state, null, 2), 'utf-8');
}

// 获取 tenant_access_token
function getTenantToken() {
  return new Promise((resolve, reject) => {
    const data = JSON.stringify({ app_id: appId, app_secret: appSecret });
    const options = {
      hostname: 'open.feishu.cn',
      port: 443,
      path: '/open-apis/auth/v3/tenant_access_token/internal',
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    };
    const req = https.request(options, (res) => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => {
        try {
          const result = JSON.parse(body);
          if (result.code !== 0) {
            reject(new Error(`Token error: ${result.code} - ${result.msg}`));
          } else {
            resolve(result.tenant_access_token);
          }
        } catch (e) {
          reject(e);
        }
      });
    });
    req.on('error', reject);
    req.write(data);
    req.end();
  });
}

// 获取聊天记录
async function getRecentMessages(chatId, token) {
  return new Promise((resolve, reject) => {
    const path = `/open-apis/im/v1/messages?container_id_type=chat_id&container_id=${chatId}&page_size=20`;
    const options = {
      hostname: 'open.feishu.cn',
      port: 443,
      path: path,
      method: 'GET',
      headers: { 
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    };
    const req = https.request(options, (res) => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => {
        try {
          resolve(JSON.parse(body));
        } catch (e) {
          reject(e);
        }
      });
    });
    req.on('error', reject);
    req.end();
  });
}

// 检查未回复消息
async function checkUnrepliedMessages() {
  log('开始检查未回复消息...');
  
  const state = loadState();
  const now = Date.now();
  
  // 需要检查的聊天 ID（私聊 + 群聊）
  const chatIds = [
    'oc_d77a50191711fcda0c3fab1a2d0e910c',  // 私聊
    'oc_860db5e4fd90a53f2153619054abd26b'   // 张氏集团
  ];
  
  let hasUnrepliedMessage = false;
  let lastUserMessage = null;
  
  try {
    const token = await getTenantToken();
    
    for (const chatId of chatIds) {
      log(`检查聊天：${chatId}`);
      
      const result = await getRecentMessages(chatId, token);
      if (result.code !== 0) {
        log(`获取消息失败：${result.msg}`);
        continue;
      }
      
      const messages = result.data?.items || [];
      
      // 查找最近的用户消息和 bot 回复
      let lastUserMsg = null;
      let lastBotMsg = null;
      
      for (const msg of messages) {
        const senderId = msg.sender_id;
        const isUser = senderId === 'ou_ae328677b7d00c73ec3bff84e95ceb84';
        const isBot = senderId?.includes('bot') || msg.sender_type === 'bot';
        
        if (isUser && !lastUserMsg) {
          lastUserMsg = msg;
        }
        if (isBot && !lastBotMsg) {
          lastBotMsg = msg;
        }
        
        if (lastUserMsg && lastBotMsg) break;
      }
      
      // 检查是否有未回复的用户消息
      if (lastUserMsg) {
        const userMsgTime = new Date(lastUserMsg.create_time).getTime();
        const timeSinceUserMsg = now - userMsgTime;
        
        log(`最后用户消息：${lastUserMsg.create_time} (${Math.round(timeSinceUserMsg/1000/60)}分钟前)`);
        
        if (timeSinceUserMsg > TIMEOUT_THRESHOLD_MS) {
          // 用户消息超过 5 分钟
          if (!lastBotMsg || new Date(lastBotMsg.create_time).getTime() < userMsgTime) {
            // bot 没有回复这条消息
            log(`⚠️ 发现未回复消息！聊天：${chatId}`);
            hasUnrepliedMessage = true;
            lastUserMessage = lastUserMsg;
          }
        }
      }
    }
    
    // 更新状态
    state.lastCheck = new Date().toISOString();
    if (hasUnrepliedMessage) {
      state.missedReplies = (state.missedReplies || 0) + 1;
      state.lastUnrepliedMessage = lastUserMessage;
    }
    saveState(state);
    
    return { hasUnrepliedMessage, lastUserMessage };
    
  } catch (e) {
    log(`检查失败：${e.message}`);
    return { hasUnrepliedMessage: false, error: e.message };
  }
}

// 发送提醒消息到飞书
async function sendReminder(chatId, messageContent) {
  log(`发送提醒到聊天：${chatId}`);
  
  const token = await getTenantToken();
  
  // 解析用户消息内容
  let userMsgText = '';
  try {
    const content = JSON.parse(messageContent);
    userMsgText = content.text || content.content || '用户消息';
  } catch (e) {
    userMsgText = '用户消息';
  }
  
  log(`⚠️ 发现未回复消息："${userMsgText.substring(0, 50)}..."`);
  
  // 注意：这里不自动发送消息，而是记录日志
  // 实际回复需要由主 agent 处理
  // 这个脚本只负责检测和提醒
  
  return { chatId, userMsgText };
}

// 主循环
async function main() {
  log('=== 消息心跳监控启动 ===');
  log(`检查间隔：${CHECK_INTERVAL_MS/1000/60} 分钟`);
  log(`超时阈值：${TIMEOUT_THRESHOLD_MS/1000/60} 分钟`);
  
  // 立即执行一次
  const result = await checkUnrepliedMessages();
  if (result.hasUnrepliedMessage) {
    log('发现未回复消息，触发提醒！');
    await sendReminder(result.lastUserMessage?.content);
  }
  
  // 定时检查
  setInterval(async () => {
    const result = await checkUnrepliedMessages();
    if (result.hasUnrepliedMessage) {
      log('发现未回复消息，触发提醒！');
      await sendReminder(result.lastUserMessage?.content);
    }
  }, CHECK_INTERVAL_MS);
}

// 启动
main().catch(e => {
  log(`启动失败：${e.message}`);
  process.exit(1);
});
