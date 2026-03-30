# 财务数据接口 (Financial Data)

## 概述

财务数据接口提供上市公司的财务报表数据，包括资产负债表、现金流量表、利润表、业绩快报和业绩预告。

## 类和方法

| 类名 | 描述 |
|------|------|
| `InfoData` | 信息数据查询类 |

---

## InfoData 类

### get_balance_sheet - 资产负债表

**函数接口**：`get_balance_sheet`

**功能描述**：获取指定股票列表的上市公司的资产负债表数据

**函数签名**：
```python
get_balance_sheet(code_list: list[str], local_path: str, is_local: bool = True,
                  begin_date: int = None, end_date: int = None) -> dict
```

**输入参数**：

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `code_list` | list[str] | 是 | 支持沪深 A 股的代码列表 |
| `local_path` | str | 是 | 本地存储路径（绝对路径），如 `'D://AmazingData_local_data//'` |
| `is_local` | bool | 否 | 是否使用本地缓存，默认 True |
| `begin_date` | int | 否 | 开始日期（报告期），格式 YYYYMMDD |
| `end_date` | int | 否 | 结束日期（报告期），格式 YYYYMMDD |

**输出参数**：

| 类型 | 描述 |
|------|------|
| dict | key: 证券代码，value: DataFrame（资产负债表数据） |

**DataFrame 字段**：

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `MARKET_CODE` | str | 证券代码 |
| `SECURITY_NAME` | str | 证券简称 |
| `STATEMENT_TYPE` | str | 报表类型 |
| `REPORT_TYPE` | str | 报告期名称 |
| `REPORTING_PERIOD` | str | 报告期 |
| `ANN_DATE` | str | 公告日期 |
| `ACTUAL_ANN_DATE` | str | 实际公告日期 |
| `CURRENCY_CAP` | float | 货币资金 |
| `ACCT_RECEIVABLE` | float | 应收账款 |
| `ACC_PAYABLE` | float | 应付票据及应付账款 |
| `CAP_STOCK` | float | 股本（元） |
| `CAP_RESV` | float | 资本公积金 |
| ... | ... | 更多字段见源文档 |

**使用示例**：
```python
import AmazingData as ad

ad.login(username='user', password='pass', host='host', port=port)

info_data = ad.InfoData()
base_data = ad.BaseData()

# 获取所有 A 股代码
calendar = base_data.get_calendar()
today = calendar[-1]
all_code_list = base_data.get_hist_code_list(
    security_type='EXTRA_STOCK_A_SH_SZ',
    start_date=20130101,
    end_date=today
)

# 获取资产负债表数据
balance_sheet = info_data.get_balance_sheet(
    all_code_list,
    local_path='/path/to/data',
    is_local=False  # 首次运行设为 False 从服务器获取
)

# 访问特定公司的数据
for code, df in list(balance_sheet.items())[:3]:
    print(f"代码：{code}")
    print(df.head())
```

---

### get_cash_flow - 现金流量表

**函数接口**：`get_cash_flow`

**功能描述**：获取指定股票列表的上市公司的现金流量表数据

**函数签名**：
```python
get_cash_flow(code_list: list[str], local_path: str, is_local: bool = True,
              begin_date: int = None, end_date: int = None) -> dict
```

**输入参数**：

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `code_list` | list[str] | 是 | 支持沪深 A 股的代码列表 |
| `local_path` | str | 是 | 本地存储路径 |
| `is_local` | bool | 否 | 是否使用本地缓存 |
| `begin_date` | int | 否 | 开始日期（报告期） |
| `end_date` | int | 否 | 结束日期（报告期） |

**输出参数**：

| 类型 | 描述 |
|------|------|
| dict | key: 证券代码，value: DataFrame（现金流量表数据） |

**主要字段**：

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `MARKET_CODE` | str | 证券代码 |
| `SECURITY_NAME` | str | 证券简称 |
| `SALE_SVC_REV` | float | 销售商品、提供劳务收到的现金 |
| `NET_INCR_DEP_CENTRAL_BANK` | float | 客户存款和同业存放款项净增加额 |
| `NET_CASH_FLW_OPER` | float | 经营活动产生的现金流量净额 |
| `NET_CASH_FLW_INV` | float | 投资活动产生的现金流量净额 |
| `NET_CASH_FLW_FNC` | float | 筹资活动产生的现金流量净额 |
| `NET_INCR_CASH_EQUIV` | float | 现金及现金等价物净增加额 |

---

### get_income_statement - 利润表

**函数接口**：`get_income_statement`

**功能描述**：获取指定股票列表的上市公司的利润表数据

**函数签名**：
```python
get_income_statement(code_list: list[str], local_path: str, is_local: bool = True,
                     begin_date: int = None, end_date: int = None) -> dict
```

**输入参数**：

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `code_list` | list[str] | 是 | 支持沪深 A 股的代码列表 |
| `local_path` | str | 是 | 本地存储路径 |
| `is_local` | bool | 否 | 是否使用本地缓存 |
| `begin_date` | int | 否 | 开始日期（报告期） |
| `end_date` | int | 否 | 结束日期（报告期） |

**输出参数**：

| 类型 | 描述 |
|------|------|
| dict | key: 证券代码，value: DataFrame（利润表数据） |

**主要字段**：

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `MARKET_CODE` | str | 证券代码 |
| `SECURITY_NAME` | str | 证券简称 |
| `TOT_OPER_REV` | float | 营业总收入 |
| `OPER_REV` | float | 营业收入 |
| `OPER_COST` | float | 营业成本 |
| `OPER_TAX_SURCHG` | float | 税金及附加 |
| `SELL_EXP` | float | 销售费用 |
| `ADMIN_EXP` | float | 管理费用 |
| `FIN_EXP` | float | 财务费用 |
| `OPER_PROFIT` | float | 营业利润 |
| `TOT_PROFIT` | float | 利润总额 |
| `NET_PROFIT` | float | 净利润 |
| `NET_PROFIT_ATTR_SHR` | float | 归属于母公司所有者的净利润 |

