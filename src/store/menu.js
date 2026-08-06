const localData = localStorage.getItem('pz_v3pz')

const state = localData ? JSON.parse(localData).menu :{
    isCollapse: false, //是否折叠
    selectMenu: [],  //当前选中的菜单
    routerList: [], //动态路由
    menuActive: '1-2-1', //当前激活的菜单
}

const mutations = {
    collapseMenu(state) {
        state.isCollapse = !state.isCollapse
    },
    addMenu(state, payload) {
        // 对数据去重
        if(state.selectMenu.findIndex(item => item.path === payload.path) === -1) {
            state.selectMenu.push(payload)
        }
    },
    closeMenu (state, payload) {
        //找到点击数据的索引
        const index = state.selectMenu.findIndex(val => val.name === payload.name)
        //删除数据
        state.selectMenu.splice(index, 1)
    },
    dynamicMenu(state, payload) {
        // 通过glob导入文件
        const modules = import.meta.glob('../views/**/**/*.vue')
        console.log(modules)
        function routerSet(router)  {
            router.forEach(route => {
                // 判断没有子菜单，拼接路由数据
                if(!route.children) {
                    const url = `../views${route.path}/index.vue`
                    // 拿到获取的vue组件
                    route.component = modules[url]
                } else{
                    routerSet(route.children)
                }
            })  
        }
        routerSet(payload)
        // 拿到完整的路由数据
        state.routerList = payload
    },
    updateMenuActive(state, payload) {
        state.menuActive = payload
    }
}

export default {
    state,
    mutations
}