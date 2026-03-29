<template>
  <div class="app-container">
    <el-container>
      <el-aside width="250px">
        <div class="logo">
          <h2>交易策略管理系统</h2>
          <span class="version">Version 1.0.0</span>
        </div>
        
        <el-menu
          :default-active="activeMenu"
          class="side-menu"
          router
          mode="vertical"
        >
          <el-sub-menu index="grid">
            <template #title>
              <el-icon><DataAnalysis /></el-icon>
              <span>网格交易</span>
            </template>
            <el-menu-item index="/grid/strategies">策略总览</el-menu-item>
            <el-menu-item index="/grid/new-strategy">新建策略</el-menu-item>
          </el-sub-menu>
          
          <el-sub-menu index="yip">
            <template #title>
              <el-icon><TrendCharts /></el-icon>
              <span>长赢交易</span>
            </template>
            <el-menu-item index="/yip/strategies">策略总览</el-menu-item>
            <el-menu-item index="/yip/new-strategy">新建策略</el-menu-item>
          </el-sub-menu>
        </el-menu>
      </el-aside>
      
      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { DataAnalysis, TrendCharts } from '@element-plus/icons-vue'

const route = useRoute()
const activeMenu = computed(() => {
  // 根据路径返回一级菜单的 index
  if (route.path.startsWith('/grid')) {
    return 'grid'
  } else if (route.path.startsWith('/yip')) {
    return 'yip'
  }
  return route.path
})
</script>

<style scoped>
.app-container {
  min-height: 100vh;
  background-color: #f5f7fa;
}

.el-container {
  min-height: 100vh;
}

.el-aside {
  background-color: #ffffff;
  border-right: 1px solid #e4e7ed;
}

.logo {
  padding: 20px;
  text-align: center;
  border-bottom: 1px solid #e4e7ed;
}

.logo h2 {
  margin: 0;
  font-size: 18px;
  color: #303133;
}

.version {
  font-size: 12px;
  color: #909399;
}

.side-menu {
  border-right: none;
}

.el-main {
  padding: 20px;
}
</style>
