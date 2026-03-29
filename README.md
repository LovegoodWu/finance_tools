# Finance Tools - 金融数据分析工具

一个基于 Python 的金融数据分析和网格交易系统。

**虚拟环境名称**: `financetools_env`

## 项目结构

```
finance_tools/
├── fastapi-backend/       # FastAPI 后端服务
├── grid_trading/          # 网格交易模块
├── vue-frontend/          # Vue.js 前端
├── docs/                  # 文档
├── tests/                 # 测试脚本
│   └── test_amazingdata_etf.py
├── data/                  # 数据目录
└── ...
```

## 功能特性

- **金融数据获取**: 支持 AmazingData、Baostock 等数据源
- **网格交易策略**: 自动化网格交易系统
- **策略管理**: 创建、编辑和回测交易策略
- **数据可视化**: Web 界面展示策略和交易数据

## 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/YOUR_USERNAME/finance_tools.git
cd finance_tools
```

### 2. 创建虚拟环境

```bash
# macOS/Linux
python3 -m venv financetools_env
source financetools_env/bin/activate

# Windows PowerShell
python -m venv financetools_env
.\financetools_env\Scripts\Activate.ps1
```

如果 PowerShell 提示执行策略错误：
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 3. 安装依赖

```bash
# 升级 pip
python -m pip install --upgrade pip

# 安装依赖
pip install -r requirements.txt
pip install pydantic tgw

# 安装 AmazingData（需要 wheel 文件）
pip install AmazingData-0.0.6-py3-none-any.whl
```

### 4. 运行测试

```bash
# AmazingData ETF 数据测试
python tests/test_amazingdata_etf.py
```

### 5. 启动后端服务

```bash
cd fastapi-backend
python -m uvicorn main:app --reload --port 8000
```

### 6. 启动前端服务

```bash
cd vue-frontend
npm install
npm run dev
```

## 文档

- [GitHub 和 Windows 开发环境配置](docs/GITHUB_WINDOWS_SETUP.md)
- [AmazingData SDK 介绍](docs/amazingData/SDK 的介绍、安装和登录.md)
- [Baostock 文档](docs/baoStock/)

## 开发环境

- Python 3.8+
- Node.js 16+
- FastAPI
- Vue.js 3

## License

MIT
