"""
BaoStock Data Provider
BaoStock 数据提供者 - 用于 A 股历史数据
"""

import baostock as bs
import pandas as pd
from typing import List, Dict, Optional
from datetime import datetime
import os
import json
import streamlit as st

from grid_trading.data_providers.base import DataProvider
from grid_trading.config import HISTORY_DIR, DATA_DIR


class BaoStockProvider(DataProvider):
    """BaoStock 数据提供者"""
    
    def __init__(self, cache_dir: str = None):
        """初始化数据提供者
        
        Args:
            cache_dir: 历史数据缓存目录
        """
        self.cache_dir = str(cache_dir) if cache_dir else str(HISTORY_DIR)
        os.makedirs(self.cache_dir, exist_ok=True)
        self._login()
    
    def _login(self):
        """登录 BaoStock"""
        try:
            bs.login()
        except Exception as e:
            print(f"BaoStock 登录失败：{e}")
    
    def __del__(self):
        """登出 BaoStock"""
        try:
            bs.logout()
        except:
            pass
    
    @property
    def name(self) -> str:
        return "BaoStock"
    
    def _get_cache_path(self, stock_code: str) -> str:
        """获取缓存文件路径"""
        return os.path.join(self.cache_dir, f"{stock_code}_baostock.csv")
    
    def _load_from_cache(self, stock_code: str) -> Optional[pd.DataFrame]:
        """从缓存加载数据"""
        cache_path = self._get_cache_path(stock_code)
        if os.path.exists(cache_path):
            df = pd.read_csv(cache_path, parse_dates=['date'])
            return df
        return None
    
    def _save_to_cache(self, stock_code: str, df: pd.DataFrame):
        """保存数据到缓存"""
        cache_path = self._get_cache_path(stock_code)
        df.to_csv(cache_path, index=False)
    
    def _normalize_stock_code(self, stock_code: str) -> str:
        """转换股票代码格式以适配 BaoStock
        
        BaoStock 股票代码格式：市场代码。证券代码（共 9 位）
        - sh.600000 - 沪市 A 股
        - sz.000001 - 深市 A 股
        - sh.510000 - 沪市 ETF
        - sz.159938 - 深市 ETF
        """
        # BaoStock 需要市场前缀
        if stock_code.startswith('6') or stock_code.startswith('5'):
            # 沪市：6 开头 A 股，5 开头 ETF/基金
            return f"sh.{stock_code}"
        elif stock_code.startswith(('0', '3', '1')):
            # 深市：0/3 开头 A 股，1 开头 ETF
            return f"sz.{stock_code}"
        return stock_code
    
    def get_historical_data(self, stock_code: str) -> pd.DataFrame:
        """获取历史数据（带缓存）"""
        # 尝试从缓存加载
        cached_df = self._load_from_cache(stock_code)
        
        if cached_df is not None:
            # 检查是否需要更新（只获取当天数据）
            last_date = cached_df['date'].max()
            today = datetime.now().date()
            
            if last_date.date() >= today:
                # 数据已更新到今天，直接返回
                return cached_df
            else:
                # 需要增量更新
                return self._update_historical_data(stock_code, cached_df, last_date)
        
        # 缓存不存在，获取全部数据
        return self._fetch_historical_data(stock_code)
    
    def _fetch_historical_data(self, stock_code: str) -> pd.DataFrame:
        """获取历史数据（从 BaoStock）"""
        try:
            # 转换股票代码格式
            normalized_code = self._normalize_stock_code(stock_code)
            
            # 查询历史数据
            # adjustflag: 1-后复权，2-前复权，3-不复权
            rs = bs.query_history_k_data_plus(
                normalized_code,
                "date,open,high,low,close,volume,amount",
                start_date='2000-01-01',
                end_date=datetime.now().strftime('%Y-%m-%d'),
                frequency="d",
                adjustflag="2"  # 前复权
            )
            
            # 转换为 DataFrame
            data_list = []
            while (rs.error_code == '0') and rs.next():
                data_list.append(rs.get_row_data())
            
            if data_list:
                df = pd.DataFrame(data_list, columns=rs.fields)
                
                # 数据清洗和类型转换
                df['date'] = pd.to_datetime(df['date'])
                df['open'] = pd.to_numeric(df['open'], errors='coerce')
                df['high'] = pd.to_numeric(df['high'], errors='coerce')
                df['low'] = pd.to_numeric(df['low'], errors='coerce')
                df['close'] = pd.to_numeric(df['close'], errors='coerce')
                df['volume'] = pd.to_numeric(df['volume'], errors='coerce')
                
                # 保存到缓存
                self._save_to_cache(stock_code, df)
                
                return df[["date", "open", "high", "low", "close", "volume"]]
                
        except Exception as e:
            print(f"BaoStock 获取历史数据失败：{e}")
        
        return pd.DataFrame()
    
    def _update_historical_data(self, stock_code: str, cached_df: pd.DataFrame,
                                 last_date: datetime) -> pd.DataFrame:
        """增量更新历史数据"""
        try:
            normalized_code = self._normalize_stock_code(stock_code)
            
            # 只获取从最后更新日期到今天的数据
            start_date = (last_date + pd.Timedelta(days=1)).strftime('%Y-%m-%d')
            
            rs = bs.query_history_k_data_plus(
                normalized_code,
                "date,open,high,low,close,volume,amount",
                start_date=start_date,
                end_date=datetime.now().strftime('%Y-%m-%d'),
                frequency="d",
                adjustflag="2"  # 前复权
            )
            
            # 转换为 DataFrame
            data_list = []
            while (rs.error_code == '0') and rs.next():
                data_list.append(rs.get_row_data())
            
            if data_list:
                new_data = pd.DataFrame(data_list, columns=rs.fields)
                
                # 数据清洗和类型转换
                new_data['date'] = pd.to_datetime(new_data['date'])
                new_data['open'] = pd.to_numeric(new_data['open'], errors='coerce')
                new_data['high'] = pd.to_numeric(new_data['high'], errors='coerce')
                new_data['low'] = pd.to_numeric(new_data['low'], errors='coerce')
                new_data['close'] = pd.to_numeric(new_data['close'], errors='coerce')
                new_data['volume'] = pd.to_numeric(new_data['volume'], errors='coerce')
                
                # 合并数据
                updated_df = pd.concat([cached_df, new_data], ignore_index=True)
                
                # 保存到缓存
                self._save_to_cache(stock_code, updated_df)
                
                return updated_df
            
            return cached_df
            
        except Exception as e:
            print(f"BaoStock 增量更新失败：{e}")
            return cached_df
    
    def get_current_price(self, stock_code: str) -> Optional[float]:
        """获取实时价格（BaoStock 不支持实时数据，返回最近收盘价）"""
        try:
            df = self.get_historical_data(stock_code)
            if not df.empty:
                return float(df.iloc[-1]['close'])
        except Exception as e:
            print(f"获取当前价格失败：{e}")
        
        return None
    
    def _get_stock_list_cache_path(self) -> str:
        """获取股票列表缓存文件路径"""
        return os.path.join(DATA_DIR, "stock_list.json")
    
    def _load_stock_list_from_cache(self) -> List[Dict]:
        """从缓存加载股票列表"""
        cache_path = self._get_stock_list_cache_path()
        if os.path.exists(cache_path):
            try:
                with open(cache_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return []
    
    def _save_stock_list_to_cache(self, stock_list: List[Dict]):
        """保存股票列表到缓存"""
        cache_path = self._get_stock_list_cache_path()
        try:
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump(stock_list, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存股票列表缓存失败：{e}")
    
    def _fetch_stock_list(self) -> List[Dict]:
        """从 BaoStock 获取股票列表"""
        results = []
        try:
            # 获取 A 股股票列表
            rs = bs.query_stock_basic()
            if rs.error_code == '0':
                while (rs.error_code == '0') and rs.next():
                    row = rs.get_row_data()
                    if row and len(row) >= 2:
                        code = row[0]
                        name = row[1] if len(row) > 1 else ''
                        # 提取市场代码
                        if '.' in code:
                            market, stock_code = code.split('.')
                            market = market.upper()
                            results.append({
                                'code': stock_code,
                                'name': name,
                                'market': market
                            })
        except Exception as e:
            print(f"获取股票列表失败：{e}")
        return results
    
    def search_stocks(self, keyword: str) -> List[Dict]:
        """
        搜索股票
        支持根据代码或名称搜索，优先从本地缓存搜索
        """
        results = []
        keyword = keyword.strip()
        
        # 从本地缓存加载股票列表
        stock_list = self._load_stock_list_from_cache()
        
        # 如果缓存为空，尝试从 BaoStock 获取
        if not stock_list:
            stock_list = self._fetch_stock_list()
            if stock_list:
                self._save_stock_list_to_cache(stock_list)
        
        # 在缓存中搜索
        if stock_list:
            if keyword.isdigit() and len(keyword) == 6:
                # 按代码搜索
                for stock in stock_list:
                    if stock['code'] == keyword:
                        results.append(stock)
            elif keyword:
                # 按名称搜索（支持模糊匹配）
                for stock in stock_list:
                    if keyword.lower() in stock['name'].lower():
                        results.append(stock)
        
        return results
    
    def refresh_cache(self, stock_code: str):
        """强制刷新缓存"""
        cache_path = self._get_cache_path(stock_code)
        if os.path.exists(cache_path):
            os.remove(cache_path)
        return self._fetch_historical_data(stock_code)
    
    def refresh_stock_list_cache(self):
        """刷新股票列表缓存"""
        stock_list = self._fetch_stock_list()
        if stock_list:
            self._save_stock_list_to_cache(stock_list)
        return stock_list
