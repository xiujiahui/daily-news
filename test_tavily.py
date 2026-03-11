#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import os

# 使用用户提供的Tavily API密钥
TAVILY_API_KEY = "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"

def test_tavily_api():
    """测试Tavily API调用"""
    print("===== Tavily API测试 ======")
    print(f"使用API密钥: {TAVILY_API_KEY}")
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {TAVILY_API_KEY}"
    }
    
    payload = {
        "query": "今天杭州拱墅区的天气怎么样？",
        "search_depth": "basic",
        "include_answer": True,
        "include_raw_content": False,
        "include_images": False
    }
    
    try:
        print("发送请求到Tavily API...")
        response = requests.post("https://api.tavily.com/search", headers=headers, json=payload, timeout=15)
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        response.raise_for_status()
        result = response.json()
        print(f"解析结果: {result}")
        
    except Exception as e:
        print(f"API调用失败: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_tavily_api()
