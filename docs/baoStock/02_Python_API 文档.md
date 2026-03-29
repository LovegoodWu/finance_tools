# Python API 文档

## 目录

### 1 入门示例
#### 1.1 HelloWorld

此篇为平台入门示例，安装 baostock 后，可导入包运行此示例。

```python
import baostock as bs
import pandas as pd

#### 登陆系统 ####
lg = bs.login()
# 显示登陆返回信息
print('login respond error_code:'+lg.error_code)
print('login respond error_msg:'+lg.error_msg)

#### 获取历史 K 线数据 ####
# 详细指标参数，参见"历史行情指标参数"章节
rs = bs.query_history_k_data_plus("sh.600000",
    "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,peTTM,pbMRQ,psTTM,pcfNcfTTM,isST",
    start_date='2017-06-01', end_date='2017-12-31', 
    frequency="d", adjustflag="3") #frequency="d"取日 k 线，adjustflag="3"默认不复权
print('query_history_k_data_plus respond error_code:'+rs.error_code)
print('query_history_k_data_plus respond error_msg:'+rs.error_msg)

#### 打印结果集 ####
data_list = []
while (rs.error_code == '0') & rs.next():
    # 获取一条记录，将记录合并在一起
    data_list.append(rs.get_row_data())
result = pd.DataFrame(data_list, columns=rs.fields)
#### 结果集输出到 csv 文件 ####
result.to_csv("D:/history_k_data.csv", encoding="gbk", index=False)
print(result)

#### 登出系统 ####
bs.logout()
```

### 2 登录
#### 2.1 login()

方法说明：登录系统。

使用示例：`lg = login()`

返回信息：
- lg.error_code：错误代码，当为"0"时表示成功，当为非 0 时表示失败；
- lg.error_msg：错误信息，对错误的详细解释。

### 3 登出
#### 3.1 logout()

方法说明：登出系统

使用示例：`lg = logout()`

返回信息：
- lg.error_code：错误代码，当为"0"时表示成功，当为非 0 时表示失败；
- lg.error_msg：错误信息，对错误的详细解释。

### 4 获取历史 A 股 K 线数据
#### 4.1 获取历史 A 股 K 线数据：query_history_k_data_plus()

方法说明：通过 API 接口获取 A 股历史交易数据，可以通过参数设置获取日 k 线、周 k 线、月 k 线，以及 5 分钟、15 分钟、30 分钟和 60 分钟 k 线数据，适合搭配均线数据进行选股和分析。

返回类型：pandas 的 DataFrame 类型。

- 能获取 1990-12-19 至当前时间的数据；
- 可查询不复权、前复权、后复权数据。

**日线使用示例：**

```python
import baostock as bs
import pandas as pd

#### 登陆系统 ####
lg = bs.login()
# 显示登陆返回信息
print('login respond error_code:'+lg.error_code)
print('login respond error_msg:'+lg.error_msg)

#### 获取沪深 A 股历史 K 线数据 ####
rs = bs.query_history_k_data_plus("sh.600000",
    "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST",
    start_date='2024-07-01', end_date='2024-12-31',
    frequency="d", adjustflag="3")
print('query_history_k_data_plus respond error_code:'+rs.error_code)
print('query_history_k_data_plus respond error_msg:'+rs.error_msg)

#### 打印结果集 ####
data_list = []
while (rs.error_code == '0') & rs.next():
    data_list.append(rs.get_row_data())
result = pd.DataFrame(data_list, columns=rs.fields)

#### 结果集输出到 csv 文件 ####   
result.to_csv("D:\\history_A_stock_k_data.csv", index=False)
print(result)

#### 登出系统 ####
bs.logout()
```

