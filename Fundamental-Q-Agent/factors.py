#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
因子模块：基本面因子定义、排雷规则（量化核心）
"""

from typing import Dict, List, Tuple, Optional
from config import Config


class Factors:
    """因子类"""
    
    @staticmethod
    def validate_factors(factor_data: Dict) -> Tuple[bool, List[str]]:
        """验证因子数据
        
        Args:
            factor_data: 因子数据
            
        Returns:
            Tuple[bool, List[str]]: (是否有效, 错误信息)
        """
        required_factors = [
            'roe', 'gross_margin', 'cash_flow_ratio', 'debt_ratio',
            'pe', 'pb', 'revenue_growth', 'profit_growth',
            'dividend_yield', 'cash_flow_quality'
        ]
        
        errors = []
        for factor in required_factors:
            if factor not in factor_data:
                errors.append(f"缺少因子: {factor}")
            elif factor_data[factor] is None:
                errors.append(f"因子值为空: {factor}")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def check_minefields(factor_data: Dict, business_data: Dict) -> Tuple[bool, str]:
        """检查排雷规则
        
        Args:
            factor_data: 因子数据
            business_data: 业务数据
            
        Returns:
            Tuple[bool, str]: (是否通过, 排雷结果)
        """
        # 1. 高负债检查
        debt_ratio = factor_data.get('debt_ratio', 0)
        if debt_ratio > Config.BANKRUPTCY_DEBT_RATIO:
            return False, f"高负债风险：资产负债率 {debt_ratio}% 超过阈值 {Config.BANKRUPTCY_DEBT_RATIO}%"
        
        # 2. 利润持续为负检查
        loss_years = business_data.get('loss_years', 0)
        if loss_years >= Config.LOSS_YEARS_THRESHOLD:
            return False, f"利润持续为负：连续亏损 {loss_years} 年"
        
        # 3. 现金流持续恶化检查
        cash_flow_deterioration = business_data.get('cash_flow_deterioration_years', 0)
        if cash_flow_deterioration >= Config.CASH_FLOW_DETERIORATION_YEARS:
            return False, f"现金流持续恶化：连续 {cash_flow_deterioration} 年恶化"
        
        # 4. 高质押高风险检查
        high_pledge = business_data.get('high_pledge', False)
        if high_pledge:
            return False, "高质押风险：股权质押比例过高"
        
        return True, "通过排雷检查"
    
    @staticmethod
    def score_factors(factor_data: Dict) -> Dict:
        """因子评分
        
        Args:
            factor_data: 因子数据
            
        Returns:
            Dict: 评分结果
        """
        scores = {}
        
        # ROE评分
        roe = factor_data.get('roe', 0)
        if roe >= 20:
            scores['roe'] = 5
        elif roe >= 15:
            scores['roe'] = 4
        elif roe >= 10:
            scores['roe'] = 3
        elif roe >= 5:
            scores['roe'] = 2
        else:
            scores['roe'] = 1
        
        # 毛利率评分
        gross_margin = factor_data.get('gross_margin', 0)
        if gross_margin >= 40:
            scores['gross_margin'] = 5
        elif gross_margin >= 30:
            scores['gross_margin'] = 4
        elif gross_margin >= 20:
            scores['gross_margin'] = 3
        elif gross_margin >= 10:
            scores['gross_margin'] = 2
        else:
            scores['gross_margin'] = 1
        
        # 净现比评分
        cash_flow_ratio = factor_data.get('cash_flow_ratio', 0)
        if cash_flow_ratio >= 1.5:
            scores['cash_flow_ratio'] = 5
        elif cash_flow_ratio >= 1.0:
            scores['cash_flow_ratio'] = 4
        elif cash_flow_ratio >= 0.5:
            scores['cash_flow_ratio'] = 3
        elif cash_flow_ratio >= 0.2:
            scores['cash_flow_ratio'] = 2
        else:
            scores['cash_flow_ratio'] = 1
        
        # 资产负债率评分
        debt_ratio = factor_data.get('debt_ratio', 0)
        if debt_ratio < 30:
            scores['debt_ratio'] = 5
        elif debt_ratio < 40:
            scores['debt_ratio'] = 4
        elif debt_ratio < 50:
            scores['debt_ratio'] = 3
        elif debt_ratio < 60:
            scores['debt_ratio'] = 2
        else:
            scores['debt_ratio'] = 1
        
        # PE评分
        pe = factor_data.get('pe', 0)
        if pe > 0 and pe < 15:
            scores['pe'] = 5
        elif pe >= 15 and pe < 20:
            scores['pe'] = 4
        elif pe >= 20 and pe < 25:
            scores['pe'] = 3
        elif pe >= 25 and pe < 30:
            scores['pe'] = 2
        else:
            scores['pe'] = 1
        
        # 股息率评分
        dividend_yield = factor_data.get('dividend_yield', 0)
        if dividend_yield >= 3:
            scores['dividend_yield'] = 5
        elif dividend_yield >= 2:
            scores['dividend_yield'] = 4
        elif dividend_yield >= 1:
            scores['dividend_yield'] = 3
        elif dividend_yield >= 0.5:
            scores['dividend_yield'] = 2
        else:
            scores['dividend_yield'] = 1
        
        # 营收增速评分
        revenue_growth = factor_data.get('revenue_growth', 0)
        if revenue_growth >= 30:
            scores['revenue_growth'] = 5
        elif revenue_growth >= 20:
            scores['revenue_growth'] = 4
        elif revenue_growth >= 10:
            scores['revenue_growth'] = 3
        elif revenue_growth >= 5:
            scores['revenue_growth'] = 2
        else:
            scores['revenue_growth'] = 1
        
        # 利润增速评分
        profit_growth = factor_data.get('profit_growth', 0)
        if profit_growth >= 30:
            scores['profit_growth'] = 5
        elif profit_growth >= 20:
            scores['profit_growth'] = 4
        elif profit_growth >= 10:
            scores['profit_growth'] = 3
        elif profit_growth >= 5:
            scores['profit_growth'] = 2
        else:
            scores['profit_growth'] = 1
        
        # 现金流质量评分
        cash_flow_quality = factor_data.get('cash_flow_quality', 0)
        if cash_flow_quality >= 0.8:
            scores['cash_flow_quality'] = 5
        elif cash_flow_quality >= 0.6:
            scores['cash_flow_quality'] = 4
        elif cash_flow_quality >= 0.4:
            scores['cash_flow_quality'] = 3
        elif cash_flow_quality >= 0.2:
            scores['cash_flow_quality'] = 2
        else:
            scores['cash_flow_quality'] = 1
        
        # 计算总分
        total_score = sum(scores.values())
        average_score = total_score / len(scores)
        
        return {
            'scores': scores,
            'total_score': total_score,
            'average_score': average_score,
            'grade': Factors._get_grade(average_score)
        }
    
    @staticmethod
    def _get_grade(average_score: float) -> str:
        """获取评分等级
        
        Args:
            average_score: 平均分数
            
        Returns:
            str: 评分等级
        """
        if average_score >= 4.5:
            return '优秀'
        elif average_score >= 3.5:
            return '良好'
        elif average_score >= 2.5:
            return '一般'
        elif average_score >= 1.5:
            return '较差'
        else:
            return '差'
    
    @staticmethod
    def get_key_facts(factor_data: Dict, business_data: Dict) -> List[str]:
        """获取关键事实
        
        Args:
            factor_data: 因子数据
            business_data: 业务数据
            
        Returns:
            List[str]: 关键事实列表
        """
        facts = []
        
        # 添加量化因子
        if factor_data.get('roe', 0) >= Config.MIN_ROE:
            facts.append(f"ROE: {factor_data['roe']}%")
        
        if factor_data.get('gross_margin', 0) >= Config.MIN_GROSS_MARGIN:
            facts.append(f"毛利率: {factor_data['gross_margin']}%")
        
        if factor_data.get('cash_flow_ratio', 0) >= Config.MIN_CASH_FLOW_RATIO:
            facts.append(f"净现比: {factor_data['cash_flow_ratio']}")
        
        if factor_data.get('debt_ratio', 0) <= Config.MAX_DEBT_RATIO:
            facts.append(f"资产负债率: {factor_data['debt_ratio']}%")
        
        pe = factor_data.get('pe', 0)
        if pe > 0 and pe <= Config.MAX_PE:
            facts.append(f"PE: {pe}")
        
        if factor_data.get('dividend_yield', 0) >= Config.MIN_DIVIDEND_YIELD:
            facts.append(f"股息率: {factor_data['dividend_yield']}%")
        
        # 添加业务核心
        business_core = business_data.get('business_core')
        if business_core:
            facts.append(f"业务核心: {business_core}")
        
        # 限制数量
        return facts[:Config.MAX_KEY_FACTS]
