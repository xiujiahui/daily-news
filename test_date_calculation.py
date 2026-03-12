#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试日期计算逻辑
"""

from datetime import datetime, timedelta

# 测试日期计算逻辑
print("=========================================")
print("🔄 测试日期计算逻辑...")
print("=========================================")

# 今日日期
today = datetime.now().strftime('%Y-%m-%d')
today_chinese = datetime.now().strftime('%Y年%m月%d日')

# 计算前一天日期
yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
yesterday_chinese = (datetime.now() - timedelta(days=1)).strftime('%Y年%m月%d日')

print(f"今日日期: {today} ({today_chinese})")
print(f"昨日日期: {yesterday} ({yesterday_chinese})")

# 验证日期是否正确
today_dt = datetime.strptime(today, '%Y-%m-%d')
yesterday_dt = datetime.strptime(yesterday, '%Y-%m-%d')
expected_yesterday_dt = today_dt - timedelta(days=1)

if yesterday_dt == expected_yesterday_dt:
    print("✅ 日期计算正确：昨日确实是今日的前一天")
else:
    print(f"❌ 日期计算错误：预期昨日为 {expected_yesterday_dt.strftime('%Y-%m-%d')}，实际为 {yesterday}")

# 测试不同日期的计算
print("\n📅 测试其他日期情况：")
test_dates = [
    '2026-03-12',  # 普通日期
    '2026-03-01',  # 月初
    '2026-04-01',  # 月初且跨月
    '2026-02-29',  # 闰年2月29日
    '2025-03-01',  # 平年3月1日
]

for test_date in test_dates:
    test_dt = datetime.strptime(test_date, '%Y-%m-%d')
    test_yesterday_dt = test_dt - timedelta(days=1)
    test_yesterday = test_yesterday_dt.strftime('%Y-%m-%d')
    print(f"  {test_date} 的前一天是 {test_yesterday}")

print("\n✅ 所有测试完成！")
print("=========================================")
