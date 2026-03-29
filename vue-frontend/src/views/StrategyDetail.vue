<template>
  <div class="strategy-detail" v-loading="loading">
    <div class="page-header" v-if="strategy">
      <h2 class="page-title">{{ strategy.stock_name }} ({{ strategy.stock_code }})</h2>
      <el-button @click="goBack">← 返回总览</el-button>
    </div>
    
    <div v-if="!loading && strategy" class="detail-content">
      <!-- 1. 策略信息 -->
      <el-card class="section-card">
        <template #header>
          <span class="section-title">📋 策略信息</span>
        </template>
        
        <el-row :gutter="20">
          <el-col :span="5">
            <el-statistic title="当前价格" :value="strategy.current_price || 0" :precision="3">
            </el-statistic>
          </el-col>
          <el-col :span="5">
            <el-statistic title="持仓" :value="holdingValue || 0" :precision="0">
            </el-statistic>
          </el-col>
          <el-col :span="5">
            <el-statistic
              title="总收益"
              :value="totalReturn || 0"
              :precision="2"
              :value-style="{ color: (totalReturn || 0) >= 0 ? '#f43f5e' : '#10b981', fontWeight: '700' }"
            >
              <template #suffix>
                <span :style="{ color: (totalReturn || 0) >= 0 ? '#f43f5e' : '#10b981' }" v-if="totalInvested > 0">
                  ({{ ((totalReturn / totalInvested) * 100) >= 0 ? '+' : '' }}{{ ((totalReturn / totalInvested) * 100).toFixed(1) }}%)
                </span>
              </template>
            </el-statistic>
          </el-col>
          <el-col :span="5">
            <div class="custom-statistic">
              <div class="el-statistic__title">距卖出档</div>
              <div class="el-statistic__content">
                <span v-if="typeof distanceToSell === 'string'" :style="{ color: '#f43f5e', fontWeight: 500 }">{{ distanceToSell }}</span>
                <span v-else :style="{ color: '#f43f5e', fontWeight: 500 }">+{{ distanceToSell.toFixed(2) }}%</span>
              </div>
            </div>
          </el-col>
          <el-col :span="4">
            <div class="custom-statistic">
              <div class="el-statistic__title">距买入档</div>
              <div class="el-statistic__content">
                <span v-if="typeof distanceToBuy === 'string'" :style="{ color: '#10b981', fontWeight: 500 }">{{ distanceToBuy }}</span>
                <span v-else :style="{ color: '#10b981', fontWeight: 500 }">{{ distanceToBuy.toFixed(2) }}%</span>
              </div>
            </div>
          </el-col>
        </el-row>
      </el-card>
      
      <!-- 2. 网格配置 -->
      <el-card class="section-card">
        <template #header>
          <span class="section-title">⚙️ 网格配置</span>
        </template>
        
        <el-table :data="gridMetrics" v-if="gridMetrics.length > 0" style="width: 100%">
          <el-table-column prop="level" label="档位" min-width="70" align="center">
            <template #default="{ row }">
              {{ row.level.toFixed(2) }}
            </template>
          </el-table-column>
          <el-table-column label="买入价" min-width="90" align="right">
            <template #default="{ row }">
              <span :class="{ 'highlight-buy': isCloseToCurrent(row.buy_price, 'buy'), 'pending-order-buy': isPendingBuyOrder(row) }">
                {{ row.buy_price > 0 ? row.buy_price.toFixed(3) : '' }}
              </span>
            </template>
          </el-table-column>
          <el-table-column prop="buy_qty" label="买入股数" min-width="85" align="right">
            <template #default="{ row }">
              <span :class="{ 'pending-order-buy': isPendingBuyOrder(row) }">
                {{ row.buy_qty > 0 ? row.buy_qty.toLocaleString() : '' }}
              </span>
            </template>
          </el-table-column>
          <el-table-column label="买入金额" min-width="100" align="right">
            <template #default="{ row }">
              <span :class="{ 'pending-order-buy': isPendingBuyOrder(row) }">
                {{ row.buy_amount > 0 ? Math.round(row.buy_amount).toLocaleString() : '' }}
              </span>
            </template>
          </el-table-column>
          <el-table-column label="卖出价" min-width="90" align="right">
            <template #default="{ row }">
              <span :class="{ 'highlight-sell': isCloseToCurrent(row.sell_price, 'sell'), 'pending-order-sell': isPendingSellOrder(row) }">
                {{ row.sell_price > 0 ? row.sell_price.toFixed(3) : '' }}
              </span>
            </template>
          </el-table-column>
          <el-table-column prop="sell_qty" label="卖出股数" min-width="85" align="right">
            <template #default="{ row }">
              <span :class="{ 'pending-order-sell': isPendingSellOrder(row) }">
                {{ row.sell_qty > 0 ? row.sell_qty.toLocaleString() : '' }}
              </span>
            </template>
          </el-table-column>
          <el-table-column label="卖出金额" min-width="100" align="right">
            <template #default="{ row }">
              <span :class="{ 'pending-order-sell': isPendingSellOrder(row) }">
                {{ row.sell_amount > 0 ? Math.round(row.sell_amount).toLocaleString() : '' }}
              </span>
            </template>
          </el-table-column>
          <el-table-column label="资金占用" min-width="100" align="right">
            <template #default="{ row }">
              {{ row.capital_occupied > 0 ? Math.round(row.capital_occupied).toLocaleString() : '' }}
            </template>
          </el-table-column>
        </el-table>
        
        <el-empty v-else description="暂无网格配置" />
      </el-card>
      
      <!-- 3. 走势图 -->
      <el-card class="section-card">
        <template #header>
          <span class="section-title">📈 走势图</span>
        </template>
        
        <div ref="chartContainer" class="chart-container" style="height: 400px;"></div>
      </el-card>
      
      <!-- 4. 绩效分析 -->
      <el-card class="section-card">
        <template #header>
          <span class="section-title">📊 绩效分析</span>
        </template>
        
        <el-row :gutter="20" v-if="transactions.length > 0">
          <el-col :span="5">
            <el-statistic title="总投入" :value="totalInvested" :precision="0">
              <template #prefix>¥</template>
            </el-statistic>
          </el-col>
          <el-col :span="5">
            <el-statistic 
              title="总收益" 
              :value="totalProfit" 
              :precision="2"
              :value-style="{ color: totalProfit >= 0 ? '#f56c6c' : '#67c23a' }"
            >
              <template #prefix>¥</template>
            </el-statistic>
          </el-col>
          <el-col :span="5">
            <el-statistic 
              title="绝对收益" 
              :value="absoluteReturn" 
              :precision="2"
              :value-style="{ color: absoluteReturn >= 0 ? '#f56c6c' : '#67c23a' }"
            >
              <template #prefix>¥</template>
            </el-statistic>
          </el-col>
          <el-col :span="5">
            <el-statistic title="交易次数" :value="transactions.length" suffix="次" />
          </el-col>
          <el-col :span="4">
            <el-statistic title="胜率" :value="winRate" :precision="1" suffix="%" />
          </el-col>
        </el-row>
        
        <el-empty v-else description="暂无交易记录，无法计算绩效指标" />
      </el-card>
      
      <!-- 5. 交易记录 -->
      <el-card class="section-card">
        <template #header>
          <div class="card-header-row">
            <span class="section-title">💰 交易记录</span>
            <el-button type="primary" @click="showTransactionDialog = true">➕ 录入新交易</el-button>
          </div>
        </template>
        
        <el-table :data="transactions" v-if="transactions.length > 0">
          <el-table-column prop="trade_date" label="日期" width="120" />
          <el-table-column label="类型" width="80" align="center">
            <template #default="{ row }">
              <el-tag :type="row.trade_quantity > 0 ? 'success' : 'danger'">
                {{ row.trade_quantity > 0 ? '买入' : '卖出' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="股数" width="100" align="right">
            <template #default="{ row }">
              {{ Math.abs(row.trade_quantity) }}
            </template>
          </el-table-column>
          <el-table-column prop="trade_price" label="价格" width="100" align="right">
            <template #default="{ row }">
              {{ row.trade_price.toFixed(3) }}
            </template>
          </el-table-column>
          <el-table-column label="金额" width="120" align="right">
            <template #default="{ row }">
              <span :style="{ color: row.trade_amount > 0 ? '#f43f5e' : '#10b981' }">
                {{ row.trade_amount.toFixed(2) }}
              </span>
            </template>
          </el-table-column>
          <el-table-column prop="profit" label="收益" width="100" align="right">
            <template #default="{ row }">
              <span :style="{ color: (row.profit || 0) >= 0 ? '#f43f5e' : '#10b981' }">
                {{ row.profit !== null ? ((row.profit >= 0 ? '+' : '') + row.profit.toFixed(2)) : '-' }}
              </span>
            </template>
          </el-table-column>
          <el-table-column prop="return_rate" label="收益率" width="100" align="right">
            <template #default="{ row }">
              <span :style="{ color: (row.return_rate || 0) >= 0 ? '#f43f5e' : '#10b981' }">
                {{ row.return_rate !== null ? ((row.return_rate >= 0 ? '+' : '') + row.return_rate.toFixed(2) + '%') : '-' }}
              </span>
            </template>
          </el-table-column>
          <el-table-column prop="notes" label="备注" />
        </el-table>
        
        <div class="transaction-actions" v-if="transactions.length > 0">
          <el-button type="danger" @click="deleteLastTransaction">🗑️ 删除最后一条交易记录</el-button>
        </div>
        
        <el-empty v-else description="暂无交易记录" />
      </el-card>
    </div>
    
    <!-- 交易录入对话框 -->
    <el-dialog
      v-model="showTransactionDialog"
      title="录入新交易"
      width="600px"
    >
      <el-form :model="transactionForm" label-width="100px">
        <el-form-item label="交易类型">
          <el-radio-group v-model="transactionForm.tradeType">
            <el-radio-button label="买入" />
            <el-radio-button label="卖出" />
          </el-radio-group>
        </el-form-item>
        
        <el-form-item label="交易日期">
          <el-date-picker
            v-model="transactionForm.tradeDate"
            type="date"
            placeholder="选择日期"
            value-format="YYYY-MM-DD"
          />
        </el-form-item>
        
        <el-form-item label="交易价格">
          <el-input-number
            v-model="transactionForm.tradePrice"
            :min="0"
            :step="0.001"
            :precision="3"
            style="width: 200px"
          />
        </el-form-item>
        
        <el-form-item label="交易股数">
          <el-input-number
            v-model="transactionForm.tradeQuantity"
            :min="0"
            :step="100"
            style="width: 200px"
          />
        </el-form-item>
        
        <el-form-item label="交易金额">
          <el-input-number
            v-model="transactionForm.tradeAmount"
            :min="0"
            :step="0.01"
            :precision="2"
            placeholder="不填自动计算"
            style="width: 200px"
          />
        </el-form-item>
        
        <el-form-item label="备注">
          <el-input v-model="transactionForm.notes" placeholder="例如：建仓、止盈等" />
        </el-form-item>
        
        <el-form-item label="收益" v-if="transactionForm.tradeType === '卖出'">
          <el-input-number
            v-model="transactionForm.profit"
            :step="0.01"
            :precision="2"
            style="width: 200px"
          />
        </el-form-item>
        
        <el-form-item label="收益率" v-if="transactionForm.tradeType === '卖出'">
          <el-input-number
            v-model="transactionForm.returnRate"
            :step="0.01"
            :precision="2"
            style="width: 200px"
          />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="showTransactionDialog = false">取消</el-button>
        <el-button type="primary" @click="submitTransaction">提交</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, nextTick, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { strategyApi } from '@/api'
import { createChart, CandlestickSeries } from 'lightweight-charts'

const route = useRoute()
const router = useRouter()

const loading = ref(false)
const strategy = ref(null)
const gridMetrics = ref([])
const transactions = ref([])
const chartContainer = ref(null)
const chart = ref(null)
const candlestickSeries = ref(null)
const volumeSeries = ref(null)
const pendingBuyOrders = ref([])
const pendingSellOrders = ref([])

// 交易对话框
const showTransactionDialog = ref(false)
const transactionForm = reactive({
  tradeType: '买入',
  tradeDate: new Date().toISOString().split('T')[0],
  tradePrice: 0,
  tradeQuantity: 0,
  tradeAmount: 0,
  notes: '',
  profit: null,
  returnRate: null
})

// 计算指标
const totalInvested = computed(() => {
  return transactions.value
    .filter(t => t.trade_quantity > 0)
    .reduce((sum, t) => sum + Math.abs(t.trade_amount), 0)
})

// 已卖出金额：所有卖出交易金额的绝对值之和
const totalSold = computed(() => {
  return transactions.value
    .filter(t => t.trade_quantity < 0)
    .reduce((sum, t) => sum + Math.abs(t.trade_amount), 0)
})

// 持仓金额 = 现价 × 持有份数（总买入份数 - 总卖出份数）
const holdingValue = computed(() => {
  const totalBuyQty = transactions.value
    .filter(t => t.trade_quantity > 0)
    .reduce((sum, t) => sum + t.trade_quantity, 0)
  const totalSellQty = transactions.value
    .filter(t => t.trade_quantity < 0)
    .reduce((sum, t) => sum + Math.abs(t.trade_quantity), 0)
  const holdingQty = totalBuyQty - totalSellQty
  const currentPrice = strategy.value?.current_price || 0
  return currentPrice * holdingQty
})

// 总收益 = 持仓 + 已卖出金额 - 总买入金额
const totalReturn = computed(() => {
  return holdingValue.value + totalSold.value - totalInvested.value
})

// 绝对收益（与 totalReturn 相同）
const absoluteReturn = computed(() => {
  return totalReturn.value
})

// 已实现收益：用户手动填写的 profit 字段（用于参考）
const totalProfit = computed(() => {
  return transactions.value
    .filter(t => t.profit !== null)
    .reduce((sum, t) => sum + t.profit, 0)
})

const winRate = computed(() => {
  const profitableTrades = transactions.value.filter(t => (t.profit || 0) > 0).length
  const totalTrades = transactions.value.filter(t => t.profit !== null).length
  return totalTrades > 0 ? (profitableTrades / totalTrades) * 100 : 0
})

// 加载策略详情
const loadStrategy = async () => {
  loading.value = true
  try {
    const response = await strategyApi.getDetail(route.params.stockCode)
    console.log('API Response:', response)
    // API 返回格式为 { code, message, data }，需要访问 response.data.data
    const strategyData = response.data.data
    console.log('Strategy Data:', strategyData)
    console.log('K 线 Data:', strategyData?.kline_data)
    console.log('Current Price:', strategyData?.current_price)
    strategy.value = strategyData
    gridMetrics.value = strategyData.grid_metrics || []
    transactions.value = strategyData.transactions || []
    pendingBuyOrders.value = strategyData.pending_buy_orders || []
    pendingSellOrders.value = strategyData.pending_sell_orders || []
    
    // 等待 DOM 完全渲染后再初始化图表
    await nextTick()
    setTimeout(() => {
      initChart()
    }, 100)
  } catch (error) {
    console.error('Error loading strategy:', error)
    ElMessage.error('加载策略详情失败：' + (error.message || '未知错误'))
  } finally {
    loading.value = false
  }
}

// 初始化图表
const initChart = () => {
  if (!chartContainer.value) {
    console.error('Chart container not found, retrying...')
    setTimeout(() => {
      initChart()
    }, 200)
    return
  }
  
  // 销毁旧图表
  if (chart.value) {
    chart.value.remove()
  }
  
  // 使用后端返回的 K 线数据
  const klineData = strategy.value?.kline_data || []
  console.log('K 线数据:', klineData)
  
  // 获取网格档位数据
  const gridMetrics = strategy.value?.grid_metrics || []
  console.log('Grid metrics:', gridMetrics)
  
  // 创建 Lightweight Charts 图表
  chart.value = createChart(chartContainer.value, {
    width: chartContainer.value.clientWidth,
    height: 400,
    layout: {
      background: { color: '#ffffff' },
      textColor: '#333'
    },
    grid: {
      vertLines: { color: '#f0f0f0' },
      horzLines: { color: '#f0f0f0' }
    },
    crosshair: {
      mode: 1, // CrosshairMode.Normal
      vertLine: {
        width: 1,
        color: '#1976D2',
        style: 3, // 3 = Dashed
        labelVisible: true,
        labelBackgroundColor: '#1976D2',
        labelTextColor: '#ffffff'
      },
      horzLine: {
        width: 1,
        color: '#1976D2',
        style: 3, // 3 = Dashed
        labelVisible: true,
        labelBackgroundColor: '#1976D2',
        labelTextColor: '#ffffff'
      }
    },
    timeScale: {
      timeVisible: false,
      secondsVisible: false
    }
  })
  
  // 创建 K 线系列
  candlestickSeries.value = chart.value.addSeries(CandlestickSeries, {
    upColor: '#EF5350',
    downColor: '#26A69A',
    borderUpColor: '#EF5350',
    borderDownColor: '#26A69A',
    wickUpColor: '#EF5350',
    wickDownColor: '#26A69A'
  })
  
  if (klineData.length === 0) {
    console.warn('No K 线 data available')
    return
  }
  
  // 准备图表数据
  const candleData = klineData.map(item => ({
    time: item.date,
    open: parseFloat(item.open),
    high: parseFloat(item.high),
    low: parseFloat(item.low),
    close: parseFloat(item.close)
  }))
  
  console.log('Candle data:', candleData.slice(0, 5))
  
  // 设置数据
  candlestickSeries.value.setData(candleData)
  
  // 添加网格档位价格线
  gridMetrics.forEach((grid, index) => {
    if (grid.buy_price && grid.buy_price > 0) {
      // 创建买入档位价格线（蓝色虚线）
      candlestickSeries.value.createPriceLine({
        price: grid.buy_price,
        color: '#2196F3',
        lineWidth: 2,
        lineStyle: 2, // 2 = Dashed
        axisLabelVisible: true,
        title: `买入档${grid.level.toFixed(2)}`
      })
    }
  })
  
  // 添加跨系列十字线标签显示 OHLC 数据
  chart.value.subscribeCrosshairMove((param) => {
    if (param.time && param.seriesData.size > 0) {
      const data = param.seriesData.get(candlestickSeries.value)
      if (data) {
        // 在价格轴上显示 OHLC 信息
        const ohlcLabel = `O: ${data.open.toFixed(3)} H: ${data.high.toFixed(3)} L: ${data.low.toFixed(3)} C: ${data.close.toFixed(3)}`
        console.log('Crosshair OHLC:', ohlcLabel)
      }
    }
  })
  
  // 自动缩放以适应数据
  chart.value.timeScale().fitContent()
  
  // 窗口大小变化时调整图表
  const resizeObserver = new ResizeObserver(entries => {
    if (entries.length > 0 && chart.value) {
      chart.value.applyOptions({
        width: chartContainer.value.clientWidth,
        height: 400
      })
    }
  })
  resizeObserver.observe(chartContainer.value)
}

// 判断是否接近当前价格
// type: 'buy' 表示买入档（距下档），'sell' 表示卖出档（距上档）
const isCloseToCurrent = (price, type) => {
  if (!price || !strategy.value?.current_price) return false
  const diff = Math.abs(price - strategy.value.current_price)
  return diff < 0.05 // 相差小于 0.05 元时高亮
}

// 判断是否是挂单买入档位
const isPendingBuyOrder = (gridRow) => {
  if (!pendingBuyOrders.value || pendingBuyOrders.value.length === 0) return false
  const rowBuyPrice = gridRow.buy_price
  return pendingBuyOrders.value.some(order => Math.abs(order.buy_price - rowBuyPrice) < 0.001)
}

// 判断是否是挂单卖出档位
const isPendingSellOrder = (gridRow) => {
  if (!pendingSellOrders.value || pendingSellOrders.value.length === 0) return false
  const rowSellPrice = gridRow.sell_price
  return pendingSellOrders.value.some(order => Math.abs(order.sell_price - rowSellPrice) < 0.001)
}

// 计算距买入档（距下档）的距离 - 与后端逻辑保持一致，返回负数
const distanceToBuy = computed(() => {
  if (!strategy.value?.current_price || gridMetrics.value.length === 0) return null
  const currentPrice = strategy.value.current_price
  // 找到所有买入价中低于当前价格的最高价（最近的买入档）
  const buyPrices = gridMetrics.value
    .filter(g => g.buy_price > 0 && g.buy_price < currentPrice)
    .map(g => g.buy_price)
  if (buyPrices.length === 0) return '已满仓'
  const nearestBuyPrice = Math.max(...buyPrices)
  // 与后端保持一致：返回负数，表示距离下方买入档的距离
  return -((currentPrice - nearestBuyPrice) / currentPrice * 100)
})

// 计算距卖出档（距上档）的距离 - 与后端逻辑保持一致，返回正数
const distanceToSell = computed(() => {
  if (!strategy.value?.current_price || gridMetrics.value.length === 0) return null
  const currentPrice = strategy.value.current_price
  // 找到所有卖出价中高于当前价格的最低价（最近的卖出档）
  const sellPrices = gridMetrics.value
    .filter(g => g.sell_price > 0 && g.sell_price > currentPrice)
    .map(g => g.sell_price)
  if (sellPrices.length === 0) return '暂无可卖'
  const nearestSellPrice = Math.min(...sellPrices)
  // 与后端保持一致：返回正数，表示距离上方卖出档的距离
  return (nearestSellPrice - currentPrice) / currentPrice * 100
})

// 提交交易
const submitTransaction = async () => {
  if (transactionForm.tradePrice <= 0 || transactionForm.tradeQuantity <= 0) {
    ElMessage.warning('请输入有效的交易价格和数量')
    return
  }
  
  try {
    const tradeAmount = transactionForm.tradeAmount > 0 
      ? transactionForm.tradeAmount 
      : transactionForm.tradePrice * transactionForm.tradeQuantity
    
    const data = {
      trade_date: transactionForm.tradeDate,
      trade_price: transactionForm.tradePrice,
      trade_quantity: transactionForm.tradeType === '买入' 
        ? transactionForm.tradeQuantity 
        : -transactionForm.tradeQuantity,
      trade_amount: transactionForm.tradeType === '买入' ? tradeAmount : -tradeAmount,
      profit: transactionForm.profit,
      return_rate: transactionForm.returnRate,
      notes: transactionForm.notes
    }
    
    await strategyApi.addTransaction(route.params.stockCode, data)
    ElMessage.success('交易记录添加成功！')
    showTransactionDialog.value = false
    loadStrategy()
  } catch (error) {
    ElMessage.error('添加交易失败：' + (error.message || '未知错误'))
  }
}

// 删除最后一条交易
const deleteLastTransaction = async () => {
  try {
    await strategyApi.deleteLastTransaction(route.params.stockCode)
    ElMessage.success('已删除最后一条交易记录')
    loadStrategy()
  } catch (error) {
    ElMessage.error('删除失败：' + (error.message || '未知错误'))
  }
}

// 返回总览
const goBack = () => {
  router.push('/')
}

onMounted(() => {
  loadStrategy()
})

onUnmounted(() => {
  // 清理图表
  if (chart.value) {
    chart.value.remove()
  }
})
</script>

<style scoped>
.strategy-detail {
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px;
  background: #f8f9fa;
  min-height: 100vh;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
  padding: 0 8px;
}

.page-title {
  font-size: 28px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0;
  letter-spacing: -0.5px;
}

.detail-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.section-card {
  margin-bottom: 0;
  background: #ffffff;
  border: 1px solid #e8eaed;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
  transition: box-shadow 0.2s ease;
}

.section-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

/* 自定义统计样式 */
.custom-statistic {
  text-align: center;
}

.custom-statistic .el-statistic__title {
  font-size: 14px;
  color: #6b7280;
  margin-bottom: 8px;
}

.custom-statistic .el-statistic__content {
  font-size: 20px;
  font-weight: 600;
  color: #1a1a1a;
}

.section-title {
  font-size: 15px;
  font-weight: 600;
  color: #1a1a1a;
  letter-spacing: -0.3px;
}

.card-header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chart-container {
  width: 100%;
  height: 400px;
  border-radius: 8px;
  overflow: hidden;
}

.highlight-buy {
  color: #10b981;
  font-weight: 500;
}

.highlight-sell {
  color: #f43f5e;
  font-weight: 500;
}

.transaction-actions {
  margin-top: 16px;
  text-align: right;
}

/* 表格样式优化 */
:deep(.el-table) {
  --el-table-border-color: #f0f0f0;
  --el-table-header-bg-color: #fafafa;
  --el-table-text-color: #4b5563;
  --el-table-header-text-color: #6b7280;
  --el-table-row-hover-bg-color: #f9fafb;
}

:deep(.el-table th) {
  font-weight: 600;
  font-size: 13px;
  background-color: #fafafa;
  color: #6b7280;
}

:deep(.el-table td) {
  font-size: 14px;
  color: #4b5563;
}

:deep(.el-card__header) {
  background: #fafafa;
  border-bottom: 1px solid #f0f0f0;
  padding: 16px 20px;
}

:deep(.el-card__body) {
  padding: 20px;
}

/* 按钮样式 - 轻盈扁平化设计 */
:deep(.el-button) {
  border-radius: 6px;
  font-weight: 500;
  font-size: 14px;
  padding: 8px 16px;
  transition: all 0.2s ease;
  border: none;
  box-shadow: none;
}

:deep(.el-button--primary) {
  background: #667eea;
  border: none;
}

:deep(.el-button--primary:hover) {
  background: #7c8eee;
  transform: translateY(-1px);
}

:deep(.el-button--danger) {
  background: #ff6b6b;
  border: none;
}

:deep(.el-button--danger:hover) {
  background: #ff8787;
  transform: translateY(-1px);
}

:deep(.el-button--default) {
  background: #f0f0f0;
  color: #666;
  border: none;
}

:deep(.el-button--default:hover) {
  background: #e0e0e0;
}

/* 标签样式 - 扁平化设计 */
:deep(.el-tag) {
  border-radius: 6px;
  font-weight: 500;
  border: none;
  padding: 4px 12px;
}

:deep(.el-tag--success) {
  background: #10b981;
  color: #ffffff;
}

:deep(.el-tag--danger) {
  background: #f43f5e;
  color: #ffffff;
}

:deep(.el-tag--info) {
  background: #6b7280;
  color: #ffffff;
}

/* 挂单提示 - 黄色填充 + 左侧彩色边框 */
.pending-order-buy {
  background: linear-gradient(to right, #dbeafe 0%, #fef3c7 100%);
  padding: 4px 8px;
  border-radius: 4px;
  font-weight: 600;
  border-left: 3px solid #3b82f6;
  display: inline-block;
  min-width: 60px;
  text-align: right;
}

.pending-order-sell {
  background: linear-gradient(to right, #ffedd5 0%, #fef3c7 100%);
  padding: 4px 8px;
  border-radius: 4px;
  font-weight: 600;
  border-left: 3px solid #f97316;
  display: inline-block;
  min-width: 60px;
  text-align: right;
}
</style>
