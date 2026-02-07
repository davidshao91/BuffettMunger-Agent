from src.buffett_agent.agent import run_analysis
from src.buffett_agent.data import load_sample_data

def test_agent_full_flow():
    data = load_sample_data()["600519.SH"]
    report = run_analysis(data)
    assert report["avg_score"] >= 80
    assert "强烈推荐" in report["final_decision"]
    print("✅ Agent 全流程测试通过")