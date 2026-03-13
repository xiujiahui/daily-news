#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单导入测试脚本
测试能否成功导入daily_english_report.py中的函数
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 设置环境变量以避免主脚本的环境检查失败
os.environ['FEISHU_WEBHOOK'] = 'dummy_webhook'
os.environ['DEEPSEEK_API_KEY'] = 'dummy_deepseek_key'
os.environ['TAVILY_API_KEY'] = 'dummy_tavily_key'
os.environ['ENABLE_HEALTH_CHECK'] = 'false'
os.environ['ENABLE_DATA_VALIDATION'] = 'false'

print("=" * 60)
print("🔧 开始导入测试")
print("=" * 60)

# 尝试导入模块
try:
    print("1. 尝试导入整个模块...")
    import daily_english_report
    print("   ✅ 成功导入整个模块")
    
    # 检查模块属性
    print("\n2. 检查模块中的函数...")
    functions_to_check = [
        'validate_data_quality',
        'check_data_source_health', 
        'standardize_news_data',
        'format_publish_time',
        'is_within_7_days',
        'verify_weather_info',
        'verify_news_time'
    ]
    
    for func_name in functions_to_check:
        if hasattr(daily_english_report, func_name):
            print(f"   ✅ {func_name}: 存在")
        else:
            print(f"   ❌ {func_name}: 不存在")
    
    print("\n3. 测试函数调用...")
    
    # 测试standardize_news_data函数
    try:
        test_news = {
            'title': '测试新闻',
            'description': '测试描述',
            'source': {'name': '测试来源'},
            'publish_time': '2026-03-12',
            'url': 'test.com'
        }
        
        result = daily_english_report.standardize_news_data(test_news)
        if result:
            print(f"   ✅ standardize_news_data: 函数调用成功")
            print(f"      结果: {result}")
        else:
            print(f"   ❌ standardize_news_data: 函数返回None")
    except Exception as e:
        print(f"   ❌ standardize_news_data: 调用失败 - {str(e)}")
    
    # 测试format_publish_time函数
    try:
        result = daily_english_report.format_publish_time('2026-03-12')
        print(f"   ✅ format_publish_time: 函数调用成功")
        print(f"      结果: '{result}'")
    except Exception as e:
        print(f"   ❌ format_publish_time: 调用失败 - {str(e)}")
    
    # 测试is_within_7_days函数
    try:
        from datetime import datetime
        today_str = datetime.now().strftime('%Y年%m月%d日')
        result = daily_english_report.is_within_7_days(today_str)
        print(f"   ✅ is_within_7_days: 函数调用成功")
        print(f"      结果: {result}")
    except Exception as e:
        print(f"   ❌ is_within_7_days: 调用失败 - {str(e)}")
    
    print("\n" + "=" * 60)
    print("🎉 导入测试完成！")
    print("=" * 60)
    
except ImportError as e:
    print(f"❌ 导入模块失败: {str(e)}")
    import traceback
    traceback.print_exc()
except SystemExit as e:
    print(f"❌ 模块执行过程中退出: {str(e)}")
    print("⚠️  可能是环境变量检查失败导致脚本退出")
except Exception as e:
    print(f"❌ 其他错误: {str(e)}")
    import traceback
    traceback.print_exc()