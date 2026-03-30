# 代码类型说明 (Security Type)

## 概述

本文档详细说明了 AmazingData API 中使用的证券代码类型（security_type）参数取值。

---

## 沪深北证券代码类型

| security_type 值 | 描述 | 包含内容 |
|-----------------|------|----------|
| `EXTRA_STOCK_A` | 全部 A 股 | 上交所 A 股 + 深交所 A 股 + 北交所股票 |
| `SH_A` | 上海 A 股 | 仅上交所 A 股 |
| `SZ_A` | 深圳 A 股 | 仅深交所 A 股 |
| `BJ_A` | 北京 A 股 | 仅北交所股票 |
| `EXTRA_STOCK_A_SH_SZ` | 沪深 A 股 | 上交所 A 股 + 深交所 A 股（不含北交所） |

---

## 指数代码类型

| security_type 值 | 描述 | 包含内容 |
|-----------------|------|----------|
| `EXTRA_INDEX_A` | 全部指数 | 上交所指数 + 深交所指数 + 北交所指数 |
| `SH_INDEX` | 上海指数 | 仅上交所指数 |
| `SZ_INDEX` | 深圳指数 | 仅深交所指数 |
| `BJ_INDEX` | 北证指数 | 仅北交所指数 |

---

## ETF 代码类型

| security_type 值 | 描述 | 包含内容 |
|-----------------|------|----------|
| `EXTRA_ETF` | 全部 ETF | 上交所 ETF + 深交所 ETF |
| `SH_ETF` | 上海 ETF | 仅上交所 ETF |
| `SZ_ETF` | 深圳 ETF | 仅深交所 ETF |

---

## 可转债代码类型

| security_type 值 | 描述 | 包含内容 |
|-----------------|------|----------|
| `EXTRA_KZZ` | 全部可转债 | 上交所可转债 + 深交所可转债 |
| `SH_KZZ` | 上海可转债 | 仅上交所可转债 |
| `SZ_KZZ` | 深圳可转债 | 仅深交所可转债 |

---

## 港股通代码类型

| security_type 值 | 描述 | 包含内容 |
|-----------------|------|----------|
| `EXTRA_HKT` | 全部港股通 | 沪港通 + 深港通 |
| `SH_HKT` | 沪港通 | 仅沪港通标的 |
| `SZ_HKT` | 深港通 | 仅深港通标的 |

---

## 逆回购代码类型

| security_type 值 | 描述 | 包含内容 |
|-----------------|------|----------|
| `EXTRA_GLRA` | 全部逆回购 | 上交所逆回购 + 深交所逆回购 |
| `SH_GLRA` | 上海逆回购 | 仅上交所逆回购 |
| `SZ_GLRA` | 深圳逆回购 | 仅深交所逆回购 |

---

## 期货代码类型

| security_type 值 | 描述 | 包含内容 |
|-----------------|------|----------|
| `EXTRA_FUTURE` | 全部期货 | 中金所期货 |
| `ZJ_FUTURE` | 中金所期货 | 中国金融期货交易所 |

---

## 期权代码类型

| security_type 值 | 描述 | 包含内容 |
|-----------------|------|----------|
| `EXTRA_ETF_OP` | 全部 ETF 期权 | 上交所 ETF 期权 + 深交所 ETF 期权 |
| `SH_OPTION` | 上海期权 | 仅上交所 ETF 期权 |
| `SZ_OPTION` | 深圳期权 | 仅深交所 ETF 期权 |

---

## 使用示例

```python
import AmazingData as ad

ad.login(username='user', password='pass', host='host', port=port)

base_data = ad.BaseData()

# 获取不同品种的代码列表
stock_codes = base_data.get_code_list(security_type='EXTRA_STOCK_A')
index_codes = base_data.get_code_list(security_type='EXTRA_INDEX_A')
etf_codes = base_data.get_code_list(security_type='EXTRA_ETF')
kzz_codes = base_data.get_code_list(security_type='EXTRA_KZZ')
hkt_codes = base_data.get_code_list(security_type='EXTRA_HKT')
future_codes = base_data.get_code_list(security_type='EXTRA_FUTURE')
option_codes = base_data.get_option_code_list(security_type='EXTRA_ETF_OP')

# 获取沪深 A 股（不含北交所）
sh_sz_codes = base_data.get_code_list(security_type='EXTRA_STOCK_A_SH_SZ')

# 获取历史代码列表（包含已退市）
calendar = base_data.get_calendar()
today = calendar[-1]
hist_codes = base_data.get_hist_code_list(
    security_type='EXTRA_STOCK_A_SH_SZ',
    start_date=20130101,
    end_date=today
)
```

---

## 注意事项

1. **代码格式**：证券代码格式为 `XXXXXX.SH` 或 `XXXXXX.SZ` 或 `XXXXXX.BJ`
2. **市场标识**：
   - `.SH` - 上海证券交易所
   - `.SZ` - 深圳证券交易所
   - `.BJ` - 北京证券交易所
   - `.CFE` - 中国金融期货交易所

---

## 相关文档

- [基础数据接口](../api-reference/02-base-data.md)
- [常量定义](../data-types/constants.md)
