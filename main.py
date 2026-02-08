from src.buffet_agent.agent import run_analysis
from src.buffet_agent.data import load_data, load_sample_data
import argparse

def main():
    print("=" * 60)
    print("📈 BuffettMunger-Agent 本地运行")
    print("=" * 60)

    # 解析命令行参数
    parser = argparse.ArgumentParser(description='BuffettMunger-Agent 价值投资分析工具')
    parser.add_argument('--code', type=str, help='股票代码 (例如: 600519.SH)')
    parser.add_argument('--real-time', action='store_true', help='使用实时数据')
    parser.add_argument('--all', action='store_true', help='分析所有示例股票')
    args = parser.parse_args()

    if args.code:
        # 分析指定股票
        data = load_data(args.code, args.real_time)
        print(f"\n【分析】{data['name']} ({data['code']})")
        report = run_analysis(data)
        print(f"综合评分: {report['avg_score']}")
        print(f"结论: {report['final_decision']}")
        print("\n详细分析:")
        print(f"  🛡️ 安全边际: {report['safety_margin']['score']}分｜{report['safety_margin']['level']}")
        print(f"  📈 基本面: {report['fundamental']['score']}分｜{report['fundamental']['status']}")
        print(f"  🏰 护城河: {report['moat']['score']}分｜{report['moat']['level']}")
        print(f"  ⚠️  风险评分: {report['risk']['score']}分｜{report['risk']['risk_level']}")
        
        # 打印大模型分析结果
        if 'llm_analysis' in report:
            print("\n  🤖 大模型分析:")
            llm = report['llm_analysis']
            print(f"    建议: {llm.get('investment_recommendation', '未知')}")
            print(f"    风险: {llm.get('risk_assessment', '未知')}")
            print(f"    置信度: {llm.get('confidence_score', 0):.2f}")
            print(f"    分析: {llm.get('llm_analysis', '无')}")
        
        # 打印风险警告
        if report['safety_margin']['warn']:
            print("\n  风险警告:")
            for warn in report['safety_margin']['warn']:
                print(f"    • {warn}")
        print("---")
    else:
        # 分析所有示例股票
        sample_data = load_sample_data()
        for code, data in sample_data.items():
            print(f"\n【分析】{data['name']} ({code})")
            report = run_analysis(data)
            print(f"综合评分: {report['avg_score']}")
            print(f"结论: {report['final_decision']}")
            
            # 打印大模型分析结果
            if 'llm_analysis' in report:
                llm = report['llm_analysis']
                print(f"🤖 大模型建议: {llm.get('investment_recommendation', '未知')}")
            print("---")

if __name__ == "__main__":
    main()