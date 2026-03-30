# ETF 数据接口 (ETF Data)

## 概述

ETF 数据接口提供 ETF 的申赎数据、基金份额、收盘 IOPV 等信息。

## InfoData 类方法

---

### get_etf_pcf - ETF 申赎数据

**函数接口**：`get_etf_pcf`

**功能描述**：获取指定 ETF 的申赎和成分股数据（沪深交易所的 ETF）

**函数签名**：
```python
get_etf_pcf(code_list: list[str]) -> tuple[pd.DataFrame, dict]
```

**输入参数**：

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `code_list` | list[str] | 是 | 支持沪深 ETF 的代码列表 |

**输出参数**：

| 类型 | 描述 |
|------|------|
| tuple | `(etf_pcf_info, etf_pcf_constituent)` |
| `etf_pcf_info` | DataFrame | ETF 申赎信息 |
| `etf_pcf_constituent` | dict | key: ETF 代码，value: DataFrame（成分股数据） |

**etf_pcf_info 主要字段**：

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `creation_redemption_unit` | int | 每个篮子对应的 ETF 份数 |
| `max_cash_ratio` | str | 最大现金替代比例 |
| `publish` | str | 是否发布 IOPV（Y/N） |
| `creation` | str | 是否允许申购（Y/N） |
| `redemption` | str | 是否允许赎回（Y/N） |
| `estimate_cash_component` | int | 预估现金差额 |
| `trading_day` | int | 当前交易日 |
| `cash_component` | int | 前一日现金差额 |
| `nav_per_cu` | int | 前一日最小申赎单位净值 |
| `nav` | int | 前一日基金份额净值 |

**etf_pcf_constituent 主要字段**：

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `underlying_symbol` | str | 成份证券简称 |
| `component_share` | int | 成份证券数量 |
| `substitute_flag` | str | 现金替代标志 |
| `premium_ratio` | int | 溢价比例 |
| `discount_ratio` | int | 折价比例 |

**使用示例**：
```python
import AmazingData as ad

ad.login(username='user', password='pass', host='host', port=port)

base_data = ad.BaseData()
info_data = ad.InfoData()

# 获取 ETF 代码列表
etf_codes = base_data.get_code_list(security_type='EXTRA_ETF')

# 获取 ETF 申赎数据
etf_pcf_info, etf_pcf_constituent = base_data.get_etf_pcf(etf_codes)

print("ETF 申赎信息:")
print(etf_pcf_info.head())

# 查看特定 ETF 的成分股
etf_code = '510050.SH'
if etf_code in etf_pcf_constituent:
    print(f"\n{etf_code} 成分股:")
    print(etf_pcf_constituent[etf_code].head())
```

---

### get_fund_share - ETF 基金份额

**函数接口**：`get_fund_share`

**功能描述**：获取指定 ETF 列表的基金份额数据

**函数签名**：
```python
get_fund_share(code_list: list[str], local_path: str, is_local: bool = True,
               begin_date: int = None, end_date: int = None) -> dict
```

**输入参数**：

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `code_list` | list[str] | 是 | ETF 代码列表 |
| `local_path` | str | 是 | 本地存储路径 |
| `is_local` | bool | 否 | 是否使用本地缓存 |
| `begin_date` | int | 否 | 开始日期 |
| `end_date` | int | 否 | 结束日期 |

**输出参数**：

| 类型 | 描述 |
|------|------|
| dict | key: ETF 代码，value: DataFrame（基金份额数据） |

**主要字段**：

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `FUND_SHARE` | float | 基金份额（万份） |
| `CHANGE_REASON` | str | 份额变动原因 |
| `CHANGE_DATE` | str | 变动日期 |
| `TOTAL_SHARE` | float | 基金总份额（万份） |
| `FLOAT_SHARE` | float | 流通份额（万份） |

---

### get_fund_iopv - ETF 收盘 IOPV

**函数接口**：`get_fund_iopv`

**功能描述**：获取指定 ETF 的每日收盘 IOPV 数据

**函数签名**：
```python
get_fund_iopv(code_list: list[str], local_path: str, is_local: bool = True,
              begin_date: int = None, end_date: int = None) -> dict
```

**输出参数**：

| 类型 | 描述 |
|------|------|
| dict | key: ETF 代码，value: DataFrame（IOPV 数据） |

**主要字段**：

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `MARKET_CODE` | str | 市场代码 |
| `PRICE_DATE` | str | 日期 |
| `IOPV_NAV` | float | IOPV 收盘净值 |

---

## 使用示例

### 获取 ETF 全部数据

```python
import AmazingData as ad

ad.login(username='user', password='pass', host='host', port=port)

base_data = ad.BaseData()
info_data = ad.InfoData()

# 获取 ETF 代码列表
etf_codes = base_data.get_code_list(security_type='EXTRA_ETF')
local_path = '/path/to/data'

# 获取 ETF 申赎数据
etf_pcf_info, etf_pcf_constituent = base_data.get_etf_pcf(etf_codes)

# 获取 ETF 份额数据
fund_share = info_data.get_fund_share(etf_codes, local_path, is_local=False)

# 获取 ETF IOPV 数据
fund_iopv = info_data.get_fund_iopv(etf_codes, local_path, is_local=False)

# 分析特定 ETF
etf_code = '510050.SH'

if etf_code in fund_share:
    df = fund_share[etf_code]
    print(f"{etf_code} 份额变化:")
    print(df[['CHANGE_DATE', 'FUND_SHARE', 'CHANGE_REASON']].tail(10))

if etf_code in fund_iopv:
    df = fund_iopv[etf_code]
    print(f"\n{etf_code} IOPV 数据:")
    print(df.tail())
```

---

## 相关文档

- [期权数据](10-option-data.md)
- [实时行情数据](03-realtime-market.md)
