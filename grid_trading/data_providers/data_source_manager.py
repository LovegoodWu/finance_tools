"""
Data Source Manager
数据源管理器 - 用于管理和切换不同的数据提供者
"""

from typing import Optional, List, Dict
import pandas as pd

from grid_trading.data_providers.base import DataProvider
from grid_trading.data_providers.baostock_provider import BaoStockProvider
from grid_trading.config import HISTORY_DIR


class DataSourceManager:
    """数据源管理器"""
    
    def __init__(self, cache_dir: str = None):
        """初始化数据源管理器
        
        Args:
            cache_dir: 历史数据缓存目录
        """
        self.cache_dir = str(cache_dir) if cache_dir else str(HISTORY_DIR)
        self.providers: Dict[str, DataProvider] = {}
        self.default_provider: Optional[DataProvider] = None
        
        # 注册所有可用的数据提供者
        self._register_providers()
    
    def _register_providers(self):
        """注册数据提供者"""
        # 注册 BaoStock - 作为默认提供者（前复权数据）
        try:
            baostock_provider = BaoStockProvider(cache_dir=self.cache_dir)
            self.providers["baostock"] = baostock_provider
            self.default_provider = baostock_provider
        except Exception as e:
            print(f"BaoStock 初始化失败：{e}")
    
    def get_provider(self, name: str) -> Optional[DataProvider]:
        """获取指定的数据提供者
        
        Args:
            name: 数据提供者名称
            
        Returns:
            数据提供者实例，如果不存在则返回 None
        """
        return self.providers.get(name)
    
    def get_default_provider(self) -> DataProvider:
        """获取默认数据提供者"""
        return self.default_provider
    
    def set_default_provider(self, name: str):
        """设置默认数据提供者
        
        Args:
            name: 数据提供者名称
        """
        if name in self.providers:
            self.default_provider = self.providers[name]
    
    def get_available_providers(self) -> List[str]:
        """获取所有可用的数据提供者名称列表"""
        return list(self.providers.keys())
    
    def get_provider_info(self) -> str:
        """获取当前数据提供者信息"""
        if self.default_provider:
            return f"当前数据源：BaoStock（前复权）"
        return "未初始化"
    
    def get_historical_data(self, stock_code: str, 
                           provider_name: Optional[str] = None) -> pd.DataFrame:
        """获取历史数据
        
        Args:
            stock_code: 股票代码
            provider_name: 数据提供者名称，如果为 None 则使用默认提供者
            
        Returns:
            历史数据 DataFrame
        """
        if provider_name:
            provider = self.get_provider(provider_name)
            if provider:
                return provider.get_historical_data(stock_code)
        
        return self.default_provider.get_historical_data(stock_code)
    
    def get_current_price(self, stock_code: str,
                         provider_name: Optional[str] = None) -> Optional[float]:
        """获取实时价格
        
        Args:
            stock_code: 股票代码
            provider_name: 数据提供者名称
            
        Returns:
            实时价格
        """
        if provider_name:
            provider = self.get_provider(provider_name)
            if provider:
                return provider.get_current_price(stock_code)
        
        return self.default_provider.get_current_price(stock_code)
    
    def search_stocks(self, keyword: str,
                     provider_name: Optional[str] = None) -> List[Dict]:
        """搜索股票
        
        Args:
            keyword: 搜索关键词
            provider_name: 数据提供者名称
            
        Returns:
            股票列表
        """
        if provider_name:
            provider = self.get_provider(provider_name)
            if provider:
                return provider.search_stocks(keyword)
        
        return self.default_provider.search_stocks(keyword)
    
    def refresh_cache(self, stock_code: str,
                     provider_name: Optional[str] = None):
        """强制刷新缓存
        
        Args:
            stock_code: 股票代码
            provider_name: 数据提供者名称
        """
        if provider_name:
            provider = self.get_provider(provider_name)
            if provider:
                return provider.refresh_cache(stock_code)
        
        return self.default_provider.refresh_cache(stock_code)
    
    def refresh_stock_list_cache(self, provider_name: Optional[str] = None):
        """刷新股票列表缓存
        
        Args:
            provider_name: 数据提供者名称
        """
        if provider_name:
            provider = self.get_provider(provider_name)
            if provider and hasattr(provider, 'refresh_stock_list_cache'):
                return provider.refresh_stock_list_cache()
        
        if self.default_provider and hasattr(self.default_provider, 'refresh_stock_list_cache'):
            return self.default_provider.refresh_stock_list_cache()
        return []


# 创建全局单例
data_source_manager = DataSourceManager()
