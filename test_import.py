"""测试导入路径"""
import sys
print("Python路径:", sys.path)

# 尝试导入模块
try:
    from src.buffet_agent import data
    print("✅ 成功导入 src.buffet_agent.data")
except Exception as e:
    print(f"❌ 导入失败: {e}")
