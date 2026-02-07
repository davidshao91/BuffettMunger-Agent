from . import skills

def run_analysis(company_data):
    """
    运行完整价值投资分析流程
    """
    safety = skills.safety_margin(company_data)
    fund = skills.fundamental(company_data)
    moat = skills.moat(company_data)
    risk = skills.risk(company_data)
    final = skills.final_rating([safety, fund, moat, risk])

    return {
        "safety_margin": safety,
        "fundamental": fund,
        "moat": moat,
        "risk": risk,
        "avg_score": final["avg"],
        "final_decision": final["decision"]
    }