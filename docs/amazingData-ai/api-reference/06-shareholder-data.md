# 股东股本数据接口 (Shareholder Data)

## 概述

股东股本数据接口提供股东户数、股本结构、股权冻结/质押、限售股解禁等数据。

## InfoData 类方法

---

### get_top_10_holders - 十大股东数据

**函数接口**：`get_top_10_holders`

**功能描述**：获取指定股票列表的十大股东数据

**函数签名**：
```python
get_top_10_holders(code_list: list[str], local_path: str, is_local: bool = True,
                   begin_date: int = None, end_date: int = None) -> dict
```

**输入参数**：

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `code_list` | list[str] | 是 | 支持沪深 A 股的代码列表 |
| `local_path` | str | 是 | 本地存储路径 |
| `is_local` | bool | 否 | 是否使用本地缓存 |
| `begin_date` | int | 否 | 开始日期 |
| `end_date` | int | 否 | 结束日期 |

**输出参数**：

| 类型 | 描述 |
|------|------|
| dict | key: 证券代码，value: DataFrame（十大股东数据） |

**主要字段**：

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `MARKET_CODE` | str | 证券代码 |
| `SECURITY_NAME` | str | 证券简称 |
| `HOLDER_NAME` | str | 股东名称 |
| `HOLD_SHARES` | float | 持股数量 |
| `HOLD_RATIO` | float | 持股比例 (%) |
| `SHARE_TYPE` | str | 股份类型 |
| `CHANGE_REASON` | str | 变动原因 |

---

### get_shareholder_count - 股东户数

**函数接口**：`get_shareholder_count`

**功能描述**：获取指定股票列表的股东户数数据

**函数签名**：
```python
get_shareholder_count(code_list: list[str], local_path: str, is_local: bool = True,
                      begin_date: int = None, end_date: int = None) -> dict
```

**输出参数**：

| 类型 | 描述 |
|------|------|
| dict | key: 证券代码，value: DataFrame（股东户数数据） |

**主要字段**：

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `MARKET_CODE` | str | 证券代码 |
| `SECURITY_NAME` | str | 证券简称 |
| `SHAREHOLDER_COUNT` | int | 股东户数 |
| `AVG_HOLDING` | float | 户均持股数 |
| `CHANGE_RATIO` | float | 较上期变化率 (%) |
| `TRADE_DATE` | str | 交易日期 |

---

### get_capital_structure - 股本结构

**函数接口**：`get_capital_structure`

**功能描述**：获取指定股票列表的股本结构数据

**函数签名**：
```python
get_capital_structure(code_list: list[str], local_path: str, is_local: bool = True,
                      begin_date: int = None, end_date: int = None) -> dict
```

**输出参数**：

| 类型 | 描述 |
|------|------|
| dict | key: 证券代码，value: DataFrame（股本结构数据） |

**主要字段**：

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `MARKET_CODE` | str | 证券代码 |
| `SECURITY_NAME` | str | 证券简称 |
| `TOTAL_SHARES` | float | 总股本 |
| `LISTED_SHARES` | float | 已上市流通股本 |
| `NON_LISTED_SHARES` | float | 未上市流通股本 |
| `TRADE_DATE` | str | 交易日期 |

---

### get_equity_freeze - 股权冻结/质押

**函数接口**：`get_equity_freeze`

**功能描述**：获取指定股票列表的股权冻结/质押数据

**函数签名**：
```python
get_equity_freeze(code_list: list[str], local_path: str, is_local: bool = True,
                  begin_date: int = None, end_date: int = None) -> dict
```

**输出参数**：

| 类型 | 描述 |
|------|------|
| dict | key: 证券代码，value: DataFrame（股权冻结/质押数据） |

**主要字段**：

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `MARKET_CODE` | str | 证券代码 |
| `SECURITY_NAME` | str | 证券简称 |
| `HOLDER_NAME` | str | 股东名称 |
| `FROZEN_SHARES` | float | 冻结股份数 |
| `FROZEN_RATIO` | float | 冻结比例 (%) |
| `FREEZE_DATE` | str | 冻结日期 |
| `UNFREEZE_DATE` | str | 解冻日期 |
| `FREEZE_REASON` | str | 冻结原因 |

---

### get_restricted_shares - 限售股解禁

**函数接口**：`get_restricted_shares`

**功能描述**：获取指定股票列表的限售股解禁数据

**函数签名**：
```python
get_restricted_shares(code_list: list[str], local_path: str, is_local: bool = True,
                      begin_date: int = None, end_date: int = None) -> dict
```

**输出参数**：

| 类型 | 描述 |
|------|------|
| dict | key: 证券代码，value: DataFrame（限售股解禁数据） |

**主要字段**：

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `MARKET_CODE` | str | 证券代码 |
| `SECURITY_NAME` | str | 证券简称 |
| `RELEASE_DATE` | str | 解禁日期 |
| `RELEASE_SHARES` | float | 解禁数量 |
| `RELEASE_RATIO` | float | 解禁比例 (%) |
| `HOLDER_NAME` | str | 股东名称 |
| `SHARE_TYPE` | str | 股份类型 |

---

## 使用示例

### 获取股东数据

```python
import AmazingData as ad

ad.login(username='user', password='pass', host='host', port=port)

info_data = ad.InfoData()
base_data = ad.BaseData()

# 获取 A 股代码列表
code_list = base_data.get_code_list(security_type='EXTRA_STOCK_A')
local_path = '/path/to/data'

# 获取十大股东数据
top_10_holders = info_data.get_top_10_holders(code_list[:100], local_path, is_local=False)

# 获取股东户数数据
shareholder_count = info_data.get_shareholder_count(code_list[:100], local_path, is_local=False)

# 获取股本结构数据
capital_structure = info_data.get_capital_structure(code_list[:100], local_path, is_local=False)
```

### 分析特定公司的股东变化

```python
# 分析特定公司
code = '600519.SH'

# 获取股东户数变化
sh_count = info_data.get_shareholder_count([code], local_path, is_local=True)
if code in sh_count:
    df = sh_count[code]
    print(f"{code} 股东户数变化:")
    print(df[['TRADE_DATE', 'SHAREHOLDER_COUNT', 'CHANGE_RATIO']].tail(10))

# 获取限售股解禁信息
restricted = info_data.get_restricted_shares([code], local_path, is_local=True)
if code in restricted:
    print(f"\n{code} 限售股解禁:")
    print(restricted[code].tail())
```

---

## 相关文档

- [股东权益数据](07-shareholder-equity.md)
- [财务数据](05-financial-data.md)
