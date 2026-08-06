<template>
    <div class="header-container">
        <div class="header-left flex-box">
            <el-icon class="icon" size="20" @click="store.commit('collapseMenu')"><Fold /></el-icon>
            <ul class="flex-box">
                <li 
                    v-for="(item,index) of selectMenu" 
                    :key="item.path"
                    :class="{selected: route.path === item.path}"
                    class="tab flex-box">
                    <el-icon size="12"><component :is="item.icon" /></el-icon>
                    <router-link class="text flex-box" :to="item.path">
                        {{ item.name }}
                    </router-link>
                    <el-icon class="close" size="12" @click="closeTap(item,index)"><Close /></el-icon>
                </li>
            </ul>
        </div>
        <div class="header-right">
            <el-dropdown @command="handleClick">
                <div class="el-dropdown-link flex-box">
                    <el-avatar
                       :src="userInfo.avatar"
                    />
                    <p class="user-name">{{ userInfo.nickName }}</p>
                </div>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item command="cancel">退出登录</el-dropdown-item>
                  </el-dropdown-menu>
                </template>
            </el-dropdown>
        </div>
    </div>
</template>

<script setup>
import { computed,ref } from 'vue'
import { useStore } from 'vuex'
import router from '../router';
import { useRoute } from 'vue-router';

//拿到store实例
const store = useStore()
//拿到当前路由
const route = useRoute()
const selectMenu = computed(() => store.state.menu.selectMenu)

const userInfo = JSON.parse(localStorage.getItem('pz_userInfo'))

//点击关闭tag
const closeTap = (item,index) => {
    store.commit('closeMenu',item)
    //删除的非当前页tag
    if(item.path !== route.path){
        return
    }
    //删除的是当前页tag
    const selectMenuData = selectMenu.value
    //删除的是最后一个tag
    if(index === selectMenuData.length){
        //如果只有一个tag，则跳转到首页
        if(!selectMenuData.length){
            router.push('/')
        }else{
            router.push({
                path: selectMenuData[index-1].path
            })
        }
    } else {
        router.push({
            path: selectMenuData[index].path
        })
    }
}

const handleClick = (command) => {
    if(command === 'cancel'){
        localStorage.removeItem('pz_token')
        localStorage.removeItem('pz_userInfo')
        localStorage.removeItem('pz_v3pz')
        window.location.href = window.location.origin
    }
}

</script>

<style lang="less" scoped>
.flex-box{
    display: flex;
    align-items: center;
    height: 100%;
}
.header-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    height: 100%;
    background-color: #fff;
    padding-right: 25px;
    .header-left {
        height: 100%;
        .icon {
            width:45px;
            height:100%;
        }
        .icon:hover{
            background-color: #f5f5f5;
            cursor: pointer;
        }
        .tab {
            padding: 0 10px;
            height: 100%;
            .text {
                margin: 0 5px;
            }
            .close {
                visibility: hidden;
            }
            &.selected {
                a {
                    color: #409eff;
                }
                i {
                    color: #409eff;
                }
                background-color: #f5f5f5;
            }
        }
        .tab:hover {
            background-color: #f5f5f5;
            .close{
                visibility: inherit;
                cursor: pointer;
                color:#333;
            }
        }
    }
    .header-right {
        .user-name {
            margin-left: 10px;
        }
    }
    a {
        height: 100%;
        color: #333;
        font-size: 15px;
    }
}
</style>
