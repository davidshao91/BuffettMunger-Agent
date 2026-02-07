from src.buffett_agent import skills

def test_safety_margin():
    data = {
        "pe_hist_percent": 22,
        "pb_hist_percent": 18,
        "peg": 0.8,
        "roe_ttm": 22.5,
        "debt_to_asset": 35
    }
    res = skills.safety_margin(data)
    assert res["score"] == 100
    assert res["level"] == "安全｜可关注"
    print("✅ 安全边际测试通过")

def test_moat():
    data = {
        "gross_margin": 74,
        "roe_ttm": 25.2,
        "pe_hist_percent": 25,
        "debt_to_asset": 28,
        "revenue_growth": 10
    }
    res = skills.moat(data)
    assert res["score"] >= 70
    assert res["level"] == "强护城河"
    print("✅ 护城河测试通过")