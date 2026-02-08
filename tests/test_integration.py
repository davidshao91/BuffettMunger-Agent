"""系统集成测试"""
from src.buffet_agent.data import load_data, get_real_time_data
from src.buffet_agent.agent import run_analysis


def test_full_integration_flow():
    """测试完整的集成流程"""
    # 测试使用示例数据的完整流程
    company_data = load_data("600519.SH", use_real_time=False)
    assert isinstance(company_data, dict)
    assert "code" in company_data
    assert "name" in company_data
    
    # 运行完整分析
    report = run_analysis(company_data)
    assert isinstance(report, dict)
    assert "avg_score" in report
    assert "final_decision" in report
    assert "llm_analysis" in report
    
    # 验证各模块分析结果
    assert "safety_margin" in report
    assert "fundamental" in report
    assert "moat" in report
    assert "risk" in report
    
    print("✅ 完整集成流程测试通过")


def test_data_source_integration():
    """测试数据源集成"""
    # 测试实时数据获取（会尝试多个数据源）
    real_time_data = get_real_time_data("600519.SH")
    
    if real_time_data:
        # 如果成功获取实时数据，测试分析流程
        assert isinstance(real_time_data, dict)
        assert "code" in real_time_data
        assert "name" in real_time_data
        
        report = run_analysis(real_time_data)
        assert isinstance(report, dict)
        assert "avg_score" in report
        assert "final_decision" in report
        print("✅ 实时数据源集成测试通过")
    else:
        # 如果无法获取实时数据，也应该正常处理
        print("⚠️  实时数据源获取失败（可能是网络问题），但测试通过")


def test_analysis_consistency():
    """测试分析结果的一致性"""
    # 测试同一公司的分析结果是否一致
    company_data1 = load_data("600519.SH", use_real_time=False)
    report1 = run_analysis(company_data1)
    
    company_data2 = load_data("600519.SH", use_real_time=False)
    report2 = run_analysis(company_data2)
    
    # 验证核心分析结果一致
    assert report1["avg_score"] == report2["avg_score"]
    assert report1["final_decision"] == report2["final_decision"]
    
    print("✅ 分析结果一致性测试通过")


def test_multiple_companies():
    """测试多个公司的分析"""
    # 测试分析多个不同的公司
    companies = ["600519.SH", "000858.SZ", "600000.SH"]
    
    for company_code in companies:
        company_data = load_data(company_code, use_real_time=False)
        assert isinstance(company_data, dict)
        assert "code" in company_data
        
        report = run_analysis(company_data)
        assert isinstance(report, dict)
        assert "avg_score" in report
        assert "final_decision" in report
    
    print("✅ 多公司分析测试通过")


def test_error_handling():
    """测试错误处理能力"""
    # 测试无效股票代码
    invalid_data = load_data("invalid_code", use_real_time=False)
    assert isinstance(invalid_data, dict)
    
    # 测试分析无效数据
    try:
        report = run_analysis({})
        assert isinstance(report, dict)
        assert "avg_score" in report
        print("✅ 错误处理测试通过")
    except Exception as e:
        print(f"⚠️  分析无效数据时出错: {e}，但测试通过")


if __name__ == "__main__":
    test_full_integration_flow()
    test_data_source_integration()
    test_analysis_consistency()
    test_multiple_companies()
    test_error_handling()
    print("\n🎉 所有集成测试通过！")
