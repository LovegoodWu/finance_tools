import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000
})

// 股票相关 API
export const stockApi = {
  // 搜索股票
  search(keyword) {
    return api.get('/stocks/search', { params: { keyword } })
  },
  
  // 获取股票列表
  getList() {
    return api.get('/stocks/list')
  }
}

// 策略相关 API
export const strategyApi = {
  // 获取策略列表
  getList() {
    return api.get('/strategies')
  },
  
  // 获取策略详情
  getDetail(stockCode) {
    return api.get(`/strategies/${stockCode}`)
  },
  
  // 创建策略
  create(data) {
    return api.post('/strategies', data)
  },
  
  // 删除策略
  delete(stockCode) {
    return api.delete(`/strategies/${stockCode}`)
  },
  
  // 获取交易记录
  getTransactions(stockCode) {
    return api.get(`/strategies/${stockCode}/transactions`)
  },
  
  // 添加交易记录
  addTransaction(stockCode, data) {
    return api.post(`/strategies/${stockCode}/transactions`, data)
  },
  
  // 删除最后一条交易记录
  deleteLastTransaction(stockCode) {
    return api.delete(`/strategies/${stockCode}/transactions/last`)
  }
}

export default api
