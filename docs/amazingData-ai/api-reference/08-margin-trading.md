# 融资融券数据接口 (Margin Trading)

## 概述

融资融券数据接口提供融资融券成交汇总和交易明细数据。

## InfoData 类方法

---

### get_margin_trading_summary - 融资融券成交汇总

**函数接口**：`get_margin_trading_summary`

**功能描述**：获取融资融券成交汇总数据

**函数签名**：
```python
get_margin_trading_summary(code_list: list[str], local_path: str, is_local: bool = True,
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
| dict | key: 证券代码，value: DataFrame（融资融券汇总数据） |

**主要字段**：

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `MARKET_CODE` | str | 证券代码 |
| `SECURITY_NAME` | str | 证券简称 |
| `TRADE_DATE` | str | 交易日期 |
| `FIN_BUY_AMT` | float | 融资买入额（元） |
| `FIN_REPAY_AMT` | float | 融资偿还额（元） |
| `FIN_BALANCE` | float | 融资余额（元） |
| `SFT_SELL_AMT` | float | 融券卖出量 |
| `SFT_REPAY_AMT` | float | 融券偿还量 |
| `SFT_BALANCE` | float | 融券余量 |

---

### get_margin_trading_detail - 融资融券交易明细

**函数接口**：`get_margin_trading_detail`

**功能描述**：获取融资融券交易明细数据

**函数签名**：
```python
get_margin_trading_detail(code_list: list[str], local_path: str, is_local: bool = True,
                          begin_date: int = None, end_date: int = None) -> dict
```

**输出参数**：

| 类型 | 描述 |
|------|------|
| dict | key: 证券代码，value: DataFrame（融资融券明细数据） |

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

# 获取融资融券汇总数据
margin_summary = info_data.get_margin_trading_summary(
    code_list[:100],
    local_path,
    is_local=False
)

# 查看特定股票的融资融券数据
code = '000001.SZ'
if code in margin_summary:
    df = margin_summary[code]
    print(f"{code} 融资融券数据:")
    print(df.tail(10))
```

---

## 相关文档

- [交易异动数据](09-trading-anomaly.md)
- [基础数据接口](02-base-data.md)
