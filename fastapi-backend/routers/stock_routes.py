"""
Stock-related API endpoints
"""

from fastapi import APIRouter, HTTPException
from typing import List, Dict
import json
import os

router = APIRouter(prefix="/api/stocks", tags=["stocks"])

# Data directory
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data")
STOCK_LIST_FILE = os.path.join(DATA_DIR, "stock_list.json")


@router.get("/search")
async def search_stocks(keyword: str) -> Dict:
    """搜索股票"""
    if not keyword:
        return {"code": 0, "message": "success", "data": []}
    
    try:
        with open(STOCK_LIST_FILE, 'r', encoding='utf-8') as f:
            stock_list = json.load(f)
        
        keyword = keyword.lower()
        results = [
            stock for stock in stock_list
            if keyword in stock.get('code', '').lower() or
               keyword in stock.get('name', '').lower()
        ][:20]
        
        return {"code": 0, "message": "success", "data": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/list")
async def get_stock_list() -> Dict:
    """获取所有股票"""
    try:
        with open(STOCK_LIST_FILE, 'r', encoding='utf-8') as f:
            stock_list = json.load(f)
        return {"code": 0, "message": "success", "data": stock_list}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
