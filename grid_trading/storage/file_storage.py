"""
File Storage Module
文件存储模块 - JSON/CSV 文件读写
"""

import json
import csv
import os
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime

from grid_trading.config import STRATEGIES_DIR, TRANSACTIONS_DIR


class FileStorage:
    """JSON/CSV 文件存储"""
    
    def __init__(self, strategies_dir: Optional[Path] = None, 
                 transactions_dir: Optional[Path] = None):
        self.strategies_dir = strategies_dir or STRATEGIES_DIR
        self.transactions_dir = transactions_dir or TRANSACTIONS_DIR
        
        # 确保目录存在
        self.strategies_dir.mkdir(parents=True, exist_ok=True)
        self.transactions_dir.mkdir(parents=True, exist_ok=True)
    
    # ========== 策略管理 ==========
    
    def get_strategy_file(self, stock_code: str) -> Path:
        """获取策略文件路径"""
        return self.strategies_dir / f"{stock_code}.json"
    
    def save_strategy(self, stock_code: str, stock_name: str,
                     grid_config: List[Dict]) -> Dict:
        """保存策略配置（包含计算后的网格数据）"""
        # 计算网格数据
        calculated_grid = self._calculate_grid_metrics(grid_config)
        
        strategy_data = {
            "stock_code": stock_code,
            "stock_name": stock_name,
            "created_at": datetime.now().strftime("%Y-%m-%d"),
            "updated_at": datetime.now().strftime("%Y-%m-%d"),
            "grid_config": grid_config,
            "grid_metrics": calculated_grid
        }
        
        file_path = self.get_strategy_file(stock_code)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(strategy_data, f, ensure_ascii=False, indent=2)
        
        # 创建空交易文件
        self._create_empty_transactions(stock_code)
        
        return strategy_data
    
    def _calculate_grid_metrics(self, grid_config: List[Dict]) -> List[Dict]:
        """计算网格指标：档位、买入金额、卖出金额、资金占用"""
        if not grid_config:
            return []
        
        # 按买入价格从高到低排序
        grid_sorted = sorted(grid_config, key=lambda x: x.get('buy_price', 0), reverse=True)
        
        # 获取第一档的买入价（最高买入价）
        first_buy_price = grid_sorted[0].get('buy_price', 1.0) if grid_sorted else 1.0
        
        calculated = []
        cumulative_buy_amount = 0.0
        
        for level in grid_sorted:
            buy_price = level.get('buy_price', 0)
            buy_qty = level.get('buy_qty', 0)
            sell_price = level.get('sell_price', 0)
            sell_qty = level.get('sell_qty', 0)
            
            # 计算档位
            level_ratio = round(buy_price / first_buy_price, 2) if buy_price and first_buy_price else 0
            
            # 计算买入金额
            buy_amount = round(buy_price * buy_qty, 2) if buy_price and buy_qty else 0
            
            # 计算卖出金额
            sell_amount = round(sell_price * sell_qty, 2) if sell_price and sell_qty else 0
            
            # 累加资金占用
            cumulative_buy_amount += buy_amount
            
            calculated.append({
                'level': level_ratio,
                'buy_price': buy_price,
                'buy_qty': buy_qty,
                'buy_amount': buy_amount,
                'sell_price': sell_price,
                'sell_qty': sell_qty,
                'sell_amount': sell_amount,
                'capital_occupied': round(cumulative_buy_amount, 2)
            })
        
        return calculated
    
    def load_strategy(self, stock_code: str) -> Optional[Dict]:
        """加载策略配置（实时计算 current_price, total_invested, total_return）"""
        from grid_trading.data_providers.baostock_provider import BaoStockProvider
        
        file_path = self.get_strategy_file(stock_code)
        if not file_path.exists():
            return None
        
        with open(file_path, 'r', encoding='utf-8') as f:
            strategy = json.load(f)
        
        # 实时计算当前价格
        provider = BaoStockProvider(cache_dir=str(self.transactions_dir.parent / "history"))
        strategy['current_price'] = provider.get_current_price(stock_code)
        
        # 实时计算总投入和总收益
        transactions = self.load_transactions(stock_code)
        # 当前持仓 = 持仓股数 × 当前价格
        total_shares = sum(
            t['trade_quantity'] 
            for t in transactions 
        )
        current_price = strategy.get('current_price')
        strategy['total_invested'] = total_shares * current_price if current_price and total_shares > 0 else 0
        strategy['total_return'] = sum(
            t.get('profit', 0) or 0 
            for t in transactions 
            if t.get('profit') is not None
        )
        
        return strategy
    
    def update_strategy(self, stock_code: str, **kwargs) -> Optional[Dict]:
        """更新策略配置"""
        strategy = self.load_strategy(stock_code)
        if not strategy:
            return None
        
        strategy.update(kwargs)
        strategy["updated_at"] = datetime.now().strftime("%Y-%m-%d")
        
        with open(self.get_strategy_file(stock_code), 'w', encoding='utf-8') as f:
            json.dump(strategy, f, ensure_ascii=False, indent=2)
        
        return strategy
    
    def delete_strategy(self, stock_code: str) -> bool:
        """删除策略及其交易记录"""
        strategy_file = self.get_strategy_file(stock_code)
        transactions_file = self.transactions_dir / f"{stock_code}.csv"
        
        if strategy_file.exists():
            strategy_file.unlink()
        if transactions_file.exists():
            transactions_file.unlink()
        
        return True
    
    def list_strategies(self) -> List[Dict]:
        """列出所有策略（实时计算 current_price, total_invested, total_return）"""
        from grid_trading.data_providers.baostock_provider import BaoStockProvider
        
        strategies = []
        provider = BaoStockProvider(cache_dir=str(self.transactions_dir.parent / "history"))
        
        for file_path in self.strategies_dir.glob("*.json"):
            with open(file_path, 'r', encoding='utf-8') as f:
                strategy = json.load(f)
            
            # 实时计算当前价格
            stock_code = strategy.get('stock_code')
            if stock_code:
                strategy['current_price'] = provider.get_current_price(stock_code)
            
            # 实时计算总投入和总收益
            transactions = self.load_transactions(stock_code) if stock_code else []
            # 当前持仓 = 持仓股数 × 当前价格
            total_shares = sum(
                t['trade_quantity'] 
                for t in transactions 
            )
            current_price = strategy.get('current_price')
            strategy['total_invested'] = total_shares * current_price if current_price and total_shares > 0 else 0
            strategy['total_return'] = sum(
                t.get('profit', 0) or 0 
                for t in transactions 
                if t.get('profit') is not None
            )
            
            strategies.append(strategy)
        return strategies
    
    # ========== 交易记录管理 ==========
    
    def get_transactions_file(self, stock_code: str) -> Path:
        """获取交易记录文件路径"""
        return self.transactions_dir / f"{stock_code}.csv"
    
    def _create_empty_transactions(self, stock_code: str):
        """创建空交易文件"""
        file_path = self.get_transactions_file(stock_code)
        if not file_path.exists():
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['trade_date', 'trade_price', 'trade_quantity', 
                               'trade_amount', 'profit', 'return_rate', 'notes'])
    
    def add_transaction(self, stock_code: str, trade_date: str, 
                       trade_price: float, trade_quantity: int,
                       trade_amount: float, profit: Optional[float] = None,
                       return_rate: Optional[float] = None,
                       notes: str = "") -> bool:
        """添加交易记录"""
        file_path = self.get_transactions_file(stock_code)
        
        with open(file_path, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                trade_date, trade_price, trade_quantity, 
                trade_amount, profit or "", return_rate or "", notes
            ])
        
        return True
    
    def load_transactions(self, stock_code: str) -> List[Dict]:
        """加载交易记录"""
        file_path = self.get_transactions_file(stock_code)
        if not file_path.exists():
            return []
        
        transactions = []
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                transactions.append({
                    'trade_date': row['trade_date'],
                    'trade_price': float(row['trade_price']),
                    'trade_quantity': int(row['trade_quantity']),
                    'trade_amount': float(row['trade_amount']),
                    'profit': float(row['profit']) if row['profit'] else None,
                    'return_rate': float(row['return_rate']) if row['return_rate'] else None,
                    'notes': row.get('notes', '')
                })
        return transactions
    
    def delete_transaction(self, stock_code: str, index: int) -> bool:
        """删除指定交易记录（按行号）"""
        file_path = self.get_transactions_file(stock_code)
        if not file_path.exists():
            return False
        
        # 读取所有记录
        transactions = self.load_transactions(stock_code)
        if index < 0 or index >= len(transactions):
            return False
        
        # 删除指定记录
        transactions.pop(index)
        
        # 重写文件
        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['trade_date', 'trade_price', 'trade_quantity', 
                           'trade_amount', 'profit', 'return_rate', 'notes'])
            for tx in transactions:
                writer.writerow([
                    tx['trade_date'], tx['trade_price'], tx['trade_quantity'],
                    tx['trade_amount'], tx['profit'] or '', 
                    tx['return_rate'] or '', tx['notes']
                ])
        
        return True
    
    def update_strategy_metrics(self, stock_code: str) -> Optional[Dict]:
        """更新策略的总投入和总收益"""
        strategy = self.load_strategy(stock_code)
        if not strategy:
            return None
        
        transactions = self.load_transactions(stock_code)
        
        # 计算总投入（买入交易金额总和）
        total_invested = sum(
            abs(t['trade_amount']) 
            for t in transactions 
            if t['trade_quantity'] > 0
        )
        
        # 计算总收益（卖出交易收益总和）
        total_return = sum(
            t.get('profit', 0) or 0 
            for t in transactions 
            if t.get('profit') is not None
        )
        
        # 更新策略
        strategy['total_invested'] = total_invested
        strategy['total_return'] = total_return
        
        return self.update_strategy(stock_code,
                                   total_invested=total_invested,
                                   total_return=total_return)
    
    def save_transactions(self, stock_code: str, transactions: List[Dict]) -> bool:
        """保存交易记录列表到文件"""
        file_path = self.get_transactions_file(stock_code)
        
        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['trade_date', 'trade_price', 'trade_quantity',
                            'trade_amount', 'profit', 'return_rate', 'notes'])
            for tx in transactions:
                writer.writerow([
                    tx['trade_date'], tx['trade_price'], tx['trade_quantity'],
                    tx['trade_amount'], tx.get('profit', '') or '',
                    tx.get('return_rate', '') or '', tx.get('notes', '')
                ])
        
        return True
