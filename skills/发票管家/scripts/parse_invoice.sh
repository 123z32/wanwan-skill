#!/bin/bash
# 发票 PDF 解析脚本
# 使用 pdftotext 提取发票内容

set -e

PDF_FILE="$1"

if [ -z "$PDF_FILE" ]; then
    echo "用法：$0 <pdf 文件路径>"
    exit 1
fi

if [ ! -f "$PDF_FILE" ]; then
    echo "错误：文件不存在 - $PDF_FILE"
    exit 1
fi

# 检查 pdftotext 是否安装
if ! command -v pdftotext &> /dev/null; then
    echo "错误：pdftotext 未安装，请先安装 poppler-utils"
    exit 1
fi

# 解析 PDF
echo "正在解析：$PDF_FILE"
pdftotext "$PDF_FILE" -
