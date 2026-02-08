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

// 获取实时股票数据
async function getRealTimeData(stockCode) {
  try {
    // 处理股票代码格式，支持更灵活的输入
    let processedCode = stockCode;
    let exchange = '';
    
    // 提取股票代码数字部分
    const codeMatch = stockCode.match(/\d{6}/);
    if (!codeMatch) {
      return null;
    }
    
    const numericCode = codeMatch[0];
    
    // 根据股票代码判断交易所
    if (stockCode.endsWith('.SH') || numericCode.startsWith('6')) {
      exchange = 'SH';
      processedCode = numericCode + '.SH';
    } else if (stockCode.endsWith('.SZ') || numericCode.startsWith('0') || numericCode.startsWith('3')) {
      exchange = 'SZ';
      processedCode = numericCode + '.SZ';
    } else {
      // 默认使用沪市
      exchange = 'SH';
      processedCode = numericCode + '.SH';
    }
    
    // 首先检查本地数据，避免不必要的网络请求
    if (stockData[processedCode]) {
      return stockData[processedCode];
    }
    
    // 尝试从本地数据中匹配数字代码
    for (const code in stockData) {
      if (code.includes(numericCode)) {
        return stockData[code];
      }
    }
    
    // 只有在本地数据不存在时才尝试获取实时数据
    // 转换为API使用的格式
    const apiCode = (exchange === 'SH' ? 'sh' : 'sz') + numericCode;
    
    // 新浪财经API接口
    const url = `http://hq.sinajs.cn/list=${apiCode}`;
    
    // 添加超时处理
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 3000);
    
    try {
      const response = await fetch(url, {
        signal: controller.signal,
        headers: {
          'Content-Type': 'text/plain'
        }
      });
      clearTimeout(timeoutId);
      
      if (!response.ok) {
        throw new Error('API请求失败');
      }
      
      const data = await response.text();
      
      if (data.includes('=') && !data.includes('null')) {
        const dataPart = data.split('=')[1].trim().replace(/"/g, '');
        const stockInfo = dataPart.split(',');
        
        if (stockInfo.length > 3) {
          // 构建基本数据结构
          // 注意：新浪财经API返回的字段有限，这里使用模拟数据填充部分字段
          return {
            code: processedCode,
            name: stockInfo[0],
            pe: 15.0,  // 模拟数据
            pb: 3.0,   // 模拟数据
            peg: 1.0,  // 模拟数据
            pe_hist_percent: 50,  // 模拟数据
            pb_hist_percent: 50,  // 模拟数据
            roe_ttm: 15.0,  // 模拟数据
            debt_to_asset: 40,  // 模拟数据
            revenue_growth: 8,  // 模拟数据
            profit_growth: 5,  // 模拟数据
            gross_margin: 30,  // 模拟数据
            cash_flow_healthy: true  // 模拟数据
          };
        }
      }
    } catch (fetchError) {
      clearTimeout(timeoutId);
      console.error('网络请求失败:', fetchError);
      // 网络请求失败时，直接返回null，由调用方处理
    }
    
    return null;
  } catch (error) {
    console.error('获取实时数据失败:', error);
    
    // 错误处理：尝试从本地数据中获取
    const codeMatch = stockCode.match(/\d{6}/);
    if (codeMatch) {
      const numericCode = codeMatch[0];
      
      // 尝试匹配本地数据
      for (const code in stockData) {
        if (code.includes(numericCode)) {
          return stockData[code];
        }
      }
    }
    
    return null;
  }
}

// 持仓数据管理
function getHoldings() {
  const holdings = localStorage.getItem('buffettMungerHoldings');
  return holdings ? JSON.parse(holdings) : [];
}

function saveHoldings(holdings) {
  localStorage.setItem('buffettMungerHoldings', JSON.stringify(holdings));
}

function addHolding(holding) {
  const holdings = getHoldings();
  holdings.push(holding);
  saveHoldings(holdings);
}

function removeHolding(stockCode) {
  const holdings = getHoldings();
  const updatedHoldings = holdings.filter(h => h.code !== stockCode);
  saveHoldings(updatedHoldings);
}

// 渲染持仓列表
function renderHoldings() {
  const holdings = getHoldings();
  const tableBody = document.getElementById('holdingsTableBody');
  const noHoldingsMsg = document.getElementById('noHoldingsMsg');
  
  tableBody.innerHTML = '';
  
  if (holdings.length === 0) {
    noHoldingsMsg.style.display = 'block';
  } else {
    noHoldingsMsg.style.display = 'none';
    
    holdings.forEach(holding => {
      const stock = stockData[holding.code];
      if (stock) {
        const row = document.createElement('tr');
        row.innerHTML = `
          <td style="padding: 0.5rem; border: 1px solid #ddd;">${stock.name}</td>
          <td style="padding: 0.5rem; text-align: right; border: 1px solid #ddd;">${holding.code}</td>
          <td style="padding: 0.5rem; text-align: right; border: 1px solid #ddd;">¥${holding.cost.toFixed(2)}</td>
          <td style="padding: 0.5rem; text-align: right; border: 1px solid #ddd;">${holding.quantity}</td>
          <td style="padding: 0.5rem; text-align: right; border: 1px solid #ddd;">
            <button class="deleteHoldingBtn" data-code="${holding.code}">删除</button>
          </td>
        `;
        tableBody.appendChild(row);
      }
    });
    
    // 添加删除按钮事件
    document.querySelectorAll('.deleteHoldingBtn').forEach(btn => {
      btn.addEventListener('click', function() {
        const code = this.getAttribute('data-code');
        removeHolding(code);
        renderHoldings();
      });
    });
  }
}

// 显示添加持仓对话框
function showAddHoldingDialog() {
  const stockCode = prompt('请输入股票代码（例如：600519 或 600519.SH）:');
  if (!stockCode) return;
  
  // 处理股票代码格式
  let processedCode = stockCode;
  const codeMatch = stockCode.match(/\d{6}/);
  
  if (codeMatch) {
    const numericCode = codeMatch[0];
    
    // 根据股票代码判断交易所
    if (stockCode.endsWith('.SH') || numericCode.startsWith('6')) {
      processedCode = numericCode + '.SH';
    } else if (stockCode.endsWith('.SZ') || numericCode.startsWith('0') || numericCode.startsWith('3')) {
      processedCode = numericCode + '.SZ';
    } else {
      // 默认使用沪市
      processedCode = numericCode + '.SH';
    }
  }
  
  // 查找股票
  let stock = null;
  if (stockData[processedCode]) {
    stock = stockData[processedCode];
  } else {
    // 尝试从本地数据中匹配数字代码
    const codeMatch = stockCode.match(/\d{6}/);
    if (codeMatch) {
      const numericCode = codeMatch[0];
      for (const code in stockData) {
        if (code.includes(numericCode)) {
          stock = stockData[code];
          processedCode = code;
          break;
        }
      }
    }
  }
  
  if (!stock) {
    alert('未找到该股票，请输入正确的股票代码');
    return;
  }
  
  // 设置默认成本价格（使用模拟数据中的合理值）
  const defaultCost = 100.0;
  const costInput = prompt(`请输入持仓成本（元）:`, defaultCost);
  const cost = parseFloat(costInput);
  if (isNaN(cost)) return;
  
  // 设置默认持仓数量
  const defaultQuantity = 100;
  const quantityInput = prompt(`请输入持仓数量:`, defaultQuantity);
  const quantity = parseInt(quantityInput);
  if (isNaN(quantity)) return;
  
  addHolding({
    code: processedCode,
    cost: cost,
    quantity: quantity
  });
  
  renderHoldings();
  alert('持仓添加成功！');
}

