# 配置文件

import os
from pathlib import Path

# 基础目录
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR.parent / "data"

# 数据目录
STRATEGIES_DIR = DATA_DIR / "strategies"
TRANSACTIONS_DIR = DATA_DIR / "transactions"
HISTORY_DIR = DATA_DIR / "history"

# 确保目录存在
STRATEGIES_DIR.mkdir(parents=True, exist_ok=True)
TRANSACTIONS_DIR.mkdir(parents=True, exist_ok=True)
HISTORY_DIR.mkdir(parents=True, exist_ok=True)

# 应用配置
APP_TITLE = "交易策略管理系统"
APP_VERSION = "1.0.0"