---

### get_performance_express - 业绩快报

**函数接口**：`get_performance_express`

**功能描述**：获取指定股票列表的上市公司业绩快报数据

**函数签名**：
```python
get_performance_express(code_list: list[str], local_path: str, is_local: bool = True,
                        begin_date: int = None, end_date: int = None) -> dict
```

**输入参数**：

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `code_list` | list[str] | 是 | 支持沪深 A 股的代码列表 |
| `local_path` | str | 是 | 本地存储路径 |
| `is_local` | bool | 否 | 是否使用本地缓存 |
| `begin_date` | int | 否 | 开始日期（报告期） |
| `end_date` | int | 否 | 结束日期（报告期） |

**输出参数**：

| 类型 | 描述 |
|------|------|
| dict | key: 证券代码，value: DataFrame（业绩快报数据） |

**主要字段**：

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `MARKET_CODE` | str | 证券代码 |
| `SECURITY_NAME` | str | 证券简称 |
| `REPORTING_PERIOD` | str | 报告期 |
| `ANN_DATE` | str | 公告日期 |
| `EPS` | float | 每股收益 |
| `NET_PROFIT` | float | 净利润 |
| `NET_PROFIT_YOY` | float | 净利润同比增长率 |
| `TOTAL_ASSETS` | float | 总资产 |
| `NET_ASSETS` | float | 净资产 |
| `ROE` | float | 净资产收益率 |

---

### get_performance_forecast - 业绩预告

**函数接口**：`get_performance_forecast`

**功能描述**：获取指定股票列表的上市公司业绩预告数据

**函数签名**：
```python
get_performance_forecast(code_list: list[str], local_path: str, is_local: bool = True,
                         begin_date: int = None, end_date: int = None) -> dict
```

**输入参数**：

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `code_list` | list[str] | 是 | 支持沪深 A 股的代码列表 |
| `local_path` | str | 是 | 本地存储路径 |
| `is_local` | bool | 否 | 是否使用本地缓存 |
| `begin_date` | int | 否 | 开始日期（报告期） |
| `end_date` | int | 否 | 结束日期（报告期） |

**输出参数**：

| 类型 | 描述 |
|------|------|
| dict | key: 证券代码，value: DataFrame（业绩预告数据） |

**主要字段**：

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `MARKET_CODE` | str | 证券代码 |
| `SECURITY_NAME` | str | 证券简称 |
| `REPORTING_PERIOD` | str | 报告期 |
| `ANN_DATE` | str | 公告日期 |
| `FORECAST_TYPE` | str | 预告类型（增盈/减盈/扭亏/续亏等） |
| `NET_PROFIT_MIN` | float | 净利润下限 |
| `NET_PROFIT_MAX` | float | 净利润上限 |
| `NET_PROFIT_YOY_MIN` | float | 净利润同比增长率下限 |
| `NET_PROFIT_YOY_MAX` | float | 净利润同比增长率上限 |

---

## 使用示例

### 获取全部财务数据

```python
import AmazingData as ad
import pandas as pd

ad.login(username='user', password='pass', host='host', port=port)

info_data = ad.InfoData()
base_data = ad.BaseData()

# 获取所有 A 股代码
calendar = base_data.get_calendar()
today = calendar[-1]
all_code_list = base_data.get_hist_code_list(
    security_type='EXTRA_STOCK_A_SH_SZ',
    start_date=20130101,
    end_date=today
)

local_path = '/path/to/data'

# 获取所有财务数据（首次运行从服务器获取）
print("获取资产负债表...")
balance_sheet = info_data.get_balance_sheet(all_code_list, local_path, is_local=False)

print("获取现金流量表...")
cash_flow = info_data.get_cash_flow(all_code_list, local_path, is_local=False)

print("获取利润表...")
income_stmt = info_data.get_income_statement(all_code_list, local_path, is_local=False)

print("获取业绩快报...")
perf_express = info_data.get_performance_express(all_code_list, local_path, is_local=False)

print("获取业绩预告...")
perf_forecast = info_data.get_performance_forecast(all_code_list, local_path, is_local=False)

print("完成！")
```

### 分析特定公司的财务数据

```python
# 分析特定公司（如贵州茅台）
code = '600519.SH'

# 获取资产负债表
bs = info_data.get_balance_sheet([code], local_path, is_local=True)
if code in bs:
    print(f"\n{code} 资产负债表:")
    print(bs[code].tail())

# 获取利润表
is_data = info_data.get_income_statement([code], local_path, is_local=True)
if code in is_data:
    print(f"\n{code} 利润表:")
    df = is_data[code]
    # 计算关键指标
    if 'TOT_OPER_REV' in df.columns and 'NET_PROFIT' in df.columns:
        print(f"营业收入：{df['TOT_OPER_REV'].iloc[-1]:.2f} 元")
        print(f"净利润：{df['NET_PROFIT'].iloc[-1]:.2f} 元")
```

---

## 注意事项

1. **数据范围**：仅支持沪深 A 股
2. **本地缓存**：财务数据量较大，建议使用本地缓存
3. **首次运行**：首次运行时需设置 `is_local=False` 从服务器获取数据
4. **报告期**：可通过 `begin_date` 和 `end_date` 指定报告期范围

---

## 相关文档

- [基础数据接口](02-base-data.md)
- [股东股本数据](06-shareholder-data.md)
- [代码类型说明](../appendix/security-type.md)
