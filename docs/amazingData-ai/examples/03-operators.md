# 金融算子使用指南 (Financial Operators)

## 概述

AmazingData 提供了丰富的金融算子，用于对金融数据进行各种数学和统计计算。算子分为以下几类：

1. **数学函数** - 基本数学运算
2. **统计函数** - 统计分析
3. **时序函数** - 时间序列分析
4. **截面函数** - 截面数据分析

---

## 1. 数学函数 (Math Functions)

数学函数用于基本的数学运算，返回 `pd.Series` 类型。

### 导入方式

```python
from AmazingData.operator.math_function import MathFunction
```

### 常用函数

| 函数名 | 描述 | 用法 |
|--------|------|------|
| `ABS` | 绝对值 | `MathFunction.ABS(x)` |
| `SQRT` | 平方根 | `MathFunction.SQRT(x)` |
| `LOG` | 自然对数 | `MathFunction.LOG(x)` |
| `LOG10` | 常用对数 | `MathFunction.LOG10(x)` |
| `SIN/COS/TAN` | 三角函数 | `MathFunction.SIN(x)` |
| `ASIN/ACOS/ATAN` | 反三角函数 | `MathFunction.ASIN(x)` |
| `CEILING` | 向上取整 | `MathFunction.CEILING(x)` |
| `FLOOR` | 向下取整 | `MathFunction.FLOOR(x)` |
| `ROUND` | 四舍五入 | `MathFunction.ROUND(x)` |
| `MAX/MIN` | 最大/最小值 | `MathFunction.MAX(x, y)` |
| `POW` | 幂运算 | `MathFunction.POW(x, n)` |
| `BETWEEN` | 范围判断 | `MathFunction.BETWEEN(x, a, b)` |

### 使用示例

```python
import AmazingData as ad
from AmazingData.operator.math_function import MathFunction
import pandas as pd

ad.login(username='user', password='pass', host='host', port=port)

# 获取数据
base_data = ad.BaseData()
calendar = base_data.get_calendar()
market_data = ad.MarketData(calendar)

code_list = ['000001.SZ']
kline_dict = market_data.query_kline(
    code_list,
    begin_date=20240101,
    end_date=20241231,
    period=ad.constant.Period.day.value
)

df = kline_dict['000001.SZ']

# 计算收盘价的绝对值（通常用于变化量）
abs_close = MathFunction.ABS(df['close'])

# 计算收盘价的对数收益率
log_return = MathFunction.LOG(df['close'] / df['close'].shift(1))

# 计算最高价和最低价的平均值
avg_price = (df['high'] + df['low']) / 2

# 范围判断：收盘价是否在 20 日均线附近 5% 范围内
ma20 = df['close'].rolling(20).mean()
in_range = MathFunction.BETWEEN(df['close'], ma20 * 0.95, ma20 * 1.05)
```

---

## 2. 统计函数 (Statistics Functions)

统计函数用于统计分析。

### 导入方式

```python
from AmazingData.operator.statistics_function import StatisticsFunction
```

### 常用函数

| 函数名 | 描述 | 用法 |
|--------|------|------|
| `COUNT` | 计数 | `StatisticsFunction.COUNT(x, n)` |
| `SUM` | 求和 | `StatisticsFunction.SUM(x, n)` |
| `MEAN` | 平均值 | `StatisticsFunction.MEAN(x, n)` |
| `STD` | 标准差 | `StatisticsFunction.STD(x, n)` |
| `VAR` | 方差 | `StatisticsFunction.VAR(x, n)` |
| `MAX/MIN` | 最大/最小值 | `StatisticsFunction.MAX(x, n)` |
| `MEDIAN` | 中位数 | `StatisticsFunction.MEDIAN(x, n)` |
| `CORR` | 相关系数 | `StatisticsFunction.CORR(x, y, n)` |
| `COV` | 协方差 | `StatisticsFunction.COV(x, y, n)` |
| `SKEW` | 偏度 | `StatisticsFunction.SKEW(x, n)` |
| `KURT` | 峰度 | `StatisticsFunction.KURT(x, n)` |

