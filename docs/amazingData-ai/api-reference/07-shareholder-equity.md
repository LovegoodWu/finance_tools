# 股东权益数据接口 (Shareholder Equity)

## 概述

股东权益数据接口提供上市公司的分红数据和配股数据。

## InfoData 类方法

---

### get_dividend - 分红数据

**函数接口**：`get_dividend`

**功能描述**：获取指定股票列表的分红数据

**函数签名**：
```python
get_dividend(code_list: list[str], local_path: str, is_local: bool = True,
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
| dict | key: 证券代码，value: DataFrame（分红数据） |

**主要字段**：

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `MARKET_CODE` | str | 证券代码 |
| `SECURITY_NAME` | str | 证券简称 |
| `ANN_DATE` | str | 公告日期 |
| `RECORD_DATE` | str | 股权登记日 |
| `EX_DIVIDEND_DATE` | str | 除权除息日 |
| `DIVIDEND_PLAN` | str | 分红方案 |
| `CASH_DIVIDEND` | float | 每股派息（元） |
| `BONUS_SHARE` | float | 每股送股 |
| `CAP_RESV_TO_SHARE` | float | 每股转增股本 |
| `DIVIDEND_PROGRESS` | str | 分红进度 |

**分红进度代码**：

| 代码 | 描述 |
|------|------|
| 1 | 董事会预案 |
| 2 | 股东大会通过 |
| 3 | 实施 |
| 4 | 未通过 |

**使用示例**：
```python
import AmazingData as ad

ad.login(username='user', password='pass', host='host', port=port)

info_data = ad.InfoData()
base_data = ad.BaseData()

# 获取 A 股代码列表
code_list = base_data.get_code_list(security_type='EXTRA_STOCK_A')
local_path = '/path/to/data'

# 获取分红数据
dividend = info_data.get_dividend(code_list, local_path, is_local=False)

# 查看特定公司的分红历史
code = '600519.SH'
if code in dividend:
    df = dividend[code]
    print(f"{code} 分红历史:")
    print(df[['ANN_DATE', 'DIVIDEND_PLAN', 'CASH_DIVIDEND']].tail(10))
```

---

### get_rights_issue - 配股数据

**函数接口**：`get_rights_issue`

**功能描述**：获取指定股票列表的配股数据

**函数签名**：
```python
get_rights_issue(code_list: list[str], local_path: str, is_local: bool = True,
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
| dict | key: 证券代码，value: DataFrame（配股数据） |

**主要字段**：

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `MARKET_CODE` | str | 证券代码 |
| `SECURITY_NAME` | str | 证券简称 |
| `ANN_DATE` | str | 公告日期 |
| `RIGHTS_ISSUE_PLAN` | str | 配股方案 |
| `RIGHTS_ISSUE_RATIO` | float | 配股比例 |
| `RIGHTS_ISSUE_PRICE` | float | 配股价格（元） |
| `RECORD_DATE` | str | 股权登记日 |
| `RIGHTS_ISSUE_PROGRESS` | str | 配股进度 |

**配股进度代码**：

| 代码 | 描述 |
|------|------|
| 1 | 董事会预案 |
| 2 | 股东大会通过 |
| 3 | 实施 |
| 4 | 未通过 |

**使用示例**：
```python
# 获取配股数据
rights_issue = info_data.get_rights_issue(code_list, local_path, is_local=False)

# 查看有配股记录的公司
for code, df in rights_issue.items():
    if len(df) > 0:
        print(f"{code} 配股记录:")
        print(df[['ANN_DATE', 'RIGHTS_ISSUE_PLAN', 'RIGHTS_ISSUE_PRICE']].tail())
```

---

## 使用示例

### 获取分红和配股数据

```python
import AmazingData as ad

ad.login(username='user', password='pass', host='host', port=port)

info_data = ad.InfoData()
base_data = ad.BaseData()

# 获取 A 股代码列表
code_list = base_data.get_code_list(security_type='EXTRA_STOCK_A')
local_path = '/path/to/data'

# 获取分红数据（首次运行从服务器获取）
print("获取分红数据...")
dividend = info_data.get_dividend(code_list, local_path, is_local=False)

# 获取配股数据
print("获取配股数据...")
rights_issue = info_data.get_rights_issue(code_list, local_path, is_local=False)

print("完成！")
```

### 分析高分红股票

```python
import pandas as pd

# 计算累计分红
dividend_stats = []
for code, df in dividend.items():
    if len(df) > 0 and 'CASH_DIVIDEND' in df.columns:
        total_dividend = df['CASH_DIVIDEND'].sum()
        dividend_stats.append({
            'code': code,
            'security_name': df['SECURITY_NAME'].iloc[0] if 'SECURITY_NAME' in df.columns else '',
            'total_dividend': total_dividend,
            'dividend_count': len(df)
        })

# 转换为 DataFrame 并排序
dividend_df = pd.DataFrame(dividend_stats)
top_dividend = dividend_df.nlargest(10, 'total_dividend')
print("累计分红前 10 名:")
print(top_dividend)
```

---

## 相关文档

- [股东股本数据](06-shareholder-data.md)
- [财务数据](05-financial-data.md)
