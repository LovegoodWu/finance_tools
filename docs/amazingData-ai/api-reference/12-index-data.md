# 交易所指数数据接口 (Index Data)

## 概述

交易所指数数据接口提供交易所指数的成分股和权重数据。

## InfoData 类方法

---

### get_index_constituent - 指数成分股

**函数接口**：`get_index_constituent`

**功能描述**：获取指定交易所指数列表的成分股数据

**函数签名**：
```python
get_index_constituent(code_list: list[str], local_path: str, is_local: bool = True) -> dict
```

**输入参数**：

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `code_list` | list[str] | 是 | 支持沪深指数的代码列表 |
| `local_path` | str | 是 | 本地存储路径 |
| `is_local` | bool | 否 | 是否使用本地缓存 |

**输出参数**：

| 类型 | 描述 |
|------|------|
| dict | key: 指数代码，value: DataFrame（成分股数据） |

**主要字段**：

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `INDEX_CODE` | str | 指数代码 |
| `CON_CODE` | str | 成份股代码 |
| `INDATE` | str | 纳入日期 |
| `OUTDATE` | str | 剔除日期（未剔除时为 nan） |
| `INDEX_NAME` | str | 指数名称 |

**使用示例**：
```python
import AmazingData as ad

ad.login(username='user', password='pass', host='host', port=port)

info_data = ad.InfoData()
base_data = ad.BaseData()

# 获取指数代码列表
index_codes = base_data.get_code_list(security_type='EXTRA_INDEX_A')

# 获取指数成分股数据
index_constituent = info_data.get_index_constituent(index_codes, is_local=False)

# 查看沪深 300 成分股
if '000300.SH' in index_constituent:
    df = index_constituent['000300.SH']
    print("沪深 300 成分股:")
    print(df[['CON_CODE', 'INDATE']].head(20))
```

---

### get_index_weight - 指数成分股权重

**函数接口**：`get_index_weight`

**功能描述**：获取指定交易所指数的成分股日权重数据

**函数签名**：
```python
get_index_weight(code_list: list[str], local_path: str, is_local: bool = True,
                 begin_date: int = None, end_date: int = None) -> dict
```

**输入参数**：

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `code_list` | list[str] | 是 | 指数代码列表（仅支持以下 5 个指数） |
| `local_path` | str | 是 | 本地存储路径 |
| `is_local` | bool | 否 | 是否使用本地缓存 |
| `begin_date` | int | 否 | 开始日期 |
| `end_date` | int | 否 | 结束日期 |

**支持的指数**：

| 指数名称 | 代码 |
|----------|------|
| 上证 50 | 000016.SH |
| 沪深 300 | 000300.SH |
| 中证 500 | 000905.SH |
| 中证 800 | 000906.SH |
| 中证 1000 | 000852.SH |

**输出参数**：

| 类型 | 描述 |
|------|------|
| dict | key: 指数代码，value: DataFrame（权重数据） |

**主要字段**：

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `INDEX_CODE` | str | 指数代码 |
| `CON_CODE` | str | 标的代码 |
| `TRADE_DATE` | str | 生效日期 |
| `TOTAL_SHARE` | float | 总股本（股） |
| `FREE_SHARE_RATIO` | float | 自由流通比例（%） |
| `CALC_SHARE` | float | 计算用股本（股） |
| `WEIGHT_FACTOR` | float | 权重因子 |
| `WEIGHT` | float | 权重（%） |
| `CLOSE` | float | 收盘价 |

**使用示例**：
```python
# 获取主要指数权重
index_weights = info_data.get_index_weight(
    ['000016.SH', '000300.SH', '000905.SH', '000906.SH', '000852.SH'],
    local_path='/path/to/data',
    is_local=False
)

# 查看沪深 300 权重
if '000300.SH' in index_weights:
    df = index_weights['000300.SH']
    print("沪深 300 成分股权重:")
    print(df[['TRADE_DATE', 'CON_CODE', 'WEIGHT']].tail(20))
```

---

## 使用示例

### 获取指数数据并分析

```python
import AmazingData as ad

ad.login(username='user', password='pass', host='host', port=port)

info_data = ad.InfoData()
base_data = ad.BaseData()

# 获取指数代码列表
index_codes = base_data.get_code_list(security_type='EXTRA_INDEX_A')
local_path = '/path/to/data'

# 获取指数成分股
index_constituent = info_data.get_index_constituent(index_codes, local_path, is_local=False)

# 获取指数权重
index_weights = info_data.get_index_weight(
    ['000016.SH', '000300.SH', '000905.SH'],
    local_path,
    is_local=False
)

# 分析沪深 300 成分股变化
if '000300.SH' in index_constituent:
    df = index_constituent['000300.SH']
    
    # 当前成分股
    current = df[df['OUTDATE'].isna()]
    print(f"沪深 300 当前成分股数量：{len(current)}")
    
    # 历史调入调出
    changes = df[df['OUTDATE'].notna()]
    print(f"历史调出次数：{len(changes)}")
```

---

## 相关文档

- [行业指数数据](13-industry-index.md)
- [基础数据接口](02-base-data.md)
