# Fundamental-Q-Agent

## 项目定位
**Fundamental-Q-Agent（基本面量化决策智能体）** 不是聊天AI，不是通用Agent，是带大模型推理的轻量化基本面量化引擎。

核心理念：数据因子为基、规则为护栏、模型做定性推理、输出标准化、决策可复现

## 技术栈
- **语言**：Python 3.10+
- **前端**：Streamlit（极简UI，一屏决策）
- **API**：OpenAI兼容格式（适配Kimi/Minimax/MaaS）
- **数据**：本地JSON观察池，轻量因子缓存，无数据库
- **部署**：GitHub + Streamlit Cloud / 容器友好
- **无图表、无K线、无冗余可视化**

## 核心架构

### 1. 数据层（量化核心）
- **输入**：股票代码/公司名
- **基础因子**（固定10项）：ROE、毛利率、净现比、资产负债率、PE/PB、营收/利润增速、股息率、现金流质量
- **硬排雷规则**（一票否决）：高负债、利润持续为负、现金流持续恶化、高质押高风险

### 2. 控制层（Agent核心）
- **流程固定**：输入→因子校验→排雷→模型推理→格式化输出→本地缓存
- **模型仅做推理环节**，不控制流程，不自由发挥
- **温度0.1**，强约束、防漂移、可复现

### 3. 推理层（大模型）
- **仅做定性推理**：商业模式、护城河、管理层质量、逻辑权衡、风险解释
- **禁止编造数据**，禁止技术分析，禁止短期预测

### 4. 产品层（极简UI）
- **单输入框 + 分析按钮**
- **输出固定三段**：结论→关键事实→推理链
- **本地观察列表**：增删改查，JSON持久化
- **API Key侧边栏配置**，不硬编码

## 输出格式

```
【决策结论】买入/观望/不碰 + 一句话理由
【关键事实】≤5条量化因子+业务核心（真实、可验证）
【推理逻辑】巴菲特风格，量化规则+定性逻辑，可解释、不玄学
【风险提示】≤3条核心风险
```

## 项目结构

```
Fundamental-Q-Agent/
├── app.py                  # 主程序入口
├── config.py               # API、模型、参数配置
├── factors.py              # 基本面因子定义、排雷规则（量化核心）
├── agent.py                # Agent流程控制、推理调度
├── prompt.py               # 系统提示词（巴菲特+量化对齐）
├── storage.py              # 本地JSON存储
├── requirements.txt        # 最小依赖
├── .gitignore              # Python标准
├── README.md               # 项目说明
└── LICENSE                 # MIT许可证
```

## 部署步骤

### 1. 本地运行

```bash
# 克隆项目
git clone https://github.com/yourusername/Fundamental-Q-Agent.git
cd Fundamental-Q-Agent

# 安装依赖
pip install -r requirements.txt

# 运行
streamlit run app.py
```

### 2. Streamlit Cloud部署

1. Fork本项目到你的GitHub账号
2. 访问 [Streamlit Cloud](https://streamlit.io/cloud)
3. 点击 "New app"
4. 选择你的GitHub仓库
5. 填写部署信息：
   - **Repository**：yourusername/Fundamental-Q-Agent
   - **Branch**：main
   - **Main file path**：app.py
6. 点击 "Deploy"

### 3. 容器部署

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
```

## 使用说明

1. **配置API Key**：在侧边栏输入你的OpenAI兼容API Key
2. **选择模型提供商**：支持Kimi、Minimax、OpenAI
3. **输入股票信息**：填写股票代码和公司名称
4. **填写因子数据**：输入基本面因子数据（实际项目中可接入真实数据源）
5. **点击分析**：系统会执行因子校验、排雷、模型推理等流程
6. **查看结果**：获取标准化的分析结论、关键事实和推理逻辑
7. **添加到观察列表**：将感兴趣的股票添加到本地观察池

## 核心逻辑

1. **因子校验**：确保所有必要的量化因子数据完整有效
2. **硬排雷**：对高负债、持续亏损、现金流恶化等风险进行一票否决
3. **因子评分**：对各因子进行标准化评分，生成总体等级
4. **模型推理**：使用大模型对定性因素进行分析，如商业模式、护城河等
5. **格式化输出**：按照固定格式生成分析报告
6. **本地缓存**：将分析结果缓存到本地，提高后续查询效率

## 风险提示

1. **数据准确性**：本项目使用模拟数据，实际使用中需要接入真实、可靠的数据源
2. **模型风险**：大模型可能存在推理偏差，决策结果仅供参考
3. **市场风险**：投资决策受多种因素影响，本工具不保证投资收益
4. **API依赖**：依赖第三方API服务，可能存在服务不稳定或费用问题
5. **局限性**：仅基于基本面分析，不考虑技术面和市场情绪等因素

## 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件
