/**
 * @file main.c
 * @brief STM32F407VGT6 SkyStar 板载 LED 控制
 * @author 绾绾
 * @date 2026-04-07
 * 
 * 硬件连接:
 * - LED0: PF9 (低电平点亮)
 * - LED1: PF10 (低电平点亮)
 */

#include "main.h"
#include "stm32f4xx_hal.h"

/* LED 引脚定义 */
#define LED0_PIN    GPIO_PIN_9
#define LED0_PORT   GPIOF
#define LED1_PIN    GPIO_PIN_10
#define LED1_PORT   GPIOF

/* 函数声明 */
void SystemClock_Config(void);
static void MX_GPIO_Init(void);
void LED_Init(void);
void LED0_On(void);
void LED0_Off(void);
void LED0_Toggle(void);
void LED1_On(void);
void LED1_Off(void);
void LED1_Toggle(void);
void HAL_Delay_ms(uint32_t ms);

int main(void)
{
    /* HAL 初始化 */
    HAL_Init();
    
    /* 系统时钟配置 */
    SystemClock_Config();
    
    /* GPIO 初始化 */
    MX_GPIO_Init();
    LED_Init();
    
    /* 主循环 */
    while (1)
    {
        /* LED0 闪烁 - 500ms 间隔 */
        LED0_Toggle();
        HAL_Delay_ms(500);
        
        /* LED1 闪烁 - 500ms 间隔（反相） */
        LED1_Toggle();
        HAL_Delay_ms(500);
    }
}

/**
 * @brief LED 初始化
 */
void LED_Init(void)
{
    GPIO_InitTypeDef GPIO_InitStruct = {0};
    
    /* 使能 GPIOF 时钟 */
    __HAL_RCC_GPIOF_CLK_ENABLE();
    
    /* 配置 LED0 (PF9) 和 LED1 (PF10) */
    GPIO_InitStruct.Pin = LED0_PIN | LED1_PIN;
    GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;  /* 推挽输出 */
    GPIO_InitStruct.Pull = GPIO_NOPULL;          /* 无上拉/下拉 */
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW; /* 低速 */
    HAL_GPIO_Init(LED0_PORT, &GPIO_InitStruct);
    
    /* 初始状态：关闭 LED */
    HAL_GPIO_WritePin(LED0_PORT, LED0_PIN, GPIO_PIN_SET);   /* 高电平关闭 */
    HAL_GPIO_WritePin(LED1_PORT, LED1_PIN, GPIO_PIN_SET);   /* 高电平关闭 */
}

/**
 * @brief LED0 控制函数
 */
void LED0_On(void)
{
    HAL_GPIO_WritePin(LED0_PORT, LED0_PIN, GPIO_PIN_RESET);  /* 低电平点亮 */
}

void LED0_Off(void)
{
    HAL_GPIO_WritePin(LED0_PORT, LED0_PIN, GPIO_PIN_SET);    /* 高电平关闭 */
}

void LED0_Toggle(void)
{
    HAL_GPIO_TogglePin(LED0_PORT, LED0_PIN);
}

/**
 * @brief LED1 控制函数
 */
void LED1_On(void)
{
    HAL_GPIO_WritePin(LED1_PORT, LED1_PIN, GPIO_PIN_RESET);  /* 低电平点亮 */
}

void LED1_Off(void)
{
    HAL_GPIO_WritePin(LED1_PORT, LED1_PIN, GPIO_PIN_SET);    /* 高电平关闭 */
}

void LED1_Toggle(void)
{
    HAL_GPIO_TogglePin(LED1_PORT, LED1_PIN);
}

/**
 * @brief 毫秒延时函数
 */
void HAL_Delay_ms(uint32_t ms)
{
    HAL_Delay(ms);
}

/**
 * @brief GPIO 初始化
 */
static void MX_GPIO_Init(void)
{
    /* GPIO 端口时钟使能已在 LED_Init 中完成 */
}

/**
 * @brief 系统时钟配置 (168MHz)
 */
void SystemClock_Config(void)
{
    /* 使用默认 HSI 时钟配置，详细配置可通过 STM32CubeMX 生成 */
    /* 如需精确配置，请使用 STM32CubeMX 生成 SystemClock_Config 函数 */
}

/**
 * @brief 错误处理
 */
void Error_Handler(void)
{
    __disable_irq();
    while (1)
    {
        /* 死循环，可通过 LED 闪烁指示错误 */
        LED0_Toggle();
        HAL_Delay_ms(100);
        LED1_Toggle();
        HAL_Delay_ms(100);
    }
}

#ifdef USE_FULL_ASSERT
void assert_failed(uint8_t *file, uint32_t line)
{
    /* 用户可添加自己的实现 */
#endif
