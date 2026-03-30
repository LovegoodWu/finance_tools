# 交易异动数据接口 (Trading Anomaly)

## 概述

交易异动数据接口提供龙虎榜和大宗交易数据。

## InfoData 类方法

---

### get_top_list - 龙虎榜

**函数接口**：`get_top_list`

**功能描述**：获取龙虎榜数据

**函数签名**：
```python
get_top_list(code_list: list[str], local_path: str, is_local: bool = True,
             begin_date: int = None, end_date: int = None) -> dict
```

**输入参数**：

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `code_list` | list[str] | 是 | 证券代码列表 |
| `local_path` | str | 是 | 本地存储路径 |
| `is_local` | bool | 否 | 是否使用本地缓存 |
| `begin_date` | int | 否 | 开始日期 |
| `end_date` | int | 否 | 结束日期 |

**输出参数**：

| 类型 | 描述 |
|------|------|
| dict | key: 证券代码，value: DataFrame（龙虎榜数据） |

**主要字段**：

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `MARKET_CODE` | str | 证券代码 |
| `SECURITY_NAME` | str | 证券简称 |
| `TRADE_DATE` | str | 交易日期 |
| `CLOSE` | float | 收盘价 |
| `CHANGE_RATIO` | float | 涨跌幅 (%) |
| `TURNOVER_RATIO` | float | 换手率 (%) |
| `BUY_TOTAL_AMT` | float | 买入总额（元） |
| `SELL_TOTAL_AMT` | float | 卖出总额（元） |
| `NET_AMT` | float | 净额（元） |
| `BUYER_NAME` | str | 买方营业部名称 |
| `SELLER_NAME` | str | 卖方营业部名称 |

---

### get_block_trading - 大宗交易

**函数接口**：`get_block_trading`

**功能描述**：获取大宗交易数据

**函数签名**：：
```python
get_block_trading(code_list: list[str], local_path: str, is_local: bool = True,
                  begin_date: int = None, end_date: int = None) -> dict
```

**输出参数**：

| 类型 | 描述 |
|------|------|
| dict | key: 证券代码，value: DataFrame（大宗交易数据） |

**主要字段**：

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `MARKET_CODE` | str | 证券代码 |
| `SECURITY_NAME` | str | 证券简称 |
| `TRADE_DATE` | str | 交易日期 |
| `TRADE_PRICE` | float | 成交价格（元） |
| `TRADE_VOLUME` | float | 成交数量 |
| `TRADE_AMT` | float | 成交金额（元） |
| `PREMIUM_RATIO` | float | 溢价率 (%) |
| `BUYER_NAME` | str | 买方营业部名称 |
| `SELLER_NAME` | str | 卖方营业部名称 |

---

## 使用示例

```python
import AmazingData as ad

ad.login(username='user', password='pass', host='host', port=port)

info_data = ad.InfoData()
base_data = ad.BaseData()

# 获取 A 股代码列表
code_list = base_data.get_code_list(security_type='EXTRA_STOCK_A')
local_path = '/path/to/data'

# 获取龙虎榜数据
top_list = info_data.get_top_list(
    code_list,
    local_path,
    is_local=False
)

# 获取大宗交易数据
block_trading = info_data.get_block_trading(
    code_list,
    local_path,
    is_local=False
)

# 查看特定股票的龙虎榜数据
code = '000001.SZ'
if code in top_list:
    df = top_list[code]
    print(f"{code} 龙虎榜数据:")
    print(df.tail(10))
```

---

## 相关文档

- [融资融券数据](08-margin-trading.md)
- [实时行情数据](03-realtime-market.md)
