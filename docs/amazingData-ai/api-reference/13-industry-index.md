# 行业指数数据接口 (Industry Index Data)

## 概述

行业指数数据接口提供行业指数的基本信息、成分股、权重和行情数据。

## InfoData 类方法

---

### get_industry_base_info - 行业指数基本信息

**函数接口**：`get_industry_base_info`

**功能描述**：获取行业指数的基本信息数据

**函数签名**：
```python
get_industry_base_info(local_path: str, is_local: bool = True) -> pd.DataFrame
```

**输入参数**：

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `local_path` | str | 是 | 本地存储路径 |
| `is_local` | bool | 否 | 是否使用本地缓存 |

**输出参数**：

| 类型 | 描述 |
|------|------|
| DataFrame | 行业指数基本信息 |

**主要字段**：

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `INDEX_CODE` | str | 指数代码 |
| `INDUSTRY_CODE` | str | 行业代码 |
| `LEVEL_TYPE` | int | 指数类别（1: 一级，2: 二级，3: 三级） |
| `LEVEL1_NAME` | str | 一级行业名称 |
| `LEVEL2_NAME` | str | 二级行业名称 |
| `LEVEL3_NAME` | str | 三级行业名称 |
| `IS_PUB` | int | 是否发布（1: 已发布，2: 未发布） |

**使用示例**：
```python
import AmazingData as ad

ad.login(username='user', password='pass', host='host', port=port)

info_data = ad.InfoData()
local_path = '/path/to/data'

# 获取行业指数基本信息
industry_base = info_data.get_industry_base_info(local_path, is_local=False)
print(f"行业指数数量：{len(industry_base)}")

# 查看一级行业
level1 = industry_base[industry_base['LEVEL_TYPE'] == 1]
print("\n一级行业:")
print(level1[['INDEX_CODE', 'LEVEL1_NAME']])
```

---

### get_industry_constituent - 行业指数成分股

**函数接口**：`get_industry_constituent`

**功能描述**：获取指定行业指数列表的成分股数据

**函数签名**：
```python
get_industry_constituent(code_list: list[str], local_path: str, is_local: bool = True) -> dict
```

**输入参数**：

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `code_list` | list[str] | 是 | 行业指数代码列表（从 `get_industry_base_info` 获取） |
| `local_path` | str | 是 | 本地存储路径 |
| `is_local` | bool | 否 | 是否使用本地缓存 |

**输出参数**：

| 类型 | 描述 |
|------|------|
| dict | key: 行业指数代码，value: DataFrame（成分股数据） |

**主要字段**：

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `INDEX_CODE` | str | 指数代码 |
| `CON_CODE` | str | 成份股代码 |
| `INDATE` | str | 纳入日期 |
| `OUTDATE` | str | 剔除日期 |
| `INDEX_NAME` | str | 指数名称 |

---

### get_industry_weight - 行业指数成分股权重

**函数接口**：`get_industry_weight`

**功能描述**：获取指定行业指数列表的成分股日权重数据

**函数签名**：
```python
get_industry_weight(code_list: list[str], local_path: str, is_local: bool = True,
                    begin_date: int = None, end_date: int = None) -> dict
```

**输出参数**：

| 类型 | 描述 |
|------|------|
| dict | key: 行业指数代码，value: DataFrame（权重数据） |

**主要字段**：

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `WEIGHT` | float | 权重（%） |
| `CON_CODE` | str | 成份股代码 |
| `TRADE_DATE` | str | 交易日期 |
| `INDEX_CODE` | str | 指数代码 |

---

### get_industry_daily - 行业指数日行情

**函数接口**：`get_industry_daily`

**功能描述**：获取指定行业指数列表的日行情数据

**函数签名**：
```python
get_industry_daily(code_list: list[str], local_path: str, is_local: bool = True,
                   begin_date: int = None, end_date: int = None) -> dict
```

**输出参数**：

| 类型 | 描述 |
|------|------|
| dict | key: 行业指数代码，value: DataFrame（行情数据） |

**主要字段**：

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `OPEN` | float | 开盘价 |
| `HIGH` | float | 最高价 |
| `CLOSE` | float | 收盘价 |
| `LOW` | float | 最低价 |
| `AMOUNT` | float | 成交金额（元） |
| `VOLUME` | float | 成交量（股） |
| `PB` | float | 指数市净率 |
| `PE` | float | 指数市盈率 |
| `TOTAL_CAP` | float | 总市值（万元） |
| `A_FLOAT_CAP` | float | A 股流通市值（万元） |
| `INDEX_CODE` | str | 指数代码 |
| `TRADE_DATE` | str | 交易日期 |

---

## 使用示例

### 获取行业指数全部数据

```python
import AmazingData as ad

ad.login(username='user', password='pass', host='host', port=port)

info_data = ad.InfoData()
local_path = '/path/to/data'

# 1. 获取行业指数基本信息
industry_base = info_data.get_industry_base_info(local_path, is_local=False)
industry_codes = list(industry_base['INDEX_CODE'])

# 2. 获取行业指数成分股
industry_constituent = info_data.get_industry_constituent(industry_codes, local_path, is_local=False)

# 3. 获取行业指数权重
industry_weight = info_data.get_industry_weight(industry_codes, local_path, is_local=False)

# 4. 获取行业指数行情
industry_daily = info_data.get_industry_daily(industry_codes, local_path, is_local=False)

# 分析特定行业
# 获取一级行业代码
level1_codes = industry_base[industry_base['LEVEL_TYPE'] == 1]['INDEX_CODE'].tolist()

for code in level1_codes[:5]:  # 前 5 个一级行业
    if code in industry_daily:
        df = industry_daily[code]
        print(f"\n{code} 行情数据:")
        print(df[['TRADE_DATE', 'CLOSE', 'PE', 'TOTAL_CAP']].tail())
```

---

## 相关文档

- [交易所指数数据](12-index-data.md)
- [基础数据接口](02-base-data.md)
