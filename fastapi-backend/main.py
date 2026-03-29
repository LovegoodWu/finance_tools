"""
网格策略交易系统 - FastAPI 后端
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import sys

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from grid_trading.data_providers.baostock_provider import BaoStockProvider
from routers import stock_router, strategy_router, transaction_router

app = FastAPI(title="网格策略交易系统 API", version="1.0.0")

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 数据目录
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

# 初始化数据提供者
stock_data_provider = BaoStockProvider(cache_dir=os.path.join(DATA_DIR, "history"))

# 注册路由
app.include_router(stock_router)
app.include_router(strategy_router)
app.include_router(transaction_router)


# 健康检查
@app.get("/api/health")
async def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
