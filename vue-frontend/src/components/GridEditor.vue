<template>
  <div class="grid-editor">
    <div class="toolbar">
      <el-button type="primary" @click="addLevel" :icon="Plus">
        添加档位
      </el-button>
    </div>
    
    <el-table :data="gridLevels" border class="grid-table">
      <el-table-column label="档位" width="80" align="center">
        <template #default="{ row }">
          <span class="level-text">{{ calculateLevel(row) }}</span>
        </template>
      </el-table-column>
      
      <el-table-column label="买入价" width="120">
        <template #default="{ row }">
          <el-input
            v-model="row.buyPrice"
            type="number"
            placeholder="0"
            @input="updateCalculations"
          />
        </template>
      </el-table-column>
      
      <el-table-column label="买入股数" width="120">
        <template #default="{ row }">
          <el-input
            v-model="row.buyQty"
            type="number"
            placeholder="0"
            @input="updateCalculations"
          />
        </template>
      </el-table-column>
      
      <el-table-column label="买入金额" width="120">
        <template #default="{ row }">
          <span class="calculated-value">{{ formatNumber(row.buyAmount) }}</span>
        </template>
      </el-table-column>
      
      <el-table-column label="卖出价" width="120">
        <template #default="{ row }">
          <el-input
            v-model="row.sellPrice"
            type="number"
            placeholder="0"
            @input="updateCalculations"
          />
        </template>
      </el-table-column>
      
      <el-table-column label="卖出股数" width="120">
        <template #default="{ row }">
          <el-input
            v-model="row.sellQty"
            type="number"
            placeholder="0"
            @input="updateCalculations"
          />
        </template>
      </el-table-column>
      
      <el-table-column label="卖出金额" width="120">
        <template #default="{ row }">
          <span class="calculated-value">{{ formatNumber(row.sellAmount) }}</span>
        </template>
      </el-table-column>
      
      <el-table-column label="资金占用" width="120">
        <template #default="{ row, $index }">
          <span class="calculated-value">{{ formatNumber(calculateCapitalOccupied($index)) }}</span>
        </template>
      </el-table-column>
      
      <el-table-column label="操作" width="80" align="center" fixed="right">
        <template #default="{ $index }">
          <el-button
            type="danger"
            :icon="Delete"
            circle
            size="small"
            @click="removeLevel($index)"
          />
        </template>
      </el-table-column>
    </el-table>
    
    <div class="summary" v-if="totalCapitalOccupied > 0">
      <el-tag type="success" size="large">
        总资金占用：¥{{ formatNumber(totalCapitalOccupied) }}
      </el-tag>
    </div>
  </div>
</template>

<script setup>
import { reactive, computed } from 'vue'
import { Plus, Delete } from '@element-plus/icons-vue'

// 定义发射事件
const emit = defineEmits(['update'])

// 网格档位数据 - 使用响应式数组
const gridLevels = reactive([
  { buyPrice: '', buyQty: '', sellPrice: '', sellQty: '' }
])

// 解析数值（处理空字符串）
const parseNumber = (value) => {
  if (value === '' || value === null || value === undefined) return 0
  const num = parseFloat(value)
  return isNaN(num) ? 0 : num
}

// 解析整数
const parseIntValue = (value) => {
  if (value === '' || value === null || value === undefined) return 0
  const num = parseInt(parseFloat(value))
  return isNaN(num) ? 0 : num
}

// 计算档位（相对于最高买入价的比例）
const calculateLevel = (row) => {
  const buyPrice = parseNumber(row.buyPrice)
  if (buyPrice === 0) return '0.00'
  
  // 找到最高买入价
  const maxBuyPrice = gridLevels
    .map(l => parseNumber(l.buyPrice))
    .reduce((max, curr) => Math.max(max, curr), 0)
  
  if (maxBuyPrice === 0) return '0.00'
  return (buyPrice / maxBuyPrice).toFixed(2)
}

// 更新所有计算
const updateCalculations = () => {
  gridLevels.forEach(level => {
    const buyPrice = parseNumber(level.buyPrice)
    const buyQty = parseIntValue(level.buyQty)
    const sellPrice = parseNumber(level.sellPrice)
    const sellQty = parseIntValue(level.sellQty)
    
    // 自动计算买入金额 = 买入价 × 买入股数
    level.buyAmount = buyPrice * buyQty
    
    // 自动计算卖出金额 = 卖出价 × 卖出股数
    level.sellAmount = sellPrice * sellQty
  })
  
  // 发射更新事件，将数据传递给父组件
  emit('update', gridLevels.map(level => ({
    buy_price: level.buyPrice,
    buy_qty: level.buyQty,
    sell_price: level.sellPrice,
    sell_qty: level.sellQty,
    buy_amount: level.buyAmount,
    sell_amount: level.sellAmount
  })))
}

// 计算累计资金占用
const calculateCapitalOccupied = (index) => {
  let total = 0
  for (let i = 0; i <= index; i++) {
    total += gridLevels[i].buyAmount || 0
  }
  return total
}

// 总资金占用
const totalCapitalOccupied = computed(() => {
  return gridLevels.reduce((sum, level) => sum + (level.buyAmount || 0), 0)
})

// 添加档位
const addLevel = () => {
  gridLevels.push({ buyPrice: '', buyQty: '', sellPrice: '', sellQty: '' })
}

// 删除档位
const removeLevel = (index) => {
  if (gridLevels.length === 1) {
    // 如果只剩一行，清空而不是删除
    gridLevels[0] = { buyPrice: '', buyQty: '', sellPrice: '', sellQty: '' }
  } else {
    gridLevels.splice(index, 1)
  }
  updateCalculations()
}

// 格式化数字（带千分位）
const formatNumber = (num) => {
  if (!num || num === 0) return ''
  return num.toLocaleString('zh-CN', { maximumFractionDigits: 0 })
}

// 暴露方法给父组件
defineExpose({
  getGridData: () => gridLevels.map(level => ({
    buy_price: level.buyPrice,
    buy_qty: level.buyQty,
    sell_price: level.sellPrice,
    sell_qty: level.sellQty
  }))
})
</script>

<style scoped>
.grid-editor {
  margin-top: 20px;
}

.toolbar {
  margin-bottom: 16px;
}

.grid-table {
  width: 100%;
}

.level-text {
  font-weight: 500;
  color: #606266;
}

.calculated-value {
  color: #409EFF;
  font-weight: 500;
}

:deep(.el-input__inner) {
  text-align: right;
}

:deep(.el-table__cell) {
  padding: 8px 0;
}

.summary {
  margin-top: 16px;
  text-align: right;
}

.summary .el-tag {
  font-size: 16px;
  padding: 8px 16px;
}
</style>
