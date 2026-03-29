"""
Strategy-related API endpoints
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime
import os
import sys
import json
from dataclasses import dataclass

# Add project root to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from grid_trading.data_providers.baostock_provider import BaoStockProvider

router = APIRouter(prefix="/api/strategies", tags=["strategies"])

# Data directory
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data")
STRATEGIES_DIR = os.path.join(DATA_DIR, "strategies")
TRANSACTIONS_DIR = os.path.join(DATA_DIR, "transactions")

# Initialize data provider
stock_data_provider = BaoStockProvider(cache_dir=os.path.join(DATA_DIR, "history"))


class GridLevel(BaseModel):
    buy_price: str
    buy_qty: str
    sell_price: str
    sell_qty: str


class CreateStrategyRequest(BaseModel):
    stock_code: str
    stock_name: str
    grid_config: List[GridLevel]


def get_stock_current_price(stock_code: str) -> Optional[float]:
    """获取股票当前价格（使用最近收盘价）"""
    try:
        return stock_data_provider.get_current_price(stock_code)
    except Exception as e:
        print(f"获取当前价格失败：{e}")
        return None


def get_stock_kline_data(stock_code: str) -> List[Dict]:
    """获取股票 K 线数据"""
    try:
        df = stock_data_provider.get_historical_data(stock_code)
        if df.empty:
            return []
        
        kline_data = []
        for _, row in df.iterrows():
            kline_data.append({
                'date': row['date'].strftime('%Y-%m-%d') if hasattr(row['date'], 'strftime') else str(row['date']),
                'open': float(row['open']),
                'high': float(row['high']),
                'low': float(row['low']),
                'close': float(row['close']),
                'volume': float(row['volume'])
            })
        return kline_data
    except Exception as e:
        print(f"获取 K 线数据失败：{e}")
        return []


def get_transactions_for_strategy(stock_code: str) -> List[Dict]:
    """获取策略的交易记录"""
    filepath = os.path.join(TRANSACTIONS_DIR, f"{stock_code}.csv")
    if not os.path.exists(filepath):
        return []
    
    transactions = []
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        if len(lines) > 1:
            for line in lines[1:]:
                parts = line.strip().split(',')
                if len(parts) >= 6:
                    transactions.append({
                        'trade_date': parts[0],
                        'trade_price': float(parts[1]),
                        'trade_quantity': float(parts[2]),
                        'trade_amount': float(parts[3]) if parts[3] else 0,
                        'profit': float(parts[4]) if len(parts) > 4 and parts[4] else None,
                        'return_rate': float(parts[5]) if len(parts) > 5 and parts[5] else None,
                        'notes': parts[6] if len(parts) > 6 else ''
                    })
    return transactions


def calculate_grid_metrics(grid_config: List[Dict]) -> List[Dict]:
    """计算网格指标"""
    if not grid_config:
        return []
    
    def to_float(val):
        """安全地将值转换为浮点数，处理空字符串和 None"""
        if val is None or val == '':
            return 0.0
        try:
            result = float(val)
            return result if result > 0 else 0.0
        except (ValueError, TypeError):
            return 0.0
    
    def to_int(val):
        """安全地将值转换为整数，处理空字符串和 None"""
        if val is None or val == '':
            return 0
        try:
            return int(float(val))
        except (ValueError, TypeError):
            return 0
    
    grid_sorted = sorted(grid_config, key=lambda x: to_float(x.get('buy_price', 0)), reverse=True)
    first_buy_price = to_float(grid_sorted[0].get('buy_price', 1.0)) if grid_sorted else 1.0
    
    calculated = []
    cumulative_buy_amount = 0.0
    
    for level in grid_sorted:
        buy_price = to_float(level.get('buy_price', 0))
        buy_qty = to_int(level.get('buy_qty', 0))
        sell_price = to_float(level.get('sell_price', 0))
        sell_qty = to_int(level.get('sell_qty', 0))
        
        level_ratio = round(buy_price / first_buy_price, 2) if buy_price and first_buy_price else 0
        buy_amount = round(buy_price * buy_qty, 2) if buy_price and buy_qty else 0
        sell_amount = round(sell_price * sell_qty, 2) if sell_price and sell_qty else 0
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


def calculate_distance_to_grid_levels(strategy, current_price, transactions):
    """
    计算当前价格距离当前挂的买入档和卖出档的百分比
    逻辑：
    - 如果最近一次交易是卖出：当前挂的买入档是该卖出对应的买入价，当前挂的卖出档是上一档卖出价
    - 如果最近一次交易是买入：当前挂的买入档是下一档买入价，当前挂的卖出档是该买入对应的卖出价
    - 如果没有交易记录：当前挂的买入档是最高档买入价，当前挂的卖出档是最高档对应的卖出价
    """
    grid_config = strategy.get('grid_config', [])
    if not grid_config or current_price is None:
        return None, None
    
    def to_float(val):
        """安全地将值转换为浮点数，处理空字符串和 None"""
        if val is None or val == '':
            return 0.0
        try:
            result = float(val)
            return result if result > 0 else 0.0
        except (ValueError, TypeError):
            return 0.0
    
    def to_int(val):
        """安全地将值转换为整数，处理空字符串和 None"""
        if val is None or val == '':
            return 0
        try:
            return int(float(val))
        except (ValueError, TypeError):
            return 0
    
    # 将网格配置按买入价从高到低排序
    grid_sorted = sorted(grid_config, key=lambda x: to_float(x.get('buy_price', 0)), reverse=True)
    
    # 获取所有买入价和卖出价（已排序）
    buy_prices = [to_float(g.get('buy_price')) for g in grid_sorted if to_float(g.get('buy_price')) > 0]
    sell_prices = [to_float(g.get('sell_price')) for g in grid_sorted if to_float(g.get('sell_price')) > 0]
    
    current_pending_buy_price = None
    current_pending_sell_price = None
    
    if not transactions:
        # 没有交易记录时，当前挂的买入档是最高档买入价，卖出档是最高档对应的卖出价
        if grid_sorted:
            first_grid = grid_sorted[0]
            current_pending_buy_price = to_float(first_grid.get('buy_price'))
            current_pending_sell_price = to_float(first_grid.get('sell_price'))
    else:
        # 获取最近一次交易
        last_transaction = transactions[-1]
        last_trade_price = last_transaction['trade_price']
        last_trade_qty = last_transaction['trade_quantity']
        
        if last_trade_qty < 0:
            # 最近一次是卖出
            # 找到卖出的档位（卖出价对应的网格）
            sell_grid = None
            for grid in grid_sorted:
                if abs(to_float(grid.get('sell_price')) - last_trade_price) < 0.001:
                    sell_grid = grid
                    break
            
            if sell_grid:
                # 当前挂的买入档：该笔卖出对应的买入档位
                current_pending_buy_price = to_float(sell_grid.get('buy_price'))
                
                # 当前挂的卖出档：该笔卖出上一档卖出档位（更高一档的卖出价）
                sell_price = to_float(sell_grid.get('sell_price'))
                higher_sell_prices = [p for p in sell_prices if p > sell_price]
                if higher_sell_prices:
                    current_pending_sell_price = min(higher_sell_prices)
                else:
                    current_pending_sell_price = sell_price
        else:
            # 最近一次是买入
            # 找到该买入价格对应的网格档位
            buy_grid = None
            for grid in grid_sorted:
                if abs(to_float(grid.get('buy_price')) - last_trade_price) < 0.001:
                    buy_grid = grid
                    break
            
            if buy_grid:
                # 当前挂的买入档：该买入档位的下一个买入档位（更低的买入价）
                current_buy_price = to_float(buy_grid.get('buy_price'))
                lower_buy_prices = [p for p in buy_prices if p < current_buy_price]
                if lower_buy_prices:
                    current_pending_buy_price = max(lower_buy_prices)
                
                # 当前挂的卖出档：该笔买入档位对应的卖出档位
                current_pending_sell_price = to_float(buy_grid.get('sell_price'))
    
    # 计算距离百分比
    distance_to_upper = None
    if current_pending_sell_price and current_pending_sell_price > current_price:
        distance_to_upper = ((current_pending_sell_price - current_price) / current_price) * 100
    
    distance_to_lower = None
    if current_pending_buy_price and current_pending_buy_price < current_price:
        distance_to_lower = -((current_price - current_pending_buy_price) / current_price) * 100
    
    return distance_to_upper, distance_to_lower


def calculate_pending_orders(strategy, transactions):
    """
    计算挂单提示
    返回应该挂的条件买单和条件卖单
    
    逻辑：
    - 如果最近一次交易是卖出：挂该笔卖出对应的买入档位，和该笔卖出上一档卖出档位
    - 如果最近一次交易是买入：挂该买入档位的下一个买入档位，和该笔买入档位对应的卖出档位
    """
    grid_config = strategy.get('grid_config', [])
    if not grid_config:
        return [], []
    
    # 将网格配置按买入价从高到低排序
    def to_float(val):
        """安全地将值转换为浮点数，处理空字符串和 None"""
        if val is None or val == '':
            return 0.0
        try:
            result = float(val)
            return result if result > 0 else 0.0
        except (ValueError, TypeError):
            return 0.0
    
    def to_int(val):
        """安全地将值转换为整数，处理空字符串和 None"""
        if val is None or val == '':
            return 0
        try:
            return int(float(val))
        except (ValueError, TypeError):
            return 0
    
    grid_sorted = sorted(grid_config, key=lambda x: to_float(x.get('buy_price', 0)), reverse=True)
    
    # 构建买入价到网格档位的映射
    buy_price_to_grid = {}
    sell_price_to_grid = {}
    for grid in grid_sorted:
        buy_price = to_float(grid.get('buy_price'))
        sell_price = to_float(grid.get('sell_price'))
        if buy_price > 0:
            buy_price_to_grid[buy_price] = grid
        if sell_price > 0:
            sell_price_to_grid[sell_price] = grid
    
    # 获取所有买入价和卖出价（已排序）
    buy_prices = [to_float(g.get('buy_price')) for g in grid_sorted if to_float(g.get('buy_price')) > 0]
    sell_prices = [to_float(g.get('sell_price')) for g in grid_sorted if to_float(g.get('sell_price')) > 0]
    
    pending_buy_orders = []
    pending_sell_orders = []
    
    if not transactions:
        # 没有交易记录时，挂最高档的买入单和对应的卖出单
        if grid_sorted:
            first_grid = grid_sorted[0]
            buy_price = to_float(first_grid.get('buy_price'))
            sell_price = to_float(first_grid.get('sell_price'))
            buy_qty = to_int(first_grid.get('buy_qty', 0))
            sell_qty = to_int(first_grid.get('sell_qty', 0))
            
            if buy_price > 0:
                pending_buy_orders.append({
                    'buy_price': buy_price,
                    'buy_qty': buy_qty,
                    'level': buy_price
                })
            if sell_price > 0:
                pending_sell_orders.append({
                    'sell_price': sell_price,
                    'sell_qty': sell_qty,
                    'level': buy_price  # 用买入价作为档位标识
                })
        return pending_buy_orders, pending_sell_orders
    
    # 获取最近一次交易
    last_transaction = transactions[-1]
    last_trade_price = last_transaction['trade_price']
    last_trade_qty = last_transaction['trade_quantity']
    
    if last_trade_qty < 0:
        # 最近一次是卖出
        # 找到该卖出价格对应的买入档位（卖出价通常等于上一档的买入价）
        # 或者找到最接近卖出价格的买入档位
        
        # 找到卖出的档位（卖出价对应的网格）
        sell_grid = None
        for grid in grid_sorted:
            if abs(to_float(grid.get('sell_price')) - last_trade_price) < 0.001:
                sell_grid = grid
                break
        
        if sell_grid:
            # 1. 该笔卖出对应的买入档位：即这个网格的买入价
            buy_price = to_float(sell_grid.get('buy_price'))
            buy_qty = to_int(sell_grid.get('buy_qty', 0))
            if buy_price > 0:
                pending_buy_orders.append({
                    'buy_price': buy_price,
                    'buy_qty': buy_qty,
                    'level': buy_price
                })
            
            # 2. 该笔卖出上一档卖出档位：即更高一档的卖出价
            sell_price = to_float(sell_grid.get('sell_price'))
            # 找到比当前卖出价更高的卖出价
            higher_sell_prices = [p for p in sell_prices if p > sell_price]
            if higher_sell_prices:
                next_sell_price = min(higher_sell_prices)
                # 找到这个卖出价对应的网格
                for grid in grid_sorted:
                    if abs(to_float(grid.get('sell_price')) - next_sell_price) < 0.001:
                        sell_qty = to_int(grid.get('sell_qty', 0))
                        pending_sell_orders.append({
                            'sell_price': next_sell_price,
                            'sell_qty': sell_qty,
                            'level': to_float(grid.get('buy_price'))
                        })
                        break
            else:
                # 没有更高档的卖出价，使用当前网格的卖出价
                sell_qty = to_int(sell_grid.get('sell_qty', 0))
                pending_sell_orders.append({
                    'sell_price': sell_price,
                    'sell_qty': sell_qty,
                    'level': buy_price
                })
    else:
        # 最近一次是买入
        # 找到该买入价格对应的网格档位
        buy_grid = None
        for grid in grid_sorted:
            if abs(to_float(grid.get('buy_price')) - last_trade_price) < 0.001:
                buy_grid = grid
                break
        
        if buy_grid:
            # 1. 该买入档位的下一个买入档位（更低的买入价）
            current_buy_price = to_float(buy_grid.get('buy_price'))
            lower_buy_prices = [p for p in buy_prices if p < current_buy_price]
            if lower_buy_prices:
                next_buy_price = max(lower_buy_prices)
                # 找到这个买入价对应的网格
                for grid in grid_sorted:
                    if abs(to_float(grid.get('buy_price')) - next_buy_price) < 0.001:
                        buy_qty = to_int(grid.get('buy_qty', 0))
                        pending_buy_orders.append({
                            'buy_price': next_buy_price,
                            'buy_qty': buy_qty,
                            'level': next_buy_price
                        })
                        break
            
            # 2. 该笔买入档位对应的卖出档位
            sell_price = to_float(buy_grid.get('sell_price'))
            sell_qty = to_int(buy_grid.get('sell_qty', 0))
            if sell_price > 0:
                pending_sell_orders.append({
                    'sell_price': sell_price,
                    'sell_qty': sell_qty,
                    'level': current_buy_price
                })
    
    return pending_buy_orders, pending_sell_orders


@router.get("")
async def get_strategies() -> Dict:
    """获取所有策略"""
    try:
        if not os.path.exists(STRATEGIES_DIR):
            return {"code": 0, "message": "success", "data": []}
        
        strategies = []
        for filename in os.listdir(STRATEGIES_DIR):
            if filename.endswith('.json') and not filename.startswith('.'):
                filepath = os.path.join(STRATEGIES_DIR, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    strategy = json.load(f)
                    
                    transactions = get_transactions_for_strategy(strategy['stock_code'])
                    current_price = get_stock_current_price(strategy['stock_code'])
                    strategy['current_price'] = current_price
                    
                    total_cost = sum(abs(t['trade_amount']) for t in transactions if t['trade_quantity'] > 0)
                    position_shares = sum(t['trade_quantity'] for t in transactions)
                    position_value = (current_price * position_shares) if current_price else 0
                    total_profit = position_value - total_cost
                    return_rate = (total_profit / total_cost * 100) if total_cost > 0 else 0
                    transaction_count = len(transactions)
                    
                    dist_upper, dist_lower = calculate_distance_to_grid_levels(strategy, current_price, transactions)
                    
                    strategy['position'] = position_value
                    strategy['total_cost'] = total_cost
                    strategy['total_profit'] = total_profit
                    strategy['return_rate'] = return_rate
                    strategy['transaction_count'] = transaction_count
                    strategy['distance_up'] = dist_upper
                    strategy['distance_down'] = dist_lower
                    
                    strategies.append(strategy)
        
        return {"code": 0, "message": "success", "data": strategies}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{stock_code}")
async def get_strategy(stock_code: str) -> Dict:
    """获取策略详情"""
    try:
        filepath = os.path.join(STRATEGIES_DIR, f"{stock_code}.json")
        if not os.path.exists(filepath):
            raise HTTPException(status_code=404, detail="策略不存在")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            strategy = json.load(f)
        
        transactions = get_transactions_for_strategy(stock_code)
        current_price = get_stock_current_price(stock_code)
        strategy['current_price'] = current_price
        
        total_cost = sum(abs(t['trade_amount']) for t in transactions if t['trade_quantity'] > 0)
        position_shares = sum(t['trade_quantity'] for t in transactions)
        position_value = (current_price * position_shares) if current_price else 0
        total_profit = position_value - total_cost
        return_rate = (total_profit / total_cost * 100) if total_cost > 0 else 0
        transaction_count = len(transactions)
        
        strategy['grid_metrics'] = calculate_grid_metrics(strategy.get('grid_config', []))
        strategy['position'] = position_value
        strategy['total_cost'] = total_cost
        strategy['total_profit'] = total_profit
        strategy['return_rate'] = return_rate
        strategy['transaction_count'] = transaction_count
        strategy['transactions'] = transactions
        
        dist_upper, dist_lower = calculate_distance_to_grid_levels(strategy, current_price, transactions)
        strategy['distance_up'] = dist_upper
        strategy['distance_down'] = dist_lower
        strategy['kline_data'] = get_stock_kline_data(stock_code)
        
        # 计算挂单提示
        pending_buy_orders, pending_sell_orders = calculate_pending_orders(strategy, transactions)
        strategy['pending_buy_orders'] = pending_buy_orders
        strategy['pending_sell_orders'] = pending_sell_orders
        
        return {"code": 0, "message": "success", "data": strategy}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("")
async def create_strategy(request: CreateStrategyRequest) -> Dict:
    """创建新策略"""
    try:
        os.makedirs(STRATEGIES_DIR, exist_ok=True)
        
        strategy = {
            "stock_code": request.stock_code,
            "stock_name": request.stock_name,
            "grid_config": [level.model_dump() for level in request.grid_config],
            "created_at": datetime.now().strftime("%Y-%m-%d")
        }
        
        filepath = os.path.join(STRATEGIES_DIR, f"{request.stock_code}.json")
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(strategy, f, ensure_ascii=False, indent=2)
        
        strategy['position'] = 0
        strategy['total_cost'] = 0
        strategy['total_profit'] = 0
        strategy['return_rate'] = 0
        strategy['transaction_count'] = 0
        strategy['grid_metrics'] = calculate_grid_metrics([level.model_dump() for level in request.grid_config])
        
        return {"code": 0, "message": "success", "data": strategy}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{stock_code}")
async def delete_strategy(stock_code: str) -> Dict:
    """删除策略"""
    try:
        filepath = os.path.join(STRATEGIES_DIR, f"{stock_code}.json")
        if not os.path.exists(filepath):
            raise HTTPException(status_code=404, detail="策略不存在")
        
        os.remove(filepath)
        return {"code": 0, "message": "success", "data": None}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
