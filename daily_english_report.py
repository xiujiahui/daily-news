#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每日英语学习报告生成脚本

功能：
1. 自动生成杭州拱墅区天气数据
2. 生成2个六级水平英语单词，包含中文释义、例句及发音
3. 生成中文新闻
4. 生成积极鼓励话语
5. 生成美观的HTML网页
6. 支持推送到飞书群

使用说明：
1. 安装依赖：pip install -r requirements.txt
2. 配置环境变量（可选）
3. 运行脚本：python daily_english_report.py
"""

import os
import requests
import json
from datetime import datetime

# 打印启动信息
print("=========================================")
print("🔄 启动每日英语学习报告生成脚本...")
print("=========================================")

# 今日日期
today = datetime.now().strftime('%Y-%m-%d')
today_chinese = datetime.now().strftime('%Y年%m月%d日')
print(f"📅 今日日期: {today_chinese}")

# 从环境变量读取敏感信息
import os

# 飞书Webhook地址
FEISHU_WEBHOOK = os.environ.get('FEISHU_WEBHOOK', '')

# Deepseek API配置
DEEPSEEK_API_KEY = os.environ.get('DEEPSEEK_API_KEY', '')
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

# Tavily API配置
TAVILY_API_KEY = os.environ.get('TAVILY_API_KEY', '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')

# 检查敏感信息是否配置
if not FEISHU_WEBHOOK:
    print("❌ 错误: 未配置飞书Webhook地址")
    exit(1)
    
if not DEEPSEEK_API_KEY:
    print("❌ 错误: 未配置Deepseek API Key")
    exit(1)
    
if not TAVILY_API_KEY:
    print("❌ 错误: 未配置Tavily API Key")
    exit(1)

# 调用Deepseek API的通用函数
def call_deepseek_api(prompt):
    """调用Deepseek API获取响应"""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
    }
    
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {
                "role": "system",
                "content": "你是一个英语学习助手，提供准确的信息和帮助。"
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.7,
        "max_tokens": 1000
    }
    
    try:
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=payload, timeout=15)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"❌ 调用Deepseek API失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

# 调用Tavily API的通用函数
def call_tavily_api(query, search_depth="basic"):
    """调用Tavily API获取搜索结果"""
    print(f"📞 调用Tavily API，查询: {query}")
    print(f"🔑 使用API密钥: {TAVILY_API_KEY[:10]}...")
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {TAVILY_API_KEY}"
    }
    
    payload = {
        "query": query,
        "search_depth": search_depth,
        "include_answer": True,
        "include_raw_content": False,
        "include_images": False
    }
    
    try:
        print(f"📤 发送请求到Tavily API...")
        response = requests.post("https://api.tavily.com/search", headers=headers, json=payload, timeout=15)
        print(f"📥 收到Tavily API响应，状态码: {response.status_code}")
        print(f"📥 响应内容: {response.text[:500]}...")
        
        response.raise_for_status()
        result = response.json()
        print(f"✅ Tavily API调用成功，返回结果: {result.get('answer', '')[:100]}...")
        return result.get('answer', '')
    except Exception as e:
        print(f"❌ 调用Tavily API失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

# 1. 单词筛选功能 - 六级水平，提供中文释义、例句及发音
def get_cet6_words():
    """获取2个六级水平的英语单词，包含中文释义、例句及发音"""
    print("🔍 正在获取六级英语单词...")
    
    prompt = "请提供2个英语六级水平的单词，格式如下：\n1. 单词：[单词]\n   发音：[音标]\n   中文释义：[中文意思]\n   例句：[英文例句]\n   例句中文：[中文翻译]\n\n2. 单词：[单词]\n   发音：[音标]\n   中文释义：[中文意思]\n   例句：[英文例句]\n   例句中文：[中文翻译]\n\n请确保单词是六级水平，例句地道准确。"
    
    response = call_deepseek_api(prompt)
    if not response:
        print("❌ 获取单词失败，使用默认数据")
        # 返回默认数据
        return [
            {
                'word': 'ephemeral',
                'pronunciation': '/ɪˈfemərəl/',
                'definition': '短暂的，瞬息的',
                'example': 'Fashions are ephemeral: the latest style usually disappears in a season.',
                'example_zh': '时尚是短暂的：最新款式通常在一个季节内就会消失。'
            },
            {
                'word': 'ubiquitous',
                'pronunciation': '/juːˈbɪkwɪtəs/',
                'definition': '无所不在的，普遍存在的',
                'example': 'His ubiquitous influence was felt by all the family.',
                'example_zh': '全家人都感受到了他无处不在的影响。'
            }
        ]
    
    # 解析API返回的单词数据
    words = []
    try:
        for part in response.strip().split('\n\n'):
            if part.startswith('1.') or part.startswith('2.'):
                lines = part.strip().split('\n')
                word_data = {
                    'word': lines[0].split('：')[1].strip(),
                    'pronunciation': lines[1].split('：')[1].strip(),
                    'definition': lines[2].split('：')[1].strip(),
                    'example': lines[3].split('：')[1].strip(),
                    'example_zh': lines[4].split('：')[1].strip()
                }
                words.append(word_data)
    except Exception as e:
        print(f"❌ 解析单词数据失败: {str(e)}")
        # 返回默认数据
        return [
            {
                'word': 'ephemeral',
                'pronunciation': '/ɪˈfemərəl/',
                'definition': '短暂的，瞬息的',
                'example': 'Fashions are ephemeral: the latest style usually disappears in a season.',
                'example_zh': '时尚是短暂的：最新款式通常在一个季节内就会消失。'
            },
            {
                'word': 'ubiquitous',
                'pronunciation': '/juːˈbɪkwɪtəs/',
                'definition': '无所不在的，普遍存在的',
                'example': 'His ubiquitous influence was felt by all the family.',
                'example_zh': '全家人都感受到了他无处不在的影响。'
            }
        ]
    
    return words[:2]  # 确保只返回2个单词

# 2. 天气查询功能 - 杭州拱墅区
def get_hangzhou_weather():
    """获取杭州拱墅区的实时天气数据，包含最高温度、最低温度和天气变化"""
    print("🌤️  正在获取杭州拱墅区天气...")
    
    prompt = f"请提供杭州拱墅区{today_chinese}的实时天气信息，格式必须严格如下：\n城市：杭州拱墅区\n最高温度：[数值]°C\n最低温度：[数值]°C\n天气状况：[当前天气]\n天气变化：[如果有变化请描述，如：上午多云，下午转阴；如果没有变化请写：全天无明显变化]\n\n请确保信息准确，使用最新的实时数据，只返回以上格式的内容，不要添加任何其他解释或说明。"
    
    # 使用Tavily API获取天气信息
    response = call_tavily_api(prompt, search_depth="basic")
    if not response:
        print("❌ 使用Tavily API获取天气失败，尝试使用Deepseek API...")
        response = call_deepseek_api(prompt)
        
        if not response:
            print("❌ 获取天气失败，使用默认数据")
            # 返回默认数据
            return {
                'city': '杭州拱墅区',
                'max_temp': 25,
                'min_temp': 18,
                'description': '多云',
                'change': '上午多云，下午转阴'
            }
    
    # 解析天气数据
    weather = {}
    try:
        for line in response.strip().split('\n'):
            if '：' in line:
                key, value = line.split('：', 1)
                if key == '城市':
                    weather['city'] = value.strip()
                elif key == '最高温度':
                    weather['max_temp'] = int(value.strip().replace('°C', ''))
                elif key == '最低温度':
                    weather['min_temp'] = int(value.strip().replace('°C', ''))
                elif key == '天气状况':
                    weather['description'] = value.strip()
                elif key == '天气变化':
                    weather['change'] = value.strip()
    except Exception as e:
        print(f"❌ 解析天气数据失败: {str(e)}")
        # 返回默认数据
        return {
            'city': '杭州拱墅区',
            'max_temp': 25,
            'min_temp': 18,
            'description': '多云',
            'change': '上午多云，下午转阴'
        }
    
    print(f"✅ 成功获取实时天气：{weather['city']}, {weather['max_temp']}°C/{weather['min_temp']}°C, {weather['description']}")
    return weather

# 3. 新闻筛选与整理功能
def get_chinese_news():
    """获取中文新闻并整理"""
    print("📰 正在获取中文新闻...")
    
    prompt = "请提供3条最新的中文新闻，格式如下：\n1. 标题：[新闻标题]\n   摘要：[新闻摘要]\n   来源：[新闻来源]\n   链接：[新闻链接]\n\n2. 标题：[新闻标题]\n   摘要：[新闻摘要]\n   来源：[新闻来源]\n   链接：[新闻链接]\n\n3. 标题：[新闻标题]\n   摘要：[新闻摘要]\n   来源：[新闻来源]\n   链接：[新闻链接]\n\n请确保新闻是最新的，内容积极正面。"
    
    response = call_deepseek_api(prompt)
    if not response:
        print("❌ 获取新闻失败，使用默认数据")
        # 返回默认数据
        return [
            {
                'title': '中国成功发射新一代通信卫星',
                'description': '北京时间今日凌晨，我国在西昌卫星发射中心成功发射了一颗新一代通信卫星，这将进一步提升我国的通信能力。',
                'source': {'name': '新华网'},
                'url': 'https://www.xinhuanet.com/'
            },
            {
                'title': '全球气候变化会议在巴黎召开',
                'description': '来自世界各地的领导人齐聚巴黎，讨论全球气候变化问题，寻求共同解决方案。',
                'source': {'name': '人民网'},
                'url': 'https://www.people.com.cn/'
            },
            {
                'title': '人工智能技术在医疗领域取得重大突破',
                'description': '研究人员开发的人工智能系统能够准确诊断多种疾病，诊断准确率超过90%。',
                'source': {'name': '科技日报'},
                'url': 'http://www.stdaily.com/'
            }
        ]
    
    # 解析新闻数据
    news_list = []
    try:
        for part in response.strip().split('\n\n'):
            if part.startswith('1.') or part.startswith('2.') or part.startswith('3.'):
                lines = part.strip().split('\n')
                news = {
                    'title': lines[0].split('：')[1].strip(),
                    'description': lines[1].split('：')[1].strip(),
                    'source': {'name': lines[2].split('：')[1].strip()},
                    'url': lines[3].split('：')[1].strip()
                }
                news_list.append(news)
    except Exception as e:
        print(f"❌ 解析新闻数据失败: {str(e)}")
        # 返回默认数据
        return [
            {
                'title': '中国成功发射新一代通信卫星',
                'description': '北京时间今日凌晨，我国在西昌卫星发射中心成功发射了一颗新一代通信卫星，这将进一步提升我国的通信能力。',
                'source': {'name': '新华网'},
                'url': 'https://www.xinhuanet.com/'
            },
            {
                'title': '全球气候变化会议在巴黎召开',
                'description': '来自世界各地的领导人齐聚巴黎，讨论全球气候变化问题，寻求共同解决方案。',
                'source': {'name': '人民网'},
                'url': 'https://www.people.com.cn/'
            },
            {
                'title': '人工智能技术在医疗领域取得重大突破',
                'description': '研究人员开发的人工智能系统能够准确诊断多种疾病，诊断准确率超过90%。',
                'source': {'name': '科技日报'},
                'url': 'http://www.stdaily.com/'
            }
        ]
    
    return news_list[:3]  # 确保只返回3条新闻

# 4. 生成积极鼓励话语
def get_encouraging_message():
    """生成积极的鼓励话语"""
    print("💪 正在生成鼓励话语...")
    
    prompt = "请提供一句积极的英语学习鼓励话语，简短有力，适合放在每日报告中。"
    
    response = call_deepseek_api(prompt)
    if not response:
        # 返回默认鼓励话语
        return "今天也要加油学习英语哦！每一次努力都会带来进步！"
    
    return response.strip()

# 获取数据
weather = get_hangzhou_weather()
word_info = get_cet6_words()
news_list = get_chinese_news()
encouraging_message = get_encouraging_message()

# 打印获取的数据摘要
print(f"🌤️  天气数据: {weather['city']}, {weather['max_temp']}°C/{weather['min_temp']}°C, {weather['description']}")
print(f"📚 单词数量: {len(word_info)} 个")
for i, word in enumerate(word_info):
    print(f"   单词{i+1}: {word['word']} - {word['definition']}")
print(f"📰 新闻数量: {len(news_list)} 条")
print(f"🤖 鼓励话语: {encouraging_message}")

# HTML模板
html_template = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>每日报告 - {today}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Microsoft YaHei', Arial, sans-serif; background-color: #f0f2f5; color: #333; }}
        .container {{ max-width: 800px; margin: 0 auto; padding: 20px; background-color: white; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #1890ff; text-align: center; margin-bottom: 20px; font-size: 28px; }}
        .date {{ text-align: center; color: #666; margin-bottom: 30px; font-size: 16px; }}
        .section {{ margin-bottom: 30px; padding: 20px; background-color: #fafafa; border-radius: 8px; }}
        .section h2 {{ color: #2c3e50; margin-bottom: 15px; font-size: 20px; border-left: 4px solid #1890ff; padding-left: 10px; }}
        .weather-info {{ display: flex; align-items: center; justify-content: space-around; flex-wrap: wrap; margin-bottom: 15px; }}
        .weather-item {{ text-align: center; margin: 10px; }}
        .weather-item .label {{ font-size: 14px; color: #666; margin-bottom: 5px; }}
        .weather-item .value {{ font-size: 24px; font-weight: bold; color: #1890ff; }}
        .weather-item .description {{ font-size: 16px; color: #333; }}
        .weather-change {{ text-align: center; padding: 10px; background-color: #e8f4f8; border-radius: 5px; color: #555; }}
        .word-section {{ text-align: center; margin-bottom: 30px; padding: 20px; background-color: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
        .word {{ font-size: 36px; font-weight: bold; color: #1890ff; margin-bottom: 10px; }}
        .pronunciation {{ font-size: 16px; color: #666; margin-bottom: 15px; }}
        .definition {{ font-size: 18px; margin-bottom: 15px; color: #555; line-height: 1.6; }}
        .example {{ font-size: 16px; color: #666; margin-bottom: 10px; padding: 10px; background-color: #f5f5f5; border-radius: 5px; }}
        .example-zh {{ font-size: 15px; color: #777; font-style: italic; }}
        .words-container {{ display: flex; flex-direction: column; gap: 30px; }}
        .news-list {{ list-style: none; }}
        .news-item {{ margin-bottom: 20px; padding: 15px; background-color: white; border-radius: 5px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
        .news-title {{ font-size: 18px; font-weight: bold; color: #2c3e50; margin-bottom: 8px; }}
        .news-description {{ font-size: 14px; color: #666; margin-bottom: 10px; line-height: 1.5; }}
        .news-source {{ font-size: 12px; color: #999; }}
        .news-link {{ color: #1890ff; text-decoration: none; font-size: 12px; }}
        .news-link:hover {{ text-decoration: underline; }}
        .encouraging-message {{ background-color: #e8f4f8; padding: 20px; border-radius: 5px; line-height: 1.8; color: #27ae60; font-size: 16px; text-align: center; font-weight: bold; }}
        .footer {{ text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee; color: #999; font-size: 14px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📅 每日报告</h1>
        <div class="date">📅 {today_chinese}</div>
        
        <!-- 天气模块 -->
        <div class="section">
            <h2>🌤️ 今日天气</h2>
            <div class="weather-info">
                <div class="weather-item">
                    <div class="label">城市</div>
                    <div class="value">{weather_city}</div>
                </div>
                <div class="weather-item">
                    <div class="label">最高温度</div>
                    <div class="value">{weather_max_temp}°C</div>
                </div>
                <div class="weather-item">
                    <div class="label">最低温度</div>
                    <div class="value">{weather_min_temp}°C</div>
                </div>
                <div class="weather-item">
                    <div class="label">天气状况</div>
                    <div class="description">{weather_desc}</div>
                </div>
            </div>
            <div class="weather-change">
                <strong>天气变化：</strong>{weather_change}
            </div>
        </div>
        
        <!-- 英语单词模块 -->
        <div class="section">
            <h2>📚 每日二词</h2>
            <div class="words-container">
                {words_html}
            </div>
        </div>
        
        <!-- 中文新闻模块 -->
        <div class="section">
            <h2>📰 新闻</h2>
            <ul class="news-list">
                {news_html}
            </ul>
        </div>
        
        <!-- 积极鼓励话语 -->
        <div class="section">
            <h2>💪 学习鼓励</h2>
            <div class="encouraging-message">
                {encouraging_message}
            </div>
        </div>
        
        <div class="footer">
            <p>📧 每日自动生成 | 💡 助力英语学习</p>
        </div>
    </div>
</body>
</html>
"""

