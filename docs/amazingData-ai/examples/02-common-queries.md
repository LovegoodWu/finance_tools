# 常见查询示例 (Common Queries)

## 概述

本文档提供常用的数据查询示例，帮助快速上手 AmazingData API。

---

## 1. 获取股票基础信息

```python
import AmazingData as ad

ad.login(username='user', password='pass', host='host', port=port)

base_data = ad.BaseData()
info_data = ad.InfoData()

# 获取全部 A 股代码
stock_codes = base_data.get_code_list(security_type='EXTRA_STOCK_A')
print(f"A 股数量：{len(stock_codes)}")

# 获取 ETF 代码
etf_codes = base_data.get_code_list(security_type='EXTRA_ETF')

# 获取可转债代码
kzz_codes = base_data.get_code_list(security_type='EXTRA_KZZ')

# 获取指数代码
index_codes = base_data.get_code_list(security_type='EXTRA_INDEX_A')
```

---

## 2. 获取历史行情数据

### 2.1 获取日 K 线数据

```python
calendar = base_data.get_calendar()
market_data = ad.MarketData(calendar)

# 获取日 K 线
kline_dict = market_data.query_kline(
    code_list=stock_codes[:100],
    begin_date=20240101,
    end_date=20241231,
    period=ad.constant.Period.day.value
)

# 处理数据
for code, df in kline_dict.items():
    print(f"{code}: {len(df)} 条数据")
```

### 2.2 获取分钟 K 线数据

```python
# 获取 5 分钟 K 线
kline_5min = market_data.query_kline(
    code_list=stock_codes[:10],
    begin_date=20241201,
    end_date=20241231,
    period=ad.constant.Period.min5.value
)

# 获取 60 分钟 K 线
kline_60min = market_data.query_kline(
    code_list=stock_codes[:10],
    begin_date=20241201,
    end_date=20241231,
    period=ad.constant.Period.min60.value
)
```

### 2.3 获取历史快照

```python
# 获取指定日期的快照数据
snapshot_dict = market_data.query_snapshot(
    code_list=stock_codes[:100],
    begin_date=20241231,
    end_date=20241231
)

for code, df in list(snapshot_dict.items())[:5]:
    print(f"\n{code}:")
    print(df)
```

---

## 3. 获取财务数据

```python
local_path = '/path/to/data'

# 获取资产负债表
balance_sheet = info_data.get_balance_sheet(
    stock_codes[:100],
    local_path,
    is_local=False
)

# 获取利润表
income_stmt = info_data.get_income_statement(
    stock_codes[:100],
    local_path,
    is_local=False
)

# 获取现金流量表
cash_flow = info_data.get_cash_flow(
    stock_codes[:100],
    local_path,
    is_local=False
)

# 获取业绩快报
perf_express = info_data.get_performance_express(
    stock_codes[:100],
    local_path,
    is_local=False
)
```

---

## 4. 获取股东数据

```python
# 获取十大股东
top_10_holders = info_data.get_top_10_holders(
    stock_codes[:100],
    local_path,
    is_local=False
)

# 获取股东户数
shareholder_count = info_data.get_shareholder_count(
    stock_codes[:100],
    local_path,
    is_local=False
)

# 获取分红数据
dividend = info_data.get_dividend(
    stock_codes[:100],
    local_path,
    is_local=False
)
```

---

## 5. 获取指数数据

### 5.1 获取指数成分股

```python
# 获取沪深 300 成分股
index_constituent = info_data.get_index_constituent(
    ['000300.SH'],
    local_path,
    is_local=False
)

if '000300.SH' in index_constituent:
    df = index_constituent['000300.SH']
    # 当前成分股
    current = df[df['OUTDATE'].isna()]
    print(f"沪深 300 成分股数量：{len(current)}")
```

### 5.2 获取指数权重

```python
# 获取主要指数权重
index_weights = info_data.get_index_weight(
    ['000016.SH', '000300.SH', '000905.SH'],
    local_path,
    is_local=False
)
```

---

## 6. 获取 ETF 数据

```python
# 获取 ETF 代码列表
etf_codes = base_data.get_code_list(security_type='EXTRA_ETF')

# 获取 ETF 申赎数据
etf_pcf_info, etf_pcf_constituent = base_data.get_etf_pcf(etf_codes)

# 获取 ETF 份额
fund_share = info_data.get_fund_share(etf_codes, local_path, is_local=False)

# 获取 ETF IOPV
fund_iopv = info_data.get_fund_iopv(etf_codes, local_path, is_local=False)
```

---

## 7. 实时数据订阅

### 7.1 订阅实时快照

```python
sub_data = ad.SubscribeData()

@sub_data.register(
    code_list=stock_codes[:10],
    period=ad.constant.Period.snapshot.value
)
def onSnapshot(data, period):
    print(f"{data['code']}: {data['close']}")

sub_data.run()
```

### 7.2 订阅实时 K 线

```python
sub_data = ad.SubscribeData()

@sub_data.register(
    code_list=stock_codes[:10],
    period=ad.constant.Period.min1.value
)
def OnKLine(data, period):
    print(f"{data['code']}: O={data['open']} H={data['high']} L={data['low']} C={data['close']}")

sub_data.run()
```

---

## 8. 使用金融算子

### 8.1 时序函数

```python
from AmazingData.operator.time_series_function import TimeSeriesFunction

# 获取 K 线数据
kline_dict = market_data.query_kline(
    ['000001.SZ'],
    begin_date=20240101,
    end_date=20241231,
    period=ad.constant.Period.day.value
)

df = kline_dict['000001.SZ']

# 计算移动平均线
ma5 = TimeSeriesFunction.MA(df['close'], 5)
ma10 = TimeSeriesFunction.MA(df['close'], 10)
ma20 = TimeSeriesFunction.MA(df['close'], 20)

# 计算金叉信号
golden_cross = TimeSeriesFunction.CROSS(ma5, ma10)

# 计算 RSI
rsi = TimeSeriesFunction.RSI(df['close'], 14)
```

### 8.2 截面函数

```python
from AmazingData.operator.cross_section_function import CrossSectionFunction
import pandas as pd

# 构建截面数据
codes = stock_codes[:50]
kline_multi = market_data.query_kline(
    codes,
    begin_date=20240101,
    end_date=20241231,
    period=ad.constant.Period.day.value
)

close_df = pd.DataFrame({c: kline_multi[c]['close'] for c in kline_multi})

# 截面排名
cs_rank = CrossSectionFunction.CSRANK(close_df, ascending=False)

# 截面标准化
cs_zscore = CrossSectionFunction.CSZSCORE(close_df)
```

---

## 9. 数据导出

```python
# 导出 K 线数据到 CSV
for code, df in kline_dict.items():
    df.to_csv(f'data/{code}_kline.csv')

# 导出财务数据
for code, df in balance_sheet.items():
    df.to_csv(f'data/{code}_balance_sheet.csv')

# 导出到 HDF5（适合大数据）
with pd.HDFStore('data/stock_data.h5') as store:
    for code, df in kline_dict.items():
        store.put(f'kline/{code}', df)
```

---

## 10. 错误处理

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def safe_query(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        logger.error(f"查询失败：{e}")
        return None

# 使用示例
kline_dict = safe_query(
    market_data.query_kline,
    stock_codes[:100],
    begin_date=20240101,
    end_date=20241231,
    period=ad.constant.Period.day.value
)
```

---

## 相关文档

- [快速开始](01-quickstart.md)
- [金融算子使用](03-operators.md)
