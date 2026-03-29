# GitHub 和 Windows 开发环境配置指南

本文档说明如何将项目上传到 GitHub，并在 Windows 电脑上配置开发环境。

---

## 第一部分：上传项目到 GitHub

### 步骤 1: 创建 GitHub 仓库

1. 登录 [GitHub](https://github.com)
2. 点击右上角的 "+" 按钮，选择 "New repository"
3. 填写仓库信息：
   - **Repository name**: 例如 `finance_tools`
   - **Description**: 例如 "金融数据分析和交易工具"
   - **Visibility**: 选择 Private（私有）或 Public（公开）
   - **不要** 勾选 "Initialize this repository with a README"
4. 点击 "Create repository"

### 步骤 2: 在本地初始化 Git 仓库

```bash
# 进入项目目录
cd /Users/harry/PycharmProjects/finance_tools

# 初始化 Git 仓库
git init

# 添加所有文件
git add .

# 或者只添加特定文件（推荐）
git add *.py *.md requirements.txt
git add fastapi-backend/
git add grid_trading/
git add docs/
git add data/
git add vue-frontend/

# 提交
git commit -m "Initial commit: finance tools project"

# 关联远程仓库（替换 YOUR_USERNAME 为你的 GitHub 用户名）
git remote add origin https://github.com/YOUR_USERNAME/finance_tools.git

# 推送到 GitHub
git branch -M main
git push -u origin main
```

### 步骤 3: 创建 .gitignore 文件（重要）

在项目根目录创建 `.gitignore` 文件，排除不需要上传的文件：

```bash
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
.venv/
venv/
financetools_env/
ENV/
env/
*.egg-info/
dist/
build/

# IDE
.idea/
.vscode/
*.swp
*.swo
*~

# 敏感信息
.env
*.key
*.pem
config.local.py
secrets.json

# 数据文件（可选，如果数据敏感）
data/*.json
data/history/*.csv
data/strategies/*.json
data/transactions/*.csv

# 日志
*.log

# OS
.DS_Store
Thumbs.db
```

### 步骤 4: 重新提交

```bash
# 添加 .gitignore
git add .gitignore

# 重新提交
git commit -m "Add .gitignore file"

# 推送
git push origin main
```

---

## 第二部分：在 Windows 电脑上配置开发环境

### 步骤 1: 安装必要软件

1. **安装 Python**
   - 下载 [Python 3.8+](https://www.python.org/downloads/)
   - 安装时勾选 "Add Python to PATH"

2. **安装 Git**
   - 下载 [Git for Windows](https://git-scm.com/download/win)
   - 使用默认设置安装

3. **安装 VSCode（可选）**
   - 下载 [VSCode](https://code.visualstudio.com/)
   - 安装 Python 和 Git 扩展

### 步骤 2: 克隆项目

```bash
# 打开 PowerShell 或 Git Bash

# 创建项目目录
mkdir C:\Projects
cd C:\Projects

# 克隆仓库（替换 YOUR_USERNAME）
git clone https://github.com/YOUR_USERNAME/finance_tools.git

# 进入项目目录
cd finance_tools
```

### 步骤 3: 创建虚拟环境

```bash
# 在 PowerShell 中
python -m venv amazingdata_env

# 激活虚拟环境
# PowerShell:
.\amazingdata_env\Scripts\Activate.ps1

# 或者使用 CMD:
amazingdata_env\Scripts\activate.bat

# 激活后，命令行前会显示 (amazingdata_env)
```

如果 PowerShell 执行策略限制，运行：
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 步骤 4: 安装依赖

```bash
# 确保虚拟环境已激活

# 升级 pip
python -m pip install --upgrade pip

# 安装项目依赖
pip install -r requirements.txt

# 安装 AmazingData 相关依赖
pip install pydantic tgw

# 安装 AmazingData（需要 wheel 文件）
# 先将 AmazingData-0.0.6-py3-none-any.whl 文件复制到项目目录
pip install AmazingData-0.0.6-py3-none-any.whl
```

### 步骤 5: 配置 AmazingData

编辑测试脚本，配置登录信息：

```python
# 编辑 test_amazingdata_etf.py
# 修改以下配置：
USERNAME = "your_username"      # 替换为您的账号
PASSWORD = "your_password"      # 替换为您的密码
HOST = "your_host"              # 替换为服务器 IP
PORT = 12345                    # 替换为服务器端口号
```

### 步骤 6: 运行测试

```bash
# 确保虚拟环境已激活
.\amazingdata_env\Scripts\Activate.ps1

# 运行 ETF 测试脚本
python test_amazingdata_etf.py

# 运行通用测试脚本
python test_amazingdata.py
```

### 步骤 7: 运行 FastAPI 后端（可选）

```bash
# 进入后端目录
cd fastapi-backend

# 运行服务器
python -m uvicorn main:app --reload --port 8000
```

### 步骤 8: 运行前端（可选）

```bash
# 进入前端目录
cd vue-frontend

# 安装依赖
npm install

# 运行开发服务器
npm run dev
```

---

## 第三部分：日常开发流程

### 在阿里云服务器上

```bash
# 1. 提交更改
cd /path/to/finance_tools
git add .
git commit -m "描述你的更改"
git push origin main

# 2. 查看状态
git status

# 3. 查看日志
git log --oneline
```

### 在 Windows 电脑上

```bash
# 1. 拉取最新代码
cd C:\Projects\finance_tools
git pull origin main

# 2. 开发完成后提交
git add .
git commit -m "描述你的更改"
git push origin main

# 3. 查看状态
git status
```

---

## 第四部分：常见问题

### Q1: 如何在 Windows 上查看已安装的包？
```bash
pip list
```

### Q2: 如何导出依赖列表？
```bash
pip freeze > requirements.txt
```

### Q3: 如何切换 Git 分支？
```bash
# 创建新分支
git checkout -b feature-branch

# 切换分支
git checkout feature-branch

# 返回主分支
git checkout main
```

### Q4: 如何处理 Git 冲突？
```bash
# 拉取代码时如果有冲突
git pull origin main

# 编辑冲突文件，解决冲突后
git add <conflicted_file>
git commit -m "Resolve merge conflict"
```

### Q5: Windows 上如何激活虚拟环境时遇到权限问题？
```powershell
# 以管理员身份运行 PowerShell
# 或者修改执行策略
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Q6: 如何在 Windows 上运行.sh 脚本？
Windows 不直接支持 .sh 脚本，可以：
1. 手动执行脚本中的命令
2. 使用 Git Bash 运行
3. 将脚本转换为 .bat 或 .ps1 格式

---

## 第五部分：项目结构

```
finance_tools/
├── .gitignore              # Git 忽略文件
├── requirements.txt        # Python 依赖
├── README.md              # 项目说明
├── test_amazingdata.py    # AmazingData 测试脚本
├── test_amazingdata_etf.py # ETF 数据测试脚本
├── fastapi-backend/       # FastAPI 后端
│   ├── main.py
│   └── routers/
├── grid_trading/          # 网格交易模块
│   ├── config.py
│   └── data_providers/
├── vue-frontend/          # Vue 前端
│   ├── src/
│   └── package.json
└── docs/                  # 文档
    ├── amazingData/
    └── baoStock/
```

---

## 快速参考

### macOS / Linux 命令 vs Windows PowerShell 命令

| 操作 | macOS/Linux | Windows PowerShell |
|------|-------------|-------------------|
| 激活虚拟环境 | `source venv/bin/activate` | `.\venv\Scripts\Activate.ps1` |
| 查看目录 | `ls` | `ls` 或 `dir` |
| 切换目录 | `cd dir` | `cd dir` |
| Python | `python3` | `python` |
| Pip | `pip3` | `pip` |

---

**文档版本**: 1.0  
**更新日期**: 2026-03-29