### 使用示例

```python
from AmazingData.operator.statistics_function import StatisticsFunction

# 计算 20 日收益率的标准差
returns = df['close'].pct_change()
volatility = StatisticsFunction.STD(returns, 20)

# 计算 20 日成交量的平均值
avg_volume = StatisticsFunction.MEAN(df['volume'], 20)

# 计算两只股票收益率的相关系数
returns1 = df1['close'].pct_change()
returns2 = df2['close'].pct_change()
correlation = StatisticsFunction.CORR(returns1, returns2, 60)
```

---

## 3. 时序函数 (Time Series Functions)

时序函数用于时间序列分析，是量化策略中最常用的算子。

### 导入方式

```python
from AmazingData.operator.time_series_function import TimeSeriesFunction
```

### 函数分类

#### 3.1 算术函数

| 函数名 | 描述 | 用法 |
|--------|------|------|
| `ADD` | 加法 | `TimeSeriesFunction.ADD(x, y)` |
| `SUB` | 减法 | `TimeSeriesFunction.SUB(x, y)` |
| `MUL` | 乘法 | `TimeSeriesFunction.MUL(x, y)` |
| `DIV` | 除法 | `TimeSeriesFunction.DIV(x, y)` |

#### 3.2 关系函数

| 函数名 | 描述 | 用法 |
|--------|------|------|
| `GT` | 大于 | `TimeSeriesFunction.GT(x, y)` |
| `LT` | 小于 | `TimeSeriesFunction.LT(x, y)` |
| `GE` | 大于等于 | `TimeSeriesFunction.GE(x, y)` |
| `LE` | 小于等于 | `TimeSeriesFunction.LE(x, y)` |
| `EQ` | 等于 | `TimeSeriesFunction.EQ(x, y)` |
| `NE` | 不等于 | `TimeSeriesFunction.NE(x, y)` |

#### 3.3 逻辑函数

| 函数名 | 描述 | 用法 |
|--------|------|------|
| `AND` | 与 | `TimeSeriesFunction.AND(x, y)` |
| `OR` | 或 | `TimeSeriesFunction.OR(x, y)` |
| `NOT` | 非 | `TimeSeriesFunction.NOT(x)` |
| `IF` | 条件判断 | `TimeSeriesFunction.IF(cond, x, y)` |

#### 3.4 极值函数

| 函数名 | 描述 | 用法 |
|--------|------|------|
| `HHV` | 最高值 | `TimeSeriesFunction.HHV(x, n)` |
| `LLV` | 最低值 | `TimeSeriesFunction.LLV(x, n)` |
| `HHVBARS` | 最高值位置 | `TimeSeriesFunction.HHVBARS(x, n)` |
| `LLVBARS` | 最低值位置 | `TimeSeriesFunction.LLVBARS(x, n)` |

#### 3.5 引用函数

| 函数名 | 描述 | 用法 |
|--------|------|------|
| `REF` | 引用 N 周期前 | `TimeSeriesFunction.REF(x, n)` |
| `REVERSE` | 相反数 | `TimeSeriesFunction.REVERSE(x)` |

#### 3.6 移动平均函数

| 函数名 | 描述 | 用法 |
|--------|------|------|
| `MA` | 简单移动平均 | `TimeSeriesFunction.MA(x, n)` |
| `EMA` | 指数移动平均 | `TimeSeriesFunction.EMA(x, n)` |
| `SMA` | 扩展指数平均 | `TimeSeriesFunction.SMA(x, n, m)` |
| `WMA` | 加权移动平均 | `TimeSeriesFunction.WMA(x, n)` |
| `MEMA` | 平滑移动平均 | `TimeSeriesFunction.MEMA(x, n)` |

