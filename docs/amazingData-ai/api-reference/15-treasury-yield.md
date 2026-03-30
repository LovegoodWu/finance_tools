# 国债收益率数据接口 (Treasury Yield Data)

## 概述

国债收益率数据接口提供不同期限的国债收益率数据。

## InfoData 类方法

---

### get_treasury_yield - 国债收益率

**函数接口**：`get_treasury_yield`

**功能描述**：获取指定期限的国债收益率数据

**函数签名**：
```python
get_treasury_yield(term_list: list[str], local_path: str, is_local: bool = True,
                   begin_date: int = None, end_date: int = None) -> dict
```

**输入参数**：

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `term_list` | list[str] | 是 | 期限列表，见下方说明 |
| `local_path` | str | 是 | 本地存储路径 |
| `is_local` | bool | 否 | 是否使用本地缓存 |
| `begin_date` | int | 否 | 开始日期 |
| `end_date` | int | 否 | 结束日期 |

**支持的期限**：

| 期限代码 | 描述 |
|----------|------|
| `m3` | 3 个月 |
| `m6` | 6 个月 |
| `y1` | 1 年 |
| `y2` | 2 年 |
| `y3` | 3 年 |
| `y5` | 5 年 |
| `y7` | 7 年 |
| `y10` | 10 年 |
| `y30` | 30 年 |

**输出参数**：

| 类型 | 描述 |
|------|------|
| dict | key: 期限代码，value: DataFrame（收益率数据） |

**DataFrame 字段**：

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `YIELD` | float | 国债收益率（%） |

**index**: 日期（datetime 类型）

---

## 使用示例

### 获取国债收益率数据

```python
import AmazingData as ad

ad.login(username='user', password='pass', host='host', port=port)

info_data = ad.InfoData()
local_path = '/path/to/data'

# 获取全部期限的国债收益率
term_list = ['m3', 'm6', 'y1', 'y2', 'y3', 'y5', 'y7', 'y10', 'y30']
treasury_yield = info_data.get_treasury_yield(term_list, local_path, is_local=False)

# 查看 10 年期国债收益率
if 'y10' in treasury_yield:
    df = treasury_yield['y10']
    print("10 年期国债收益率:")
    print(df.tail(10))
    
    # 绘制收益率曲线
    import matplotlib.pyplot as plt
    
    plt.figure(figsize=(12, 6))
    for term in term_list:
        if term in treasury_yield:
            plt.plot(treasury_yield[term].index, treasury_yield[term]['YIELD'], label=term)
    
    plt.xlabel('日期')
    plt.ylabel('收益率 (%)')
    plt.title('国债收益率曲线')
    plt.legend()
    plt.grid(True)
    plt.show()
```

### 分析收益率利差

```python
# 计算 10 年 -2 年利差（常用于预测经济衰退）
if 'y10' in treasury_yield and 'y2' in treasury_yield:
    y10 = treasury_yield['y10']['YIELD']
    y2 = treasury_yield['y2']['YIELD']
    
    # 对齐日期
    spread = y10 - y2
    
    print("\n10 年 -2 年利差:")
    print(spread.tail(10))
    
    # 判断是否倒挂
    inverted = spread < 0
    print(f"\n最近是否倒挂：{inverted.iloc[-1]}")
```

---

## 相关文档

- [可转债数据](14-convertible-bond.md)
- [基础数据接口](02-base-data.md)
