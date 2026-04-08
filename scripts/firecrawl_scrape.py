#!/usr/bin/env python3
"""
Firecrawl 单页爬取脚本
用法：python3 firecrawl_scrape.py <URL> [--formats markdown html] [--output file.md]
"""

import sys
import json
import urllib.request
import urllib.error
import argparse

BASE_URL = "https://api.firecrawl.dev"
API_KEY = "fc-8eaf443210bb4fe78a2a2793c31a72cf"
TIMEOUT = 60

def scrape(url, formats=None):
    """爬取单个网页"""
    if formats is None:
        formats = ["markdown"]
    
    payload = {
        "url": url,
        "formats": formats
    }
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(
        f"{BASE_URL}/v1/scrape",
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        },
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result
    except urllib.error.URLError as e:
        return {"success": False, "error": f"网络错误：{e.reason}"}
    except json.JSONDecodeError as e:
        return {"success": False, "error": f"JSON 解析错误：{e}"}
    except Exception as e:
        return {"success": False, "error": f"未知错误：{e}"}

def main():
    parser = argparse.ArgumentParser(description="Firecrawl 单页爬取工具")
    parser.add_argument("url", help="目标网页 URL")
    parser.add_argument("--formats", "-f", nargs="+", default=["markdown"],
                        choices=["markdown", "html", "screenshot", "links"],
                        help="返回格式（默认：markdown）")
    parser.add_argument("--output", "-o", help="输出文件路径")
    parser.add_argument("--json", action="store_true", help="输出原始 JSON")
    
    args = parser.parse_args()
    
    print(f"🕷️  正在爬取：{args.url}")
    print(f"📦 格式：{', '.join(args.formats)}")
    print()
    
    result = scrape(args.url, args.formats)
    
    if result.get("success"):
        data = result.get("data", {})
        
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
            return
        
        # 输出 Markdown 内容
        if "markdown" in data:
            content = data["markdown"]
            
            if args.output:
                with open(args.output, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"✅ 已保存到：{args.output}")
            else:
                print("✅ 爬取成功！")
                print()
                print("=" * 60)
                print(content)
                print("=" * 60)
        
        # 输出元数据
        metadata = data.get("metadata", {})
        if metadata:
            print()
            print("📋 元数据：")
            print(f"  标题：{metadata.get('title', 'N/A')}")
            print(f"  描述：{metadata.get('description', 'N/A')}")
            print(f"  URL: {metadata.get('sourceURL', args.url)}")
        
        # 输出截图（如果有）
        if "screenshot" in data:
            print()
            print(f"📸 截图：{data['screenshot'][:100]}...")
            
    else:
        print(f"❌ 爬取失败：{result.get('error', '未知错误')}")
        sys.exit(1)

if __name__ == "__main__":
    main()