#### 3.7 技术指标函数

| 函数名 | 描述 | 用法 |
|--------|------|------|
| `MACD` | MACD 指标 | `TimeSeriesFunction.MACD(close, short, long, mid)` |
| `KDJ` | KDJ 指标 | `TimeSeriesFunction.KDJ(high, low, close, n, m1, m2)` |
| `RSI` | RSI 指标 | `TimeSeriesFunction.RSI(close, n)` |
| `BOLL` | 布林带 | `TimeSeriesFunction.BOLL(close, n, k)` |
| `SAR` | 抛物线转向 | `TimeSeriesFunction.SAR(high, low, n, step, max_af)` |

### 使用示例

```python
from AmazingData.operator.time_series_function import TimeSeriesFunction

# 计算 MA5, MA10, MA20
ma5 = TimeSeriesFunction.MA(df['close'], 5)
ma10 = TimeSeriesFunction.MA(df['close'], 10)
ma20 = TimeSeriesFunction.MA(df['close'], 20)

# 计算 EMA12, EMA26 (用于 MACD)
ema12 = TimeSeriesFunction.EMA(df['close'], 12)
ema26 = TimeSeriesFunction.EMA(df['close'], 26)

# 计算 20 日最高价和最低价
hhv20 = TimeSeriesFunction.HHV(df['high'], 20)
llv20 = TimeSeriesFunction.LLV(df['low'], 20)

# 金叉信号：MA5 上穿 MA10
cross_over = TimeSeriesFunction.CROSS(ma5, ma10)

# 计算 RSI 指标
rsi6 = TimeSeriesFunction.RSI(df['close'], 6)
rsi12 = TimeSeriesFunction.RSI(df['close'], 12)
rsi24 = TimeSeriesFunction.RSI(df['close'], 24)

# 计算 MACD 指标
dif = ema12 - ema26
dea = TimeSeriesFunction.EMA(dif, 9)
macd = (dif - dea) * 2

# 计算布林带
mid = TimeSeriesFunction.MA(df['close'], 20)
std = df['close'].rolling(20).std()
upper = mid + 2 * std
lower = mid - 2 * std
```

---

## 4. 截面函数 (Cross Section Functions)

截面函数用于计算同一交易日内多个标的之间的统计指标。

### 导入方式

```python
from AmazingData.operator.cross_section_function import CrossSectionFunction
```

### 函数列表

| 函数名 | 描述 | 用法 |
|--------|------|------|
| `CSCOUNT` | 截面标的个数 | `CrossSectionFunction.CSCOUNT(x)` |
| `CSMEAN` | 截面平均值 | `CrossSectionFunction.CSMEAN(x)` |
| `CSMEDIAN` | 截面中位数 | `CrossSectionFunction.CSMEDIAN(x)` |
| `CSMAX` | 截面最大值 | `CrossSectionFunction.CSMAX(x)` |
| `CSMIN` | 截面最小值 | `CrossSectionFunction.CSMIN(x)` |
| `CSSTD` | 截面标准差 | `CrossSectionFunction.CSSTD(x)` |
| `CSVAR` | 截面方差 | `CrossSectionFunction.CSVAR(x)` |
| `CSSUM` | 截面求和 | `CrossSectionFunction.CSSUM(x)` |
| `CSRANK` | 截面排名 | `CrossSectionFunction.CSRANK(x, ascending)` |
| `CSPCTRANK` | 截面百分位排名 | `CrossSectionFunction.CSPCTRANK(x)` |
| `CSQUANTILE` | 截面分位数 | `CrossSectionFunction.CSQUANTILE(x, n)` |
| `CSZSCORE` | 截面 Z-score 标准化 | `CrossSectionFunction.CSZSCORE(x)` |
| `CSNORMALIZE` | 截面归一化 | `CrossSectionFunction.CSNORMALIZE(x)` |
| `CSDEMEAN` | 截面去均值 | `CrossSectionFunction.CSDEMEAN(x)` |
| `CSCOV` | 截面协方差 | `CrossSectionFunction.CSCOV(x, y)` |
| `CSCORR` | 截面相关度 | `CrossSectionFunction.CSCORR(x, y)` |

