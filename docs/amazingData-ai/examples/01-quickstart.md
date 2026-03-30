# 快速开始 (Quickstart)

## 概述

本指南将帮助您快速上手使用 AmazingData 金融数据 SDK。

---

## 1. 安装 SDK

```bash
pip install AmazingData
```

---

## 2. 登录

```python
import AmazingData as ad

# 登录到 AmazingData 服务
ad.login(
    username='your_username',
    password='your_password',
    host='your_host',
    port=your_port
)
```

---

## 3. 获取股票数据

### 3.1 获取代码列表

```python
base_data = ad.BaseData()

# 获取全部 A 股代码
stock_codes = base_data.get_code_list(security_type='EXTRA_STOCK_A')
print(f"A 股数量：{len(stock_codes)}")

# 获取 ETF 代码
etf_codes = base_data.get_code_list(security_type='EXTRA_ETF')

# 获取可转债代码
kzz_codes = base_data.get_code_list(security_type='EXTRA_KZZ')
```

### 3.2 获取历史 K 线数据

```python
# 获取交易日历
calendar = base_data.get_calendar()
print(f"交易日历天数：{len(calendar)}")
print(f"最新交易日：{calendar[-1]}")

# 创建市场数据对象
market_data = ad.MarketData(calendar)

# 获取日 K 线数据
kline_dict = market_data.query_kline(
    code_list=stock_codes[:10],  # 前 10 只股票
    begin_date=20240101,
    end_date=20241231,
    period=ad.constant.Period.day.value
)

# 查看数据
for code, df in kline_dict.items():
    print(f"\n{code} 数据条数：{len(df)}")
    print(df.tail())  # 显示最后 5 条数据
```

### 3.3 获取历史快照数据

```python
# 获取指定日期的快照数据
snapshot_dict = market_data.query_snapshot(
    code_list=stock_codes[:10],
    begin_date=20241231,
    end_date=20241231
)

for code, df in snapshot_dict.items():
    print(f"\n{code} 快照数据:")
    print(df)
```

---

## 4. 获取财务数据

```python
info_data = ad.InfoData()
local_path = '/path/to/data'  # 替换为实际路径

# 获取资产负债表
balance_sheet = info_data.get_balance_sheet(
    code_list=stock_codes[:10],
    local_path=local_path,
    is_local=False  # 首次运行设为 False
)

# 获取利润表
income_stmt = info_data.get_income_statement(
    code_list=stock_codes[:10],
    local_path=local_path,
    is_local=False
)

# 获取现金流量表
cash_flow = info_data.get_cash_flow(
    code_list=stock_codes[:10],
    local_path=local_path,
    is_local=False
)
```

---

## 5. 实时数据订阅

```python
# 创建订阅数据对象
sub_data = ad.SubscribeData()

# 注册回调函数
@sub_data.register(
    code_list=stock_codes[:5],
    period=ad.constant.Period.min1.value  # 1 分钟 K 线
)
def OnKLine(data, period):
    print(f"收到 K 线数据：code={data.get('code')}, close={data.get('close')}")

# 开始订阅
sub_data.run()
```

---

## 6. 完整示例

以下是一个完整的示例，展示如何获取股票数据并进行简单分析：

```python
import AmazingData as ad
import pandas as pd

# 1. 登录
ad.login(
    username='your_username',
    password='your_password',
    host='your_host',
    port=your_port
)

# 2. 初始化数据对象
base_data = ad.BaseData()
info_data = ad.InfoData()

# 3. 获取代码列表和交易日历
stock_codes = base_data.get_code_list(security_type='EXTRA_STOCK_A')
calendar = base_data.get_calendar()

# 4. 获取历史 K 线数据
market_data = ad.MarketData(calendar)
kline_dict = market_data.query_kline(
    code_list=stock_codes[:50],
    begin_date=20240101,
    end_date=20241231,
    period=ad.constant.Period.day.value
)

# 5. 计算收益率
returns = {}
for code, df in kline_dict.items():
    if len(df) > 1:
        df_sorted = df.sort_index()
        returns[code] = (df_sorted['close'].iloc[-1] - df_sorted['close'].iloc[0]) / df_sorted['close'].iloc[0]

# 6. 找出收益率最高的股票
returns_df = pd.DataFrame(list(returns.items()), columns=['code', 'return'])
top_gainers = returns_df.nlargest(10, 'return')
print("2024 年收益率前 10 名:")
print(top_gainers)
```

---

## 7. 登出

```python
# 使用完毕后登出
ad.logout()
```

---

## 注意事项

1. **权限**：使用前需要联系银河证券获取 API 访问权限
2. **本地缓存**：财务数据量较大，建议使用本地缓存
3. **分批处理**：大批量查询时建议分批处理，避免超时
4. **错误处理**：生产环境中应添加适当的错误处理

---

## 相关文档

- [认证接口](../api-reference/01-authentication.md)
- [基础数据接口](../api-reference/02-base-data.md)
- [历史行情数据](../api-reference/04-historical-market.md)
- [金融算子使用](03-operators.md)
