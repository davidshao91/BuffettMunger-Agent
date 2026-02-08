#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
存储模块：本地JSON存储，包含观察池和因子缓存的增删改查
"""

import json
import os
from typing import Dict, List, Optional, Any
from config import Config


class Storage:
    """存储类"""
    
    @staticmethod
    def _read_json(file_path: str) -> Dict:
        """读取JSON文件
        
        Args:
            file_path: 文件路径
            
        Returns:
            Dict: 文件内容
        """
        if not os.path.exists(file_path):
            return {}
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    
    @staticmethod
    def _write_json(file_path: str, data: Dict) -> bool:
        """写入JSON文件
        
        Args:
            file_path: 文件路径
            data: 要写入的数据
            
        Returns:
            bool: 是否写入成功
        """
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except IOError:
            return False
    
    @classmethod
    def get_observation_pool(cls) -> List[Dict]:
        """获取观察池
        
        Returns:
            List[Dict]: 观察池列表
        """
        data = cls._read_json(Config.OBSERVATION_POOL_PATH)
        return data.get('stocks', [])
    
    @classmethod
    def add_to_observation_pool(cls, stock_info: Dict) -> bool:
        """添加到观察池
        
        Args:
            stock_info: 股票信息
            
        Returns:
            bool: 是否添加成功
        """
        data = cls._read_json(Config.OBSERVATION_POOL_PATH)
        stocks = data.get('stocks', [])
        
        # 检查是否已存在
        stock_code = stock_info.get('code')
        for stock in stocks:
            if stock.get('code') == stock_code:
                return False
        
        stocks.append(stock_info)
        data['stocks'] = stocks
        return cls._write_json(Config.OBSERVATION_POOL_PATH, data)
    
    @classmethod
    def remove_from_observation_pool(cls, stock_code: str) -> bool:
        """从观察池移除
        
        Args:
            stock_code: 股票代码
            
        Returns:
            bool: 是否移除成功
        """
        data = cls._read_json(Config.OBSERVATION_POOL_PATH)
        stocks = data.get('stocks', [])
        
        new_stocks = [stock for stock in stocks if stock.get('code') != stock_code]
        if len(new_stocks) == len(stocks):
            return False
        
        data['stocks'] = new_stocks
        return cls._write_json(Config.OBSERVATION_POOL_PATH, data)
    
    @classmethod
    def update_observation_pool(cls, stock_code: str, updated_info: Dict) -> bool:
        """更新观察池中的股票信息
        
        Args:
            stock_code: 股票代码
            updated_info: 更新的信息
            
        Returns:
            bool: 是否更新成功
        """
        data = cls._read_json(Config.OBSERVATION_POOL_PATH)
        stocks = data.get('stocks', [])
        
        updated = False
        for stock in stocks:
            if stock.get('code') == stock_code:
                stock.update(updated_info)
                updated = True
                break
        
        if not updated:
            return False
        
        data['stocks'] = stocks
        return cls._write_json(Config.OBSERVATION_POOL_PATH, data)
    
    @classmethod
    def get_factor_cache(cls, stock_code: str) -> Optional[Dict]:
        """获取因子缓存
        
        Args:
            stock_code: 股票代码
            
        Returns:
            Optional[Dict]: 因子缓存数据
        """
        data = cls._read_json(Config.FACTOR_CACHE_PATH)
        return data.get(stock_code)
    
    @classmethod
    def set_factor_cache(cls, stock_code: str, factor_data: Dict) -> bool:
        """设置因子缓存
        
        Args:
            stock_code: 股票代码
            factor_data: 因子数据
            
        Returns:
            bool: 是否设置成功
        """
        data = cls._read_json(Config.FACTOR_CACHE_PATH)
        data[stock_code] = factor_data
        return cls._write_json(Config.FACTOR_CACHE_PATH, data)
    
    @classmethod
    def clear_factor_cache(cls, stock_code: Optional[str] = None) -> bool:
        """清除因子缓存
        
        Args:
            stock_code: 股票代码，None表示清除所有
            
        Returns:
            bool: 是否清除成功
        """
        if stock_code:
            data = cls._read_json(Config.FACTOR_CACHE_PATH)
            if stock_code in data:
                del data[stock_code]
                return cls._write_json(Config.FACTOR_CACHE_PATH, data)
            return True
        else:
            # 清除所有缓存
            return cls._write_json(Config.FACTOR_CACHE_PATH, {})