### 使用示例

```python
from AmazingData.operator.cross_section_function import CrossSectionFunction
import pandas as pd

# 获取多只股票数据
codes = ['000001.SZ', '000002.SZ', '000063.SZ', '000069.SZ', '000078.SZ']
kline_multi = market_data.query_kline(
    codes,
    begin_date=20240101,
    end_date=20241231,
    period=ad.constant.Period.day.value
)

# 构建截面数据 DataFrame (行：日期，列：标的)
close_df = pd.DataFrame({c: kline_multi[c]['close'] for c in codes if c in kline_multi})
open_df = pd.DataFrame({c: kline_multi[c]['open'] for c in codes if c in kline_multi})

# 截面平均值：计算每日所有股票的平均收盘价
cs_mean = CrossSectionFunction.CSMEAN(close_df)

# 截面排名：计算每日每只股票的收盘价排名
cs_rank = CrossSectionFunction.CSRANK(close_df, ascending=True)

# 截面百分位排名
cs_pct_rank = CrossSectionFunction.CSPCTRANK(close_df)

# 截面 Z-score 标准化
cs_zscore = CrossSectionFunction.CSZSCORE(close_df)

# 截面归一化 (Min-Max)
cs_normalized = CrossSectionFunction.CSNORMALIZE(close_df)

# 截面协方差
cs_cov = CrossSectionFunction.CSCOV(close_df, open_df)

# 截面相关度
cs_corr = CrossSectionFunction.CSCORR(close_df, open_df)
```

---

## 5. 综合示例：构建交易策略

```python
import AmazingData as ad
from AmazingData.operator.time_series_function import TimeSeriesFunction
from AmazingData.operator.cross_section_function import CrossSectionFunction
import pandas as pd

ad.login(username='user', password='pass', host='host', port=port)

base_data = ad.BaseData()
calendar = base_data.get_calendar()
market_data = ad.MarketData(calendar)

# 获取股票池
stock_codes = base_data.get_code_list(security_type='EXTRA_STOCK_A_SH_SZ')

# 获取 K 线数据
kline_dict = market_data.query_kline(
    stock_codes[:100],  # 使用前 100 只股票
    begin_date=20230101,
    end_date=20241231,
    period=ad.constant.Period.day.value
)

# 构建收盘价 DataFrame
close_df = pd.DataFrame({c: kline_dict[c]['close'] for c in kline_dict})

# 策略：均线交叉 + 截面排名
signals = {}

for code in kline_dict:
    df = kline_dict[code]
    
    # 计算均线
    ma5 = TimeSeriesFunction.MA(df['close'], 5)
    ma10 = TimeSeriesFunction.MA(df['close'], 10)
    ma20 = TimeSeriesFunction.MA(df['close'], 20)
    
    # 金叉信号
    golden_cross = TimeSeriesFunction.CROSS(ma5, ma10)
    
    # 均线多头排列
    bull_trend = (ma5 > ma10) & (ma10 > ma20)
    
    # RSI 超卖
    rsi = TimeSeriesFunction.RSI(df['close'], 14)
    oversold = rsi < 30
    
    # 综合信号
    signals[code] = golden_cross & bull_trend & oversold

# 转换为 DataFrame
signal_df = pd.DataFrame(signals)

# 截面排名选股
daily_rank = CrossSectionFunction.CSRANK(signal_df.astype(int).sum(axis=0).to_frame().T, ascending=False)

print("信号最强的股票:")
print(daily_rank)
```

---

## 相关文档

- [快速开始](01-quickstart.md)
- [常量定义](../data-types/constants.md)
- [历史行情数据](../api-reference/04-historical-market.md)
