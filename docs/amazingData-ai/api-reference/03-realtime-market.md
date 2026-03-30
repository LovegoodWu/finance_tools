# 实时行情数据 (Realtime Market Data)

## 概述

实时行情数据接口提供股票、指数、期货、ETF、可转债等品种的实时快照和 K 线数据订阅。

## 类和方法

| 类名 | 描述 |
|------|------|
| `SubscribeData` | 实时数据订阅类 |

---

## SubscribeData 类

### 使用步骤

1. 实例化 `SubscribeData`
2. 使用装饰器 `@register` 注册回调函数，传入 `code_list` 和 `period`
3. 调用 `run()` 开始订阅

---

## 实时快照接口

### onSnapshot - 股票实时快照

**函数接口**：`onSnapshot`

**功能描述**：Level-1 快照数据的实时订阅回调函数（股票）

**输入参数**（通过装饰器传入）：

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `code_list` | list[str] | 是 | 证券代码列表，支持北交所、上交所、深交所的股票 |
| `period` | Period | 是 | `Period.snapshot.value` |

**输出参数**（回调函数参数）：

| 参数 | 类型 | 描述 |
|------|------|------|
| `data` | Snapshot | 股票快照数据，见 [数据结构](../data-types/snapshot.md) |
| `period` | Period | 数据周期 |

**使用示例**：
```python
import AmazingData as ad

ad.login(username='user', password='pass', host='host', port=port)

base_data = ad.BaseData()
code_list = base_data.get_code_list(security_type='EXTRA_STOCK_A')

sub_data = ad.SubscribeData()

@sub_data.register(code_list=code_list, period=ad.constant.Period.snapshot.value)
def onSnapshot(data, period):
    print(f"收到快照数据：{data}")

sub_data.run()
```

---

### onSnapshotIndex - 指数实时快照

**函数接口**：`onSnapshotIndex`

**功能描述**：交易所指数快照数据的实时订阅回调函数

**输入参数**：

| 参数 | 类型 | 描述 |
|------|------|------|
| `code_list` | list[str] | 指数代码列表 |
| `period` | Period | `Period.snapshot.value` |

**输出参数**：

| 参数 | 类型 | 描述 |
|------|------|------|
| `data` | SnapshotIndex | 指数快照数据 |

**使用示例**：
```python
base_data = ad.BaseData()
code_list = base_data.get_code_list(security_type='EXTRA_INDEX_A')

sub_data = ad.SubscribeData()

@sub_data.register(code_list=code_list, period=ad.constant.Period.snapshot.value)
def onSnapshotIndex(data, period):
    print(f"指数快照：{data}")

sub_data.run()
```

---

### onSnapshotFuture - 期货实时快照

**函数接口**：`onSnapshotFuture`

**功能描述**：期货快照数据的实时订阅回调函数

**输入参数**：

| 参数 | 类型 | 描述 |
|------|------|------|
| `code_list` | list[str] | 期货代码列表（中金所） |
| `period` | Period | `Period.snapshotfuture.value` |

**输出参数**：

| 参数 | 类型 | 描述 |
|------|------|------|
| `data` | SnapshotFuture | 期货快照数据 |

**使用示例**：
```python
base_data = ad.BaseData()
code_list = base_data.get_code_list(security_type='EXTRA_FUTURE')

sub_data = ad.SubscribeData()

@sub_data.register(code_list=code_list, period=ad.constant.Period.snapshotfuture.value)
def onSnapshotFuture(data, period):
    print(f"期货快照：{data}")

sub_data.run()
```

---

### onSnapshotETF - ETF 实时快照

**函数接口**：`onSnapshotETF`

**功能描述**：ETF 快照数据的实时订阅回调函数

**输入参数**：

| 参数 | 类型 | 描述 |
|------|------|------|
| `code_list` | list[str] | ETF 代码列表 |
| `period` | Period | `Period.snapshot.value` |

**使用示例**：
```python
base_data = ad.BaseData()
code_list = base_data.get_code_list(security_type='EXTRA_ETF')

sub_data = ad.SubscribeData()

@sub_data.register(code_list=code_list, period=ad.constant.Period.snapshot.value)
def onSnapshotETF(data, period):
    print(f"ETF 快照：{data}")

sub_data.run()
```

---

### onSnapshotKZZ - 可转债实时快照

**函数接口**：`onSnapshotKZZ`

**功能描述**：可转债快照数据的实时订阅回调函数

**输入参数**：

| 参数 | 类型 | 描述 |
|------|------|------|
| `code_list` | list[str] | 可转债代码列表 |
| `period` | Period | `Period.snapshot.value` |

**使用示例**：
```python
base_data = ad.BaseData()
code_list = base_data.get_code_list(security_type='EXTRA_KZZ')

sub_data = ad.SubscribeData()

@sub_data.register(code_list=code_list, period=ad.constant.Period.snapshot.value)
def onSnapshotKZZ(data, period):
    print(f"可转债快照：{data}")

sub_data.run()
```

---

### onSnapshotHKT - 港股通实时快照

**函数接口**：`onSnapshotHKT`

**功能描述**：港股通快照数据的实时订阅回调函数

**输入参数**：

| 参数 | 类型 | 描述 |
|------|------|------|
| `code_list` | list[str] | 港股通代码列表 |
| `period` | Period | `Period.snapshotHKT.value` |

**输出参数**：

| 参数 | 类型 | 描述 |
|------|------|------|
| `data` | SnapshotHKT | 港股通快照数据 |

---

### onSnapshotOption - ETF 期权实时快照

**函数接口**：`onSnapshotOption`

**功能描述**：ETF 期权快照数据的实时订阅回调函数

**输入参数**：

