#!/usr/bin/env python3
"""
Firecrawl 爬虫客户端
用于从树莓派容器调用 Firecrawl API 进行网页爬取
"""

import requests
import json
from typing import Optional, Dict, Any

class FirecrawlClient:
    """Firecrawl API 客户端"""
    
    def __init__(self, base_url: str = "http://172.17.0.1:3002"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json"
        })
    
    def scrape(self, url: str, formats: list = None) -> Optional[Dict[str, Any]]:
        """
        爬取单个网页
        
        Args:
            url: 目标网页 URL
            formats: 返回格式列表，如 ["markdown", "html", "screenshot"]
        
        Returns:
            爬取结果字典，包含 markdown/html/screenshot 等字段
        """
        if formats is None:
            formats = ["markdown"]
        
        payload = {
            "url": url,
            "formats": formats
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/v1/scrape",
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            
            if result.get("success"):
                return result.get("data", {})
            else:
                print(f"❌ 爬取失败：{result.get('error', '未知错误')}")
                return None
                
        except requests.exceptions.Timeout:
            print("⏱️ 请求超时")
            return None
        except requests.exceptions.RequestException as e:
            print(f"❌ 请求错误：{e}")
            return None
    
    def crawl(self, url: str, limit: int = 10, max_depth: int = 2) -> list:
        """
        爬取整个网站（递归爬取多个页面）
        
        Args:
            url: 起始 URL
            limit: 最大页面数
            max_depth: 最大深度
        
        Returns:
            爬取结果列表
        """
        payload = {
            "url": url,
            "limit": limit,
            "maxDepth": max_depth,
            "formats": ["markdown"]
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/v1/crawl",
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            result = response.json()
            
            if result.get("success"):
                return result.get("data", [])
            else:
                print(f"❌ 爬取失败：{result.get('error', '未知错误')}")
                return []
                
        except Exception as e:
            print(f"❌ 请求错误：{e}")
            return []
    
    def map(self, url: str) -> list:
        """
        获取网站所有链接（类似站点地图）
        
        Args:
            url: 目标网站 URL
        
        Returns:
            URL 列表
        """
        payload = {
            "url": url
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/v1/map",
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            
            if result.get("success"):
                return result.get("data", {}).get("urls", [])
            else:
                print(f"❌ 映射失败：{result.get('error', '未知错误')}")
                return []
                
        except Exception as e:
            print(f"❌ 请求错误：{e}")
            return []
    
    def test_connection(self) -> bool:
        """测试连接是否正常"""
        try:
            response = self.session.get(self.base_url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Firecrawl 服务正常：{data.get('message')}")
                return True
            return False
        except Exception as e:
            print(f"❌ 连接失败：{e}")
            return False


# 快捷使用示例
if __name__ == "__main__":
    # 创建客户端
    client = FirecrawlClient()
    
    # 测试连接
    print("🔌 测试连接...")
    client.test_connection()
    print()
    
    # 示例 1：爬取单个网页
    print("📄 爬取 example.com...")
    result = client.scrape("https://example.com", formats=["markdown"])
    if result:
        print(f"✅ 爬取成功！")
        print(f"标题：{result.get('metadata', {}).get('title', 'N/A')}")
        print(f"内容长度：{len(result.get('markdown', ''))} 字符")
        print(f"\n内容预览（前 500 字）：")
        print(result.get('markdown', '')[:500])
    print()
    
    # 示例 2：获取网站链接
    print("🗺️ 获取 example.com 所有链接...")
    urls = client.map("https://example.com")
    if urls:
        print(f"✅ 找到 {len(urls)} 个链接：")
        for url in urls[:10]:  # 只显示前 10 个
            print(f"  - {url}")
    print()
    
    # 示例 3：爬取多个页面
    print("🕷️ 爬取 example.com（最多 3 个页面）...")
    results = client.crawl("https://example.com", limit=3, max_depth=1)
    if results:
        print(f"✅ 爬取了 {len(results)} 个页面")
        for i, page in enumerate(results, 1):
            title = page.get('metadata', {}).get('title', 'N/A')
            print(f"  {i}. {title}")
