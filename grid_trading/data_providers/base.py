"""
Data Provider Base Module
数据提供者抽象基类
"""

from abc import ABC, abstractmethod
import pandas as pd
from typing import List, Dict, Optional


class DataProvider(ABC):
    """股票数据提供者抽象基类"""
    
    @abstractmethod
    def get_historical_data(self, stock_code: str) -> pd.DataFrame:
        """
        获取历史行情数据
        
        Args:
            stock_code: 股票代码
            
        Returns:
            DataFrame with columns: date, open, high, low, close, volume
        """
        pass
    
    @abstractmethod
    def get_current_price(self, stock_code: str) -> Optional[float]:
        """
        获取当前价格
        
        Args:
            stock_code: 股票代码
            
        Returns:
            当前价格，如果获取失败返回 None
        """
        pass
    
    @abstractmethod
    def search_stocks(self, keyword: str) -> List[Dict]:
        """
        搜索股票
        
        Args:
            keyword: 搜索关键词（代码或名称）
            
        Returns:
            股票列表 [{code, name, market}, ...]
        """
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """提供者名称"""
        pass
