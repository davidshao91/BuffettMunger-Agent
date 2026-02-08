"""大模型接口测试"""
from src.buffet_agent.llm import LLMInterface, get_llm_analysis
from src.buffet_agent.agent import run_analysis


def test_llm_interface():
    """测试大模型接口"""
    llm = LLMInterface()
    
    # 测试有效的公司数据
    company_data = {
        "code": "600519.SH",
        "name": "贵州茅台",
        "pe": 15.2,
        "pb": 3.1,
        "peg": 0.8,
        "pe_hist_percent": 22,
        "pb_hist_percent": 18,
        "roe_ttm": 22.5,
        "debt_to_asset": 35,
        "revenue_growth": 12,
        "profit_growth": 10,
        "gross_margin": 40,
        "cash_flow_healthy": True
    }
    
    analysis = llm.generate_analysis(company_data)
    assert isinstance(analysis, dict)
    assert "llm_analysis" in analysis
    assert "investment_recommendation" in analysis
    assert "risk_assessment" in analysis
    assert "confidence_score" in analysis
    print("✅ 大模型接口测试通过")


def test_get_llm_analysis():
    """测试获取大模型分析结果"""
    company_data = {
        "code": "600519.SH",
        "name": "贵州茅台",
        "pe": 15.2,
        "pb": 3.1,
        "roe_ttm": 22.5
    }
    
    analysis = get_llm_analysis(company_data)
    assert isinstance(analysis, dict)
    assert "llm_analysis" in analysis
    assert "investment_recommendation" in analysis
    print("✅ 大模型分析结果获取测试通过")


def test_llm_integration():
    """测试大模型与Agent的集成"""
    company_data = {
        "code": "600519.SH",
        "name": "贵州茅台",
        "pe": 15.2,
        "pb": 3.1,
        "peg": 0.8,
        "pe_hist_percent": 22,
        "pb_hist_percent": 18,
        "roe_ttm": 22.5,
        "debt_to_asset": 35,
        "revenue_growth": 12,
        "profit_growth": 10,
        "gross_margin": 40,
        "cash_flow_healthy": True
    }
    
    report = run_analysis(company_data)
    assert isinstance(report, dict)
    assert "llm_analysis" in report
    assert isinstance(report["llm_analysis"], dict)
    assert "investment_recommendation" in report["llm_analysis"]
    print("✅ 大模型与Agent集成测试通过")


def test_llm_with_invalid_data():
    """测试大模型处理无效数据"""
    # 测试空数据
    empty_data = {}
    analysis = get_llm_analysis(empty_data)
    assert isinstance(analysis, dict)
    assert "llm_analysis" in analysis
    
    # 测试不完整数据
    incomplete_data = {"code": "600519.SH"}
    analysis = get_llm_analysis(incomplete_data)
    assert isinstance(analysis, dict)
    assert "llm_analysis" in analysis
    print("✅ 大模型处理无效数据测试通过")


if __name__ == "__main__":
    test_llm_interface()
    test_get_llm_analysis()
    test_llm_integration()
    test_llm_with_invalid_data()
    print("\n🎉 所有大模型测试通过！")
