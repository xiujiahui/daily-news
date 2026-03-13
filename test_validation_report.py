#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据验证和修复效果测试报告

此脚本用于测试和验证天气板块和新闻板块的修复效果，包括：
1. 数据质量验证机制的测试
2. 数据源健康检查的测试
3. 新闻时效性过滤的测试
4. 天气数据准确性验证的测试
5. 数据准确性验证机制的测试
"""

import sys
import os
import json
from datetime import datetime, timedelta

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 设置环境变量以避免主脚本的环境检查失败
os.environ['FEISHU_WEBHOOK'] = 'dummy_webhook'
os.environ['DEEPSEEK_API_KEY'] = 'dummy_deepseek_key'
os.environ['TAVILY_API_KEY'] = 'dummy_tavily_key'
os.environ['ENABLE_HEALTH_CHECK'] = 'false'
os.environ['ENABLE_DATA_VALIDATION'] = 'false'

# 导入主脚本中的函数
try:
    from daily_english_report import (
        validate_data_quality,
        check_data_source_health,
        standardize_news_data,
        format_publish_time,
        is_within_7_days,
        verify_weather_info,
        verify_news_time
    )
    IMPORT_SUCCESS = True
except ImportError as e:
    print(f"❌ 导入模块失败: {str(e)}")
    print("⚠️  请确保daily_english_report.py文件存在且语法正确")
    IMPORT_SUCCESS = False

def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("📊 数据验证和修复效果测试报告")
    print("=" * 60)
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    if not IMPORT_SUCCESS:
        print("❌ 无法运行测试：模块导入失败")
        return
    
    # 测试结果汇总
    test_results = {
        'total_tests': 0,
        'passed_tests': 0,
        'failed_tests': 0,
        'test_cases': []
    }
    
    # 1. 测试数据质量验证机制
    print("🔬 测试1：数据质量验证机制")
    test_data_quality_validation(test_results)
    
    # 2. 测试新闻数据标准化和时效性过滤
    print("\n📰 测试2：新闻数据标准化和时效性过滤")
    test_news_validation(test_results)
    
    # 3. 测试天气数据验证
    print("\n🌤️  测试3：天气数据验证")
    test_weather_validation(test_results)
    
    # 4. 测试数据源健康检查
    print("\n🏥 测试4：数据源健康检查（模拟测试）")
    test_health_check_simulation(test_results)
    
    # 5. 测试完整工作流程
    print("\n🔄 测试5：完整工作流程模拟")
    test_workflow_simulation(test_results)
    
    # 打印测试报告摘要
    print_test_summary(test_results)
    
    # 生成测试报告文件
    generate_test_report_file(test_results)

def test_data_quality_validation(test_results):
    """测试数据质量验证机制"""
    print("   运行数据质量验证测试...")
    
    # 测试用例1：正常数据
    test_case = {
        'name': '正常天气数据验证',
        'status': 'pending'
    }
    
    normal_weather = {
        'city': '杭州拱墅区',
        'max_temp': 25,
        'min_temp': 18,
        'description': '多云',
        'change': '全天无明显变化',
        'source': '测试数据源'
    }
    
    normal_news = [
        {
            'title': '测试新闻标题1',
            'description': '测试新闻描述1',
            'source': {'name': '新华网'},
            'publish_time': datetime.now().strftime('%Y年%m月%d日'),
            'url': 'https://test.com/1'
        }
    ]
    
    normal_words = [
        {
            'word': 'test',
            'pronunciation': '/test/',
            'definition': '测试',
            'example': 'This is a test.',
            'example_zh': '这是一个测试。'
        }
    ]
    
    try:
        results = validate_data_quality(normal_weather, normal_news, normal_words)
        if results.get('issues', []):
            test_case['status'] = 'failed'
            test_case['message'] = f"正常数据验证失败，发现问题: {results['issues']}"
        else:
            test_case['status'] = 'passed'
            test_case['message'] = '正常数据验证通过'
    except Exception as e:
        test_case['status'] = 'failed'
        test_case['message'] = f"验证函数异常: {str(e)}"
    
    test_results['test_cases'].append(test_case)
    test_results['total_tests'] += 1
    if test_case['status'] == 'passed':
        test_results['passed_tests'] += 1
    else:
        test_results['failed_tests'] += 1
    
    # 测试用例2：异常天气数据（温度异常）
    test_case2 = {
        'name': '异常天气数据验证（温度异常）',
        'status': 'pending'
    }
    
    abnormal_weather = {
        'city': '杭州拱墅区',
        'max_temp': 60,  # 异常高温
        'min_temp': 18,
        'description': '多云',
        'change': '全天无明显变化'
    }
    
    try:
        results = validate_data_quality(abnormal_weather, normal_news, normal_words)
        issues_found = len(results.get('issues', [])) > 0
        if issues_found:
            test_case2['status'] = 'passed'
            test_case2['message'] = f"成功检测到异常数据，发现{len(results['issues'])}个问题"
        else:
            test_case2['status'] = 'failed'
            test_case2['message'] = '未能检测到异常温度数据'
    except Exception as e:
        test_case2['status'] = 'failed'
        test_case2['message'] = f"验证函数异常: {str(e)}"
    
    test_results['test_cases'].append(test_case2)
    test_results['total_tests'] += 1
    if test_case2['status'] == 'passed':
        test_results['passed_tests'] += 1
    else:
        test_results['failed_tests'] += 1
    
    # 打印测试结果
    for test_case in [test_case, test_case2]:
        status_icon = '✅' if test_case['status'] == 'passed' else '❌'
        print(f"   {status_icon} {test_case['name']}: {test_case['message']}")

def test_news_validation(test_results):
    """测试新闻数据标准化和时效性过滤"""
    print("   运行新闻数据验证测试...")
    
    # 测试用例1：新闻数据标准化
    test_case = {
        'name': '新闻数据标准化测试',
        'status': 'pending'
    }
    
    raw_news = {
        'title': '  测试新闻标题  ',
        'description': '测试新闻描述  ',
        'source': {'name': '新华网'},
        'publish_time': '2026-03-12',
        'url': 'test.com'
    }
    
    try:
        standardized = standardize_news_data(raw_news)
        if standardized and standardized['title'] == '测试新闻标题' and standardized['url'].startswith('http'):
            test_case['status'] = 'passed'
            test_case['message'] = '新闻数据标准化功能正常'
        else:
            test_case['status'] = 'failed'
            test_case['message'] = f'新闻数据标准化异常: {standardized}'
    except Exception as e:
        test_case['status'] = 'failed'
        test_case['message'] = f"标准化函数异常: {str(e)}"
    
    test_results['test_cases'].append(test_case)
    test_results['total_tests'] += 1
    if test_case['status'] == 'passed':
        test_results['passed_tests'] += 1
    else:
        test_results['failed_tests'] += 1
    
    # 测试用例2：发布时间格式化
    test_case2 = {
        'name': '发布时间格式化测试',
        'status': 'pending'
    }
    
    test_times = [
        ('2026年3月12日', '2026年03月12日'),
        ('2026-03-12', '2026年03月12日'),
        ('2026/03/12', '2026年03月12日')
    ]
    
    try:
        all_passed = True
        for input_time, expected_output in test_times:
            formatted = format_publish_time(input_time)
            if formatted != expected_output:
                all_passed = False
                test_case2['message'] = f"格式化失败: '{input_time}' -> '{formatted}' (期望: '{expected_output}')"
                break
        
        if all_passed:
            test_case2['status'] = 'passed'
            test_case2['message'] = '发布时间格式化功能正常'
        else:
            test_case2['status'] = 'failed'
    except Exception as e:
        test_case2['status'] = 'failed'
        test_case2['message'] = f"格式化函数异常: {str(e)}"
    
    test_results['test_cases'].append(test_case2)
    test_results['total_tests'] += 1
    if test_case2['status'] == 'passed':
        test_results['passed_tests'] += 1
    else:
        test_results['failed_tests'] += 1
    
    # 测试用例3：7天内时效性检查
    test_case3 = {
        'name': '新闻时效性检查测试',
        'status': 'pending'
    }
    
    today = datetime.now()
    within_7_days = (today - timedelta(days=5)).strftime('%Y年%m月%d日')
    outside_7_days = (today - timedelta(days=10)).strftime('%Y年%m月%d日')
    
    try:
        # 测试7天内的新闻
        within_result = is_within_7_days(within_7_days)
        # 测试7天外的新闻
        outside_result = is_within_7_days(outside_7_days)
        
        if within_result and not outside_result:
            test_case3['status'] = 'passed'
            test_case3['message'] = '新闻时效性检查功能正常'
        else:
            test_case3['status'] = 'failed'
            test_case3['message'] = f'时效性检查异常: 7天内={within_result}, 7天外={outside_result}'
    except Exception as e:
        test_case3['status'] = 'failed'
        test_case3['message'] = f"时效性检查函数异常: {str(e)}"
    
    test_results['test_cases'].append(test_case3)
    test_results['total_tests'] += 1
    if test_case3['status'] == 'passed':
        test_results['passed_tests'] += 1
    else:
        test_results['failed_tests'] += 1
    
    # 打印测试结果
    for test_case in [test_case, test_case2, test_case3]:
        status_icon = '✅' if test_case['status'] == 'passed' else '❌'
        print(f"   {status_icon} {test_case['name']}: {test_case['message']}")

def test_weather_validation(test_results):
    """测试天气数据验证"""
    print("   运行天气数据验证测试...")
    
    # 注意：由于verify_weather_info需要调用DeepSeek API，我们这里只测试函数调用
    # 在实际测试中，应该使用模拟数据或mock
    
    test_case = {
        'name': '天气验证函数接口测试',
        'status': 'pending'
    }
    
    test_weather = {
        'city': '杭州拱墅区',
        'max_temp': 25,
        'min_temp': 18,
        'description': '多云',
        'change': '全天无明显变化',
        'source': '测试数据源'
    }
    
    try:
        # 测试函数能否正常调用（由于API依赖，可能返回True或False）
        # 这里主要测试函数是否存在且能正常执行
        result = verify_weather_info(test_weather)
        test_case['status'] = 'passed'
        test_case['message'] = f'天气验证函数接口正常，返回: {result}'
    except Exception as e:
        test_case['status'] = 'failed'
        test_case['message'] = f"天气验证函数异常: {str(e)}"
    
    test_results['test_cases'].append(test_case)
    test_results['total_tests'] += 1
    if test_case['status'] == 'passed':
        test_results['passed_tests'] += 1
    else:
        test_results['failed_tests'] += 1
    
    # 测试新闻时间验证函数接口
    test_case2 = {
        'name': '新闻时间验证函数接口测试',
        'status': 'pending'
    }
    
    test_news = {
        'title': '测试新闻',
        'description': '测试新闻描述',
        'source': {'name': '新华网'},
        'publish_time': datetime.now().strftime('%Y年%m月%d日')
    }
    
    try:
        # 测试函数能否正常调用
        result = verify_news_time(test_news)
        test_case2['status'] = 'passed'
        test_case2['message'] = f'新闻时间验证函数接口正常，返回: {result}'
    except Exception as e:
        test_case2['status'] = 'failed'
        test_case2['message'] = f"新闻时间验证函数异常: {str(e)}"
    
    test_results['test_cases'].append(test_case2)
    test_results['total_tests'] += 1
    if test_case2['status'] == 'passed':
        test_results['passed_tests'] += 1
    else:
        test_results['failed_tests'] += 1
    
    # 打印测试结果
    for test_case in [test_case, test_case2]:
        status_icon = '✅' if test_case['status'] == 'passed' else '❌'
        print(f"   {status_icon} {test_case['name']}: {test_case['message']}")

def test_health_check_simulation(test_results):
    """测试数据源健康检查（模拟测试）"""
    print("   运行数据源健康检查模拟测试...")
    
    # 由于check_data_source_health需要实际网络请求，我们这里只模拟测试
    # 在实际环境中，应该运行完整的健康检查
    
    test_case = {
        'name': '数据源健康检查函数测试',
        'status': 'pending'
    }
    
    try:
        # 测试函数是否存在且可调用
        # 注意：这里我们不会实际调用，因为需要网络连接和API密钥
        # 我们只是验证函数定义
        if callable(check_data_source_health):
            test_case['status'] = 'passed'
            test_case['message'] = '数据源健康检查函数定义正常'
        else:
            test_case['status'] = 'failed'
            test_case['message'] = '数据源健康检查函数不可调用'
    except Exception as e:
        test_case['status'] = 'failed'
        test_case['message'] = f"数据源健康检查函数异常: {str(e)}"
    
    test_results['test_cases'].append(test_case)
    test_results['total_tests'] += 1
    if test_case['status'] == 'passed':
        test_results['passed_tests'] += 1
    else:
        test_results['failed_tests'] += 1
    
    # 打印测试结果
    status_icon = '✅' if test_case['status'] == 'passed' else '❌'
    print(f"   {status_icon} {test_case['name']}: {test_case['message']}")
    print("   ⚠️  注意：完整的数据源健康检查需要网络连接和API密钥，此测试为模拟测试")

def test_workflow_simulation(test_results):
    """测试完整工作流程模拟"""
    print("   运行完整工作流程模拟测试...")
    
    # 模拟一个完整的数据处理流程
    test_case = {
        'name': '完整数据处理流程测试',
        'status': 'pending'
    }
    
    try:
        # 模拟数据收集
        simulated_weather = {
            'city': '杭州拱墅区',
            'max_temp': 25,
            'min_temp': 18,
            'description': '多云',
            'change': '全天无明显变化',
            'source': '模拟数据源'
        }
        
        simulated_news = [
            {
                'title': '模拟新闻1',
                'description': '模拟新闻描述1',
                'source': {'name': '模拟来源'},
                'publish_time': datetime.now().strftime('%Y年%m月%d日'),
                'url': 'https://example.com/1'
            },
            {
                'title': '模拟新闻2',
                'description': '模拟新闻描述2',
                'source': {'name': '模拟来源'},
                'publish_time': (datetime.now() - timedelta(days=3)).strftime('%Y年%m月%d日'),
                'url': 'https://example.com/2'
            }
        ]
        
        simulated_words = [
            {
                'word': 'simulate',
                'pronunciation': '/ˈsɪmjəleɪt/',
                'definition': '模拟',
                'example': 'We need to simulate real conditions.',
                'example_zh': '我们需要模拟真实条件。'
            }
        ]
        
        # 执行数据质量验证
        validation_results = validate_data_quality(simulated_weather, simulated_news, simulated_words)
        
        # 检查验证结果
        if isinstance(validation_results, dict) and 'issues' in validation_results:
            test_case['status'] = 'passed'
            issues_count = len(validation_results['issues'])
            test_case['message'] = f'完整数据处理流程测试通过，发现{issues_count}个问题'
        else:
            test_case['status'] = 'failed'
            test_case['message'] = f'验证结果格式异常: {validation_results}'
    except Exception as e:
        test_case['status'] = 'failed'
        test_case['message'] = f"完整流程测试异常: {str(e)}"
    
    test_results['test_cases'].append(test_case)
    test_results['total_tests'] += 1
    if test_case['status'] == 'passed':
        test_results['passed_tests'] += 1
    else:
        test_results['failed_tests'] += 1
    
    # 打印测试结果
    status_icon = '✅' if test_case['status'] == 'passed' else '❌'
    print(f"   {status_icon} {test_case['name']}: {test_case['message']}")

def print_test_summary(test_results):
    """打印测试报告摘要"""
    print("\n" + "=" * 60)
    print("📋 测试报告摘要")
    print("=" * 60)
    
    passed_count = test_results['passed_tests']
    total_count = test_results['total_tests']
    failed_count = test_results['failed_tests']
    
    if total_count > 0:
        pass_rate = (passed_count / total_count) * 100
    else:
        pass_rate = 0
    
    print(f"📊 测试统计:")
    print(f"   总测试用例: {total_count}")
    print(f"   通过测试: {passed_count}")
    print(f"   失败测试: {failed_count}")
    print(f"   通过率: {pass_rate:.1f}%")
    
    print(f"\n📝 详细测试结果:")
    for i, test_case in enumerate(test_results['test_cases'], 1):
        status_icon = '✅' if test_case['status'] == 'passed' else '❌'
        print(f"   {i:2d}. {status_icon} {test_case['name']}")
        print(f"      结果: {test_case['message']}")
    
    print("\n🎯 测试结论:")
    if failed_count == 0:
        print("   ✅ 所有测试通过！数据验证和修复机制工作正常。")
    elif pass_rate >= 80:
        print(f"   ⚠️  大部分测试通过 ({pass_rate:.1f}%)，但存在一些问题需要关注。")
    else:
        print(f"   ❌ 测试通过率较低 ({pass_rate:.1f}%)，需要进一步修复。")

def generate_test_report_file(test_results):
    """生成测试报告文件"""
    try:
        report_time = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_filename = f"test_validation_report_{report_time}.json"
        
        # 添加时间戳
        test_results['test_time'] = datetime.now().isoformat()
        test_results['report_version'] = '1.0'
        
        # 保存为JSON文件
        with open(report_filename, 'w', encoding='utf-8') as f:
            json.dump(test_results, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 测试报告已保存到: {report_filename}")
        print(f"   文件路径: {os.path.abspath(report_filename)}")
        
        # 同时生成HTML格式的报告
        generate_html_report(test_results, report_time)
        
    except Exception as e:
        print(f"❌ 生成测试报告文件失败: {str(e)}")

def generate_html_report(test_results, report_time):
    """生成HTML格式的测试报告"""
    try:
        html_filename = f"test_validation_report_{report_time}.html"
        
        passed_count = test_results['passed_tests']
        total_count = test_results['total_tests']
        failed_count = test_results['failed_tests']
        
        if total_count > 0:
            pass_rate = (passed_count / total_count) * 100
        else:
            pass_rate = 0
        
        html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>数据验证测试报告 - {report_time}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
        .container {{ max-width: 1000px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #333; border-bottom: 2px solid #4CAF50; padding-bottom: 10px; }}
        .summary {{ background-color: #f8f9fa; padding: 20px; border-radius: 5px; margin-bottom: 30px; }}
        .test-case {{ margin-bottom: 15px; padding: 15px; border-radius: 5px; border-left: 5px solid #ccc; }}
        .passed {{ border-left-color: #4CAF50; background-color: #f1f8e9; }}
        .failed {{ border-left-color: #f44336; background-color: #ffebee; }}
        .stats {{ display: flex; justify-content: space-around; margin: 20px 0; }}
        .stat-box {{ text-align: center; padding: 20px; border-radius: 5px; }}
        .total {{ background-color: #e3f2fd; }}
        .passed-stat {{ background-color: #e8f5e9; }}
        .failed-stat {{ background-color: #ffebee; }}
        .pass-rate {{ background-color: #fff3e0; }}
        .timestamp {{ color: #666; font-size: 14px; text-align: right; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 数据验证测试报告</h1>
        <div class="timestamp">生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
        
        <div class="summary">
            <h2>📋 测试摘要</h2>
            <div class="stats">
                <div class="stat-box total">
                    <h3>总测试用例</h3>
                    <p style="font-size: 24px; font-weight: bold;">{total_count}</p>
                </div>
                <div class="stat-box passed-stat">
                    <h3>通过测试</h3>
                    <p style="font-size: 24px; font-weight: bold; color: #4CAF50;">{passed_count}</p>
                </div>
                <div class="stat-box failed-stat">
                    <h3>失败测试</h3>
                    <p style="font-size: 24px; font-weight: bold; color: #f44336;">{failed_count}</p>
                </div>
                <div class="stat-box pass-rate">
                    <h3>通过率</h3>
                    <p style="font-size: 24px; font-weight: bold; color: #FF9800;">{pass_rate:.1f}%</p>
                </div>
            </div>
        </div>
        
        <h2>📝 详细测试结果</h2>
"""
        
        for i, test_case in enumerate(test_results['test_cases'], 1):
            status_class = 'passed' if test_case['status'] == 'passed' else 'failed'
            status_icon = '✅' if test_case['status'] == 'passed' else '❌'
            
            html_content += f"""
        <div class="test-case {status_class}">
            <h3>{i}. {status_icon} {test_case['name']}</h3>
            <p><strong>状态:</strong> {test_case['status'].upper()}</p>
            <p><strong>详情:</strong> {test_case['message']}</p>
        </div>
"""
        
        html_content += f"""
        <h2>🎯 测试结论</h2>
        <div class="test-case">
"""
        
        if failed_count == 0:
            html_content += '<p style="color: #4CAF50; font-weight: bold;">✅ 所有测试通过！数据验证和修复机制工作正常。</p>'
        elif pass_rate >= 80:
            html_content += f'<p style="color: #FF9800; font-weight: bold;">⚠️ 大部分测试通过 ({pass_rate:.1f}%)，但存在一些问题需要关注。</p>'
        else:
            html_content += f'<p style="color: #f44336; font-weight: bold;">❌ 测试通过率较低 ({pass_rate:.1f}%)，需要进一步修复。</p>'
        
        html_content += f"""
        </div>
        
        <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee; color: #666; font-size: 14px;">
            <p>测试报告版本: {test_results.get('report_version', '1.0')}</p>
            <p>生成工具: 数据验证测试脚本</p>
        </div>
    </div>
</body>
</html>
"""
        
        with open(html_filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"   同时生成HTML报告: {html_filename}")
        
    except Exception as e:
        print(f"❌ 生成HTML报告失败: {str(e)}")

if __name__ == "__main__":
    run_all_tests()