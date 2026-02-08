import requests
import json

# 测试/stocks接口
print("测试/stocks接口...")
r = requests.get('http://localhost:5000/api/stocks')
print(f"状态码: {r.status_code}")
print(f"响应: {r.json()}\n")

# 测试/analyze接口
print("测试/analyze接口...")
test_data = {
    "code": "600519.SH",
    "user_question": "分析贵州茅台的安全边际",
    "real_time": False
}

r = requests.post('http://localhost:5000/api/analyze', json=test_data)
print(f"状态码: {r.status_code}")
print(f"响应: {r.json()}\n")

# 测试/ask接口
print("测试/ask接口...")
test_question = {
    "question": "什么是安全边际？"
}

r = requests.post('http://localhost:5000/api/ask', json=test_question)
print(f"状态码: {r.status_code}")
print(f"响应: {r.json()}")
