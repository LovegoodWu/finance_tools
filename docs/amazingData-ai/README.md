# AmazingData API 文档 (AI Agent 优化版)

本文档是为中国银河证券星耀数智 AmazingData 金融数据服务编写的 API 参考文档，专门优化用于 AI coding agent 使用。

## 目录结构

```
docs/amazingData-ai/
├── README.md                 # 本文件，总体介绍
├── api-reference/            # API 接口参考
│   ├── 01-authentication.md  # 认证接口（登录/登出）
│   ├── 02-base-data.md       # 基础数据接口
│   ├── 03-realtime-market.md # 实时行情数据
│   ├── 04-historical-market.md # 历史行情数据
│   ├── 05-financial-data.md  # 财务数据
│   ├── 06-shareholder-data.md # 股东股本数据
│   ├── 07-shareholder-equity.md # 股东权益数据
│   ├── 08-margin-trading.md  # 融资融券数据
│   ├── 09-trading-anomaly.md # 交易异动数据
│   ├── 10-option-data.md     # 期权数据
│   ├── 11-etf-data.md        # ETF 数据
│   ├── 12-index-data.md      # 交易所指数数据
│   ├── 13-industry-index.md  # 行业指数数据
│   ├── 14-convertible-bond.md # 可转债数据
│   └── 15-treasury-yield.md  # 国债收益率数据
├── data-types/               # 数据类型定义
│   ├── snapshot.md           # 快照数据结构
│   ├── kline.md              # K 线数据结构
│   └── constants.md          # 常量定义
├── examples/                 # 使用示例
│   ├── 01-quickstart.md      # 快速开始
│   ├── 02-common-queries.md  # 常见查询
│   └── 03-operators.md       # 金融算子使用
└── appendix/                 # 附录
    ├── field-reference.md    # 字段取值说明
    └── security-type.md      # 代码类型说明
```

## 快速开始

### 1. 安装 SDK

```bash
pip install AmazingData
```

### 2. 登录

```python
import AmazingData as ad

ad.login(
    username='your_username',
    password='your_password',
    host='your_host',
    port=your_port
)
```

### 3. 获取数据

```python
# 获取代码列表
base_data = ad.BaseData()
code_list = base_data.get_code_list(security_type='EXTRA_STOCK_A')

# 获取历史 K 线
calendar = base_data.get_calendar()
market_data = ad.MarketData(calendar)
kline_dict = market_data.query_kline(
    code_list,
    begin_date=20240101,
    end_date=20241231,
    period=ad.constant.Period.day.value
)
```

## 主要功能模块

| 模块 | 描述 | 文档 |
|------|------|------|
| 认证 | 登录、登出、密码更新 | [`api-reference/01-authentication.md`](api-reference/01-authentication.md) |
| 基础数据 | 证券信息、代码表、交易日历 | [`api-reference/02-base-data.md`](api-reference/02-base-data.md) |
| 实时行情 | 股票、指数、期货、ETF 等实时快照和 K 线 | [`api-reference/03-realtime-market.md`](api-reference/03-realtime-market.md) |
| 历史行情 | 历史快照和 K 线数据 | [`api-reference/04-historical-market.md`](api-reference/04-historical-market.md) |
| 财务数据 | 资产负债表、利润表、现金流量表等 | [`api-reference/05-financial-data.md`](api-reference/05-financial-data.md) |
| 股东数据 | 股东户数、股本结构、股权冻结等 | [`api-reference/06-shareholder-data.md`](api-reference/06-shareholder-data.md) |
| 金融算子 | 数学函数、统计函数、时序函数、截面函数 | [`examples/03-operators.md`](examples/03-operators.md) |

## 数据来源

- 原始文档：[`../AmazingData 开发手册 1-70.md`](../AmazingData 开发手册 1-70.md) 等
- 文档版本：V1.0.24
- Python SDK 版本：V1.0.24

## 更新日期

2026-03-29
