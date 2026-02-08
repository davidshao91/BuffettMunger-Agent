from . import skills
from .llm import get_llm_analysis
from .github_llm import get_github_llm_analysis, ask_github_llm_follow_up
from .knowledge import enhance_analysis
from typing import Optional, Dict, Any, List

class ValueInvestmentAgent:
    """价值投资AI智能体"""
    
    def __init__(self):
        """
        初始化价值投资智能体
        """
        self.conversation_history: List[Dict[str, str]] = []
        self.analysis_history: List[Dict[str, Any]] = []
    
    def run_analysis(self, company_data: Dict[str, Any], user_question: Optional[str] = None) -> Dict[str, Any]:
        """
        运行完整价值投资分析流程
        
        Args:
            company_data: 公司数据
            user_question: 用户问题（可选）
            
        Returns:
            分析结果
        """
        # 传统分析模块
        safety = skills.safety_margin(company_data)
        fund = skills.fundamental(company_data)
        moat = skills.moat(company_data)
        risk = skills.risk(company_data)
        final = skills.final_rating([safety, fund, moat, risk])
        
        # 传统大模型分析
        llm_analysis = get_llm_analysis(company_data)
        
        # GitHub大模型深度分析
        github_analysis = get_github_llm_analysis(company_data, user_question)
        
        # 整合分析结果
        analysis_result = {
            "traditional_analysis": {
                "safety_margin": safety,
                "fundamental": fund,
                "moat": moat,
                "risk": risk,
                "avg_score": final["avg"],
                "final_decision": final["decision"]
            },
            "basic_llm_analysis": llm_analysis,
            "github_deep_analysis": github_analysis,
            "integrated_recommendation": self._integrate_recommendations(
                final["decision"], 
                github_analysis.get("investment_recommendation", "中性")
            ),
            "analysis_time": self._get_current_time(),
            "company_info": {
                "code": company_data.get("code", "未知"),
                "name": company_data.get("name", "未知")
            }
        }
        
        # 保存分析历史
        self.analysis_history.append(analysis_result)
        
        # 保存对话历史
        if user_question:
            self.conversation_history.append({"role": "user", "content": user_question})
        
        # 使用知识图谱增强分析
        enhanced_analysis = enhance_analysis(analysis_result, company_data)
        
        self.conversation_history.append({"role": "assistant", "content": str(enhanced_analysis)})
        
        return enhanced_analysis
    
    def ask_follow_up(self, question: str) -> Dict[str, Any]:
        """
        处理用户追问
        
        Args:
            question: 用户问题
            
        Returns:
            回答结果
        """
        # 使用GitHub大模型处理追问
        follow_up_response = ask_github_llm_follow_up(question)
        
        # 保存对话历史
        self.conversation_history.append({"role": "user", "content": question})
        self.conversation_history.append({"role": "assistant", "content": str(follow_up_response)})
        
        return follow_up_response
    
    def get_analysis_history(self) -> List[Dict[str, Any]]:
        """
        获取分析历史
        
        Returns:
            分析历史列表
        """
        return self.analysis_history
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """
        获取对话历史
        
        Returns:
            对话历史列表
        """
        return self.conversation_history
    
    def clear_history(self):
        """
        清除历史记录
        """
        self.conversation_history = []
        self.analysis_history = []
    
    def _integrate_recommendations(self, traditional_decision: str, github_recommendation: str) -> str:
        """
        整合传统分析和GitHub大模型的推荐结果
        
        Args:
            traditional_decision: 传统分析的决策
            github_recommendation: GitHub大模型的推荐
            
        Returns:
            整合后的推荐结果
        """
        # 推荐等级映射
        recommendation_map = {
            "强烈推荐": 5,
            "买入": 4,
            "建议关注": 3,
            "持有": 3,
            "中性观察": 2,
            "中性": 2,
            "规避": 1,
            "卖出": 1
        }
        
        # 提取传统分析的推荐等级
        traditional_level = 3  # 默认中性
        for key, level in recommendation_map.items():
            if key in traditional_decision:
                traditional_level = level
                break
        
        # 提取GitHub大模型的推荐等级
        github_level = recommendation_map.get(github_recommendation, 3)
        
        # 计算综合推荐等级（加权平均）
        # 传统分析权重60%，GitHub大模型权重40%
        combined_level = traditional_level * 0.6 + github_level * 0.4
        
        # 映射回推荐等级
        if combined_level >= 4.5:
            return "🌟 强烈推荐"
        elif combined_level >= 3.5:
            return "✅ 建议买入"
        elif combined_level >= 2.5:
            return "⚠️  中性观察"
        else:
            return "❌ 建议规避"
    
    def _get_current_time(self) -> str:
        """
        获取当前时间
        
        Returns:
            当前时间字符串
        """
        import datetime
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# 保持向后兼容
def run_analysis(company_data: Dict[str, Any], user_question: Optional[str] = None) -> Dict[str, Any]:
    """
    运行完整价值投资分析流程（向后兼容）
    """
    agent = ValueInvestmentAgent()
    return agent.run_analysis(company_data, user_question)

# 新增追问功能
def ask_follow_up(question: str) -> Dict[str, Any]:
    """
    处理用户追问
    """
    return ask_github_llm_follow_up(question)