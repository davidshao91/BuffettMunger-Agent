#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主程序入口：Streamlit界面
"""

import streamlit as st
import time
from agent import FundamentalQAgent
from storage import Storage


# 页面配置
st.set_page_config(
    page_title="Fundamental-Q-Agent",
    page_icon="📊",
    layout="centered",
    initial_sidebar_state="expanded"
)

# 标题
st.title("Fundamental-Q-Agent")
st.subheader("基本面量化决策智能体")

# 侧边栏配置
with st.sidebar:
    st.header("API配置")
    api_key = st.text_input("API Key", type="password")
    model_provider = st.selectbox("模型提供商", ["kimi", "minimax", "openai"])
    model_name = st.text_input("模型名称", value="moonshot-v1-8k")
    
    st.header("观察列表")
    observation_pool = Storage.get_observation_pool()
    
    if observation_pool:
        st.subheader("当前观察池")
        for stock in observation_pool:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"{stock['code']} - {stock['name']}")
                st.caption(f"结论: {stock['conclusion']}")
            with col2:
                if st.button("移除", key=f"remove_{stock['code']}"):
                    Storage.remove_from_observation_pool(stock['code'])
                    st.experimental_rerun()
    else:
        st.info("观察池为空")

# 主界面
st.header("股票分析")

# 输入区域
col1, col2 = st.columns([2, 1])
with col1:
    stock_code = st.text_input("股票代码")
with col2:
    company_name = st.text_input("公司名称")

# 因子数据输入（模拟数据，实际项目中应接入真实数据源）
st.subheader("基本面因子")
col1, col2, col3 = st.columns(3)

with col1:
    roe = st.number_input("ROE (%)", min_value=0.0, max_value=100.0, value=15.0)
    gross_margin = st.number_input("毛利率 (%)", min_value=0.0, max_value=100.0, value=30.0)
    cash_flow_ratio = st.number_input("净现比", min_value=0.0, max_value=5.0, value=1.2)

with col2:
    debt_ratio = st.number_input("资产负债率 (%)", min_value=0.0, max_value=100.0, value=40.0)
    pe = st.number_input("PE", min_value=0.0, max_value=100.0, value=20.0)
    pb = st.number_input("PB", min_value=0.0, max_value=20.0, value=3.0)

with col3:
    revenue_growth = st.number_input("营收增速 (%)", min_value=-100.0, max_value=200.0, value=15.0)
    profit_growth = st.number_input("利润增速 (%)", min_value=-100.0, max_value=200.0, value=20.0)
    dividend_yield = st.number_input("股息率 (%)", min_value=0.0, max_value=20.0, value=2.0)
    cash_flow_quality = st.number_input("现金流质量", min_value=0.0, max_value=1.0, value=0.8)

# 业务数据输入
st.subheader("业务数据")
business_core = st.text_input("业务核心", value="高端制造")
loss_years = st.number_input("连续亏损年数", min_value=0, max_value=10, value=0)
cash_flow_deterioration_years = st.number_input("现金流恶化年数", min_value=0, max_value=10, value=0)
high_pledge = st.checkbox("高质押风险")

# 分析按钮
if st.button("分析"):
    if not api_key:
        st.error("请输入API Key")
    elif not stock_code or not company_name:
        st.error("请输入股票代码和公司名称")
    else:
        with st.spinner("分析中..."):
            # 构建因子数据
            factor_data = {
                "roe": roe,
                "gross_margin": gross_margin,
                "cash_flow_ratio": cash_flow_ratio,
                "debt_ratio": debt_ratio,
                "pe": pe,
                "pb": pb,
                "revenue_growth": revenue_growth,
                "profit_growth": profit_growth,
                "dividend_yield": dividend_yield,
                "cash_flow_quality": cash_flow_quality
            }
            
            # 构建业务数据
            business_data = {
                "business_core": business_core,
                "loss_years": loss_years,
                "cash_flow_deterioration_years": cash_flow_deterioration_years,
                "high_pledge": high_pledge
            }
            
            # 初始化Agent
            agent = FundamentalQAgent(api_key, model_provider, model_name)
            
            # 执行分析
            result = agent.analyze(stock_code, company_name, factor_data, business_data)
            
            # 显示结果
            if "error" in result:
                st.error(result["error"])
            else:
                st.subheader("分析结果")
                
                # 决策结论
                st.markdown(f"### 【决策结论】")
                st.write(result["conclusion"])
                
                # 关键事实
                st.markdown(f"### 【关键事实】")
                for fact in result["key_facts"]:
                    st.write(f"- {fact}")
                
                # 推理逻辑
                st.markdown(f"### 【推理逻辑】")
                st.write(result["reasoning"])
                
                # 风险提示
                st.markdown(f"### 【风险提示】")
                for risk in result["risks"]:
                    st.write(f"- {risk}")
                
                # 添加到观察列表按钮
                if st.button("添加到观察列表"):
                    success = agent.add_to_observation(stock_code, company_name, result)
                    if success:
                        st.success("已添加到观察列表")
                    else:
                        st.warning("已在观察列表中")

# 页脚
st.footer("Fundamental-Q-Agent - 基本面量化决策智能体")
