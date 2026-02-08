# BuffettMunger-Agent
📈 数字化巴菲特与芒格｜开源·可测试·可自动化·纯价值投资智能体

---

## 🧠 项目理念
我们把价值投资的核心——**安全边际、护城河、财务健康、风险控制、理性决策**——工程化为一套可复用、可自动化、可验证的 Skill 体系。

让每个人都能拥有：
不情绪化、不追高、不博弈、长期稳健的投资分析系统。

---

## ✨ 核心能力（5大工业级 Skill）
- 🛡️ **安全边际分析**（巴菲特核心）
- 📊 **基本面健康度扫描**
- 🏰 **护城河壁垒评分**（芒格核心）
- ⚠️ **财务风险自动排雷**
- 🎯 **综合价值评级决策**

---

## 🚀 在线 Demo（无需安装，点开即玩）
👉 **直接体验：https://davidshao91.github.io/BuffettMunger-Agent/**

无需Python、无需环境、无需配置，
选择公司 → 运行Agent → 查看完整价投分析报告。

---

## 📂 快速启动（本地运行）
```bash
# 克隆项目
git clone https://github.com/davidshao91/BuffettMunger-Agent.git
cd BuffettMunger-Agent

# 一键运行
python main.py

# 分析指定股票
python main.py --code 600519.SH

# 使用实时数据
python main.py --code 600519.SH --real-time
```

---

## 📊 数据源支持

BuffettMunger-Agent 支持从多个数据源获取数据：

- **雪球网**：提供详细的股票数据和市场信息
- **新浪财经**：提供实时的股票报价数据
- **小红书**：提供市场情绪和相关投资话题
- **示例数据**：内置的离线数据，确保系统在无网络环境下也能运行

---

## 🤖 大模型集成

系统集成了大模型分析能力，为投资决策提供更全面的支持：

- **智能分析**：利用大模型分析公司财务数据和市场信息
- **投资建议**：基于综合分析生成投资建议
- **风险评估**：评估投资风险和不确定性
- **置信度评分**：为分析结果提供置信度评估

---

## 🧪 测试指南

### 运行所有测试
```bash
# 使用测试运行脚本
python run_tests.py

# 或单独运行测试文件
python tests/test_data.py
python tests/test_skills.py
python tests/test_agent.py
python tests/test_llm.py
python tests/test_integration.py
```

### 测试内容
- **数据获取测试**：验证多数据源的连接和数据获取
- **技能模块测试**：测试核心分析功能
- **Agent测试**：测试完整的分析流程
- **大模型测试**：测试大模型接口和集成
- **集成测试**：测试系统各模块的协同工作