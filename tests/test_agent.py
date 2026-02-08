from src.buffet_agent.agent import run_analysis
from src.buffet_agent.data import load_sample_data

def test_agent_full_flow():
    data = load_sample_data()["600519.SH"]
    report = run_analysis(data)
    # 适应新的返回格式
    assert report["traditional_analysis"]["avg_score"] >= 80
    assert "强烈推荐" in report["traditional_analysis"]["final_decision"]
    print("✅ Agent 全流程测试通过")