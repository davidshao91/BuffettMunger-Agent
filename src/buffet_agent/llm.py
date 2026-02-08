"""大模型接口模块"""
import os
import json
from typing import Optional, Dict, Any


class LLMInterface:
    """大模型接口封装"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        """
        初始化大模型接口
        
        Args:
            api_key: API密钥
            model: 模型名称
        """
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self.model = model
    
    def generate_analysis(self, company_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        使用大模型生成投资分析
        
        Args:
            company_data: 公司数据
            
        Returns:
            分析结果
        """
        try:
            # 构建提示词
            prompt = self._build_prompt(company_data)
            
            # 这里使用模拟数据，实际项目中应该调用真实的LLM API
            # 例如使用OpenAI的API
            # import openai
            # response = openai.ChatCompletion.create(
            #     model=self.model,
            #     messages=[{"role": "user", "content": prompt}],
            #     api_key=self.api_key
            # )
            # analysis = response.choices[0].message.content
            
            # 模拟大模型返回的分析结果
            return self._mock_llm_response(company_data)
            
        except Exception as e:
            print(f"大模型分析失败: {e}")
            # 返回默认分析结果
            return {
                "llm_analysis": "大模型分析失败，使用默认分析",
                "investment_recommendation": "中性",
                "risk_assessment": "中等",
                "confidence_score": 0.5
            }
    
    def _build_prompt(self, company_data: Dict[str, Any]) -> str:
        """
        构建大模型提示词
        
        Args:
            company_data: 公司数据
            
        Returns:
            提示词字符串
        """
        prompt = f"""请作为一名专业的价值投资分析师，根据以下公司数据进行全面分析：

公司信息：
- 股票代码: {company_data.get('code', '未知')}
- 公司名称: {company_data.get('name', '未知')}

财务数据：
- 市盈率(PE): {company_data.get('pe', '未知')}
- 市净率(PB): {company_data.get('pb', '未知')}
- PEG比率: {company_data.get('peg', '未知')}
- 市盈率历史分位: {company_data.get('pe_hist_percent', '未知')}%
- 市净率历史分位: {company_data.get('pb_hist_percent', '未知')}%
- 净资产收益率(ROE): {company_data.get('roe_ttm', '未知')}%
- 资产负债率: {company_data.get('debt_to_asset', '未知')}%
- 营收增长率: {company_data.get('revenue_growth', '未知')}%
- 利润增长率: {company_data.get('profit_growth', '未知')}%
- 毛利率: {company_data.get('gross_margin', '未知')}%
- 现金流健康度: {company_data.get('cash_flow_healthy', '未知')}

请提供以下分析：
1. 公司的投资价值评估
2. 主要风险因素
3. 投资建议（买入/持有/卖出）
4. 置信度评分（0-1）

请以JSON格式返回分析结果，包含以下字段：
- llm_analysis: 详细分析
- investment_recommendation: 投资建议
- risk_assessment: 风险评估
- confidence_score: 置信度评分
"""
        return prompt
    
    def _mock_llm_response(self, company_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        模拟大模型返回的分析结果
        
        Args:
            company_data: 公司数据
            
        Returns:
            模拟的分析结果
        """
        # 根据公司数据生成合理的模拟分析
        pe = company_data.get('pe', 0)
        pb = company_data.get('pb', 0)
        roe = company_data.get('roe_ttm', 0)
        
        # 基于财务数据判断投资价值
        if pe < 20 and pb < 3 and roe > 15:
            recommendation = "买入"
            risk = "低"
            confidence = 0.85
        elif pe < 30 and pb < 5 and roe > 10:
            recommendation = "持有"
            risk = "中等"
            confidence = 0.65
        else:
            recommendation = "卖出"
            risk = "高"
            confidence = 0.7
        
        return {
            "llm_analysis": f"基于公司的财务数据，{company_data.get('name', '该公司')}具有{'较好' if recommendation == '买入' else '一般' if recommendation == '持有' else '较差'}的投资价值。",
            "investment_recommendation": recommendation,
            "risk_assessment": risk,
            "confidence_score": confidence
        }


def get_llm_analysis(company_data: Dict[str, Any], api_key: Optional[str] = None) -> Dict[str, Any]:
    """
    获取大模型分析结果
    
    Args:
        company_data: 公司数据
        api_key: API密钥
        
    Returns:
        分析结果
    """
    llm = LLMInterface(api_key)
    return llm.generate_analysis(company_data)
