#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agent模块：流程控制、推理调度
"""

import os
import json
import time
from typing import Dict, List, Tuple, Optional
import openai
from config import Config, ModelProvider
from factors import Factors
from prompt import SystemPrompt
from storage import Storage


class FundamentalQAgent:
    """基本面量化决策智能体"""
    
    def __init__(self, api_key: str, model_provider: str = "kimi", model_name: str = "moonshot-v1-8k"):
        """初始化智能体
        
        Args:
            api_key: API密钥
            model_provider: 模型提供商
            model_name: 模型名称
        """
        self.api_key = api_key
        self.model_provider = model_provider
        self.model_name = model_name
        
        # 配置OpenAI客户端
        self.client = openai.OpenAI(
            api_key=api_key,
            base_url=ModelProvider.get_api_base(model_provider)
        )
    
    def analyze(self, stock_code: str, company_name: str, factor_data: Dict, business_data: Dict) -> Dict:
        """执行分析流程
        
        Args:
            stock_code: 股票代码
            company_name: 公司名称
            factor_data: 因子数据
            business_data: 业务数据
            
        Returns:
            Dict: 分析结果
        """
        try:
            # 1. 因子校验
            valid, errors = Factors.validate_factors(factor_data)
            if not valid:
                return {
                    "error": f"因子数据无效: {'; '.join(errors)}"
                }
            
            # 2. 排雷
            minefield_passed, minefield_result = Factors.check_minefields(factor_data, business_data)
            
            # 3. 因子评分
            score_result = Factors.score_factors(factor_data)
            
            # 4. 模型推理
            analysis_result = self._model_reasoning(factor_data, business_data, minefield_result, score_result)
            
            # 5. 格式化输出
            formatted_result = self._format_output(analysis_result, factor_data, business_data)
            
            # 6. 本地缓存
            cache_data = {
                "stock_code": stock_code,
                "company_name": company_name,
                "factor_data": factor_data,
                "business_data": business_data,
                "analysis_result": formatted_result,
                "timestamp": time.time()
            }
            Storage.set_factor_cache(stock_code, cache_data)
            
            return formatted_result
            
        except Exception as e:
            return {
                "error": f"分析失败: {str(e)}"
            }
    
    def _model_reasoning(self, factor_data: Dict, business_data: Dict, minefield_result: str, score_result: Dict) -> str:
        """模型推理
        
        Args:
            factor_data: 因子数据
            business_data: 业务数据
            minefield_result: 排雷结果
            score_result: 评分结果
            
        Returns:
            str: 模型推理结果
        """
        system_prompt = SystemPrompt.get_buffett_prompt()
        user_prompt = SystemPrompt.get_analysis_prompt(factor_data, business_data, minefield_result, score_result)
        
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=Config.MODEL_TEMPERATURE,
            max_tokens=Config.MAX_TOKENS,
            timeout=Config.TIMEOUT
        )
        
        return response.choices[0].message.content
    
    def _format_output(self, analysis_result: str, factor_data: Dict, business_data: Dict) -> Dict:
        """格式化输出
        
        Args:
            analysis_result: 分析结果
            factor_data: 因子数据
            business_data: 业务数据
            
        Returns:
            Dict: 格式化的分析结果
        """
        # 解析模型输出
        lines = analysis_result.strip().split('\n')
        
        result = {
            "conclusion": "",
            "key_facts": [],
            "reasoning": "",
            "risks": []
        }
        
        current_section = None
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            if line.startswith("【决策结论】"):
                current_section = "conclusion"
                result["conclusion"] = line.replace("【决策结论】", "").strip()
            elif line.startswith("【关键事实】"):
                current_section = "key_facts"
            elif line.startswith("【推理逻辑】"):
                current_section = "reasoning"
                result["reasoning"] = line.replace("【推理逻辑】", "").strip()
            elif line.startswith("【风险提示】"):
                current_section = "risks"
            else:
                if current_section == "key_facts" and line:
                    result["key_facts"].append(line)
                elif current_section == "reasoning" and line:
                    result["reasoning"] += " " + line
                elif current_section == "risks" and line:
                    result["risks"].append(line)
        
        # 限制数量
        result["key_facts"] = result["key_facts"][:Config.MAX_KEY_FACTS]
        result["risks"] = result["risks"][:Config.MAX_RISKS]
        
        return result
    
    def get_cached_analysis(self, stock_code: str) -> Optional[Dict]:
        """获取缓存的分析结果
        
        Args:
            stock_code: 股票代码
            
        Returns:
            Optional[Dict]: 缓存的分析结果
        """
        cache_data = Storage.get_factor_cache(stock_code)
        if cache_data:
            return cache_data.get("analysis_result")
        return None
    
    def add_to_observation(self, stock_code: str, company_name: str, analysis_result: Dict) -> bool:
        """添加到观察列表
        
        Args:
            stock_code: 股票代码
            company_name: 公司名称
            analysis_result: 分析结果
            
        Returns:
            bool: 是否添加成功
        """
        stock_info = {
            "code": stock_code,
            "name": company_name,
            "conclusion": analysis_result.get("conclusion", ""),
            "timestamp": time.time()
        }
        return Storage.add_to_observation_pool(stock_info)
