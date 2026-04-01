#!/usr/bin/env node
/**
 * OpenClaw 定时健康检查（Node.js 版）
 * 每 5 分钟检查一次系统状态
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const WORKSPACE = '/home/node/.openclaw/workspace';
const LOG_FILE = path.join(WORKSPACE, 'logs/cron-healthcheck.log');
const HEAL_SCRIPT = path.join(WORKSPACE, 'scripts/auto-heal.sh');
const CHECK_INTERVAL = 5 * 60 * 1000; // 5 分钟

// 确保日志目录存在
const logDir = path.dirname(LOG_FILE);
if (!fs.existsSync(logDir)) {
    fs.mkdirSync(logDir, { recursive: true });
}

function log(message, level = 'INFO') {
    const timestamp = new Date().toISOString().replace('T', ' ').substring(0, 19);
    const logLine = `[${timestamp}] [${level}] ${message}\n`;
    fs.appendFileSync(LOG_FILE, logLine);
    console.log(logLine.trim());
}

function run(command) {
    try {
        return execSync(command, { encoding: 'utf8', stdio: ['pipe', 'pipe', 'ignore'] });
    } catch (error) {
        return null;
    }
}

function checkGateway() {
    const pid = run("pgrep -f 'openclaw-gateway' | head -1");
    return pid && pid.trim().length > 0;
}

function checkDisk() {
    const df = run("df / | awk 'NR==2 {print $5}' | sed 's/%//'");
    return df ? parseInt(df.trim()) : 0;
}

function checkMemory() {
    const mem = run("free -m | awk '/^Mem:/ {print $7}'");
    return mem ? parseInt(mem.trim()) : 0;
}

function triggerHeal() {
    log('触发自动恢复脚本...', 'WARN');
    try {
        execSync(`bash ${HEAL_SCRIPT}`, { stdio: 'inherit' });
        log('自动恢复完成', 'INFO');
    } catch (error) {
        log(`自动恢复失败：${error.message}`, 'ERROR');
    }
}

function healthCheck() {
    log('========================================', 'INFO');
    log('定时健康检查', 'INFO');
    log('========================================', 'INFO');
    
    let issues = [];
    
    // 检查 Gateway
    if (checkGateway()) {
        const pid = run("pgrep -f 'openclaw-gateway' | head -1").trim();
        log(`✅ Gateway 运行正常 (PID: ${pid})`, 'INFO');
    } else {
        log('❌ Gateway 未运行', 'ERROR');
        issues.push('gateway');
    }
    
    // 检查磁盘
    const diskUsage = checkDisk();
    if (diskUsage < 85) {
        log(`✅ 磁盘使用率：${diskUsage}%`, 'INFO');
    } else {
        log(`⚠️  磁盘使用率：${diskUsage}%`, 'WARN');
        issues.push('disk');
    }
    
    // 检查内存
    const memAvailable = checkMemory();
    if (memAvailable >= 500) {
        log(`✅ 可用内存：${memAvailable}MB`, 'INFO');
    } else {
        log(`⚠️  可用内存：${memAvailable}MB`, 'WARN');
        issues.push('memory');
    }
    
    // 如果有问题，触发恢复
    if (issues.includes('gateway')) {
        triggerHeal();
    }
    
    log('✅ 健康检查完成', 'INFO');
}

// 主函数
function main() {
    log('启动定时健康检查服务', 'INFO');
    log(`检查间隔：${CHECK_INTERVAL / 1000}秒`, 'INFO');
    
    // 立即执行一次
    healthCheck();
    
    // 定时执行
    setInterval(healthCheck, CHECK_INTERVAL);
}

main();
