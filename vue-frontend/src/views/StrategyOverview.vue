<template>
  <div class="strategy-overview">
    <h2 class="page-title">策略总览</h2>
    <p class="page-subtitle">共 {{ strategies.length }} 个策略</p>
    
    <el-card class="table-card" v-loading="loading">
      <el-table
        :data="strategies"
        style="width: 100%"
        class="modern-table"
      >
        <el-table-column prop="stock_name" label="股票名称" min-width="200" />
        <el-table-column prop="stock_code" label="股票代码" min-width="80" />
        <el-table-column label="当前价格" min-width="100" align="right">
          <template #default="{ row }">
            <span class="price-value">{{ row.current_price?.toFixed(3) || '0.000' }}</span>
          </template>
        </el-table-column>
        <el-table-column label="持仓" min-width="100" align="right">
          <template #default="{ row }">
            <span class="position-value">{{ (row.position || 0).toLocaleString() }}</span>
          </template>
        </el-table-column>
        <el-table-column label="距卖出档" min-width="100" align="right">
          <template #default="{ row }">
            <span v-if="row.distance_up === null || row.distance_up === undefined || row.distance_up === '暂无可卖'" style="color: #f43f5e; font-weight: 500;">暂无可卖</span>
            <span v-else style="color: #f43f5e; font-weight: 500;">
              +{{ row.distance_up?.toFixed(1) || 0 }}%
            </span>
          </template>
        </el-table-column>
        <el-table-column label="距买入档" min-width="100" align="right">
          <template #default="{ row }">
            <span v-if="row.distance_down === null || row.distance_down === undefined || row.distance_down === '已突破下限'" style="color: #10b981; font-weight: 500;">已满仓</span>
            <span v-else style="color: #10b981; font-weight: 500;">
              -{{ Math.abs(row.distance_down)?.toFixed(1) || 0 }}%
            </span>
          </template>
        </el-table-column>
        <el-table-column label="收益" min-width="180" align="right">
          <template #default="{ row }">
            <span :class="{ 'text-profit': row.total_profit >= 0, 'text-loss': row.total_profit < 0 }">
              {{ row.total_profit?.toFixed(2) || '0.00' }} ({{ row.return_rate?.toFixed(2) || 0 }}%)
            </span>
          </template>
        </el-table-column>
        <el-table-column label="交易次数" min-width="100" align="right">
          <template #default="{ row }">
            {{ row.transaction_count || 0 }}次
          </template>
        </el-table-column>
        <el-table-column label="操作" min-width="90" align="center" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="viewDetail(row.stock_code)">
              查看
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <el-empty v-if="!loading && strategies.length === 0" description="暂无策略，点击左侧「新建策略」创建" />
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { strategyApi } from '@/api'

const router = useRouter()

const strategies = ref([])
const loading = ref(false)

// 加载策略列表
const loadStrategies = async () => {
  loading.value = true
  try {
    const response = await strategyApi.getList()
    strategies.value = response.data.data || []
  } catch (error) {
    console.error('加载策略列表失败:', error)
  } finally {
    loading.value = false
  }
}

// 查看详情
const viewDetail = (stockCode) => {
  router.push(`/strategy/${stockCode}`)
}

onMounted(() => {
  loadStrategies()
})
</script>

<style scoped>
.strategy-overview {
  max-width: 1400px;
  margin: 0 auto;
  padding: 24px;
  background: #f8f9fa;
  min-height: 100vh;
}

.page-title {
  font-size: 28px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0;
  letter-spacing: -0.5px;
}

.page-subtitle {
  font-size: 14px;
  color: #6b7280;
  margin-bottom: 24px;
  padding: 0 8px;
}

.table-card {
  background: #ffffff;
  border: 1px solid #e8eaed;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
  transition: box-shadow 0.2s ease;
}

.table-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

/* 现代表格样式 */
.modern-table {
  --el-table-border-color: #f0f0f0;
  --el-table-header-bg-color: #fafafa;
  --el-table-text-color: #4b5563;
  --el-table-header-text-color: #6b7280;
  --el-table-row-hover-bg-color: #f9fafb;
}

.modern-table .el-table__header th {
  font-weight: 600;
  font-size: 13px;
  background-color: #fafafa;
  color: #6b7280;
}

.modern-table .el-table__body td {
  font-size: 14px;
  color: #4b5563;
}

.modern-table .el-table__body tr:hover td {
  background-color: #f9fafb;
}

/* 价格数值样式 */
.price-value {
  font-weight: 600;
  color: #1a1a1a;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}

.position-value {
  color: #4b5563;
}

/* 收益颜色 */
.text-profit {
  color: #f43f5e;
  font-weight: 600;
}

.text-loss {
  color: #10b981;
  font-weight: 600;
}

/* 按钮样式 - 扁平化设计 */
:deep(.el-button) {
  border-radius: 8px;
  font-weight: 500;
  font-size: 14px;
  padding: 10px 20px;
  transition: all 0.2s ease;
  border: none;
  box-shadow: none;
}

:deep(.el-button--primary) {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
}

:deep(.el-button--primary:hover) {
  background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

:deep(.el-button--default) {
  background: #f3f4f6;
  color: #4b5563;
  border: none;
}

:deep(.el-button--default:hover) {
  background: #e5e7eb;
  transform: translateY(-1px);
}

/* 卡片样式 */
:deep(.el-card__header) {
  background: #fafafa;
  border-bottom: 1px solid #f0f0f0;
  padding: 16px 20px;
}

:deep(.el-card__body) {
  padding: 20px;
}
</style>
