"""运行所有测试"""
import os
import sys

# 确保项目根目录在Python路径中
sys.path.insert(0, os.path.abspath('.'))

print("开始运行所有测试...")
print("=" * 60)

# 运行数据测试
print("\n1. 运行数据获取测试:")
print("-" * 40)
try:
    from tests import test_data
    test_data.test_load_sample_data()
    test_data.test_get_sina_finance_data()
    test_data.test_get_xueqiu_data()
    test_data.test_get_xiaohongshu_data()
    test_data.test_get_real_time_data()
    test_data.test_get_real_time_data_invalid()
    test_data.test_load_data_with_real_time()
    test_data.test_load_data_fallback()
    print("✅ 数据获取测试通过！")
except Exception as e:
    print(f"❌ 数据获取测试失败: {e}")

# 运行技能测试
print("\n2. 运行技能模块测试:")
print("-" * 40)
try:
    from tests import test_skills
    test_skills.test_safety_margin()
    test_skills.test_moat()
    print("✅ 技能模块测试通过！")
except Exception as e:
    print(f"❌ 技能模块测试失败: {e}")

# 运行Agent测试
print("\n3. 运行Agent测试:")
print("-" * 40)
try:
    from tests import test_agent
    test_agent.test_agent_full_flow()
    print("✅ Agent测试通过！")
except Exception as e:
    print(f"❌ Agent测试失败: {e}")

# 运行大模型测试
print("\n4. 运行大模型测试:")
print("-" * 40)
try:
    from tests import test_llm
    test_llm.test_llm_interface()
    test_llm.test_get_llm_analysis()
    test_llm.test_llm_integration()
    test_llm.test_llm_with_invalid_data()
    print("✅ 大模型测试通过！")
except Exception as e:
    print(f"❌ 大模型测试失败: {e}")

# 运行集成测试
print("\n5. 运行集成测试:")
print("-" * 40)
try:
    from tests import test_integration
    test_integration.test_full_integration_flow()
    test_integration.test_data_source_integration()
    test_integration.test_analysis_consistency()
    test_integration.test_multiple_companies()
    test_integration.test_error_handling()
    print("✅ 集成测试通过！")
except Exception as e:
    print(f"❌ 集成测试失败: {e}")

print("\n" + "=" * 60)
print("所有测试运行完成！")
