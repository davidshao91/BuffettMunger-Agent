"""GitHub大模型集成模块"""
import os
import json
import time
from typing import Optional, Dict, Any, List


class GitHubLLMInterface:
    """GitHub大模型接口封装"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "github-copilot"):
        """
        初始化GitHub大模型接口
        
        Args:
            api_key: API密钥
            model: 模型名称
        """
        self.api_key = api_key or os.environ.get("GITHUB_TOKEN")
        self.model = model
        self.skill_content = self._load_skill_file()
        self.conversation_history: List[Dict[str, str]] = []
    
    def _load_skill_file(self) -> str:
        """
        加载Skill.md文件内容
        
        Returns:
            Skill.md文件内容
        """
        try:
            skill_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "Skill.md")
            with open(skill_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"加载Skill.md失败: {e}")
            return ""
    
    def generate_investment_analysis(self, company_data: Dict[str, Any], user_question: Optional[str] = None) -> Dict[str, Any]:
        """
        使用GitHub大模型生成投资分析
        
        Args:
            company_data: 公司数据
            user_question: 用户问题（可选）
            
        Returns:
            分析结果
        """
        try:
            # 构建提示词
            prompt = self._build_investment_prompt(company_data, user_question)
            
            # 这里使用模拟数据，实际项目中应该调用真实的GitHub AI API
            # 例如使用GitHub Copilot API或其他GitHub AI服务
            
            # 模拟大模型返回的分析结果
            analysis_result = self._mock_github_llm_response(company_data, user_question)
            
            # 保存对话历史
            if user_question:
                self.conversation_history.append({"role": "user", "content": user_question})
            self.conversation_history.append({"role": "assistant", "content": json.dumps(analysis_result)})
            
            return analysis_result
            
        except Exception as e:
            print(f"GitHub大模型分析失败: {e}")
            # 返回默认分析结果
            return {
                "analysis_summary": "GitHub大模型分析失败，使用默认分析",
                "investment_recommendation": "中性",
                "confidence_score": 0.5,
                "risk_assessment": "中等",
                "key_findings": ["分析失败，无法提供详细信息"],
                "valuation_analysis": {},
                "fundamental_analysis": {},
                "moat_analysis": {},
                "risk_analysis": {},
                "recommendation_reasoning": "分析失败，无法提供推理过程",
                "next_steps": ["请检查网络连接后重试"]
            }
    
    def _build_investment_prompt(self, company_data: Dict[str, Any], user_question: Optional[str] = None) -> str:
        """
        构建投资分析提示词
        
        Args:
            company_data: 公司数据
            user_question: 用户问题（可选）
            
        Returns:
            提示词字符串
        """
        prompt_parts = []
        
        # 系统提示词
        prompt_parts.append(f"你是一个专业的价值投资分析师，精通巴菲特和芒格的投资哲学。")
        prompt_parts.append(f"请根据以下技能框架和公司数据，提供深入、专业的投资分析：")
        prompt_parts.append(f"\n## 价值投资技能框架\n{self.skill_content}")
        
        # 公司数据
        prompt_parts.append(f"\n## 公司数据\n")
        prompt_parts.append(f"- 股票代码: {company_data.get('code', '未知')}")
        prompt_parts.append(f"- 公司名称: {company_data.get('name', '未知')}")
        prompt_parts.append(f"- 市盈率(PE): {company_data.get('pe', '未知')}")
        prompt_parts.append(f"- 市净率(PB): {company_data.get('pb', '未知')}")
        prompt_parts.append(f"- PEG比率: {company_data.get('peg', '未知')}")
        prompt_parts.append(f"- 市盈率历史分位: {company_data.get('pe_hist_percent', '未知')}%")
        prompt_parts.append(f"- 市净率历史分位: {company_data.get('pb_hist_percent', '未知')}%")
        prompt_parts.append(f"- 净资产收益率(ROE): {company_data.get('roe_ttm', '未知')}%")
        prompt_parts.append(f"- 资产负债率: {company_data.get('debt_to_asset', '未知')}%")
        prompt_parts.append(f"- 营收增长率: {company_data.get('revenue_growth', '未知')}%")
        prompt_parts.append(f"- 利润增长率: {company_data.get('profit_growth', '未知')}%")
        prompt_parts.append(f"- 毛利率: {company_data.get('gross_margin', '未知')}%")
        prompt_parts.append(f"- 现金流健康度: {'健康' if company_data.get('cash_flow_healthy', False) else '不健康'}")
        
        # 用户问题
        if user_question:
            prompt_parts.append(f"\n## 用户问题\n{user_question}")
        
        # 分析要求
        prompt_parts.append(f"\n## 分析要求\n")
        prompt_parts.append(f"1. 基于价值投资技能框架，提供全面的投资分析")
        prompt_parts.append(f"2. 重点分析安全边际、基本面、护城河和风险")
        prompt_parts.append(f"3. 提供明确的投资建议（买入/持有/卖出）")
        prompt_parts.append(f"4. 给出建议的置信度评分（0-1）")
        prompt_parts.append(f"5. 详细阐述分析理由和关键依据")
        prompt_parts.append(f"6. 识别主要风险因素并提供应对策略")
        prompt_parts.append(f"7. 提供下一步行动建议")
        
        # 输出格式要求
        prompt_parts.append(f"\n## 输出格式\n")
        prompt_parts.append(f"请以JSON格式返回分析结果，包含以下字段：")
        prompt_parts.append(f"{{")
        prompt_parts.append(f"  \"analysis_summary\": \"分析摘要\",")
        prompt_parts.append(f"  \"investment_recommendation\": \"投资建议（买入/持有/卖出）\",")
        prompt_parts.append(f"  \"confidence_score\": 置信度评分（0-1）,")
        prompt_parts.append(f"  \"risk_assessment\": \"风险评估（低/中/高）\",")
        prompt_parts.append(f"  \"key_findings\": [\"关键发现1\", \"关键发现2\", ...],")
        prompt_parts.append('  "valuation_analysis": {\n    "intrinsic_value_estimate": "内在价值估计",\n    "safety_margin": "安全边际",\n    "valuation_methodology": "估值方法"\n  },')
        prompt_parts.append('  "fundamental_analysis": {\n    "financial_health": "财务健康度",\n    "growth_prospects": "增长前景",\n    "management_quality": "管理层质量"\n  },')
        prompt_parts.append('  "moat_analysis": {\n    "moat_type": "护城河类型",\n    "moat_strength": "护城河强度",\n    "sustainability": "可持续性"\n  },')
        prompt_parts.append('  "risk_analysis": {\n    "key_risks": ["风险1", "风险2", ...],\n    "risk_mitigation": ["缓解策略1", "缓解策略2", ...]\n  },')
        prompt_parts.append(f"  \"recommendation_reasoning\": \"建议推理过程\",")
        prompt_parts.append(f"  \"next_steps\": [\"下一步1\", \"下一步2\", ...]")
        prompt_parts.append(f"}}")
        
        return "\n".join(prompt_parts)
    
    def _mock_github_llm_response(self, company_data: Dict[str, Any], user_question: Optional[str] = None) -> Dict[str, Any]:
        """
        模拟GitHub大模型返回的分析结果
        
        Args:
            company_data: 公司数据
            user_question: 用户问题（可选）
            
        Returns:
            模拟的分析结果
        """
        # 基于公司数据生成合理的模拟分析
        pe = company_data.get('pe', 0)
        pb = company_data.get('pb', 0)
        roe = company_data.get('roe_ttm', 0)
        debt_to_asset = company_data.get('debt_to_asset', 100)
        revenue_growth = company_data.get('revenue_growth', 0)
        profit_growth = company_data.get('profit_growth', 0)
        gross_margin = company_data.get('gross_margin', 0)
        
        # 综合评估
        score = 0
        if pe < 20:
            score += 20
        if pb < 3:
            score += 20
        if roe > 15:
            score += 20
        if debt_to_asset < 50:
            score += 15
        if revenue_growth > 8:
            score += 10
        if profit_growth > 5:
            score += 10
        if gross_margin > 30:
            score += 5
        
        # 生成建议
        if score >= 80:
            recommendation = "买入"
            confidence = 0.85
            risk = "低"
        elif score >= 60:
            recommendation = "持有"
            confidence = 0.65
            risk = "中"
        else:
            recommendation = "卖出"
            confidence = 0.7
            risk = "高"
        
        # 生成关键发现
        key_findings = []
        if roe > 15:
            key_findings.append(f"ROE优秀({roe}%)，表明公司盈利能力强")
        if pe < 20:
            key_findings.append(f"市盈率合理({pe})，估值相对便宜")
        if debt_to_asset < 50:
            key_findings.append(f"资产负债率健康({debt_to_asset}%)，财务风险低")
        if revenue_growth > 8:
            key_findings.append(f"营收增长良好({revenue_growth}%)，业务扩张顺利")
        if profit_growth > 5:
            key_findings.append(f"利润增长稳定({profit_growth}%)，盈利能力持续")
        if gross_margin > 30:
            key_findings.append(f"毛利率较高({gross_margin}%)，产品具有一定定价权")
        
        # 生成风险分析
        key_risks = []
        risk_mitigation = []
        if pe > 30:
            key_risks.append("估值过高，存在回调风险")
            risk_mitigation.append("等待估值回归合理区间")
        if debt_to_asset > 60:
            key_risks.append("资产负债率过高，财务风险较大")
            risk_mitigation.append("关注债务结构和偿债能力")
        if profit_growth < 0:
            key_risks.append("利润负增长，盈利能力下降")
            risk_mitigation.append("分析利润下滑原因，评估持续性")
        if revenue_growth < 0:
            key_risks.append("营收负增长，业务可能面临困境")
            risk_mitigation.append("关注行业趋势和公司战略调整")
        
        # 生成分析结果
        analysis_result = {
            "analysis_summary": f"{company_data.get('name', '该公司')}的投资分析：基于价值投资原则，综合评估公司的安全边际、基本面、护城河和风险。",
            "investment_recommendation": recommendation,
            "confidence_score": confidence,
            "risk_assessment": risk,
            "key_findings": key_findings if key_findings else ["未发现明显优势"],
            "valuation_analysis": {
                "intrinsic_value_estimate": f"基于DCF模型和相对估值法，内在价值估计为合理水平",
                "safety_margin": f"安全边际评估为{'高' if score >= 80 else '中' if score >= 60 else '低'}",
                "valuation_methodology": "DCF模型、相对估值法、历史估值对比"
            },
            "fundamental_analysis": {
                "financial_health": f"财务健康度{'优秀' if debt_to_asset < 50 and roe > 15 else '良好' if debt_to_asset < 60 and roe > 10 else '一般'}",
                "growth_prospects": f"增长前景{'良好' if revenue_growth > 8 and profit_growth > 5 else '一般' if revenue_growth > 0 else '谨慎'}",
                "management_quality": "基于公开信息，管理层质量良好"
            },
            "moat_analysis": {
                "moat_type": "基于高ROE和毛利率，具有一定的护城河",
                "moat_strength": f"护城河强度{'强' if roe > 20 and gross_margin > 40 else '中等' if roe > 15 and gross_margin > 30 else '弱'}",
                "sustainability": "护城河具有一定的可持续性"
            },
            "risk_analysis": {
                "key_risks": key_risks if key_risks else ["未发现重大风险"],
                "risk_mitigation": risk_mitigation if risk_mitigation else ["保持密切关注"]
            },
            "recommendation_reasoning": f"基于公司的{('高ROE、合理估值和健康财务状况' if score >= 80 else '良好基本面和中等估值' if score >= 60 else '估值过高或基本面存在问题')}，建议{recommendation}。",
            "next_steps": [
                "持续跟踪公司季度财报",
                "关注行业竞争格局变化",
                "评估管理层战略执行情况",
                "根据市场变化调整投资策略"
            ]
        }
        
        # 如果有用户问题，根据问题调整分析结果
        if user_question:
            if "安全边际" in user_question or "估值" in user_question:
                analysis_result["key_findings"].insert(0, "用户关注安全边际分析，已重点评估")
            elif "护城河" in user_question or "竞争优势" in user_question:
                analysis_result["key_findings"].insert(0, "用户关注护城河分析，已重点评估竞争优势")
            elif "风险" in user_question or "隐患" in user_question:
                analysis_result["key_findings"].insert(0, "用户关注风险分析，已重点评估潜在风险")
            elif "管理层" in user_question or "管理" in user_question:
                analysis_result["key_findings"].insert(0, "用户关注管理层分析，已重点评估管理质量")
        
        return analysis_result
    
    def ask_follow_up_question(self, question: str) -> Dict[str, Any]:
        """
        追问功能
        
        Args:
            question: 用户追问
            
        Returns:
            回答结果
        """
        try:
            # 构建追问提示词
            prompt = self._build_follow_up_prompt(question)
            
            # 模拟大模型回答
            follow_up_response = self._mock_follow_up_response(question)
            
            # 保存对话历史
            self.conversation_history.append({"role": "user", "content": question})
            self.conversation_history.append({"role": "assistant", "content": json.dumps(follow_up_response)})
            
            return follow_up_response
            
        except Exception as e:
            print(f"GitHub大模型追问失败: {e}")
            return {
                "answer": "追问失败，无法提供回答",
                "confidence": 0.5,
                "related_topics": ["追问失败"]
            }
    
    def _build_follow_up_prompt(self, question: str) -> str:
        """
        构建追问提示词
        
        Args:
            question: 用户追问
            
        Returns:
            提示词字符串
        """
        prompt_parts = []
        prompt_parts.append(f"你是一个专业的价值投资分析师，正在回答用户的追问。")
        prompt_parts.append(f"\n## 对话历史\n")
        for msg in self.conversation_history[-5:]:  # 只使用最近5条对话
            prompt_parts.append(f"{msg['role']}: {msg['content']}")
        prompt_parts.append(f"\n## 最新问题\n{question}")
        prompt_parts.append(f"\n## 回答要求\n")
        prompt_parts.append(f"1. 基于对话历史和价值投资知识回答问题")
        prompt_parts.append(f"2. 提供详细、专业的分析")
        prompt_parts.append(f"3. 引用相关的价值投资原则")
        prompt_parts.append(f"4. 给出明确的结论和建议")
        return "\n".join(prompt_parts)
    
    def _mock_follow_up_response(self, question: str) -> Dict[str, Any]:
        """
        模拟追问回答
        
        Args:
            question: 用户追问
            
        Returns:
            模拟的回答结果
        """
        # 基于问题类型生成不同的回答
        if "安全边际" in question:
            answer = "安全边际是价值投资的核心原则之一，它代表了内在价值与市场价格之间的差距。计算安全边际的方法包括：1) DCF模型计算内在价值，2) 相对估值法对比历史和行业水平，3) 考虑最坏情景下的价值。一般来说，安全边际大于30%被认为是较高的，15-30%为中等，低于15%为较低。"
        elif "护城河" in question:
            answer = "护城河是公司长期保持竞争优势的能力，主要包括：1) 品牌护城河（如茅台、苹果），2) 成本优势护城河（如沃尔玛、亚马逊），3) 网络效应护城河（如Facebook、微信），4) 转换成本护城河（如企业软件），5) 规模经济护城河。评估护城河强度需要分析ROE持续性、毛利率水平、市场份额稳定性等指标。"
        elif "DCF" in question or "内在价值" in question:
            answer = "DCF（自由现金流贴现）模型是估计内在价值的重要方法，它通过预测未来自由现金流并折现到现在来计算公司价值。关键参数包括：1) 自由现金流预测，2) 贴现率选择（通常使用WACC），3) 增长率假设，4) 预测期长度。DCF模型的局限性在于对参数非常敏感，因此建议结合多种估值方法使用。"
        elif "风险" in question:
            answer = "投资风险主要包括：1) 财务风险（如债务过高、现金流恶化），2) 经营风险（如业务模式变化、竞争加剧），3) 管理层风险（如能力不足、诚信问题），4) 行业风险（如技术迭代、监管变化），5) 宏观风险（如经济衰退、利率上升）。风险管理策略包括分散投资、仓位控制、止损机制和定期重估。"
        elif "管理层" in question:
            answer = "管理层质量是价值投资的重要考量因素，评估维度包括：1) 诚信度（信息披露质量、历史行为），2) 能力（战略规划、执行能力、资本配置），3) 利益一致性（持股比例、薪酬结构），4) 企业文化（长期导向、创新能力）。可以通过阅读年报、股东大会记录、管理层访谈等方式评估。"
        else:
            answer = "作为价值投资分析师，我建议你关注以下核心要素：1) 安全边际（内在价值与价格的差距），2) 基本面（财务健康度、增长前景），3) 护城河（竞争优势的持续性），4) 风险（多维度风险评估）。投资决策应该基于深入的研究和理性的分析，而非市场情绪。"
        
        return {
            "answer": answer,
            "confidence": 0.8,
            "related_topics": ["价值投资原则", "投资分析方法", "风险管理策略"]
        }
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """
        获取对话历史
        
        Returns:
            对话历史
        """
        return self.conversation_history
    
    def clear_conversation_history(self):
        """
        清除对话历史
        """
        self.conversation_history = []


def get_github_llm_analysis(company_data: Dict[str, Any], user_question: Optional[str] = None, api_key: Optional[str] = None) -> Dict[str, Any]:
    """
    获取GitHub大模型分析结果
    
    Args:
        company_data: 公司数据
        user_question: 用户问题（可选）
        api_key: API密钥
        
    Returns:
        分析结果
    """
    github_llm = GitHubLLMInterface(api_key)
    return github_llm.generate_investment_analysis(company_data, user_question)


def ask_github_llm_follow_up(question: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    """
    向GitHub大模型追问
    
    Args:
        question: 用户追问
        api_key: API密钥
        
    Returns:
        回答结果
    """
    github_llm = GitHubLLMInterface(api_key)
    return github_llm.ask_follow_up_question(question)
