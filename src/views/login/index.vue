<template>
    <el-row class="login-container" justify="center" :align="'middle'">
        <el-card style="max-width: 480px;">
            <template #header>
                <div class="card-header">
                    <img :src="imgUrl">
                </div>
            </template>
            <div class="jump-link">
                <el-link type="primary" @click="handleChange">{{formType ? '已有账号，去登录' : '没有账号，去注册'}}</el-link>
            </div>
            <el-form
                ref="loginFormRef"
                :model="loginForm" 
                style="max-width: 600px;"
                class="demo-ruleForm"
                :rules="rules">
                <el-form-item prop="username">
                    <el-input v-model="loginForm.userName" placeholder="请输入手机号" :prefix-icon="UserFilled"></el-input>
                </el-form-item>
                <el-form-item prop="password">
                    <el-input v-model="loginForm.passWord" placeholder="请输入密码" :prefix-icon="Lock"></el-input>
                </el-form-item>
                <el-form-item v-if="formType" prop="validCode">
                    <el-input v-model="loginForm.validCode" placeholder="请输入验证码" :prefix-icon="Bell">
                        <template #append>
                            <span @click="countdownChange">{{ countdown.validText }}</span>
                        </template>
                    </el-input>
                </el-form-item>
                <el-form-item>
                    <el-button typr="primary" :style="{width:'100%'}" @click="submitForm(loginFormRef)">
                        {{ !formType ? '登录' : '注册账号'}}
                    </el-button>
                </el-form-item>
            </el-form>
        </el-card>
        <el-dialog v-model="codeDialogVisible" title="验证码提示" width="360px">
            <div style="font-size: 16px; line-height: 1.8;">
                <div>本次验证码：</div>
                <div style="font-size: 28px; font-weight: 700; letter-spacing: 3px; margin: 12px 0;">
                    {{ currentCode }}
                </div>
                <div style="color: #888;">请尽快用于注册，5 秒后自动关闭</div>
            </div>

            <template #footer>
                <el-button @click="closeDialog">关闭</el-button>
                <el-button type="primary" @click="copyCode">复制验证码</el-button>
            </template>
        </el-dialog>
    </el-row>
</template>

<script setup>
import { ref, reactive,computed,toRaw } from 'vue'
import { getCode,userAuthentication,login, menuPermissions  } from '../../api'
import { ElMessageBox } from 'element-plus'
import { UserFilled,Lock,Bell } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'

const codeDialogVisible = ref(false)
const currentCode = ref('')
let dialogTimer = null
const copyCode = async () => {
  try {
    await navigator.clipboard.writeText(currentCode.value)
    ElMessage.success('验证码已复制')
  } catch (e) {
    ElMessage.error('复制失败')
  }
}

const closeDialog = () => {
  codeDialogVisible.value = false
  if (dialogTimer) {
    clearTimeout(dialogTimer)
    dialogTimer = null
  }
}

const imgUrl = new URL('../../assets/login-head.png', import.meta.url).href


// 登录表单
const loginForm = reactive({
    userName: '',
    passWord: '',
    validCode: ''
})

//切换表单（0登录，1注册）
const formType = ref(0)
// 切换登录方式
const handleChange = () => {
    formType.value = formType.value ? 0 : 1
}

//账号校验规则
const validateUser = (rule , value, callback) => {
    //不能为空
    if(!value) {
        callback(new Error('手机号不能为空，请输入手机号'))
    } else {
        const phoneReg = /^1(3[0-9]|4[01456879]|5[0-35-9]|6[2567]|7[0-8]|8[0-9]|9[0-35-9])\d{8}$/
        phoneReg.test(value) ? callback() : callback(new Error('手机号格式不对，请输入正确的手机号'))
    }
    
}

//密码校验规则
const validatePass = (rule , value, callback) => {
    //不能为空
    if(!value) {
        callback(new Error('密码不能为空，请输入密码'))
    } else {
        const reg = /^[a-zA-Z0-9_-]{4,16}$/
        reg.test(value) ? callback() : callback(new Error('密码格式不对，需要4-16位字符，请输入正确的格式'))
    }
}

//表单验证
const rules = reactive({
    userName:[{ validator: validateUser , trigger: 'blur' }],
    passWord:[{ validator: validatePass , trigger: 'blur' }],
})

//发送验证码
const countdown = reactive({
    validText: '获取验证码',
    time: 60
})
let flag = false
const countdownChange = () => {
    // 防止重复点击
    if(flag) return

    //判断手机号格式
    const phoneReg = /^1(3[0-9]|4[01456879]|5[0-35-9]|6[2567]|7[0-8]|8[0-9]|9[0-35-9])\d{8}$/
    if(!loginForm.userName || !phoneReg.test(loginForm.userName)) {
        return ElMessage({
            message: '请检查手机号是否正确',
            type: 'warning',
        })
    }

    //倒计时
    const time = setInterval(() => {
       if(countdown.time <= 0) {
            countdown.time = 60
            countdown.validText = '获取验证码'
            flag = false
            // 清除计时器
            clearInterval(time)
       } else {
            countdown.time -= 1
            countdown.validText = `剩余${countdown.time}s`
       }
    },1000)
    flag = true
    getCode({ tel: loginForm.userName }).then(({ data }) => {
        if (data.code === 10000) {
            ElMessage.success('发送成功')
            currentCode.value = data.data.code
            codeDialogVisible.value = true
            if (dialogTimer) clearTimeout(dialogTimer)
            dialogTimer = setTimeout(() => {
                closeDialog()
            }, 5000)
        }
    })
}
// 路由实例
const router = useRouter()
const loginFormRef = ref()
const store = useStore()

const routerList = computed(() => store.state.menu.routerList)

//提交表单
const submitForm = async (formEl) => {
    if (!formEl) return

    // 校验表单
    await formEl.validate((valid, fields) => {
        if (valid) {
          console.log('submit!')
            if (formType.value) {
                userAuthentication(loginForm).then(( {data} ) => {
                    if(data.code === 10000){
                        ElMessage.success('注册成功,请登录')
                        formType.value = 0
                    }
                })
            } else {
                //登录页面
                login(loginForm).then(( {data} ) =>{
                    if(data.code === 10000){
                        ElMessage.success('登录成功！')
                        // 将token和用户信息缓存到浏览器
                        localStorage.setItem('pz_token',data.data.token)
                        localStorage.setItem('pz_userInfo',JSON.stringify(data.data.userInfo))
                        menuPermissions().then(({ data }) => {
                            store.commit('dynamicMenu', data.data)
                        
                            toRaw(routerList.value).forEach(item => {
                                if (!router.hasRoute(item.name)) {
                                    router.addRoute('main', item)
                                }
                            })
                        
                            router.push('/auth/admin')
                        })
                    }
                })
            }
        } else {
          console.log('error submit!', fields)
        }
    })
}

</script>



<style lang="less" scoped>
:deep(.el-card__header) {
    padding: 0
  }
    .login-container {
      height: 100%;
      .card-header{
        background-color: #899fe1;
        img {
          width: 430px;
        }
    }
    .jump-link {
      text-align: right;
      margin-bottom: 10px;
    }
}
</style>