<template>
  <div class="new-strategy">
    <h2 class="page-title">新建策略</h2>
    
    <!-- 1. 选择股票 -->
    <el-card class="section-card">
      <template #header>
        <span class="section-title">1. 选择股票</span>
      </template>
      
      <el-form @submit.prevent>
        <el-form-item label="搜索股票">
          <div class="stock-input-wrapper">
            <el-autocomplete
              v-model="searchKeyword"
              :fetch-suggestions="fetchStockSuggestions"
              placeholder="输入股票代码或名称，例如：159938 或 医药 ETF"
              clearable
              @select="onStockSelect"
              style="width: 400px"
            >
              <template #default="{ item }">
                <span>{{ item.name }} ({{ item.code }}) - {{ item.market }}</span>
              </template>
            </el-autocomplete>
            <span v-if="selectedStock" class="success-icon">✅</span>
          </div>
        </el-form-item>
      </el-form>
    </el-card>
    
    <!-- 2. 配置网格档位 -->
    <el-card class="section-card">
      <template #header>
        <span class="section-title">2. 配置网格档位</span>
      </template>
      
      <GridEditor ref="gridEditorRef" @update="onGridUpdate" />
    </el-card>
    
    <!-- 3. 创建策略 -->
    <el-card class="section-card">
      <template #header>
        <span class="section-title">3. 创建策略</span>
      </template>
      
      <div class="action-buttons">
        <el-button type="primary" size="large" @click="createStrategy">
          创建策略
        </el-button>
        <el-button @click="resetForm">重置</el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import { stockApi, strategyApi } from '@/api'
import GridEditor from '@/components/GridEditor.vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// 搜索相关
const searchKeyword = ref('')
const selectedStock = ref(null)

// 网格编辑器
const gridEditorRef = ref(null)
const gridData = ref([])

// 处理网格更新
const onGridUpdate = (data) => {
  gridData.value = data
}

// 获取股票建议（用于 el-autocomplete）
const fetchStockSuggestions = async (queryString, cb) => {
  if (!queryString.trim()) {
    cb([])
    return
  }
  
  try {
    const response = await stockApi.search(queryString)
    const results = response.data.data || []
    cb(results)
  } catch (error) {
    ElMessage.error('搜索失败：' + (error.message || '未知错误'))
    cb([])
  }
}

// 选择股票（从 autocomplete 下拉框选择）
const onStockSelect = (stock) => {
  selectedStock.value = stock
  searchKeyword.value = `${stock.name} (${stock.code})`
}

// 创建策略
const createStrategy = async () => {
  // 验证股票
  if (!selectedStock.value) {
    ElMessage.warning('请选择股票')
    return
  }
  
  // 验证网格数据
  const gridConfig = gridEditorRef.value?.getGridData()
  if (!gridConfig || gridConfig.length === 0 || 
      gridConfig.every(l => !l.buy_price || parseFloat(l.buy_price) === 0)) {
    ElMessage.warning('请至少配置一个有效的网格档位')
    return
  }
  
  try {
    const strategyData = {
      stock_code: selectedStock.value.code,
      stock_name: selectedStock.value.name,
      grid_config: gridConfig
    }
    
    const response = await strategyApi.create(strategyData)
    
    ElMessage.success(`策略创建成功！${selectedStock.value.name}`)
    
    // 跳转到策略详情页
    router.push(`/strategy/${selectedStock.value.code}`)
  } catch (error) {
    ElMessage.error('创建策略失败：' + (error.response?.data?.message || error.message || '未知错误'))
  }
}

// 重置表单
const resetForm = () => {
  searchKeyword.value = ''
  selectedStock.value = null
  if (gridEditorRef.value) {
    // 重置网格编辑器
    gridEditorRef.value.getGridData().fill({ buy_price: '', buy_qty: '', sell_price: '', sell_qty: '' })
  }
  ElMessage.info('已重置表单')
}
</script>

<style scoped>
.new-strategy {
  max-width: 1200px;
  margin: 0 auto;
}

.page-title {
  font-size: 24px;
  color: #303133;
  margin-bottom: 24px;
}

.section-card {
  margin-bottom: 20px;
}

.section-title {
  font-size: 16px;
  font-weight: 500;
  color: #303133;
}


.stock-input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.success-icon {
  margin-left: 8px;
  font-size: 18px;
}

.action-buttons {
  display: flex;
  gap: 12px;
  justify-content: flex-start;
}
</style>
