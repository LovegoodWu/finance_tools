import { createRouter, createWebHistory } from 'vue-router'
import StrategyOverview from '../views/StrategyOverview.vue'
import NewStrategy from '../views/NewStrategy.vue'
import StrategyDetail from '../views/StrategyDetail.vue'

const routes = [
  {
    path: '/',
    redirect: '/grid/strategies'
  },
  {
    path: '/grid',
    name: 'GridTrading',
    redirect: '/grid/strategies',
    children: [
      {
        path: 'strategies',
        name: 'GridStrategyOverview',
        component: StrategyOverview
      },
      {
        path: 'new-strategy',
        name: 'GridNewStrategy',
        component: NewStrategy
      }
    ]
  },
  {
    path: '/strategy/:stockCode',
    name: 'StrategyDetail',
    component: StrategyDetail,
    props: true
  },
  {
    path: '/yip',
    name: 'YipTrading',
    redirect: '/yip/strategies',
    children: [
      {
        path: 'strategies',
        name: 'YipStrategyOverview',
        component: { template: '<div class="placeholder"><h2>长赢策略 - 开发中</h2></div>' }
      },
      {
        path: 'new-strategy',
        name: 'YipNewStrategy',
        component: { template: '<div class="placeholder"><h2>长赢策略 - 开发中</h2></div>' }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