# 构建天气HTML
weather_city = weather['city']
weather_max_temp = weather['max_temp']
weather_min_temp = weather['min_temp']
weather_desc = weather['description']
weather_change = weather['change']
print("🔨 正在构建天气HTML...")

# 构建单词HTML（支持2个单词）
words_html = ''
print("🔨 正在构建单词HTML...")
for i, word_data in enumerate(word_info, 1):
    word = word_data['word']
    pronunciation = word_data['pronunciation']
    definition = word_data['definition']
    example = word_data['example']
    example_zh = word_data['example_zh']
    
    words_html += f'''    <div class="word-section">
        <h3 style="color: #1890ff; margin-bottom: 15px; font-size: 18px;">第{i}个词</h3>
        <div class="word">{word}</div>
        <div class="pronunciation">{pronunciation}</div>
        <div class="definition">{definition}</div>
        <div class="example">{example}</div>
        <div class="example-zh">{example_zh}</div>
    </div>
    '''

# 构建新闻HTML
news_html = ''
print("🔨 正在构建新闻HTML...")
for news in news_list:
    title = news['title']
    description = news['description']
    source = news['source']['name']
    url = news['url']
    
    news_html += f'''    <li class="news-item">
        <div class="news-title">{title}</div>
        <div class="news-description">{description}</div>
        <div class="news-source">来源: {source} | <a href="{url}" class="news-link" target="_blank">阅读全文</a></div>
    </li>
    '''

