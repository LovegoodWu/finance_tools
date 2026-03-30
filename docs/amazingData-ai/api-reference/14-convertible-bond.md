# 可转债数据接口 (Convertible Bond Data)

## 概述

可转债数据接口提供可转债的发行、份额、转股、修正、赎回、回售等数据。

## InfoData 类方法

---

### get_kzz_issuance - 可转债发行数据

**函数接口**：`get_kzz_issuance`

**功能描述**：获取指定可转债列表的发行数据

**函数签名**：
```python
get_kzz_issuance(code_list: list[str], local_path: str, is_local: bool = True) -> dict
```

**主要字段**：

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `MARKET_CODE` | str | 市场代码 |
| `STOCK_CODE` | str | 正股代码 |
| `LISTED_DATE` | str | 上市日期 |
| `LIST_ISSUE_SIZE` | float | 发行规模（万元） |
| `TERM_YEAR` | float | 债券期限（年） |
| `COUPON_RATE` | float | 利率（%） |
| `CLAUSE_INI_CONV_PRICE` | float | 初始转换价格 |
| `CLAUSE_PUT_ITEM` | str | 回售条款 |
| `CLAUSE_CALL_ITEM` | str | 赎回条款 |

---

### get_kzz_share - 可转债份额数据

**函数接口**：`get_kzz_share`

**功能描述**：获取指定可转债列表的份额数据

**函数签名**：
```python
get_kzz_share(code_list: list[str], local_path: str, is_local: bool = True) -> dict
```

**主要字段**：

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `CHANGE_DATE` | str | 变动日期 |
| `BOND_SHARE` | float | 债券份额（万元） |
| `CONV_SHARE` | float | 已转成股份数 |
| `CHANGE_REASON` | str | 变动原因 |

---

### get_kzz_conv - 可转债转股数据

**函数接口**：`get_kzz_conv`

**功能描述**：获取指定可转债列表的转股数据

**函数签名**：
```python
get_kzz_conv(code_list: list[str], local_path: str, is_local: bool = True) -> dict
```

**主要字段**：

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `CONV_PRICE` | float | 转股价格 |
| `CONV_START_DATE` | str | 自愿转换期起始日 |
| `CONV_END_DATE` | str | 自愿转换期截止日 |
| `FORCED_CONV_DATE` | str | 强制转换日 |

---

### get_kzz_conv_change - 可转债转股变动数据

**函数接口**：`get_kzz_conv_change`

**功能描述**：获取指定可转债列表的转股变动数据

**函数签名**：
```python
get_kzz_conv_change(code_list: list[str], local_path: str, is_local: bool = True) -> dict
```

**主要字段**：

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `CHANGE_DATE` | str | 变动日期 |
| `CONV_PRICE` | float | 转股价格 |
| `CHANGE_REASON` | str | 变动原因 |

---

### get_kzz_corr - 可转债修正数据

**函数接口**：`get_kzz_corr`

**功能描述**：获取指定可转债列表的修正数据

**函数签名**：
```python
get_kzz_corr(code_list: list[str], local_path: str, is_local: bool = True) -> dict
```

**主要字段**：

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `START_DATE` | str | 特别修正起始时间 |
| `END_DATE` | str | 特别修正结束时间 |
| `SPEC_CORR_TRIG_RATIO` | float | 特别修正触发比例（%） |
| `CORR_TIMES_LIMIT` | str | 修正次数限制 |

---

### get_kzz_call - 可转债赎回数据

**函数接口**：`get_kzz_call`

**功能描述**：获取指定可转债列表的赎回数据

**函数签名**：
```python
get_kzz_call(code_list: list[str], local_path: str, is_local: bool = True) -> dict
```

**主要字段**：

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `CALL_PRICE` | float | 赎回价 |
| `BEGIN_DATE` | str | 起始日期 |
| `END_DATE` | str | 截止日期 |
| `TRI_RATIO` | float | 触发比例（%） |

---

### get_kzz_put - 可转债回售数据

**函数接口**：`get_kzz_put`

**功能描述**：获取指定可转债列表的回售数据

**函数签名**：
```python
get_kzz_put(code_list: list[str], local_path: str, is_local: bool = True) -> dict
```

**主要字段**：

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `PUT_PRICE` | float | 回售价 |
| `BEGIN_DATE` | str | 起始日期 |
| `END_DATE` | str | 截止日期 |
| `TRI_RATIO` | float | 触发比例（%） |

---

### get_kzz_put_call_item - 可转债回售赎回条款

**函数接口**：`get_kzz_put_call_item`

**功能描述**：获取指定可转债列表的回售赎回条款数据

**函数签名**：
```python
get_kzz_put_call_item(code_list: list[str], local_path: str, is_local: bool = True) -> dict
```

**主要字段**：

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `MAND_PUT_PERIOD` | str | 无条件回售期 |
| `MAND_PUT_PRICE` | float | 无条件回售价 |
| `CON_CALL_START_DATE` | str | 有条件赎回起始日期 |
| `CALL_TRI_CON_INS` | str | 赎回触发条件说明 |
| `IS_CALL_ITEM` | int | 是否有赎回条款 |
| `IS_PUT_ITEM` | int | 是否有回售条款 |

---

### get_kzz_suspend - 可转债停复牌信息

**函数接口**：`get_kzz_suspend`

**功能描述**：获取指定可转债列表的停复牌信息

**函数签名**：
```python
get_kzz_suspend(code_list: list[str], local_path: str, is_local: bool = True) -> dict
```

**主要字段**：

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `SUSPEND_DATE` | str | 停牌日期 |
| `SUSPEND_TYPE` | int | 停牌类型 |
| `RESUMP_DATE` | str | 复牌日期 |
| `CHANGE_REASON` | str | 停牌原因 |

---

## 使用示例

```python
import AmazingData as ad

ad.login(username='user', password='pass', host='host', port=port)

info_data = ad.InfoData()
base_data = ad.BaseData()

# 获取可转债代码列表
kzz_codes = base_data.get_code_list(security_type='EXTRA_KZZ')
local_path = '/path/to/data'

# 获取可转债发行数据
kzz_issuance = info_data.get_kzz_issuance(kzz_codes, local_path, is_local=False)

# 获取可转债转股数据
kzz_conv = info_data.get_kzz_conv(kzz_codes, local_path, is_local=False)

# 查看特定可转债的数据
code = '110034.SH'
if code in kzz_issuance:
    df = kzz_issuance[code]
    print(f"{code} 发行数据:")
    print(df[['LISTED_DATE', 'LIST_ISSUE_SIZE', 'TERM_YEAR', 'COUPON_RATE']])

if code in kzz_conv:
    df = kzz_conv[code]
    print(f"\n{code} 转股数据:")
    print(df[['CONV_PRICE', 'CONV_START_DATE', 'CONV_END_DATE']])
```

---

## 相关文档

- [基础数据接口](02-base-data.md)
- [国债收益率数据](15-treasury-yield.md)
