# 快照数据结构 (Snapshot Data Types)

## 概述

本文档定义了 AmazingData API 中使用的各种快照数据结构。

---

## Snapshot - 股票/ETF/可转债快照

用于股票、ETF 和可转债的 Level-1 快照数据。

| 字段名 | 类型 | 描述 | 备注 |
|--------|------|------|------|
| `code` | str | 证券代码 | |
| `trade_date` | int | 交易日期 | 格式 YYYYMMDD |
| `trade_time` | int | 交易时间 | 格式 HHMMSSmmm |
| `open` | float | 开盘价 | |
| `high` | float | 最高价 | |
| `low` | float | 最低价 | |
| `close` | float | 最新价/收盘价 | |
| `volume` | int | 成交量 | 股/手 |
| `amount` | float | 成交额 | 元 |
| `bid_price` | list[float] | 买盘价格 | 5 档 [bid1, bid2, bid3, bid4, bid5] |
| `bid_volume` | list[int] | 买盘量 | 5 档 |
| `ask_price` | list[float] | 卖盘价格 | 5 档 [ask1, ask2, ask3, ask4, ask5] |
| `ask_volume` | list[int] | 卖盘量 | 5 档 |
| `pre_close` | float | 昨收盘 | |

---

## SnapshotIndex - 指数快照

用于交易所指数的快照数据。

| 字段名 | 类型 | 描述 | 备注 |
|--------|------|------|------|
| `code` | str | 指数代码 | |
| `trade_date` | int | 交易日期 | 格式 YYYYMMDD |
| `trade_time` | int | 交易时间 | |
| `open` | float | 开盘价 | |
| `high` | float | 最高价 | |
| `low` | float | 最低价 | |
| `close` | float | 最新价 | |
| `volume` | int | 成交量 | |
| `amount` | float | 成交额 | 元 |
| `pre_close` | float | 昨收盘 | |

---

## SnapshotFuture - 期货快照

用于期货的快照数据。

| 字段名 | 类型 | 描述 | 备注 |
|--------|------|------|------|
| `code` | str | 期货代码 | |
| `trade_date` | int | 交易日期 | |
| `trade_time` | int | 交易时间 | |
| `open` | float | 开盘价 | |
| `high` | float | 最高价 | |
| `low` | float | 最低价 | |
| `close` | float | 最新价 | |
| `volume` | int | 成交量 | |
| `open_interest` | int | 持仓量 | |
| `settlement` | float | 结算价 | |

---

## SnapshotHKT - 港股通快照

用于港股通的快照数据。

| 字段名 | 类型 | 描述 | 备注 |
|--------|------|------|------|
| `code` | str | 港股通代码 | |
| `trade_date` | int | 交易日期 | |
| `close` | float | 最新价 | |
| `change` | float | 涨跌额 | |
| `change_rate` | float | 涨跌幅 (%) | |
| `volume` | int | 成交量 | |
| `amount` | float | 成交额 | |
| `high` | float | 最高价 | |
| `low` | float | 最低价 | |
| `pre_close` | float | 昨收盘 | |

---

## SnapshotOption - ETF 期权快照

用于 ETF 期权的快照数据。

| 字段名 | 类型 | 描述 | 备注 |
|--------|------|------|------|
| `code` | str | 期权代码 | |
| `trade_date` | int | 交易日期 | |
| `close` | float | 最新价 | |
| `bid_price` | float | 买一价 | |
| `ask_price` | float | 卖一价 | |
| `bid_volume` | int | 买一量 | |
| `ask_volume` | int | 卖一量 | |
| `volume` | int | 成交量 | |
| `open_interest` | int | 持仓量 | |
| `high` | float | 最高价 | |
| `low` | float | 最低价 | |

---

## 使用示例

### 访问快照数据

```python
import AmazingData as ad

ad.login(username='user', password='pass', host='host', port=port)

# 实时订阅快照数据
base_data = ad.BaseData()
code_list = base_data.get_code_list(security_type='EXTRA_STOCK_A')

sub_data = ad.SubscribeData()

@sub_data.register(code_list=code_list[:10], period=ad.constant.Period.snapshot.value)
def onSnapshot(data, period):
    # 访问字段
    print(f"代码：{data['code']}")
    print(f"最新价：{data['close']}")
    print(f"买一价：{data['bid_price'][0]}")
    print(f"卖一价：{data['ask_price'][0]}")

sub_data.run()
```

### 查询历史快照

```python
# 查询历史快照
market_data = ad.MarketData(calendar)
snapshot_dict = market_data.query_snapshot(
    code_list,
    begin_date=20241231,
    end_date=20241231
)

for code, df in list(snapshot_dict.items())[:3]:
    print(f"\n{code}:")
    print(df.columns.tolist())
    print(df.head())
```

---

## 相关文档

- [K 线数据结构](kline.md)
- [实时行情数据](../api-reference/03-realtime-market.md)
- [历史行情数据](../api-reference/04-historical-market.md)
