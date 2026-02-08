"""高级集成测试"""
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.buffet_agent import run_analysis, ask_follow_up
from src.buffet_agent.data import load_sample_data
from src.buffet_agent.github_llm import get_github_llm_analysis
from src.buffet_agent.knowledge import build_investment_reasoning


def test_github_llm_integration():
    """
    测试GitHub大模型集成
    """
    # 加载示例数据
    sample_data = load_sample_data()
    company_data = sample_data["600519.SH"]
    
    # 测试GitHub大模型分析
    analysis_result = get_github_llm_analysis(company_data)
    
    # 验证返回结果格式
    assert isinstance(analysis_result, dict)
    assert "analysis_summary" in analysis_result
    assert "investment_recommendation" in analysis_result
    assert "confidence_score" in analysis_result
    assert "risk_assessment" in analysis_result
    assert "key_findings" in analysis_result
    assert "valuation_analysis" in analysis_result
    assert "fundamental_analysis" in analysis_result
    assert "moat_analysis" in analysis_result
    assert "risk_analysis" in analysis_result
    assert "recommendation_reasoning" in analysis_result
    assert "next_steps" in analysis_result
    
    # 验证置信度评分范围
    assert 0 <= analysis_result["confidence_score"] <= 1
    
    # 验证推荐结果
    assert analysis_result["investment_recommendation"] in ["买入", "持有", "卖出"]
    
    # 验证风险评估
    assert analysis_result["risk_assessment"] in ["低", "中", "高"]
    
    print("✅ GitHub大模型集成测试通过")


def test_knowledge_graph_reasoning():
    """
    测试知识图谱推理能力
    """
    # 加载示例数据
    sample_data = load_sample_data()
    company_data = sample_data["600519.SH"]
    
    # 测试投资推理链构建
    reasoning_chain = build_investment_reasoning(company_data)
    
    # 验证返回结果格式
    assert isinstance(reasoning_chain, dict)
    assert "company" in reasoning_chain
    assert "industry" in reasoning_chain
    assert "evidence" in reasoning_chain
    assert "applicable_logics" in reasoning_chain
    assert "reasoning_steps" in reasoning_chain
    assert "conclusion" in reasoning_chain
    assert "confidence" in reasoning_chain
    
    # 验证证据列表
    assert isinstance(reasoning_chain["evidence"], list)
    
    # 验证推理步骤
    assert isinstance(reasoning_chain["reasoning_steps"], list)
    
    # 验证置信度评分范围
    assert 0.3 <= reasoning_chain["confidence"] <= 0.95
    
    print("✅ 知识图谱推理能力测试通过")


def test_advanced_agent_analysis():
    """
    测试增强的智能体分析功能
    """
    # 加载示例数据
    sample_data = load_sample_data()
    company_data = sample_data["600519.SH"]
    
    # 测试完整分析流程
    analysis_result = run_analysis(company_data, "分析贵州茅台的投资价值")
    
    # 验证返回结果格式
    assert isinstance(analysis_result, dict)
    
    # 验证传统分析结果
    assert "traditional_analysis" in analysis_result
    assert "safety_margin" in analysis_result["traditional_analysis"]
    assert "fundamental" in analysis_result["traditional_analysis"]
    assert "moat" in analysis_result["traditional_analysis"]
    assert "risk" in analysis_result["traditional_analysis"]
    assert "avg_score" in analysis_result["traditional_analysis"]
    assert "final_decision" in analysis_result["traditional_analysis"]
    
    # 验证基础大模型分析
    assert "basic_llm_analysis" in analysis_result
    
    # 验证GitHub大模型深度分析
    assert "github_deep_analysis" in analysis_result
    
    # 验证知识增强分析
    assert "knowledge_enhanced" in analysis_result
    assert "reasoning_chain" in analysis_result["knowledge_enhanced"]
    assert "industry_insights" in analysis_result["knowledge_enhanced"]
    assert "company_relationships" in analysis_result["knowledge_enhanced"]
    assert "confidence_enhancement" in analysis_result["knowledge_enhanced"]
    assert "knowledge_based_recommendation" in analysis_result["knowledge_enhanced"]
    
    # 验证综合推荐
    assert "integrated_recommendation" in analysis_result
    
    # 验证公司信息
    assert "company_info" in analysis_result
    assert "code" in analysis_result["company_info"]
    assert "name" in analysis_result["company_info"]
    
    # 验证分析时间
    assert "analysis_time" in analysis_result
    
    print("✅ 增强的智能体分析功能测试通过")


def test_follow_up_question():
    """
    测试追问功能
    """
    # 测试追问
    follow_up_response = ask_follow_up("什么是安全边际？")
    
    # 验证返回结果格式
    assert isinstance(follow_up_response, dict)
    assert "answer" in follow_up_response
    assert "confidence" in follow_up_response
    assert "related_topics" in follow_up_response
    
    # 验证置信度评分范围
    assert 0 <= follow_up_response["confidence"] <= 1
    
    # 验证相关话题
    assert isinstance(follow_up_response["related_topics"], list)
    
    print("✅ 追问功能测试通过")


def test_agent_with_different_companies():
    """
    测试智能体对不同公司的分析
    """
    # 加载示例数据
    sample_data = load_sample_data()
    
    # 测试多家公司
    for code, company_data in sample_data.items():
        analysis_result = run_analysis(company_data)
        
        # 验证返回结果格式
        assert isinstance(analysis_result, dict)
        assert "traditional_analysis" in analysis_result
        assert "github_deep_analysis" in analysis_result
        assert "knowledge_enhanced" in analysis_result
        assert "integrated_recommendation" in analysis_result
        
        print(f"✅ 智能体分析 {company_data['name']} 测试通过")


def test_github_llm_with_user_question():
    """
    测试GitHub大模型处理用户问题
    """
    # 加载示例数据
    sample_data = load_sample_data()
    company_data = sample_data["600519.SH"]
    
    # 测试不同类型的用户问题
    test_questions = [
        "分析贵州茅台的安全边际",
        "五粮液的护城河分析",
        "银行股的投资机会",
        "如何评估一家公司的投资价值"
    ]
    
    for question in test_questions:
        analysis_result = get_github_llm_analysis(company_data, question)
        
        # 验证返回结果格式
        assert isinstance(analysis_result, dict)
        assert "analysis_summary" in analysis_result
        assert "investment_recommendation" in analysis_result
        
        print(f"✅ GitHub大模型处理问题 '{question}' 测试通过")


if __name__ == "__main__":
    # 运行所有测试
    test_github_llm_integration()
    test_knowledge_graph_reasoning()
    test_advanced_agent_analysis()
    test_follow_up_question()
    test_agent_with_different_companies()
    test_github_llm_with_user_question()
    print("\n🎉 所有高级集成测试通过！")
