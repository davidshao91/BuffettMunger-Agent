function safetyMargin(data) {
  let score = 0;
  let reason = [];
  let warn = [];
  if (data.pe_hist_percent < 30) { score += 20; reason.push(`PE处于历史低分位(${data.pe_hist_percent}%)`); }
  if (data.pb_hist_percent < 30) { score += 20; reason.push(`PB处于历史低分位(${data.pb_hist_percent}%)`); }
  if (data.peg < 1) { score += 20; reason.push(`PEG合理(${data.peg})`); }
  if (data.roe_ttm > 15) { score += 20; reason.push(`ROE优秀(${data.roe_ttm}%)`); }
  if (data.debt_to_asset < 50) { score += 20; reason.push(`负债健康(${data.debt_to_asset}%)`); }
  let level, margin, suggest;
  if (score >= 80) {
    level = "安全｜可关注"; margin = "高安全边际"; suggest = "可分批布局，长期持有";
  } else if (score >= 60) {
    level = "一般｜观察"; margin = "中等安全边际"; suggest = "持续跟踪，等待更好价格";
  } else {
    level = "危险｜回避"; margin = "无安全边际"; suggest = "估值偏高，建议规避";
  }
  if (data.pe > 50) warn.push("PE过高，估值泡沫风险");
  if (data.debt_to_asset > 70) warn.push("负债率过高，财务风险大");
  return { score, level, margin, reason, warn, suggest };
}

function fundamental(data) {
  let score = 0;
  let reason = [];
  let warn = [];
  if (data.roe_ttm > 15) { score += 25; reason.push("ROE连续优秀"); }
  if (data.gross_margin > 30) { score += 25; reason.push("毛利率健康，具备定价权"); }
  if (data.revenue_growth > 8) { score += 20; reason.push("营收稳步增长"); }
  if (data.profit_growth > 5) { score += 20; reason.push("利润增长稳定"); }
  if (data.cash_flow_healthy) { score += 10; reason.push("现金流健康"); }
  let status = score >= 70 ? "优秀" : score >= 50 ? "一般" : "较差";
  if (data.profit_growth < 0) warn.push("利润负增长");
  return { score, status, reason, warn };
}

function moat(data) {
  let score = 0;
  let reason = [];
  if (data.gross_margin > 40) { score += 25; reason.push("高毛利→品牌/定价权护城河"); }
  if (data.roe_ttm > 20) { score += 25; reason.push("长期高ROE→壁垒强"); }
  if (data.pe_hist_percent < 50) { score += 20; reason.push("市场长期稳定认可"); }
  if (data.debt_to_asset < 40) { score += 20; reason.push("财务稳健，抗周期"); }
  if (data.revenue_growth > 10) { score += 10; reason.push("规模护城河"); }
  let level = score >= 70 ? "强护城河" : score >= 50 ? "一般" : "无明显护城河";
  return { score, level, reason };
}

function risk(data) {
  let score = 100;
  let warn = [];
  if (data.debt_to_asset > 60) { score -= 30; warn.push("负债率过高"); }
  if (data.pe > 50) { score -= 20; warn.push("估值过高"); }
  if (data.profit_growth < 0) { score -= 25; warn.push("利润下滑"); }
  if (!data.cash_flow_healthy) { score -= 25; warn.push("现金流不健康"); }
  score = Math.max(score, 0);
  let riskLevel = score >= 70 ? "低风险" : score >= 50 ? "中风险" : "高风险";
  return { score, riskLevel, warn };
}

function finalRating(results) {
  let total = 0, cnt = 0;
  let allWarn = [];
  for (let r of results) {
    if (r.score !== undefined) { total += r.score; cnt++; }
    if (r.warn) allWarn.push(...r.warn);
  }
  let avg = cnt > 0 ? Math.round(total / cnt) : 0;
  let decision;
  if (avg >= 80) decision = "🌟 强烈推荐｜价值优质 + 安全边际高";
  else if (avg >= 65) decision = "✅ 建议关注｜基本面稳健";
  else if (avg >= 50) decision = "⚠️ 中性观察｜需等待更好价格";
  else decision = "❌ 规避｜风险或估值过高";
  return { avg, decision, allWarn };
}

document.addEventListener("DOMContentLoaded", () => {
  const sel = document.getElementById("stockSelector");
  const runBtn = document.getElementById("runBtn");
  const result = document.getElementById("result");
  const report = document.querySelector(".report");
  const loading = document.querySelector(".loading");

  for (let code in stockData) {
    const opt = document.createElement("option");
    opt.value = code;
    opt.textContent = `${stockData[code].name} (${code})`;
    sel.appendChild(opt);
  }

  runBtn.addEventListener("click", () => {
    const code = sel.value;
    if (!code) return alert("请选择公司");
    const data = stockData[code];
    result.classList.remove("hidden");
    loading.classList.remove("hidden");
    report.textContent = "";
    runBtn.disabled = true;

    setTimeout(() => {
      const r1 = safetyMargin(data);
      const r2 = fundamental(data);
      const r3 = moat(data);
      const r4 = risk(data);
      const final = finalRating([r1, r2, r3, r4]);

      let out = `📊 公司：${data.name} (${data.code})\n\n`;
      out += `🛡️ 安全边际：${r1.score}分｜${r1.level}\n`;
      out += `📈 基本面：${r2.score}分｜${r2.status}\n`;
      out += `🏰 护城河：${r3.score}分｜${r3.level}\n`;
      out += `⚠️  风险评分：${r4.score}分｜${r4.riskLevel}\n\n`;
      out += `🎯 综合评分：${final.avg}\n`;
      out += `✅ 最终结论：${final.decision}\n\n`;
      if (final.allWarn.length > 0) {
        out += "警告：\n" + final.allWarn.map(w => "• " + w).join("\n") + "\n\n";
      }
      out += "本分析基于离线沙盒数据，仅供学习，不构成投资建议。";

      report.textContent = out;
      loading.classList.add("hidden");
      runBtn.disabled = false;
    }, 1200);
  });
});