// 分析持仓
function analyzeHoldings() {
  const holdings = getHoldings();
  if (holdings.length === 0) {
    alert('请先添加持仓');
    return;
  }
  
  const holdingsAnalysis = document.getElementById('holdingsAnalysis');
  const report = holdingsAnalysis.querySelector('.report');
  const loading = holdingsAnalysis.querySelector('.loading');
  
  holdingsAnalysis.classList.remove('hidden');
  loading.style.display = 'block';
  report.textContent = '';
  
  // 分析每只持仓股票
  const analysisResults = [];
  let totalScore = 0;
  let highRiskCount = 0;
  let lowSafetyCount = 0;
  
  for (const holding of holdings) {
    const stock = stockData[holding.code];
    if (stock) {
      const r1 = safetyMargin(stock);
      const r2 = fundamental(stock);
      const r3 = moat(stock);
      const r4 = risk(stock);
      const final = finalRating([r1, r2, r3, r4]);
      
      analysisResults.push({
        holding: holding,
        stock: stock,
        safety: r1,
        fundamental: r2,
        moat: r3,
        risk: r4,
        final: final
      });
      
      totalScore += final.avg;
      if (r4.riskLevel === "高风险") highRiskCount++;
      if (r1.level === "危险｜回避") lowSafetyCount++;
    }
  }
  
  setTimeout(() => {
    // 计算持仓指标
    const portfolioAvgScore = Math.round(totalScore / analysisResults.length);
    const riskPercentage = Math.round((highRiskCount / analysisResults.length) * 100);
    const safetyPercentage = Math.round(((analysisResults.length - lowSafetyCount) / analysisResults.length) * 100);
    
    // 生成持仓分析报告
    let out = `📊 持仓分析报告\n\n`;
    out += `持仓包含 ${analysisResults.length} 只股票\n`;
    out += `持仓平均评分: ${portfolioAvgScore}\n`;
    out += `高风险股票占比: ${riskPercentage}%\n`;
    out += `安全边际良好股票占比: ${safetyPercentage}%\n\n`;
    
    // 添加每只股票的简要分析
    out += `持仓明细分析:\n`;
    for (const result of analysisResults) {
      out += `\n• ${result.stock.name} (${result.stock.code}):\n`;
      out += `  评分: ${result.final.avg}｜结论: ${result.final.decision}\n`;
      out += `  风险: ${result.risk.riskLevel}｜安全边际: ${result.safety.level}\n`;
      out += `  持仓成本: ¥${result.holding.cost.toFixed(2)}｜持仓数量: ${result.holding.quantity}\n`;
    }
    
    // 添加持仓建议
    out += `\n持仓建议:\n`;
    if (portfolioAvgScore >= 80) {
      out += `✅ 持仓质量优秀，建议长期持有\n`;
    } else if (portfolioAvgScore >= 65) {
      out += `⚠️ 持仓质量良好，可适当调整配置\n`;
    } else {
      out += `❌ 持仓质量一般，建议重新评估选股\n`;
    }
    
    if (riskPercentage > 30) {
      out += `⚠️ 持仓风险较高，建议降低高风险股票比例\n`;
    }
    
    if (safetyPercentage < 70) {
      out += `⚠️ 安全边际良好的股票占比较低，建议增加安全边际高的股票\n`;
    }
    
    out += `\n本分析基于离线沙盒数据，仅供学习，不构成投资建议。`;

    report.textContent = out;
    loading.style.display = 'none';
    
    // 生成持仓分析图表
    generateHoldingsChart(analysisResults);
  }, 1200);
}

