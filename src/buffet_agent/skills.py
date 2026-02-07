def safety_margin(data):
    score = 0
    reason = []
    warn = []

    if data.get("pe_hist_percent", 99) < 30:
        score += 20
        reason.append(f"PE处于历史低分位({data['pe_hist_percent']}%)")
    if data.get("pb_hist_percent", 99) < 30:
        score += 20
        reason.append(f"PB处于历史低分位({data['pb_hist_percent']}%)")
    if data.get("peg", 99) < 1.0:
        score += 20
        reason.append(f"PEG合理({data['peg']})")
    if data.get("roe_ttm", 0) > 15:
        score += 20
        reason.append(f"ROE优秀({data['roe_ttm']}%)")
    if data.get("debt_to_asset", 100) < 50:
        score += 20
        reason.append(f"负债健康({data['debt_to_asset']}%)")

    if score >= 80:
        level = "安全｜可关注"
        margin = "高安全边际"
        suggest = "可分批布局，长期持有"
    elif score >= 60:
        level = "一般｜观察"
        margin = "中等安全边际"
        suggest = "持续跟踪，等待更好价格"
    else:
        level = "危险｜回避"
        margin = "无安全边际"
        suggest = "估值偏高，建议规避"

    if data.get("pe", 0) > 50:
        warn.append("PE过高，估值泡沫风险")
    if data.get("debt_to_asset", 0) > 70:
        warn.append("负债率过高，财务风险大")

    return {
        "score": score,
        "level": level,
        "margin": margin,
        "reason": reason,
        "warn": warn,
        "suggest": suggest
    }

def fundamental(data):
    score = 0
    reason = []
    warn = []

    if data.get("roe_ttm", 0) > 15:
        score += 25
        reason.append("ROE连续优秀")
    if data.get("gross_margin", 0) > 30:
        score += 25
        reason.append("毛利率健康，具备定价权")
    if data.get("revenue_growth", 0) > 8:
        score += 20
        reason.append("营收稳步增长")
    if data.get("profit_growth", 0) > 5:
        score += 20
        reason.append("利润增长稳定")
    if data.get("cash_flow_healthy", False):
        score += 10
        reason.append("现金流健康")

    status = "优秀" if score >= 70 else "一般" if score >= 50 else "较差"

    if data.get("profit_growth", 0) < 0:
        warn.append("利润出现负增长")

    return {
        "score": score,
        "status": status,
        "reason": reason,
        "warn": warn
    }

def moat(data):
    score = 0
    reason = []

    if data.get("gross_margin", 0) > 40:
        score += 25
        reason.append("高毛利 → 品牌/定价权护城河")
    if data.get("roe_ttm", 0) > 20:
        score += 25
        reason.append("长期高ROE → 竞争壁垒强")
    if data.get("pe_hist_percent", 100) < 50:
        score += 20
        reason.append("市场长期给予稳定估值 → 认可度高")
    if data.get("debt_to_asset", 100) < 40:
        score += 20
        reason.append("财务稳健 → 抗周期能力强")
    if data.get("revenue_growth", 0) > 10:
        score += 10
        reason.append("成长稳定 → 规模护城河")

    level = "强护城河" if score >= 70 else "一般" if score >= 50 else "无明显护城河"
    return {
        "score": score,
        "level": level,
        "reason": reason
    }

def risk(data):
    score = 100
    warn = []

    if data.get("debt_to_asset", 0) > 60:
        score -= 30
        warn.append("负债率过高")
    if data.get("pe", 0) > 50:
        score -= 20
        warn.append("估值过高")
    if data.get("profit_growth", 0) < 0:
        score -= 25
        warn.append("利润下滑")
    if not data.get("cash_flow_healthy", False):
        score -= 25
        warn.append("现金流不健康")

    risk_level = "低风险" if score >= 70 else "中风险" if score >= 50 else "高风险"
    return {
        "score": max(score, 0),
        "risk_level": risk_level,
        "warn": warn
    }

def final_rating(results):
    total = 0
    count = 0
    all_warn = []

    for res in results:
        if "score" in res:
            total += res["score"]
            count += 1
        if "warn" in res and res["warn"]:
            all_warn.extend(res["warn"])

    avg = total // count if count > 0 else 0

    if avg >= 80:
        final = "🌟 强烈推荐｜价值优质 + 安全边际高"
    elif avg >= 65:
        final = "✅ 建议关注｜基本面稳健"
    elif avg >= 50:
        final = "⚠️  中性观察｜需等待更好价格"
    else:
        final = "❌ 规避｜风险偏高或估值过贵"

    return {
        "avg": avg,
        "decision": final,
        "all_warnings": all_warn
    }