#!/usr/bin/env python3

# 检查依赖是否安装
print("检查依赖是否安装...")

try:
    import requests
    print("✅ requests库已安装")
    print(f"   版本: {requests.__version__}")
except ImportError:
    print("❌ requests库未安装")

try:
    from dotenv import load_dotenv
    print("✅ python-dotenv库已安装")
    print(f"   版本: {load_dotenv.__version__}")
except ImportError:
    print("❌ python-dotenv库未安装")

print("依赖检查完成")
