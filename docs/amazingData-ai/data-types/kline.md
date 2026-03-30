# K 线数据结构 (Kline Data Type)

## 概述

本文档定义了 AmazingData API 中使用的 K 线数据结构。

---

## Kline - K 线数据

用于所有品种的 K 线数据。

| 字段名 | 类型 | 描述 | 备注 |
|--------|------|------|------|
| `code` | str | 证券代码 | |
| `trade_date` | int | 交易日期 | 格式 YYYYMMDD |
| `trade_time` | int | 交易时间 | 格式 HHMM 或 HHMMSS |
| `open` | float | 开盘价 | |
| `high` | float | 最高价 | |
| `low` | float | 最低价 | |
| `close` | float | 收盘价 | |
| `volume` | int | 成交量 | 股/手 |
| `amount` | float | 成交额 | 元 |

---

## 数据周期

K 线数据支持以下周期：

| 周期 | 常量值 | 描述 |
|------|--------|------|
| 1 分钟 | `Period.min1` | 1 分钟 K 线 |
| 5 分钟 | `Period.min5` | 5 分钟 K 线 |
| 15 分钟 | `Period.min15` | 15 分钟 K 线 |
| 30 分钟 | `Period.min30` | 30 分钟 K 线 |
| 60 分钟 | `Period.min60` | 60 分钟 K 线 |
| 日 K | `Period.day` | 日 K 线 |
| 周 K | `Period.week` | 周 K 线 |
| 月 K | `Period.month` | 月 K 线 |
| 季 K | `Period.quarter` | 季 K 线 |
| 年 K | `Period.year` | 年 K 线 |

---

## 使用示例

### 获取 K 线数据

```python
import AmazingData as ad

ad.login(username='user', password='pass', host='host', port=port)

base_data = ad.BaseData()
code_list = base_data.get_code_list(security_type='EXTRA_STOCK_A')
calendar = base_data.get_calendar()

market_data = ad.MarketData(calendar)

# 获取日 K 线数据
kline_dict = market_data.query_kline(
    code_list[:10],
    begin_date=20240101,
    end_date=20241231,
    period=ad.constant.Period.day.value
)

# 访问 K 线数据
for code, df in kline_dict.items():
    print(f"\n{code} K 线数据:")
    print(f"数据条数：{len(df)}")
    print(f"字段：{df.columns.tolist()}")
    print(df.tail())
```

### K 线数据处理

```python
import pandas as pd

# 计算技术指标
for code, df in kline_dict.items():
    # 移动平均线
    df['ma5'] = df['close'].rolling(5).mean()
    df['ma10'] = df['close'].rolling(10).mean()
    df['ma20'] = df['close'].rolling(20).mean()
    
    # 成交量均线
    df['vol_ma5'] = df['volume'].rolling(5).mean()
    
    # 收益率
    df['return'] = df['close'].pct_change()
    
    # 波动率
    df['volatility'] = df['return'].rolling(20).std()
```

### 实时 K 线订阅

```python
# 实时订阅 K 线数据
sub_data = ad.SubscribeData()

@sub_data.register(
    code_list=code_list[:10],
    period=ad.constant.Period.min1.value  # 1 分钟 K 线
)
def OnKLine(data, period):
    print(f"收到 K 线数据:")
    print(f"  代码：{data['code']}")
    print(f"  时间：{data['trade_time']}")
    print(f"  开盘：{data['open']}")
    print(f"  最高：{data['high']}")
    print(f"  最低：{data['low']}")
    print(f"  收盘：{data['close']}")
    print(f"  成交量：{data['volume']}")

sub_data.run()
```

---

## K 线算法说明

### 日 K 线

- **开盘价**：当日第一笔成交价
- **收盘价**：当日最后一笔成交价
- **最高价**：当日最高成交价
- **最低价**：当日最低成交价
- **成交量**：当日总成交量
- **成交额**：当日总成交额

### 分钟 K 线

- **开盘价**：该分钟第一笔成交价
- **收盘价**：该分钟最后一笔成交价
- **最高价**：该分钟最高成交价
- **最低价**：该分钟最低成交价
- **成交量**：该分钟总成交量
- **成交额**：该分钟总成交额

### 周 K 线

- **开盘价**：本周第一个交易日的开盘价
- **收盘价**：本周最后一个交易日的收盘价
- **最高价**：本周最高价
- **最低价**：本周最低价
- **成交量**：本周总成交量
- **成交额**：本周总成交额

### 月 K 线

- **开盘价**：本月第一个交易日的开盘价
- **收盘价**：本月最后一个交易日的收盘价
- **最高价**：本月最高价
- **最低价**：本月最低价
- **成交量**：本月总成交量
- **成交额**：本月总成交额

---

## 相关文档

- [快照数据结构](snapshot.md)
- [常量定义](constants.md)
- [历史行情数据](../api-reference/04-historical-market.md)
