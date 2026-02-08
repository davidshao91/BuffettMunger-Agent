#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置文件：API、模型、参数配置
"""


class Config:
    """配置类"""
    # 模型配置
    MODEL_TEMPERATURE = 0.1  # 温度设置，强约束、防漂移、可复现
    MAX_TOKENS = 1000  # 最大令牌数
    TIMEOUT = 30  # API超时时间（秒）
    
    # 因子配置
    MIN_ROE = 10  # 最低ROE要求（%）
    MIN_GROSS_MARGIN = 20  # 最低毛利率要求（%）
    MIN_CASH_FLOW_RATIO = 0.5  # 最低净现比要求
    MAX_DEBT_RATIO = 70  # 最高资产负债率要求（%）
    MAX_PE = 30  # 最高PE要求
    MIN_DIVIDEND_YIELD = 1  # 最低股息率要求（%）
    
    # 排雷规则阈值
    BANKRUPTCY_DEBT_RATIO = 80  # 破产风险资产负债率（%）
    LOSS_YEARS_THRESHOLD = 2  # 连续亏损年数阈值
    CASH_FLOW_DETERIORATION_YEARS = 2  # 现金流持续恶化年数
    
    # 存储配置
    OBSERVATION_POOL_PATH = "observation_pool.json"  # 观察池文件路径
    FACTOR_CACHE_PATH = "factor_cache.json"  # 因子缓存文件路径
    
    # 分析配置
    MAX_KEY_FACTS = 5  # 关键事实最大数量
    MAX_RISKS = 3  # 风险提示最大数量
    

class ModelProvider:
    """模型提供商配置"""
    # OpenAI兼容API基础URL
    PROVIDERS = {
        "kimi": "https://api.moonshot.cn/v1",
        "minimax": "https://api.minimax.chat/v1",
        "openai": "https://api.openai.com/v1",
    }
    
    @classmethod
    def get_api_base(cls, provider):
        """获取API基础URL
        
        Args:
            provider: 模型提供商名称
            
        Returns:
            str: API基础URL
        """
        return cls.PROVIDERS.get(provider, cls.PROVIDERS["openai"])
