"""
Transaction-related API endpoints
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
import os

router = APIRouter(prefix="/api/strategies/{stock_code}/transactions", tags=["transactions"])

# Data directory
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data")
TRANSACTIONS_DIR = os.path.join(DATA_DIR, "transactions")


class TransactionRequest(BaseModel):
    trade_date: str
    trade_price: float
    trade_quantity: float
    trade_amount: float
    profit: Optional[float] = None
    return_rate: Optional[float] = None
    notes: Optional[str] = None


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


@router.get("")
async def get_transactions(stock_code: str) -> Dict:
    """获取交易记录"""
    try:
        transactions = get_transactions_for_strategy(stock_code)
        return {"code": 0, "message": "success", "data": transactions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("")
async def add_transaction(stock_code: str, request: TransactionRequest) -> Dict:
    """添加交易记录"""
    try:
        os.makedirs(TRANSACTIONS_DIR, exist_ok=True)
        filepath = os.path.join(TRANSACTIONS_DIR, f"{stock_code}.csv")
        
        write_header = not os.path.exists(filepath)
        
        with open(filepath, 'a', encoding='utf-8') as f:
            if write_header:
                f.write("trade_date,trade_price,trade_quantity,trade_amount,profit,return_rate,notes\n")
            
            f.write(f"{request.trade_date},{request.trade_price},{request.trade_quantity},"
                   f"{request.trade_amount},{request.profit or ''},{request.return_rate or ''},"
                   f"{request.notes or ''}\n")
        
        return {"code": 0, "message": "success", "data": None}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/last")
async def delete_last_transaction(stock_code: str) -> Dict:
    """删除最后一条交易记录"""
    try:
        filepath = os.path.join(TRANSACTIONS_DIR, f"{stock_code}.csv")
        if not os.path.exists(filepath):
            return {"code": 0, "message": "success", "data": None}
        
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        if len(lines) > 1:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.writelines(lines[:-1])
        
        return {"code": 0, "message": "success", "data": None}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
