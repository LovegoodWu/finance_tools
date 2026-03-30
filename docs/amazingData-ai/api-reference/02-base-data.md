# 基础数据接口 (Base Data)

## 概述

基础数据接口提供证券信息、代码表、交易日历、复权因子等基础金融数据。

## 类和方法

| 类名 | 描述 |
|------|------|
| `BaseData` | 基础数据查询类 |
| `InfoData` | 信息数据查询类 |

---

## BaseData 类

### get_code_list

**功能描述**：获取指定类型的证券代码列表

**函数签名**：
```python
get_code_list(security_type: str) -> list[str]
```

**输入参数**：

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `security_type` | str | 是 | 代码类型，见 [`security_type`](../appendix/security-type.md) |

**输出参数**：

| 类型 | 描述 |
|------|------|
| list[str] | 证券代码列表 |

**常用 security_type 值**：

| 值 | 描述 |
|----|------|
| `EXTRA_STOCK_A` | 上交所 A 股、深交所 A 股和北交所的股票列表 |
| `EXTRA_INDEX_A` | 上交所、深交所和北交所的指数列表 |
| `EXTRA_ETF` | 上交所、深交所的 ETF 列表 |
| `EXTRA_KZZ` | 上交所、深交所的可转债列表 |
| `EXTRA_HKT` | 沪深港通 |
| `EXTRA_FUTURE` | 期货（中金所） |
| `EXTRA_ETF_OP` | ETF 期权（上交所/深交所） |

**使用示例**：
```python
import AmazingData as ad

ad.login(username='user', password='pass', host='host', port=port)

base_data = ad.BaseData()

# 获取 A 股代码列表
stock_codes = base_data.get_code_list(security_type='EXTRA_STOCK_A')

# 获取 ETF 代码列表
etf_codes = base_data.get_code_list(security_type='EXTRA_ETF')
```

---

### get_hist_code_list

**功能描述**：获取历史证券代码列表（包含已退市的证券）

**函数签名**：
```python
get_hist_code_list(security_type: str, start_date: int, end_date: int) -> list[str]
```

**输入参数**：

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `security_type` | str | 是 | 代码类型 |
| `start_date` | int | 是 | 开始日期，格式 YYYYMMDD |
| `end_date` | int | 是 | 结束日期，格式 YYYYMMDD |

**输出参数**：

| 类型 | 描述 |
|------|------|
| list[str] | 历史证券代码列表 |

**使用示例**：
```python
base_data = ad.BaseData()
calendar = base_data.get_calendar()
today = calendar[-1]

# 获取历史 A 股代码列表
hist_codes = base_data.get_hist_code_list(
    security_type='EXTRA_STOCK_A_SH_SZ',
    start_date=20130101,
    end_date=today
)
```

---

### get_calendar

**功能描述**：获取交易日历

**函数签名**：
```python
get_calendar() -> list[int]
```

**输出参数**：

| 类型 | 描述 |
|------|------|
| list[int] | 交易日期列表，格式 YYYYMMDD |

**使用示例**：
```python
base_data = ad.BaseData()
calendar = base_data.get_calendar()
print(f"最新交易日：{calendar[-1]}")
```

---

### get_option_code_list

**功能描述**：获取期权代码列表

**函数签名**：
```python
get_option_code_list(security_type: str) -> list[str]
```

**输入参数**：

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `security_type` | str | 是 | 期权代码类型，如 `EXTRA_ETF_OP` |

**输出参数**：

| 类型 | 描述 |
|------|------|
| list[str] | 期权代码列表 |

---

## InfoData 类

### get_bj_code_mapping

**功能描述**：获取北交所新旧代码对照表

**函数签名**：
```python
get_bj_code_mapping() -> pd.DataFrame
```

**输出参数字段**：

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `OLD_CODE` | str | 旧代码 |
| `NEW_CODE` | str | 新代码 |
| `SECURITY_NAME` | str | 证券简称 |
| `LISTING_DATE` | int | 上市日期 |

**使用示例**：
```python
info_data = ad.InfoData()
bj_mapping = info_data.get_bj_code_mapping()
print(bj_mapping.head())
```

---

### get_reinstatement_factor

**功能描述**：获取复权因子数据（后复权因子）

**函数签名**：
```python
get_reinstatement_factor(code_list: list[str], local_path: str, is_local: bool = True, 
                         begin_date: int = None, end_date: int = None) -> dict
```

**输入参数**：

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `code_list` | list[str] | 是 | 证券代码列表 |
| `local_path` | str | 是 | 本地存储路径（绝对路径） |
| `is_local` | bool | 否 | 是否使用本地缓存，默认 True |
| `begin_date` | int | 否 | 开始日期 |
| `end_date` | int | 否 | 结束日期 |

**输出参数**：

| 类型 | 描述 |
|------|------|
| dict | key: 代码，value: DataFrame（复权因子数据） |

---

### get_single_reinstatement

**功能描述**：获取单次复权因子数据

**函数签名**：
```python
get_single_reinstatement(code_list: list[str], local_path: str, is_local: bool = True,
                         begin_date: int = None, end_date: int = None) -> dict
```

---

### get_security_info

**功能描述**：获取每日最新证券信息

**函数签名**：
```python
get_security_info(code_list: list[str]) -> pd.DataFrame
```

---

### get_hist_security_info

**功能描述**：获取历史证券信息

**函数签名**：
```python
get_hist_security_info(code_list: list[str], start_date: int, end_date: int,
                       local_path: str, is_local: bool = True) -> dict
```

---

## 数据结构

### 证券信息字段

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `MARKET_CODE` | str | 证券代码 |
| `SECURITY_NAME` | str | 证券简称 |
| `SECURITY_TYPE` | str | 证券类型 |
| `LISTING_DATE` | int | 上市日期 |
| `MARKET` | str | 所属市场 |

---

## 相关文档

- [代码类型说明](../appendix/security-type.md)
- [历史行情数据](04-historical-market.md)