| 参数 | 类型 | 描述 |
|------|------|------|
| `code_list` | list[str] | ETF 期权代码列表 |
| `period` | Period | `Period.snapshotoption.value` |

**输出参数**：

| 参数 | 类型 | 描述 |
|------|------|------|
| `data` | SnapshotOption | ETF 期权快照数据 |

**使用示例**：
```python
base_data = ad.BaseData()
option_code_list = base_data.get_option_code_list(security_type='EXTRA_ETF_OP')

sub_data = ad.SubscribeData()

@sub_data.register(code_list=option_code_list, period=ad.constant.Period.snapshotoption.value)
def onSnapshotOption(data, period):
    print(f"期权快照：{data}")

sub_data.run()
```

---

### onSnapshotGLRA - 逆回购实时快照

**函数接口**：`onSnapshotGLRA`

**功能描述**：逆回购快照数据的实时订阅回调函数

**输入参数**：

| 参数 | 类型 | 描述 |
|------|------|------|
| `code_list` | list[str] | 逆回购代码列表 |
| `period` | Period | `Period.snapshot.value` |

**使用示例**：
```python
base_data = ad.BaseData()
code_list = base_data.get_code_list(security_type='EXTRA_GLRA')

sub_data = ad.SubscribeData()

@sub_data.register(code_list=code_list, period=ad.constant.Period.snapshot.value)
def onSnapshotGLRA(data, period):
    print(f"逆回购快照：{data}")

sub_data.run()
```

---

## 实时 K 线接口

### OnKLine - 实时 K 线

**函数接口**：`OnKLine`

**功能描述**：K 线数据的实时订阅回调函数

**输入参数**：

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `code_list` | list[str] | 是 | 证券代码列表，支持股票、指数、ETF、可转债、期货等 |
| `period` | Period | 是 | 数据周期，如 `Period.min1.value`（1 分钟） |

**输出参数**：

| 参数 | 类型 | 描述 |
|------|------|------|
| `data` | Kline | K 线数据，见 [数据结构](../data-types/kline.md) |
| `period` | Period | 数据周期 |

**支持的数据周期**：

| 周期 | 值 | 描述 |
|------|-----|------|
| 1 分钟 | `Period.min1.value` | 1 分钟 K 线 |
| 5 分钟 | `Period.min5.value` | 5 分钟 K 线 |
| 15 分钟 | `Period.min15.value` | 15 分钟 K 线 |
| 30 分钟 | `Period.min30.value` | 30 分钟 K 线 |
| 60 分钟 | `Period.min60.value` | 60 分钟 K 线 |
| 日 K | `Period.day.value` | 日 K 线 |
| 周 K | `Period.week.value` | 周 K 线 |
| 月 K | `Period.month.value` | 月 K 线 |

**使用示例**：
```python
import AmazingData as ad

ad.login(username='user', password='pass', host='host', port=port)

base_data = ad.BaseData()
code_list = base_data.get_code_list(security_type='EXTRA_STOCK_A')

sub_data = ad.SubscribeData()

@sub_data.register(code_list=code_list, period=ad.constant.Period.min1.value)
def OnKLine(data, period):
    print(f"收到 K 线数据：code={data.get('code')}, close={data.get('close')}")

sub_data.run()
```

---

## 数据结构

### Snapshot（股票/ETF/可转债快照）

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `code` | str | 证券代码 |
| `open` | float | 开盘价 |
| `high` | float | 最高价 |
| `low` | float | 最低价 |
| `close` | float | 最新价/收盘价 |
| `volume` | int | 成交量 |
| `amount` | float | 成交额 |
| `bid_price` | list | 买盘价格 |
| `bid_volume` | list | 买盘量 |
| `ask_price` | list | 卖盘价格 |
| `ask_volume` | list | 卖盘量 |
| `trade_date` | int | 交易日期 |
| `trade_time` | int | 交易时间 |

### SnapshotIndex（指数快照）

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `code` | str | 指数代码 |
| `open` | float | 开盘价 |
| `high` | float | 最高价 |
| `low` | float | 最低价 |
| `close` | float | 最新价 |
| `volume` | int | 成交量 |
| `amount` | float | 成交额 |
| `pre_close` | float | 昨收盘 |

### SnapshotFuture（期货快照）

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `code` | str | 期货代码 |
| `open` | float | 开盘价 |
| `high` | float | 最高价 |
| `low` | float | 最低价 |
| `close` | float | 最新价 |
| `volume` | int | 成交量 |
| `open_interest` | int | 持仓量 |

### SnapshotHKT（港股通快照）

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `code` | str | 港股通代码 |
| `close` | float | 最新价 |
| `change` | float | 涨跌额 |
| `change_rate` | float | 涨跌幅 |
| `volume` | int | 成交量 |
| `amount` | float | 成交额 |

### SnapshotOption（ETF 期权快照）

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `code` | str | 期权代码 |
| `close` | float | 最新价 |
| `bid_price` | float | 买一价 |
| `ask_price` | float | 卖一价 |
| `volume` | int | 成交量 |
| `open_interest` | int | 持仓量 |

### Kline（K 线数据）

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `code` | str | 证券代码 |
| `trade_date` | int | 交易日期 |
| `trade_time` | int | 交易时间 |
| `open` | float | 开盘价 |
| `high` | float | 最高价 |
| `low` | float | 最低价 |
| `close` | float | 收盘价 |
| `volume` | int | 成交量 |
| `amount` | float | 成交额 |

---

## 相关文档

- [历史行情数据](04-historical-market.md)
- [数据结构 - Snapshot](../data-types/snapshot.md)
- [数据结构 - Kline](../data-types/kline.md)
- [常量定义](../data-types/constants.md)
