# 期权数据接口 (Option Data)

## 概述

期权数据接口提供 ETF 期权的基本资料、标准合约属性等信息。

## InfoData 类方法

---

### get_option_std_ctr_specs - 期权标准合约属性

**函数接口**：`get_option_std_ctr_specs`

**功能描述**：获取期权标准合约属性（沪深交易所的 ETF 期权）

**函数签名**：
```python
get_option_std_ctr_specs(code_list: list[str], is_local: bool = True) -> pd.DataFrame
```

**输入参数**：

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `code_list` | list[str] | 是 | 支持沪深 ETF 期权的代码列表 |
| `is_local` | bool | 否 | 是否使用本地缓存 |

**输出参数**：

| 类型 | 描述 |
|------|------|
| DataFrame | 期权标准合约属性数据 |

**主要字段**：

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `MARKET_CODE` | str | 市场代码 |
| `OPTION_NAME` | str | 期权名称 |
| `OPTION_TYPE` | str | 期权类型（认购/认沽） |
| `EXERCISE_PRICE` | float | 行权价（元） |
| `EXERCISE_DATE` | str | 行权日 |
| `CONTRACT_UNIT` | int | 合约单位 |
| `LAST_TRADING_DATE` | str | 最后交易日 |
| `LISTED_DATE` | str | 上市日期 |
| `CONTRACT_VALUE` | float | 合约价值 |
| `PREMIUM` | str | 期权金 |
| `EXERCISE_METHOD` | str | 行权方式 |
| `DELIVERY_METHOD` | str | 交割方式 |

**使用示例**：
```python
import AmazingData as ad

ad.login(username='user', password='pass', host='host', port=port)

info_data = ad.InfoData()
base_data = ad.BaseData()

# 获取 ETF 期权代码列表
option_code_list = base_data.get_option_code_list(security_type='EXTRA_ETF_OP')

# 获取期权标准合约属性
option_specs = info_data.get_option_std_ctr_specs(option_code_list, is_local=False)
print(option_specs.head())
```

---

### get_option_mon_ctr_specs - 期权月合约属性变动

**函数接口**：`get_option_mon_ctr_specs`

**功能描述**：获取期权月合约属性变动

**函数签名**：
```python
get_option_mon_ctr_specs(code_list: list[str], local_path: str, is_local: bool = True) -> pd.DataFrame
```

**输入参数**：

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `code_list` | list[str] | 是 | 期权代码列表 |
| `local_path` | str | 是 | 本地存储路径 |
| `is_local` | bool | 否 | 是否使用本地缓存 |

**输出参数**：

| 类型 | 描述 |
|------|------|
| DataFrame | 期权月合约属性变动数据 |

**主要字段**：

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `MARKET_CODE` | str | 市场代码 |
| `CODE_OLD` | str | 原交易代码 |
| `CODE_NEW` | str | 新交易代码 |
| `NAME_OLD` | str | 原合约简称 |
| `NAME_NEW` | str | 新合约简称 |
| `EXERCISE_PRICE_OLD` | float | 原行权价（元） |
| `EXERCISE_PRICE_NEW` | float | 新行权价（元） |
| `UNIT_OLD` | float | 原合约单位（股） |
| `UNIT_NEW` | float | 新合约单位（股） |
| `CHANGE_DATE` | str | 调整日期 |
| `CHANGE_REASON` | str | 调整原因 |

---

## 使用示例

### 获取期权数据

```python
import AmazingData as ad

ad.login(username='user', password='pass', host='host', port=port)

info_data = ad.InfoData()
base_data = ad.BaseData()

# 获取 ETF 期权代码列表
option_codes = base_data.get_option_code_list(security_type='EXTRA_ETF_OP')
print(f"ETF 期权数量：{len(option_codes)}")

# 获取期权标准合约属性
option_specs = info_data.get_option_std_ctr_specs(option_codes, is_local=False)

# 查看特定 ETF 的期权合约
underlying = '510050.SH'  # 华夏上证 50ETF
underlying_options = option_specs[option_specs['UNDERLYING'] == underlying]
print(f"\n{underlying} 的期权合约:")
print(underlying_options[['OPTION_NAME', 'OPTION_TYPE', 'EXERCISE_PRICE', 'EXERCISE_DATE']])
```

---

## 相关文档

- [ETF 数据](11-etf-data.md)
- [实时行情数据](03-realtime-market.md)
- [代码类型说明](../appendix/security-type.md)
