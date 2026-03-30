# 历史行情数据 (Historical Market Data)

## 概述

历史行情数据接口提供股票、指数、期货、ETF 等品种的历史快照和历史 K 线数据查询。

## 类和方法

| 类名 | 描述 |
|------|------|
| `MarketData` | 市场数据查询类 |

---

## MarketData 类

### 初始化

**函数签名**：
```python
MarketData(calendar: list[int])
```

**输入参数**：

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `calendar` | list[int] | 是 | 交易日历，从 `BaseData.get_calendar()` 获取 |

**使用示例**：
```python
import AmazingData as ad

ad.login(username='user', password='pass', host='host', port=port)

base_data = ad.BaseData()
calendar = base_data.get_calendar()
market_data = ad.MarketData(calendar)
```

---

### query_snapshot - 查询历史快照

**函数接口**：`query_snapshot`

**功能描述**：查询历史快照数据

**函数签名**：
```python
query_snapshot(code_list: list[str], begin_date: int, end_date: int, 
               begin_time: int = None, end_time: int = None) -> dict
```

**输入参数**：

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `code_list` | list[str] | 是 | 证券代码列表，支持股票、指数、ETF、可转债、港股通、ETF 期权等 |
| `begin_date` | int | 是 | 开始日期，格式 YYYYMMDD，如 `20240101` |
| `end_date` | int | 是 | 结束日期，格式 YYYYMMDD，如 `20241231` |
| `begin_time` | int | 否 | 开始时间（时分秒毫秒），如 9 点整为 `90000000` |
| `end_time` | int | 否 | 结束时间（时分秒毫秒），如 17 点 25 分为 `172500000` |

**输出参数**：

| 类型 | 描述 |
|------|------|
| dict | 字典的 key 为证券代码，value 为 DataFrame |

**DataFrame 结构**：
- **columns**: 快照数据字段（如 `open`, `high`, `low`, `close`, `volume` 等）
- **index**: 日期（datetime 类型）

**数据类型说明**：
- 股票、ETF、可转债：`Snapshot` 结构
- 指数：`SnapshotIndex` 结构
- 港股通：`SnapshotHKT` 结构
- ETF 期权：`SnapshotOption` 结构

**使用示例**：
```python
import AmazingData as ad

ad.login(username='user', password='pass', host='host', port=port)

base_data = ad.BaseData()
code_list = base_data.get_code_list(security_type='EXTRA_STOCK_A')
calendar = base_data.get_calendar()

market_data = ad.MarketData(calendar)

# 查询 2024 年 5 月 30 日的快照数据
snapshot_dict = market_data.query_snapshot(
    code_list,
    begin_date=20240530,
    end_date=20240530
)

# 访问特定股票的快照数据
for code, df in snapshot_dict.items():
    print(f"代码：{code}")
    print(df.head())
```

---

### query_kline - 查询历史 K 线

**函数接口**：`query_kline`

**功能描述**：查询历史 K 线数据，支持全部周期

**函数签名**：
```python
query_kline(code_list: list[str], begin_date: int, end_date: int,
            period: Period, begin_time: int = None, end_time: int = None) -> dict
```

**输入参数**：

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `code_list` | list[str] | 是 | 证券代码列表，支持股票、指数、ETF、可转债、期货、ETF 期权 |
| `begin_date` | int | 是 | 开始日期，格式 YYYYMMDD |
| `end_date` | int | 是 | 结束日期，格式 YYYYMMDD |
| `period` | Period | 是 | 数据周期，见下方说明 |
| `begin_time` | int | 否 | 开始时间（时分），如 9 点整为 `900` |
| `end_time` | int | 否 | 结束时间（时分），如 17 点 25 分为 `1725` |

**支持的数据周期**：

