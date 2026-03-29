# 测试目录

此目录包含所有测试脚本。

## 测试文件

- `test_amazingdata_etf.py` - ETF 数据获取测试（包含登录）

## 运行测试

### 方法 1: 直接运行测试脚本

```bash
# 激活虚拟环境
# macOS/Linux:
source amazingdata_env/bin/activate

# Windows PowerShell:
.\amazingdata_env\Scripts\Activate.ps1

# 运行测试
python tests/test_amazingdata_etf.py
```

### 方法 2: 使用 pytest

```bash
# 安装 pytest（如果未安装）
pip install pytest

# 运行所有测试
python -m pytest tests/

# 运行特定测试
python -m pytest tests/test_amazingdata_etf.py -v
```

## 配置

编辑测试脚本，修改以下配置：

```python
USERNAME = "your_username"      # 替换为您的账号
PASSWORD = "your_password"      # 替换为您的密码
HOST = "your_host"              # 替换为服务器 IP
PORT = 12345                    # 替换为服务器端口号
```