**参数含义：**
- code：股票代码，sh 或 sz.+6 位数字代码，或者指数代码，如：sh.601398。sh：上海；sz：深圳。此参数不可为空；
- fields：指示简称，支持多指标输入，以半角逗号分隔，填写内容作为返回类型的列。详细指标列表见历史行情指标参数章节，日线与分钟线参数不同。此参数不可为空；
- start：开始日期（包含），格式"YYYY-MM-DD"，为空时取 2015-01-01；
- end：结束日期（包含），格式"YYYY-MM-DD"，为空时取最近一个交易日；
- frequency：数据类型，默认为 d，日 k 线；d=日 k 线、w=周、m=月、5=5 分钟、15=15 分钟、30=30 分钟、60=60 分钟 k 线数据，不区分大小写；指数没有分钟线数据；周线每周最后一个交易日才可以获取，月线每月最后一个交易日才可以获取。
- adjustflag：复权类型，默认不复权：3；1：后复权；2：前复权。已支持分钟线、日线、周线、月线前后复权。

**注意：**
- 股票停牌时，对于日线，开、高、低、收价都相同，且都为前一交易日的收盘价，成交量、成交额为 0，换手率为空。
- 如果需要将换手率转为 float 类型，可使用如下方法转换：`result["turn"] = [0 if x == "" else float(x) for x in result["turn"]]`

**关于复权数据的说明：**
BaoStock 使用"涨跌幅复权法"进行复权。不同系统间采用复权方式可能不一致，导致数据不一致。

### 5 查询除权除息信息
#### 5.1 除权除息信息：query_dividend_data()

通过 API 接口获取除权除息信息数据（预披露、预案、正式都已通过）。

**参数含义：**
- code：股票代码，sh 或 sz.+6 位数字代码，或者指数代码，如：sh.601398。sh：上海；sz：深圳。此参数不可为空；
- year：年份，如：2017。此参数不可为空；
- yearType：年份类别，默认为"report":预案公告年份，可选项"operate":除权除息年份。此参数不可为空。

### 6 查询复权因子信息
#### 6.1 复权因子：query_adjust_factor()

通过 API 接口获取复权因子信息数据。BaoStock 提供的是涨跌幅复权算法复权因子。

**参数含义：**
- code：股票代码，sh 或 sz.+6 位数字代码，或者指数代码，如：sh.601398。sh：上海；sz：深圳。此参数不可为空；
- start_date：开始日期，为空时默认为 2015-01-01，包含此日期；
- end_date：结束日期，为空时默认当前日期，包含此日期。

### 7 查询季频财务数据信息
#### 7.1 季频盈利能力：query_profit_data()
#### 7.2 季频营运能力：query_operation_data()
#### 7.3 季频成长能力：query_growth_data()
#### 7.4 季频偿债能力：query_balance_data()
#### 7.5 季频现金流量：query_cash_flow_data()
#### 7.6 季频杜邦指数：query_dupont_data()

### 8 查询季频公司报告信息
#### 8.1 季频公司业绩快报：query_performance_express_report()
#### 8.2 季频公司业绩预告：query_forecast_report()

### 9 证券基本资料
#### 9.1 证券基本资料：query_stock_basic()

### 10 获取证券元信息
#### 10.1 交易日查询：query_trade_dates()
#### 10.2 证券代码查询：query_all_stock()

### 11 宏观经济数据
#### 11.1 存款利率：query_deposit_rate_data()
#### 11.2 贷款利率：query_loan_rate_data()
#### 11.3 存款准备金率：query_required_reserve_ratio_data()
#### 11.4 货币供应量：query_money_supply_data_month()
#### 11.5 货币供应量 (年底余额)：query_money_supply_data_year()

### 12 板块数据
#### 12.1 行业分类：query_stock_industry()
#### 12.2 上证 50 成分股：query_sz50_stocks()
#### 12.3 沪深 300 成分股：query_hs300_stocks()
#### 12.4 中证 500 成分股：query_zz500_stocks()

### 13 示例程序
#### 13.1 获取指定日期全部股票的日 K 线数据：query_history_k_data_plus()