| 周期 | 常量值 | 描述 |
|------|--------|------|
| 1 分钟 | `ad.constant.Period.min1.value` | 1 分钟 K 线 |
| 5 分钟 | `ad.constant.Period.min5.value` | 5 分钟 K 线 |
| 15 分钟 | `ad.constant.Period.min15.value` | 15 分钟 K 线 |
| 30 分钟 | `ad.constant.Period.min30.value` | 30 分钟 K 线 |
| 60 分钟 | `ad.constant.Period.min60.value` | 60 分钟 K 线 |
| 日 K | `ad.constant.Period.day.value` | 日 K 线 |
| 周 K | `ad.constant.Period.week.value` | 周 K 线 |
| 月 K | `ad.constant.Period.month.value` | 月 K 线 |
| 年 K | `ad.constant.Period.year.value` | 年 K 线 |
| 季 K | `ad.constant.Period.quarter.value` | 季 K 线 |

**输出参数**：

| 类型 | 描述 |
|------|------|
| dict | 字典的 key 为证券代码，value 为 DataFrame |

**DataFrame 结构**：
- **columns**: K 线数据字段
  - `open`: 开盘价
  - `high`: 最高价
  - `low`: 最低价
  - `close`: 收盘价
  - `volume`: 成交量
  - `amount`: 成交额
- **index**: 日期（datetime 类型）

**使用示例**：
```python
import AmazingData as ad

ad.login(username='user', password='pass', host='host', port=port)

base_data = ad.BaseData()
code_list = base_data.get_code_list(security_type='EXTRA_STOCK_A')
calendar = base_data.get_calendar()

market_data = ad.MarketData(calendar)

# 查询日 K 线数据
kline_dict = market_data.query_kline(
    code_list,
    begin_date=20240101,
    end_date=20241231,
    period=ad.constant.Period.day.value
)

# 访问特定股票的 K 线数据
for code, df in list(kline_dict.items())[:5]:  # 只显示前 5 只股票
    print(f"代码：{code}")
    print(f"数据条数：{len(df)}")
    print(df.tail())  # 显示最后 5 条数据
```

**多周期 K 线查询示例**：
```python
# 查询 5 分钟 K 线
kline_5min = market_data.query_kline(
    code_list,
    begin_date=20240501,
    end_date=20240531,
    period=ad.constant.Period.min5.value
)

# 查询 60 分钟 K 线
kline_60min = market_data.query_kline(
    code_list,
    begin_date=20240501,
    end_date=20240531,
    period=ad.constant.Period.min60.value
)
```

**期货 K 线查询示例**：
```python
# 获取期货代码列表
future_codes = base_data.get_code_list(security_type='EXTRA_FUTURE')

# 查询期货 K 线
future_kline = market_data.query_kline(
    future_codes,
    begin_date=20240101,
    end_date=20241231,
    period=ad.constant.Period.day.value
)
```

---

## 数据字段说明

### K 线数据字段

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `open` | float | 开盘价 |
| `high` | float | 最高价 |
| `low` | float | 最低价 |
| `close` | float | 收盘价 |
| `volume` | int | 成交量（股/手） |
| `amount` | float | 成交额（元） |

### 快照数据字段

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `open` | float | 开盘价 |
| `high` | float | 最高价 |
| `low` | float | 最低价 |
| `close` | float | 最新价/收盘价 |
| `volume` | int | 成交量 |
| `amount` | float | 成交额 |
| `bid_price` | list[float] | 买盘价格（5 档） |
| `bid_volume` | list[int] | 买盘量（5 档） |
| `ask_price` | list[float] | 卖盘价格（5 档） |
| `ask_volume` | list[int] | 卖盘量（5 档） |
| `pre_close` | float | 昨收盘 |

---

## 注意事项

1. **数据范围**：
   - 股票数据：2013 年至今
   - 期货数据：2010 年 4 月至今
   - 期权数据：2015 年至今

2. **性能优化**：
   - 大批量查询时建议分批处理
   - 使用本地缓存可减少网络请求

3. **日期格式**：
   - 日期参数使用 8 位整数格式：YYYYMMDD
   - 时间参数使用 8-9 位整数格式：HHMMSSmmm

---

## 相关文档

- [实时行情数据](03-realtime-market.md)
- [数据结构 - Snapshot](../data-types/snapshot.md)
- [数据结构 - Kline](../data-types/kline.md)
- [常量定义](../data-types/constants.md)