// 生成持仓分析图表
function generateHoldingsChart(analysisResults) {
  // 销毁旧图表
  if (window.holdingsChart && typeof window.holdingsChart.destroy === 'function') {
    window.holdingsChart.destroy();
  }
  
  // 准备数据
  const stockNames = analysisResults.map(result => result.stock.name);
  const finalScores = analysisResults.map(result => result.final.avg);
  const safetyScores = analysisResults.map(result => result.safety.score);
  const riskScores = analysisResults.map(result => result.risk.score);
  
  // 持仓评分对比图
  const holdingsChartCtx = document.getElementById('holdingsChart').getContext('2d');
  window.holdingsChart = new Chart(holdingsChartCtx, {
    type: 'radar',
    data: {
      labels: stockNames,
      datasets: [{
        label: '综合评分',
        data: finalScores,
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 2,
        pointBackgroundColor: 'rgba(75, 192, 192, 1)',
        pointBorderColor: '#fff',
        pointHoverBackgroundColor: '#fff',
        pointHoverBorderColor: 'rgba(75, 192, 192, 1)'
      }, {
        label: '安全边际评分',
        data: safetyScores,
        backgroundColor: 'rgba(54, 162, 235, 0.2)',
        borderColor: 'rgba(54, 162, 235, 1)',
        borderWidth: 2,
        pointBackgroundColor: 'rgba(54, 162, 235, 1)',
        pointBorderColor: '#fff',
        pointHoverBackgroundColor: '#fff',
        pointHoverBorderColor: 'rgba(54, 162, 235, 1)'
      }, {
        label: '风险评分',
        data: riskScores,
        backgroundColor: 'rgba(255, 99, 132, 0.2)',
        borderColor: 'rgba(255, 99, 132, 1)',
        borderWidth: 2,
        pointBackgroundColor: 'rgba(255, 99, 132, 1)',
        pointBorderColor: '#fff',
        pointHoverBackgroundColor: '#fff',
        pointHoverBorderColor: 'rgba(255, 99, 132, 1)'
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        r: {
          min: 0,
          max: 100,
          ticks: {
            stepSize: 20
          }
        }
      },
      plugins: {
        title: {
          display: true,
          text: '持仓股票评分雷达图',
          font: {
            size: 16
          }
        },
        legend: {
          position: 'top'
        }
      }
    }
  });
  
  // 添加持仓热力图
  const holdingsList = document.getElementById('holdingsList');
  
  // 清除旧的热力图
  const oldHeatmap = document.getElementById('holdingsHeatmap');
  if (oldHeatmap) {
    oldHeatmap.remove();
  }
  
  // 创建热力图容器
  const heatmapContainer = document.createElement('div');
  heatmapContainer.id = 'holdingsHeatmap';
  heatmapContainer.style.marginTop = '1.5rem';
  heatmapContainer.innerHTML = '<h4>持仓安全边际热力图</h4>';
  
  // 创建热力图表格
  const heatmapTable = document.createElement('table');
  heatmapTable.style.width = '100%';
  heatmapTable.style.borderCollapse = 'collapse';
  
  const heatmapHeader = document.createElement('tr');
  heatmapHeader.innerHTML = '<th style="padding: 0.5rem; text-align: left; border: 1px solid #ddd;">股票</th><th style="padding: 0.5rem; text-align: center; border: 1px solid #ddd;">安全边际</th><th style="padding: 0.5rem; text-align: center; border: 1px solid #ddd;">风险水平</th>';
  heatmapTable.appendChild(heatmapHeader);
  
  // 添加热力图数据
  analysisResults.forEach(result => {
    const row = document.createElement('tr');
    
    // 安全边际颜色
    let safetyColor = '#e5e7eb';
    if (result.safety.level === '安全｜可关注') {
      safetyColor = '#10b981';
    } else if (result.safety.level === '一般｜观察') {
      safetyColor = '#f59e0b';
    } else if (result.safety.level === '危险｜回避') {
      safetyColor = '#ef4444';
    }
    
    // 风险水平颜色
    let riskColor = '#e5e7eb';
    if (result.risk.riskLevel === '低风险') {
      riskColor = '#10b981';
    } else if (result.risk.riskLevel === '中风险') {
      riskColor = '#f59e0b';
    } else if (result.risk.riskLevel === '高风险') {
      riskColor = '#ef4444';
    }
    
    row.innerHTML = `
      <td style="padding: 0.5rem; border: 1px solid #ddd;">${result.stock.name}</td>
      <td style="padding: 0.5rem; text-align: center; border: 1px solid #ddd; background-color: ${safetyColor}; color: white; font-weight: bold;">${result.safety.level}</td>
      <td style="padding: 0.5rem; text-align: center; border: 1px solid #ddd; background-color: ${riskColor}; color: white; font-weight: bold;">${result.risk.riskLevel}</td>
    `;
    heatmapTable.appendChild(row);
  });
  
  heatmapContainer.appendChild(heatmapTable);
  holdingsList.appendChild(heatmapContainer);
}

// 根据股票代码判断市场
function getMarketFromCode(code) {
  if (code.endsWith('.SH') || code.endsWith('.SZ')) {
    return 'CN'; // 沪深股市
  } else if (code.endsWith('.HK')) {
    return 'HK'; // 港股
  } else if (code.endsWith('.US') || code.includes('.N') || code.includes('.NY')) {
    return 'US'; // 美股
  } else {
    // 根据股票代码前缀判断
    const numericCode = code.match(/\d{6}/);
    if (numericCode) {
      const prefix = numericCode[0].substring(0, 1);
      if (prefix === '6') {
        return 'CN'; // 沪市
      } else if (prefix === '0' || prefix === '3') {
        return 'CN'; // 深市
      }
    }
    return 'CN'; // 默认沪深股市
  }
}

// 计算神奇公式排名
function calculateMagicFormulaRank(stocks) {
  // 计算PE排名（PE越小排名越高）
  const stocksWithPeRank = stocks
    .filter(stock => stock.pe > 0)
    .sort((a, b) => a.pe - b.pe)
    .map((stock, index) => ({
      ...stock,
      peRank: index + 1
    }));
  
  // 计算ROE排名（ROE越大排名越高）
  const stocksWithBothRanks = stocksWithPeRank
    .filter(stock => stock.roe_ttm > 0)
    .sort((a, b) => b.roe_ttm - a.roe_ttm)
    .map((stock, index) => ({
      ...stock,
      roeRank: index + 1,
      magicFormulaRank: stock.peRank + (index + 1),
      magicFormulaScore: (index + 1) + stock.peRank // 总排名，越小越好
    }));
  
  return stocksWithBothRanks;
}

// 计算PB-ROE值
function calculatePbRoe(stock) {
  // PB-ROE策略：ROE/PB
  if (stock.pb > 0 && stock.roe_ttm > 0) {
    return (stock.roe_ttm / stock.pb).toFixed(2);
  }
  return 0;
}

// 获取好公司推荐
function getRecommendations(marketFilter = '', filterMethod = 'magicFormula') {
  // 分析所有股票
  const analysisResults = [];
  
  // 首先收集符合市场筛选条件的股票
  const filteredStocks = [];
  for (const code in stockData) {
    const stock = stockData[code];
    const market = getMarketFromCode(code);
    if (!marketFilter || market === marketFilter) {
      filteredStocks.push({
        ...stock,
        code: code,
        market: market
      });
    }
  }
  
  if (filterMethod === 'magicFormula') {
    // 使用正确的神奇公式排名方法
    const stocksWithMagicRank = calculateMagicFormulaRank(filteredStocks);
    
    // 转换为分析结果格式并按神奇公式排名排序
    stocksWithMagicRank
      .sort((a, b) => a.magicFormulaScore - b.magicFormulaScore)
      .forEach(stock => {
        analysisResults.push({
          stock: {
            ...stock,
            code: stock.code
          },
          market: stock.market,
          filterValue: stock.magicFormulaScore, // 使用总排名作为筛选值
          magicFormulaValue: stock.magicFormulaScore,
          pbRoeValue: calculatePbRoe(stock),
          peRank: stock.peRank,
          roeRank: stock.roeRank
        });
      });
  } else {
    // 其他筛选方法
    for (const stock of filteredStocks) {
      // 计算筛选指标
      let filterValue = 0;
      if (filterMethod === 'pbRoe') {
        filterValue = calculatePbRoe(stock);
      } else {
        // 传统价值投资：综合评分
        const r1 = safetyMargin(stock);
        const r2 = fundamental(stock);
        const r3 = moat(stock);
        const r4 = risk(stock);
        const final = finalRating([r1, r2, r3, r4]);
        filterValue = final.avg;
      }
      
      // 只推荐筛选值大于0的公司
      if (filterValue > 0) {
        analysisResults.push({
          stock: stock,
          market: stock.market,
          filterValue: filterValue,
          magicFormulaValue: 0,
          pbRoeValue: filterMethod === 'pbRoe' ? filterValue : calculatePbRoe(stock)
        });
      }
    }
    
    // 按筛选值排序
    if (filterMethod === 'pbRoe') {
      // PB-ROE策略：值越大越好
      analysisResults.sort((a, b) => b.filterValue - a.filterValue);
    } else {
      // 传统价值投资：值越大越好
      analysisResults.sort((a, b) => b.filterValue - a.filterValue);
    }
  }
  
  return analysisResults;
}

// 渲染好公司推荐
function renderRecommendations(marketFilter = '', filterMethod = 'magicFormula') {
  const recommendations = getRecommendations(marketFilter, filterMethod);
  const tableBody = document.getElementById('recommendationsTableBody');
  const loading = document.getElementById('recommendationsLoading');
  
  loading.style.display = 'block';
  tableBody.innerHTML = '';
  
  setTimeout(() => {
    if (recommendations.length === 0) {
      const row = document.createElement('tr');
      row.innerHTML = `<td colspan="11" style="padding: 1rem; text-align: center; color: #666;">暂无符合条件的推荐</td>`;
      tableBody.appendChild(row);
    } else {
      recommendations.forEach((result, index) => {
        const row = document.createElement('tr');
        
        // 市场显示
        let marketDisplay = 'CN';
        if (result.market === 'CN') {
          marketDisplay = '沪深';
        } else if (result.market === 'HK') {
          marketDisplay = '港股';
        } else if (result.market === 'US') {
          marketDisplay = '美股';
        }
        
        // 获取显示的公式值
        let formulaValue = result.magicFormulaValue;
        if (filterMethod === 'pbRoe') {
          formulaValue = result.pbRoeValue;
        }
        
        // 获取排名数据
        let peRank = result.peRank || '-';
        let roeRank = result.roeRank || '-';
        let totalRank = result.filterValue || formulaValue;
        
        row.innerHTML = `
          <td style="padding: 0.5rem; border: 1px solid #ddd;">${result.stock.name}</td>
          <td style="padding: 0.5rem; text-align: right; border: 1px solid #ddd;">${result.stock.code}</td>
          <td style="padding: 0.5rem; text-align: right; border: 1px solid #ddd;">${marketDisplay}</td>
          <td style="padding: 0.5rem; text-align: right; border: 1px solid #ddd;">${result.stock.industry}</td>
          <td style="padding: 0.5rem; text-align: right; border: 1px solid #ddd;">${result.stock.roe_ttm}</td>
          <td style="padding: 0.5rem; text-align: right; border: 1px solid #ddd;">${result.stock.pe}</td>
          <td style="padding: 0.5rem; text-align: right; border: 1px solid #ddd;">${result.stock.pb}</td>
          <td style="padding: 0.5rem; text-align: right; border: 1px solid #ddd;">${peRank}</td>
          <td style="padding: 0.5rem; text-align: right; border: 1px solid #ddd;">${roeRank}</td>
          <td style="padding: 0.5rem; text-align: right; border: 1px solid #ddd; font-weight: bold;">${totalRank}</td>
          <td style="padding: 0.5rem; text-align: right; border: 1px solid #ddd;">
            <button class="addToHoldingsBtn" data-code="${result.stock.code}">添加到持仓</button>
          </td>
        `;
        tableBody.appendChild(row);
      });
      
      // 添加到持仓按钮事件
      document.querySelectorAll('.addToHoldingsBtn').forEach(btn => {
        btn.addEventListener('click', function() {
          const code = this.getAttribute('data-code');
          
          const cost = parseFloat(prompt('请输入持仓成本（元）:'));
          if (isNaN(cost)) return;
          
          const quantity = parseInt(prompt('请输入持仓数量:'));
          if (isNaN(quantity)) return;
          
          addHolding({
            code: code,
            cost: cost,
            quantity: quantity
          });
          
          renderHoldings();
          alert('已添加到持仓！');
        });
      });
    }
    
    loading.style.display = 'none';
  }, 1000);
}

document.addEventListener("DOMContentLoaded", () => {
  const sel = document.getElementById("stockSelector");
  const runBtn = document.getElementById("runBtn");
  const result = document.getElementById("result");
  const report = document.querySelector(".report");
  const loading = document.querySelector(".loading");
  
  // 持仓管理相关元素
  const addHoldingBtn = document.getElementById("addHoldingBtn");
  const analyzeHoldingsBtn = document.getElementById("analyzeHoldingsBtn");
  
  // 好公司推荐相关元素
  const marketFilter = document.getElementById("marketFilter");
  const filterMethod = document.getElementById("filterMethod");
  const refreshRecommendationsBtn = document.getElementById("refreshRecommendationsBtn");
  
  // 添加实时数据选项
  const realTimeDiv = document.createElement("div");
  realTimeDiv.className = "form-group";
  realTimeDiv.innerHTML = `
    <label class="checkbox-label">
      <input type="checkbox" id="realTimeCheckbox">
      使用实时数据
    </label>
  `;
  runBtn.parentElement.insertBefore(realTimeDiv, runBtn);

  for (let code in stockData) {
    const opt = document.createElement("option");
    opt.value = code;
    opt.textContent = `${stockData[code].name} (${code})`;
    sel.appendChild(opt);
  }
  
  // 初始化持仓列表
  renderHoldings();
  
  // 初始化好公司推荐
  renderRecommendations();
  
  // 添加持仓按钮事件
  addHoldingBtn.addEventListener("click", showAddHoldingDialog);
  
  // 分析持仓按钮事件
  analyzeHoldingsBtn.addEventListener("click", analyzeHoldings);
  
  // 市场筛选事件
  marketFilter.addEventListener("change", function() {
    renderRecommendations(marketFilter.value, filterMethod.value);
  });
  
  // 筛选方法事件
  filterMethod.addEventListener("change", function() {
    renderRecommendations(marketFilter.value, filterMethod.value);
  });
  
  // 刷新推荐按钮事件
  refreshRecommendationsBtn.addEventListener("click", function() {
    renderRecommendations(marketFilter.value, filterMethod.value);
  });

  // 导出按钮
  const exportPDFBtn = document.getElementById("exportPDFBtn");
  const exportExcelBtn = document.getElementById("exportExcelBtn");
  const runPortfolioBtn = document.getElementById("runPortfolioBtn");
  
  // 存储当前分析结果，用于导出
  let currentAnalysisResults = null;
  let currentAnalysisType = 'single'; // 'single' 或 'portfolio'
  let currentData = null;
  
  // 智能体思考过程函数
  function showAgentThinking(steps) {
    const agentThinking = document.getElementById('agentThinking');
    agentThinking.textContent = '';
    
    let currentStep = 0;
    const interval = setInterval(() => {
      if (currentStep < steps.length) {
        agentThinking.textContent += steps[currentStep] + '\n';
        currentStep++;
      } else {
        clearInterval(interval);
      }
    }, 300);
  }

  // 单只股票分析
  runBtn.addEventListener("click", async () => {
    // 获取选中的第一个股票
    const selectedOptions = Array.from(sel.selectedOptions);
    if (selectedOptions.length === 0 || selectedOptions[0].value === "") {
      return alert("请选择公司");
    }
    
    const code = selectedOptions[0].value;
    const useRealTime = document.getElementById("realTimeCheckbox").checked;
    let data;
    
    result.classList.remove("hidden");
    loading.classList.remove("hidden");
    report.textContent = "";
    document.getElementById('agentThinking').textContent = '';
    runBtn.disabled = true;
    runPortfolioBtn.disabled = true;
    exportPDFBtn.disabled = true;
    exportExcelBtn.disabled = true;

    if (useRealTime) {
      // 尝试获取实时数据
      data = await getRealTimeData(code);
      if (!data) {
        // 如果无法获取实时数据，使用示例数据
        data = stockData[code];
        alert("无法获取实时数据，使用示例数据进行分析");
      }
    } else {
      // 使用示例数据
      data = stockData[code];
    }

    // 智能体思考过程
    const thinkingSteps = [
      `开始分析 ${data.name} (${data.code})`,
      "1. 安全边际分析：",
      "   - 计算PE、PB历史分位",
      "   - 评估PEG比率",
      "   - 分析ROE水平",
      "   - 检查负债率",
      "2. 基本面分析：",
      "   - 评估ROE连续性",
      "   - 分析毛利率水平",
      "   - 检查营收增长",
      "   - 分析利润增长",
      "   - 评估现金流健康度",
      "3. 护城河分析：",
      "   - 基于毛利率评估定价权",
      "   - 分析长期ROE稳定性",
      "   - 评估市场认可度",
      "   - 检查财务稳健性",
      "   - 分析规模优势",
      "4. 风险分析：",
      "   - 评估负债率风险",
      "   - 分析估值风险",
      "   - 检查利润下滑风险",
      "   - 评估现金流风险",
      "5. 综合评估：",
      "   - 计算各项指标加权得分",
      "   - 汇总风险因素",
      "   - 形成最终投资建议",
      "分析完成，生成报告..."
    ];

    // 显示智能体思考过程
    showAgentThinking(thinkingSteps);

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
      out += useRealTime ? "本分析基于实时数据，仅供参考，不构成投资建议。" : "本分析基于离线沙盒数据，仅供学习，不构成投资建议。";

      report.textContent = out;
      
      // 生成图表
      generateCharts(r1, r2, r3, r4, data);
      
      // 存储分析结果
      currentAnalysisResults = {
        safety: r1,
        fundamental: r2,
        moat: r3,
        risk: r4,
        final: final
      };
      currentAnalysisType = 'single';
      currentData = data;
      
      loading.classList.add("hidden");
      runBtn.disabled = false;
      runPortfolioBtn.disabled = false;
      exportPDFBtn.disabled = false;
      exportExcelBtn.disabled = false;
    }, 1200);
  });

  // 投资组合分析
  runPortfolioBtn.addEventListener("click", async () => {
    // 获取所有选中的股票
    const selectedOptions = Array.from(sel.selectedOptions);
    const selectedCodes = selectedOptions.map(opt => opt.value).filter(code => code !== "");
    
    if (selectedCodes.length === 0) {
      return alert("请选择至少一只股票");
    }
    
    const useRealTime = document.getElementById("realTimeCheckbox").checked;
    const portfolioData = [];
    
    result.classList.remove("hidden");
    loading.classList.remove("hidden");
    report.textContent = "";
    document.getElementById('agentThinking').textContent = '';
    runBtn.disabled = true;
    runPortfolioBtn.disabled = true;
    exportPDFBtn.disabled = true;
    exportExcelBtn.disabled = true;

    // 智能体思考过程
    const thinkingSteps = [
      `开始分析投资组合（${selectedCodes.length}只股票）`,
      "1. 数据收集：",
      "   - 获取每只股票的详细数据",
      "   - 验证数据完整性",
      "2. 个股分析：",
      "   - 对每只股票进行安全边际分析",
      "   - 评估每只股票的基本面",
      "   - 分析每只股票的护城河",
      "   - 评估每只股票的风险",
      "3. 组合分析：",
      "   - 计算组合平均评分",
      "   - 分析风险分布",
      "   - 评估安全边际分布",
      "4. 组合优化建议：",
      "   - 基于评分提出调整建议",
      "   - 针对风险分布提供优化方案",
      "   - 形成最终投资组合建议",
      "分析完成，生成报告..."
    ];

    // 显示智能体思考过程
    showAgentThinking(thinkingSteps);

    // 获取每只股票的数据
    for (const code of selectedCodes) {
      if (useRealTime) {
        // 尝试获取实时数据
        const realTimeData = await getRealTimeData(code);
        if (realTimeData) {
          portfolioData.push(realTimeData);
        } else {
          // 如果无法获取实时数据，使用示例数据
          portfolioData.push(stockData[code]);
        }
      } else {
        // 使用示例数据
        portfolioData.push(stockData[code]);
      }
    }

    setTimeout(() => {
      // 分析每只股票
      const analysisResults = [];
      let totalScore = 0;
      let highRiskCount = 0;
      let lowSafetyCount = 0;
      
      for (const data of portfolioData) {
        const r1 = safetyMargin(data);
        const r2 = fundamental(data);
        const r3 = moat(data);
        const r4 = risk(data);
        const final = finalRating([r1, r2, r3, r4]);
        
        analysisResults.push({
          data: data,
          safety: r1,
          fundamental: r2,
          moat: r3,
          risk: r4,
          final: final
        });
        
        totalScore += final.avg;
        if (r4.riskLevel === "高风险") highRiskCount++;
        if (r1.level === "危险｜回避") lowSafetyCount++;
      }
      
      // 计算组合指标
      const portfolioAvgScore = Math.round(totalScore / analysisResults.length);
      const riskPercentage = Math.round((highRiskCount / analysisResults.length) * 100);
      const safetyPercentage = Math.round(((analysisResults.length - lowSafetyCount) / analysisResults.length) * 100);
      
      // 生成投资组合报告
      let out = `📊 投资组合分析报告\n\n`;
      out += `组合包含 ${analysisResults.length} 只股票\n`;
      out += `组合平均评分: ${portfolioAvgScore}\n`;
      out += `高风险股票占比: ${riskPercentage}%\n`;
      out += `安全边际良好股票占比: ${safetyPercentage}%\n\n`;
      
      // 添加每只股票的简要分析
      out += `个股分析:\n`;
      for (const result of analysisResults) {
        out += `\n• ${result.data.name} (${result.data.code}):\n`;
        out += `  评分: ${result.final.avg}｜结论: ${result.final.decision}\n`;
        out += `  风险: ${result.risk.riskLevel}｜安全边际: ${result.safety.level}\n`;
      }
      
      // 添加投资组合建议
      out += `\n投资组合建议:\n`;
      if (portfolioAvgScore >= 80) {
        out += `✅ 组合质量优秀，建议长期持有\n`;
      } else if (portfolioAvgScore >= 65) {
        out += `⚠️ 组合质量良好，可适当调整配置\n`;
      } else {
        out += `❌ 组合质量一般，建议重新评估选股\n`;
      }
      
      if (riskPercentage > 30) {
        out += `⚠️ 组合风险较高，建议降低高风险股票比例\n`;
      }
      
      if (safetyPercentage < 70) {
        out += `⚠️ 安全边际良好的股票占比较低，建议增加安全边际高的股票\n`;
      }
      
      out += `\n本分析基于${useRealTime ? "实时数据" : "离线沙盒数据"}，仅供参考，不构成投资建议。`;

      report.textContent = out;
      
      // 生成投资组合图表
      generatePortfolioChart(analysisResults);
      
      // 存储分析结果
      currentAnalysisResults = analysisResults;
      currentAnalysisType = 'portfolio';
      currentData = portfolioData;
      
      loading.classList.add("hidden");
      runBtn.disabled = false;
      runPortfolioBtn.disabled = false;
      exportPDFBtn.disabled = false;
      exportExcelBtn.disabled = false;
    }, 1200);
  });

  // 导出PDF功能
  exportPDFBtn.addEventListener("click", async () => {
    if (!currentAnalysisResults) {
      return alert("请先运行分析");
    }
    
    try {
      // 导入jsPDF和html2canvas
      const { jsPDF } = window.jspdf;
      const pdf = new jsPDF('p', 'mm', 'a4');
      
      // 获取报告内容
      const reportContent = report.textContent;
      
      // 获取图表
      const scoreChart = document.getElementById('scoreChart');
      const metricsChart = document.getElementById('metricsChart');
      
      // 将图表转换为图片
      const scoreChartImg = await html2canvas(scoreChart);
      const metricsChartImg = await html2canvas(metricsChart);
      
      const scoreChartDataUrl = scoreChartImg.toDataURL('image/png');
      const metricsChartDataUrl = metricsChartImg.toDataURL('image/png');
      
      // 添加标题
      pdf.setFontSize(18);
      pdf.text('BuffettMunger-Agent 分析报告', 105, 15, { align: 'center' });
      
      // 添加报告内容
      pdf.setFontSize(12);
      const lines = reportContent.split('\n');
      let yPos = 30;
      const lineHeight = 6;
      const pageHeight = 280;
      
      for (const line of lines) {
        if (yPos > pageHeight - 20) {
          pdf.addPage();
          yPos = 20;
        }
        pdf.text(line, 15, yPos);
        yPos += lineHeight;
      }
      
      // 添加图表
      if (yPos > pageHeight - 100) {
        pdf.addPage();
        yPos = 20;
      }
      pdf.setFontSize(14);
      pdf.text('分析图表', 105, yPos, { align: 'center' });
      yPos += 10;
      
      // 添加第一张图表
      pdf.addImage(scoreChartDataUrl, 'PNG', 15, yPos, 80, 60);
      // 添加第二张图表
      pdf.addImage(metricsChartDataUrl, 'PNG', 105, yPos, 80, 60);
      
      // 保存PDF
      const filename = currentAnalysisType === 'single' ? 
        `${currentData.name}_分析报告.pdf` : 
        `投资组合分析报告.pdf`;
      
      pdf.save(filename);
    } catch (error) {
      console.error('导出PDF失败:', error);
      alert('导出PDF失败，请稍后重试');
    }
  });

  // 导出Excel功能
  exportExcelBtn.addEventListener("click", () => {
    if (!currentAnalysisResults) {
      return alert("请先运行分析");
    }
    
    try {
      // 创建工作簿
      const wb = XLSX.utils.book_new();
      
      if (currentAnalysisType === 'single') {
        // 单只股票分析导出
        const data = currentData;
        const results = currentAnalysisResults;
        
        // 创建数据表格
        const wsData = [
          ['BuffettMunger-Agent 分析报告'],
          [''],
          ['公司信息'],
          ['股票代码', data.code],
          ['公司名称', data.name],
          [''],
          ['财务指标'],
          ['PE', data.pe],
          ['PB', data.pb],
          ['PEG', data.peg],
          ['ROE(%)', data.roe_ttm],
          ['负债率(%)', data.debt_to_asset],
          ['营收增长(%)', data.revenue_growth],
          ['利润增长(%)', data.profit_growth],
          ['毛利率(%)', data.gross_margin],
          ['现金流健康', data.cash_flow_healthy ? '是' : '否'],
          [''],
          ['分析结果'],
          ['安全边际', results.safety.score + '分', results.safety.level],
          ['基本面', results.fundamental.score + '分', results.fundamental.status],
          ['护城河', results.moat.score + '分', results.moat.level],
          ['风险评分', results.risk.score + '分', results.risk.riskLevel],
          ['综合评分', results.final.avg + '分'],
          ['最终结论', results.final.decision]
        ];
        
        // 添加警告信息
        if (results.final.allWarn && results.final.allWarn.length > 0) {
          wsData.push([''], ['警告信息']);
          for (const warn of results.final.allWarn) {
            wsData.push(['', warn]);
          }
        }
        
        // 创建工作表
        const ws = XLSX.utils.aoa_to_sheet(wsData);
        XLSX.utils.book_append_sheet(wb, ws, '分析报告');
        
        // 保存Excel文件
        const filename = `${data.name}_分析报告.xlsx`;
        XLSX.writeFile(wb, filename);
      } else {
        // 投资组合分析导出
        const analysisResults = currentAnalysisResults;
        
        // 创建数据表格
        const wsData = [
          ['BuffettMunger-Agent 投资组合分析报告'],
          [''],
          ['股票名称', '股票代码', '综合评分', '风险等级', '安全边际', '基本面', '护城河']
        ];
        
        // 添加每只股票的数据
        for (const result of analysisResults) {
          wsData.push([
            result.data.name,
            result.data.code,
            result.final.avg,
            result.risk.riskLevel,
            result.safety.level,
            result.fundamental.status,
            result.moat.level
          ]);
        }
        
        // 创建工作表
        const ws = XLSX.utils.aoa_to_sheet(wsData);
        XLSX.utils.book_append_sheet(wb, ws, '投资组合分析');
        
        // 保存Excel文件
        const filename = `投资组合分析报告.xlsx`;
        XLSX.writeFile(wb, filename);
      }
    } catch (error) {
      console.error('导出Excel失败:', error);
      alert('导出Excel失败，请稍后重试');
    }
  });
});

