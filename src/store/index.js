import{ createStore } from 'vuex'
import menu from './menu'
//  实现vuex数据持久化
import createPersistedState from 'vuex-persistedstate'

export default createStore({
    plugins: [createPersistedState({
        // 持久化哪些数据
        key: 'pz_v3pz'
    })],
    modules:{
        //模块
        menu
    }
})