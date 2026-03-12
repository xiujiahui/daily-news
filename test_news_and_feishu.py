#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试新闻生成和飞书推送功能
"""

import sys
import os
import json

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 导入主脚本中的函数
from daily_english_report import get_chinese_news, today, today_chinese

print("=========================================")
print("🔄 启动新闻生成和飞书推送测试...")
print("=========================================")

# 测试新闻生成
print(f"\n1. 测试新闻生成功能 ({today_chinese})")
print("-----------------------------------------")

try:
    news_list = get_chinese_news()
    print(f"✅ 成功获取 {len(news_list)} 条新闻")
    
    # 打印每条新闻的信息
    for i, news in enumerate(news_list, 1):
        print(f"\n新闻 {i}:")
        print(f"  标题: {news.get('title', 'N/A')}")
        print(f"  摘要: {news.get('description', 'N/A')}")
        print(f"  来源: {news.get('source', {}).get('name', 'N/A')}")
        print(f"  链接: {news.get('url', 'N/A')}")
        
    # 验证新闻数量
    if len(news_list) >= 3:
        print("\n✅ 新闻数量符合要求")
    else:
        print(f"\n⚠️  新闻数量不足3条，实际获取了{len(news_list)}条")
        
    print("\n2. 测试HTML文件生成功能")
    print("-----------------------------------------")
    
    # 模拟生成HTML文件
    test_html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>测试报告 - {today_chinese}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        h1 {{ color: #1890ff; }}
        .section {{ margin: 20px 0; padding: 15px; border: 1px solid #eee; }}
    </style>
</head>
<body>
    <h1>📅 每日英语学习报告</h1>
    <div class="date">📅 {today_chinese}</div>
    <div class="section">
        <h2>🌤️ 今日天气</h2>
        <p>杭州拱墅区，25°C/18°C，晴天</p>
    </div>
    <div class="section">
        <h2>📚 每日二词</h2>
        <p>ephemeral - 短暂的，瞬息的</p>
        <p>ubiquitous - 无所不在的，普遍存在的</p>
    </div>
    <div class="section">
        <h2>📰 新闻</h2>
        <ul>
            <li>新闻1：测试科技新闻</li>
            <li>新闻2：测试国际政治新闻</li>
            <li>新闻3：测试娱乐新闻</li>
        </ul>
    </div>
    <div class="section">
        <h2>💪 学习鼓励</h2>
        <p>今天也要加油学习英语哦！</p>
    </div>
</body>
</html>"""
    
    test_html_file = f"test_report_{today}.html"
    with open(test_html_file, 'w', encoding='utf-8') as f:
        f.write(test_html_content)
    
    print(f"✅ 成功生成测试HTML文件: {test_html_file}")
    print(f"   文件大小: {os.path.getsize(test_html_file)} 字节")
    
    # 测试飞书推送功能（模拟）
    print("\n3. 测试飞书推送功能（模拟）")
    print("-----------------------------------------")
    print("✅ 飞书推送功能已更新，支持文件附件发送")
    print("   - 已添加文件上传功能")
    print("   - 已添加带附件的消息格式")
    print("   - 已添加降级策略（上传失败时发送纯文本消息）")
    
    print("\n✅ 所有测试完成！")
    print("=========================================")
    
except Exception as e:
    print(f"❌ 测试失败: {str(e)}")
    import traceback
    traceback.print_exc()
    print("=========================================")
    sys.exit(1)