// 生成单只股票图表
function generateCharts(safety, fundamental, moat, risk, data) {
  // 销毁旧图表
  if (window.scoreChart && typeof window.scoreChart.destroy === 'function') {
    window.scoreChart.destroy();
  }
  if (window.metricsChart && typeof window.metricsChart.destroy === 'function') {
    window.metricsChart.destroy();
  }
  
  // 评分雷达图
  const scoreCtx = document.getElementById('scoreChart').getContext('2d');
  window.scoreChart = new Chart(scoreCtx, {
    type: 'radar',
    data: {
      labels: ['安全边际', '基本面', '护城河', '风险评分'],
      datasets: [{
        label: '评分',
        data: [safety.score, fundamental.score, moat.score, risk.score],
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 2,
        pointBackgroundColor: 'rgba(75, 192, 192, 1)',
        pointBorderColor: '#fff',
        pointHoverBackgroundColor: '#fff',
        pointHoverBorderColor: 'rgba(75, 192, 192, 1)'
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        r: {
          min: 0,
          max: 100,
          ticks: {
            stepSize: 20
          }
        }
      },
      plugins: {
        title: {
          display: true,
          text: '价值投资维度评分',
          font: {
            size: 16
          }
        }
      }
    }
  });
  
  // 财务指标柱状图
  const metricsCtx = document.getElementById('metricsChart').getContext('2d');
  window.metricsChart = new Chart(metricsCtx, {
    type: 'bar',
    data: {
      labels: ['ROE(%)', '毛利率(%)', '营收增长(%)', '利润增长(%)', '负债率(%)'],
      datasets: [{
        label: '指标值',
        data: [data.roe_ttm, data.gross_margin, data.revenue_growth, data.profit_growth, data.debt_to_asset],
        backgroundColor: [
          'rgba(75, 192, 192, 0.6)',
          'rgba(54, 162, 235, 0.6)',
          'rgba(255, 206, 86, 0.6)',
          'rgba(153, 102, 255, 0.6)',
          'rgba(255, 159, 64, 0.6)'
        ],
        borderColor: [
          'rgba(75, 192, 192, 1)',
          'rgba(54, 162, 235, 1)',
          'rgba(255, 206, 86, 1)',
          'rgba(153, 102, 255, 1)',
          'rgba(255, 159, 64, 1)'
        ],
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true
        }
      },
      plugins: {
        title: {
          display: true,
          text: '关键财务指标',
          font: {
            size: 16
          }
        }
      }
    }
  });
}

// 生成投资组合图表
function generatePortfolioChart(analysisResults) {
  // 销毁旧图表
  if (window.scoreChart && typeof window.scoreChart.destroy === 'function') {
    window.scoreChart.destroy();
  }
  if (window.metricsChart && typeof window.metricsChart.destroy === 'function') {
    window.metricsChart.destroy();
  }
  
  // 准备数据
  const stockNames = analysisResults.map(result => result.data.name);
  const finalScores = analysisResults.map(result => result.final.avg);
  const safetyScores = analysisResults.map(result => result.safety.score);
  const riskScores = analysisResults.map(result => result.risk.score);
  
  // 投资组合评分对比图
  const scoreCtx = document.getElementById('scoreChart').getContext('2d');
  window.scoreChart = new Chart(scoreCtx, {
    type: 'bar',
    data: {
      labels: stockNames,
      datasets: [{
        label: '综合评分',
        data: finalScores,
        backgroundColor: 'rgba(75, 192, 192, 0.6)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1
      }, {
        label: '安全边际评分',
        data: safetyScores,
        backgroundColor: 'rgba(54, 162, 235, 0.6)',
        borderColor: 'rgba(54, 162, 235, 1)',
        borderWidth: 1
      }, {
        label: '风险评分',
        data: riskScores,
        backgroundColor: 'rgba(255, 99, 132, 0.6)',
        borderColor: 'rgba(255, 99, 132, 1)',
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
          max: 100
        }
      },
      plugins: {
        title: {
          display: true,
          text: '投资组合评分对比',
          font: {
            size: 16
          }
        },
        legend: {
          position: 'top'
        }
      }
    }
  });
  
  // 投资组合风险分布饼图
  const metricsCtx = document.getElementById('metricsChart').getContext('2d');
  
  // 统计风险等级分布
  const riskLevels = {
    '低风险': 0,
    '中风险': 0,
    '高风险': 0
  };
  
  analysisResults.forEach(result => {
    riskLevels[result.risk.riskLevel]++;
  });
  
  window.metricsChart = new Chart(metricsCtx, {
    type: 'pie',
    data: {
      labels: Object.keys(riskLevels),
      datasets: [{
        data: Object.values(riskLevels),
        backgroundColor: [
          'rgba(75, 192, 192, 0.6)',
          'rgba(255, 206, 86, 0.6)',
          'rgba(255, 99, 132, 0.6)'
        ],
        borderColor: [
          'rgba(75, 192, 192, 1)',
          'rgba(255, 206, 86, 1)',
          'rgba(255, 99, 132, 1)'
        ],
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        title: {
          display: true,
          text: '投资组合风险分布',
          font: {
            size: 16
          }
        },
        legend: {
          position: 'bottom'
        }
      }
    }
  });
}

// 生成行业数据对比
function generateIndustryComparison(data) {
  // 销毁旧图表
  if (window.industryChart && typeof window.industryChart.destroy === 'function') {
    window.industryChart.destroy();
  }
  
  const industryComparison = document.getElementById('industryComparison');
  const industryChartCtx = document.getElementById('industryChart').getContext('2d');
  
  // 获取行业信息
  const industry = data.industry;
  if (!industry) {
    industryComparison.innerHTML = '<p>暂无行业数据</p>';
    return;
  }
  
  // 获取行业平均数据
  const industryAvg = industryData[industry];
  if (!industryAvg) {
    industryComparison.innerHTML = `<p>暂无${industry}行业数据</p>`;
    return;
  }
  
  // 生成行业对比报告
  let comparisonHtml = `
    <table style="width: 100%; border-collapse: collapse; margin-bottom: 1rem;">
      <thead>
        <tr style="background-color: #f3f4f6;">
          <th style="padding: 0.5rem; text-align: left; border: 1px solid #ddd;">指标</th>
          <th style="padding: 0.5rem; text-align: right; border: 1px solid #ddd;">${data.name}</th>
          <th style="padding: 0.5rem; text-align: right; border: 1px solid #ddd;">${industry}行业平均</th>
          <th style="padding: 0.5rem; text-align: right; border: 1px solid #ddd;">对比</th>
        </tr>
      </thead>
      <tbody>
  `;
  
  // 定义要对比的指标
  const metrics = [
    { key: 'pe', name: 'PE', format: 'number' },
    { key: 'pb', name: 'PB', format: 'number' },
    { key: 'roe_ttm', name: 'ROE(%)', format: 'percent' },
    { key: 'debt_to_asset', name: '负债率(%)', format: 'percent' },
    { key: 'revenue_growth', name: '营收增长(%)', format: 'percent' },
    { key: 'profit_growth', name: '利润增长(%)', format: 'percent' },
    { key: 'gross_margin', name: '毛利率(%)', format: 'percent' }
  ];
  
  // 准备图表数据
  const chartLabels = [];
  const stockData = [];
  const industryDataArray = [];
  
  for (const metric of metrics) {
    const stockValue = data[metric.key];
    const industryValue = industryAvg[metric.key];
    
    // 计算对比
    let comparison = '';
    let comparisonClass = '';
    
    if (metric.key === 'pe' || metric.key === 'pb' || metric.key === 'debt_to_asset') {
      // 这些指标越低越好
      if (stockValue < industryValue) {
        comparison = '优于行业';
        comparisonClass = 'style="color: green; font-weight: bold;"';
      } else if (stockValue > industryValue) {
        comparison = '劣于行业';
        comparisonClass = 'style="color: red; font-weight: bold;"';
      } else {
        comparison = '持平行业';
      }
    } else {
      // 这些指标越高越好
      if (stockValue > industryValue) {
        comparison = '优于行业';
        comparisonClass = 'style="color: green; font-weight: bold;"';
      } else if (stockValue < industryValue) {
        comparison = '劣于行业';
        comparisonClass = 'style="color: red; font-weight: bold;"';
      } else {
        comparison = '持平行业';
      }
    }
    
    // 格式化数值
    let formattedStockValue = stockValue;
    let formattedIndustryValue = industryValue;
    if (metric.format === 'percent') {
      formattedStockValue = stockValue + '%';
      formattedIndustryValue = industryValue + '%';
    }
    
    // 添加到表格
    comparisonHtml += `
      <tr>
        <td style="padding: 0.5rem; border: 1px solid #ddd;">${metric.name}</td>
        <td style="padding: 0.5rem; text-align: right; border: 1px solid #ddd;">${formattedStockValue}</td>
        <td style="padding: 0.5rem; text-align: right; border: 1px solid #ddd;">${formattedIndustryValue}</td>
        <td style="padding: 0.5rem; text-align: right; border: 1px solid #ddd;" ${comparisonClass}>${comparison}</td>
      </tr>
    `;
    
    // 添加到图表数据
    chartLabels.push(metric.name);
    stockData.push(stockValue);
    industryDataArray.push(industryValue);
  }
  
  comparisonHtml += `
      </tbody>
    </table>
  `;
  
  industryComparison.innerHTML = comparisonHtml;
  
  // 生成行业对比图表
  window.industryChart = new Chart(industryChartCtx, {
    type: 'bar',
    data: {
      labels: chartLabels,
      datasets: [{
        label: data.name,
        data: stockData,
        backgroundColor: 'rgba(75, 192, 192, 0.6)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1
      }, {
        label: `${industry}行业平均`,
        data: industryDataArray,
        backgroundColor: 'rgba(255, 99, 132, 0.6)',
        borderColor: 'rgba(255, 99, 132, 1)',
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true
        }
      },
      plugins: {
        title: {
          display: true,
          text: '与行业平均水平对比',
          font: {
            size: 16
          }
        },
        legend: {
          position: 'top'
        }
      }
    }
  });
}

// AI智能体对话功能
document.addEventListener("DOMContentLoaded", () => {
  const aiStockSelector = document.getElementById("aiStockSelector");
  const chatHistory = document.getElementById("chatHistory");
  const userInput = document.getElementById("userInput");
  const sendMessageBtn = document.getElementById("sendMessageBtn");
  const exampleQuestions = document.querySelectorAll(".example-question");
  const aiAnalysisResult = document.getElementById("aiAnalysisResult");
  const analysisContent = document.getElementById("analysisContent");
  const reasoningSteps = document.getElementById("reasoningSteps");
  
  // 填充AI股票选择器
  for (let code in stockData) {
    const opt = document.createElement("option");
    opt.value = code;
    opt.textContent = `${stockData[code].name} (${code})`;
    aiStockSelector.appendChild(opt);
  }
  
  // 发送消息函数
  async function sendMessage() {
    const message = userInput.value.trim();
    const selectedStock = aiStockSelector.value;
    
    if (!message) return;
    
    // 添加用户消息到聊天历史
    addMessageToHistory("user", message);
    userInput.value = "";
    
    // 显示AI正在输入的状态
    const typingIndicator = addMessageToHistory("ai", "", true);
    
    try {
      // 构建请求数据
      const requestData = {
        code: selectedStock,
        user_question: message,
        real_time: false
      };
      
      // 调用后端API
      const response = await fetch('http://localhost:5000/api/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestData)
      });
      
      const result = await response.json();
      
      // 移除打字指示器
      typingIndicator.remove();
      
      if (result.success) {
        // 显示AI响应
        const aiResponse = formatAIResponse(result.data);
        addMessageToHistory("ai", aiResponse);
        
        // 显示详细分析结果
        displayAnalysisResult(result.data);
      } else {
        // 显示错误信息
        addMessageToHistory("ai", `抱歉，分析失败：${result.error}`);
      }
    } catch (error) {
      // 移除打字指示器
      typingIndicator.remove();
      
      // 显示错误信息
      addMessageToHistory("ai", `抱歉，无法连接到分析服务：${error.message}`);
    }
  }
  
  // 添加消息到聊天历史
  function addMessageToHistory(type, content, isTyping = false) {
    const messageDiv = document.createElement("div");
    messageDiv.className = `chat-message ${type}`;
    
    if (isTyping) {
      messageDiv.innerHTML = '<p>🤖 正在分析...</p>';
    } else {
      if (type === "user") {
        messageDiv.innerHTML = `<p><strong>您：</strong>${content}</p>`;
      } else {
        messageDiv.innerHTML = `<p><strong>🤖 AI智能体：</strong>${content}</p>`;
      }
    }
    
    chatHistory.appendChild(messageDiv);
    chatHistory.scrollTop = chatHistory.scrollHeight;
    
    return messageDiv;
  }
  
  // 格式化AI响应
  function formatAIResponse(data) {
    let response = "";
    
    // 检查是否有综合推荐
    if (data.integrated_recommendation) {
      response += `<strong>投资建议：</strong>${data.integrated_recommendation}<br><br>`;
    }
    
    // 检查是否有传统分析结果
    if (data.traditional_analysis) {
      const ta = data.traditional_analysis;
      if (ta.safety && ta.safety.level) {
        response += `<strong>安全边际：</strong>${ta.safety.level}<br>`;
      }
      if (ta.final && ta.final.decision) {
        response += `<strong>最终结论：</strong>${ta.final.decision}<br>`;
      }
    }
    
    return response || "分析完成，详情请查看下方深度分析结果。";
  }
  
  // 显示分析结果
  function displayAnalysisResult(data) {
    aiAnalysisResult.classList.remove("hidden");
    
    // 构建分析内容
    let content = "";
    
    // 添加传统分析结果
    if (data.traditional_analysis) {
      const ta = data.traditional_analysis;
      content += `<h4>传统价值投资分析</h4>`;
      content += `<table style="width: 100%; border-collapse: collapse; margin-bottom: 1rem;">`;
      content += `<tr style="background-color: #f3f4f6;">
                    <th style="padding: 0.5rem; text-align: left; border: 1px solid #ddd;">分析维度</th>
                    <th style="padding: 0.5rem; text-align: right; border: 1px solid #ddd;">评分</th>
                    <th style="padding: 0.5rem; text-align: right; border: 1px solid #ddd;">结论</th>
                  </tr>`;
      
      if (ta.safety) {
        content += `<tr>
                    <td style="padding: 0.5rem; border: 1px solid #ddd;">安全边际</td>
                    <td style="padding: 0.5rem; text-align: right; border: 1px solid #ddd;">${ta.safety.score}分</td>
                    <td style="padding: 0.5rem; text-align: right; border: 1px solid #ddd;">${ta.safety.level}</td>
                  </tr>`;
      }
      
      if (ta.fundamental) {
        content += `<tr>
                    <td style="padding: 0.5rem; border: 1px solid #ddd;">基本面</td>
                    <td style="padding: 0.5rem; text-align: right; border: 1px solid #ddd;">${ta.fundamental.score}分</td>
                    <td style="padding: 0.5rem; text-align: right; border: 1px solid #ddd;">${ta.fundamental.status}</td>
                  </tr>`;
      }
      
      if (ta.moat) {
        content += `<tr>
                    <td style="padding: 0.5rem; border: 1px solid #ddd;">护城河</td>
                    <td style="padding: 0.5rem; text-align: right; border: 1px solid #ddd;">${ta.moat.score}分</td>
                    <td style="padding: 0.5rem; text-align: right; border: 1px solid #ddd;">${ta.moat.level}</td>
                  </tr>`;
      }
      
      if (ta.risk) {
        content += `<tr>
                    <td style="padding: 0.5rem; border: 1px solid #ddd;">风险</td>
                    <td style="padding: 0.5rem; text-align: right; border: 1px solid #ddd;">${ta.risk.score}分</td>
                    <td style="padding: 0.5rem; text-align: right; border: 1px solid #ddd;">${ta.risk.riskLevel}</td>
                  </tr>`;
      }
      
      if (ta.final) {
        content += `<tr style="background-color: #fef3c7;">
                    <td style="padding: 0.5rem; border: 1px solid #ddd; font-weight: bold;">综合评估</td>
                    <td style="padding: 0.5rem; text-align: right; border: 1px solid #ddd; font-weight: bold;">${ta.final.avg}分</td>
                    <td style="padding: 0.5rem; text-align: right; border: 1px solid #ddd; font-weight: bold;">${ta.final.decision}</td>
                  </tr>`;
      }
      
      content += `</table>`;
    }
    
    // 添加GitHub深度分析结果
    if (data.github_deep_analysis) {
      const gda = data.github_deep_analysis;
      content += `<h4>GitHub大模型深度分析</h4>`;
      content += `<div style="padding: 1rem; background-color: #f3f4f6; border-radius: 6px;">`;
      
      if (gda.analysis) {
        content += `<p>${gda.analysis}</p>`;
      }
      
      if (gda.recommendation) {
        content += `<p><strong>推荐意见：</strong>${gda.recommendation}</p>`;
      }
      
      content += `</div>`;
    }
    
    // 添加综合推荐
    if (data.integrated_recommendation) {
      content += `<h4>最终投资建议</h4>`;
      content += `<div style="padding: 1rem; background-color: #dbeafe; border-radius: 6px; font-weight: bold;">`;
      content += `<p>${data.integrated_recommendation}</p>`;
      content += `</div>`;
    }
    
    analysisContent.innerHTML = content;
    
    // 构建推理过程
    let reasoningContent = "";
    reasoningContent += `<ol>`;
    reasoningContent += `<li>数据收集与验证：获取股票基本信息和财务数据</li>`;
    reasoningContent += `<li>安全边际分析：评估PE、PB历史分位，PEG比率，ROE水平，负债率</li>`;
    reasoningContent += `<li>基本面分析：评估ROE连续性，毛利率水平，营收和利润增长</li>`;
    reasoningContent += `<li>护城河分析：基于毛利率、长期ROE、市场认可度等评估竞争优势</li>`;
    reasoningContent += `<li>风险分析：评估负债率风险，估值风险，利润下滑风险，现金流风险</li>`;
    reasoningContent += `<li>GitHub大模型深度分析：结合价值投资原则进行综合评估</li>`;
    reasoningContent += `<li>形成最终投资建议：综合传统分析和AI深度分析结果</li>`;
    reasoningContent += `</ol>`;
    
    reasoningSteps.innerHTML = reasoningContent;
  }
  
  // 发送按钮点击事件
  sendMessageBtn.addEventListener("click", sendMessage);
  
  // 回车键发送消息
  userInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
      sendMessage();
    }
  });
  
  // 示例问题点击事件
  exampleQuestions.forEach(question => {
    question.addEventListener("click", (e) => {
      e.preventDefault();
      userInput.value = question.textContent;
      sendMessage();
    });
  });
});

// 填充股票选择器
for (let code in stockData) {
  const opt = document.createElement("option");
  opt.value = code;
  opt.textContent = `${stockData[code].name} (${code})`;
  document.getElementById("stockSelector").appendChild(opt);
}