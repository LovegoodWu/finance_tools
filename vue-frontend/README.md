# 网格策略交易系统 - Vue 前端版本

这是一个使用 Vue 3 + Vite + Element Plus 构建的网格策略交易系统前端，具有实时计算功能。

## 技术栈

- **前端**: Vue 3 + Vite
- **UI 组件库**: Element Plus
- **状态管理**: Pinia
- **路由**: Vue Router
- **HTTP 客户端**: Axios
- **后端**: FastAPI

## 主要特性

### 实时计算
- **买入金额** = 买入价 × 买入股数（自动计算）
- **卖出金额** = 卖出价 × 卖出股数（自动计算）
- **资金占用** = 累计买入金额（自动计算）
- **档位** = 当前买入价 / 最高买入价（自动计算）

### 与 Streamlit 版本对比

| 特性 | Streamlit | Vue + FastAPI |
|------|-----------|---------------|
| 实时计算 | ❌ 需要 rerun | ✅ 输入即计算 |
| 响应速度 | 慢（整页刷新） | 快（局部更新） |
| UI 定制 | 有限 | 灵活 |
| 开发难度 | 低（纯 Python） | 中（需前端知识） |
| 部署复杂度 | 低 | 中 |

## 安装和运行

### 1. 安装前端依赖

```bash
cd vue-frontend
npm install
```

### 2. 安装后端依赖

```bash
pip install fastapi uvicorn
```

### 3. 启动后端服务

```bash
cd fastapi-backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 4. 启动前端开发服务器

```bash
cd vue-frontend
npm run dev
```

### 5. 访问应用

打开浏览器访问：http://localhost:3000

## 项目结构

```
finance_tools/
├── vue-frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── GridEditor.vue       # 网格编辑器（核心组件，含实时计算）
│   │   ├── views/
│   │   │   ├── NewStrategy.vue      # 新建策略页面
│   │   │   └── StrategyOverview.vue # 策略总览页面
│   │   ├── api/
│   │   │   └── index.js             # API 客户端
│   │   ├── router/
│   │   │   └── index.js             # 路由配置
│   │   ├── App.vue                  # 根组件
│   │   └── main.js                  # 入口文件
│   ├── package.json
│   └── vite.config.js
└── fastapi-backend/
    └── main.py                      # FastAPI 后端
```

## 核心代码示例

### Vue 实时计算（GridEditor.vue）

```vue
<script setup>
import { reactive } from 'vue'

const gridLevels = reactive([
  { buyPrice: '', buyQty: '', sellPrice: '', sellQty: '' }
])

// 输入时自动触发计算
const updateCalculations = () => {
  gridLevels.forEach(level => {
    const buyPrice = parseFloat(level.buyPrice) || 0
    const buyQty = parseInt(level.buyQty) || 0
    
    // 自动计算买入金额
    level.buyAmount = buyPrice * buyQty
  })
}
</script>

<template>
  <el-input
    v-model="row.buyPrice"
    @input="updateCalculations"
  />
  <el-input
    v-model="row.buyQty"
    @input="updateCalculations"
  />
  <!-- 只读显示计算结果 -->
  <span>{{ row.buyAmount }}</span>
</template>
```

## API 接口

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | /api/stocks/search?keyword=xxx | 搜索股票 |
| GET | /api/strategies | 获取策略列表 |
| GET | /api/strategies/{code} | 获取策略详情 |
| POST | /api/strategies | 创建策略 |
| DELETE | /api/strategies/{code} | 删除策略 |
