from src.buffett_agent.agent import run_analysis
from src.buffett_agent.data import load_sample_data

def main():
    print("=" * 60)
    print("📈 BuffettMunger-Agent 本地运行")
    print("=" * 60)

    # 加载示例数据
    sample_data = load_sample_data()

    for code, data in sample_data.items():
        print(f"\n【分析】{data['name']} ({code})")
        report = run_analysis(data)
        print(f"综合评分: {report['avg_score']}")
        print(f"结论: {report['final_decision']}")
        print("---")

if __name__ == "__main__":
    main()