# 填充HTML模板
print("🔨 正在填充HTML模板...")
html_content = html_template.format(
    today=today,
    today_chinese=today_chinese,
    weather_city=weather_city,
    weather_max_temp=weather_max_temp,
    weather_min_temp=weather_min_temp,
    weather_desc=weather_desc,
    weather_change=weather_change,
    words_html=words_html,
    news_html=news_html,
    encouraging_message=encouraging_message
)

# 保存HTML文件
html_file = f"daily_report_{today}.html"
abs_file_path = os.path.abspath(html_file)
print(f"📄 准备生成文件: {html_file}")
print(f"📍 文件绝对路径: {abs_file_path}")

# 保存文件
try:
    with open(abs_file_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    # 检查文件是否存在
    if os.path.exists(abs_file_path):
        file_size = os.path.getsize(abs_file_path)
        print(f"🎉 HTML报告已成功生成: {html_file}")
        print(f"📏 文件大小: {file_size} 字节")
        print("=========================================")
        print(f"📖 如何查看报告:")
        print(f"   1. 直接双击文件: {html_file}")
        print(f"   2. 或在浏览器中打开: {abs_file_path}")
        print("=========================================")
    else:
        print(f"❌ ERROR: HTML报告生成失败，文件不存在: {abs_file_path}")
        print("\n📋 当前目录下的文件:")
        for file in os.listdir('.'):
            print(f"   {file}")
except Exception as e:
    print(f"❌ ERROR: 生成文件时出错: {str(e)}")
    import traceback
    traceback.print_exc()

# 飞书Webhook推送功能
def send_to_feishu(html_file):
    """将HTML报告推送到飞书群"""
    print("=========================================")
    print("📤 开始推送到飞书群...")
    
    try:
        # 获取GitHub Pages URL
        github_repo = os.environ.get('GITHUB_REPOSITORY', '')  # 格式：owner/repo
        if github_repo:
            # 构建GitHub Pages URL
            github_pages_url = f"https://{github_repo.split('/')[0]}.github.io/{github_repo.split('/')[1]}/{html_file}"
        else:
            github_pages_url = os.path.abspath(html_file)
        
        # 构建飞书消息卡片
        payload = {
            "msg_type": "text",
            "content": {
                "text": f"📅 **{today_chinese}**\n已生成今日英语学习报告\n\n🌤️  天气：{weather['city']} {weather['max_temp']}°C/{weather['min_temp']}°C {weather['description']}\n📚 单词：{word_info[0]['word']}, {word_info[1]['word']}\n📰 新闻：{len(news_list)}条\n💪 鼓励：{encouraging_message}\n\n请查看完整报告：{github_pages_url}"
            }
        }
        
        # 发送请求到飞书Webhook
        headers = {
            'Content-Type': 'application/json'
        }
        
        response = requests.post(FEISHU_WEBHOOK, headers=headers, json=payload, timeout=10)
        data = response.json()
        
        print(f"📝 飞书响应状态码: {response.status_code}")
        print(f"📝 飞书响应内容: {json.dumps(data, ensure_ascii=False)}")
        
        if response.status_code == 200 and data.get('code') == 0:
            print("✅ 推送飞书群成功！")
            return True
        else:
            print(f"❌ 推送飞书群失败: {data.get('msg', '未知错误')}")
            return False
    except Exception as e:
        print(f"❌ 推送飞书群异常: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

# 调用飞书推送
send_to_feishu(html_file)

print("=========================================")
print("✅ 脚本执行完成！")
print("=========================================")
