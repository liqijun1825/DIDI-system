import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router/index.js'
import store from './store/index.js'
import panelHead from './components/panelHead.vue'

//刷新后的动态路由添加
const localData = localStorage.getItem('pz_v3pz')
if (localData) {
  store.commit('dynamicMenu', JSON.parse(localData).menu.routerList)
  store.state.menu.routerList.forEach((item) => {
    if (!router.hasRoute(item.name)) {
      router.addRoute('main', item)
    }
  })
}

//路由守卫
router.beforeEach((to, from) => {
  const token = localStorage.getItem('pz_token')
  // 非登录页面，没有token，跳转到登录页面
  if (!token && to.path !== '/login') {
    return '/login'
  } else if (token && to.path === '/login') {
    return '/'
  } else{
    return true
  }
})

// main.ts

// 如果您正在使用CDN引入，请删除下面一行。
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

const app = createApp(App)
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

app.component('panelHead', panelHead)

//挂载路由
app.use(router)
//store挂载
app.use(store)

app.mount('#app')
