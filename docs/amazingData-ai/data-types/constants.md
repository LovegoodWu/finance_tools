# 常量定义 (Constants)

## 概述

本文档定义了在 AmazingData SDK 中使用的常量枚举值。

---

## Period - 数据周期

用于指定 K 线数据的时间周期。

**使用方式**：
```python
import AmazingData as ad

# 访问周期常量
period_value = ad.constant.Period.day.value
```

### 周期枚举值

| 常量名 | 值 | 描述 |
|--------|-----|------|
| `Period.snapshot` | 0 | 快照数据 |
| `Period.min1` | 1 | 1 分钟 K 线 |
| `Period.min5` | 5 | 5 分钟 K 线 |
| `Period.min15` | 15 | 15 分钟 K 线 |
| `Period.min30` | 30 | 30 分钟 K 线 |
| `Period.min60` | 60 | 60 分钟 K 线 |
| `Period.day` | 300 | 日 K 线 |
| `Period.week` | 301 | 周 K 线 |
| `Period.month` | 302 | 月 K 线 |
| `Period.year` | 303 | 年 K 线 |
| `Period.quarter` | 304 | 季 K 线 |
| `Period.snapshotfuture` | 400 | 期货快照 |
| `Period.snapshotHKT` | 500 | 港股通快照 |
| `Period.snapshotoption` | 600 | ETF 期权快照 |

### 使用示例

```python
import AmazingData as ad

ad.login(username='user', password='pass', host='host', port=port)

base_data = ad.BaseData()
code_list = base_data.get_code_list(security_type='EXTRA_STOCK_A')
calendar = base_data.get_calendar()

market_data = ad.MarketData(calendar)

# 查询日 K 线
kline_day = market_data.query_kline(
    code_list,
    begin_date=20240101,
    end_date=20241231,
    period=ad.constant.Period.day.value
)

# 查询 5 分钟 K 线
kline_5min = market_data.query_kline(
    code_list,
    begin_date=20240501,
    end_date=20240531,
    period=ad.constant.Period.min5.value
)
```

---

## SecurityType - 证券类型

用于指定证券代码类型。

### 常用证券类型

| 常量值 | 描述 |
|--------|------|
| `EXTRA_STOCK_A` | 上交所 A 股、深交所 A 股和北交所的股票列表 |
| `SH_A` | 上交所 A 股的股票列表 |
| `SZ_A` | 深交所 A 股的股票列表 |
| `BJ_A` | 北交所的股票列表 |
| `EXTRA_STOCK_A_SH_SZ` | 上交所 A 股和深交所 A 股的股票列表 |
| `EXTRA_INDEX_A` | 上交所、深交所和北交所的指数列表 |
| `SH_INDEX` | 上交所指数列表 |
| `SZ_INDEX` | 深交所指数列表 |
| `BJ_INDEX` | 北交所指数列表 |
| `EXTRA_ETF` | 上交所、深交所的 ETF 列表 |
| `SH_ETF` | 上交所的 ETF 列表 |
| `SZ_ETF` | 深交所的 ETF 列表 |
| `EXTRA_KZZ` | 上交所、深交所的可转债列表 |
| `SH_KZZ` | 上交所的可转债列表 |
| `SZ_KZZ` | 深交所的可转债列表 |
| `EXTRA_HKT` | 沪深港通 |
| `SH_HKT` | 沪港通 |
| `SZ_HKT` | 深港通 |
| `EXTRA_GLRA` | 沪深逆回购 |
| `EXTRA_FUTURE` | 期货（中金所） |
| `EXTRA_ETF_OP` | ETF 期权（上交所/深交所） |

### 使用示例

```python
base_data = ad.BaseData()

# 获取 A 股代码列表
stock_codes = base_data.get_code_list(security_type='EXTRA_STOCK_A')

# 获取 ETF 代码列表
etf_codes = base_data.get_code_list(security_type='EXTRA_ETF')

# 获取可转债代码列表
kzz_codes = base_data.get_code_list(security_type='EXTRA_KZZ')

# 获取指数代码列表
index_codes = base_data.get_code_list(security_type='EXTRA_INDEX_A')
```

---

## Market - 市场类型

用于指定交易所市场。

| 常量值 | 描述 |
|--------|------|
| `SH` | 上海证券交易所 |
| `SZ` | 深圳证券交易所 |
| `BJ` | 北京证券交易所 |
| `CFE` | 中国金融期货交易所（中金所） |
| `SHN` | 沪港通 |
| `SZN` | 深港通 |
| `HK` | 香港交易所 |

---

## 相关文档

- [实时行情数据](../api-reference/03-realtime-market.md)
- [历史行情数据](../api-reference/04-historical-market.md)
- [代码类型说明](../appendix/security-type.md)
