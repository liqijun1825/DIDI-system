<template>
    <panel-head :route="route"/>
    <div class="btns">
        <el-button :icon="Plus" type="primary" @click="open(null)" size="small">新增</el-button>   
    </div>

    <el-table :data="tableData.list" style="width: 100%;">
      <el-table-column prop="id" label="id" />
      <el-table-column prop="name" label="名称" />
      <el-table-column prop="permissionName" label="菜单权限" width="500px" />
      <el-table-column label="操作">
        <template #default="scope">
          <el-button type="primary" @click="open(scope.row)">编辑</el-button>
        </template>
      </el-table-column>
    </el-table>
      <div class="pagination-info">
          <el-pagination
            v-model:current-page="paginationData.pageNum"
            :page-size="paginationData.pageSize"
            :background="false"
            size="small"
            layout="total, prev, pager, next"
            :total="tableData.total"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
          />
      </div>
    <el-dialog
      v-model="dialogFormVisible"
      :before-close="beforeClose"
      title="添加权限"
      width="500"
    >
      <el-form
        ref="formRef"
        label-width="100px"
        label-position="left"
        :model="form"
        :rules="rules"
      >
        <el-form-item v-show="false" prop="id">
          <el-input v-model="form.id" />
        </el-form-item> 
        <el-form-item label="名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入权限名称" />
        </el-form-item> 
        <el-form-item label="权限" prop="permissions">
          <el-tree
            ref="treeRef"
            style="max-width: 600px;"
            :data="permissionData"
            node-key="id"
            show-checkbox
            :default-checked-keys="defaultCheckedKeys"
            :default-expanded-keys="[2]"
          />
        </el-form-item>
      </el-form>    
      <template #footer>
        <div class="dialog-footer">
          <el-button type="primary" @click="confirm">确认</el-button>
        </div>
      </template>
    </el-dialog>
</template>

<script setup>
import { ref, reactive, onMounted, nextTick } from 'vue'
import { userGetMenu, userSetMenu, menuList } from '../../../api'
import { Plus } from '@element-plus/icons-vue'
import { useRoute } from 'vue-router';

const route = useRoute()

// 默认固定勾选的权限
const fixedKeys = [2, 201, 202]
const defaultCheckedKeys = ref([2, 201, 202])

// 给固定权限加禁用状态，避免被取消
const setDisabled = (list) => {
  return list.map(item => {
    const node = { ...item }
    if (fixedKeys.includes(node.id)) {
      node.disabled = true
    }
    if (node.children && node.children.length) {
      node.children = setDisabled(node.children)
    }
    return node
  })
}

// 列表数据
const tableData = reactive({
  list: [],
  total: 0
})

// 分页参数
const paginationData = reactive({
  pageNum: 1,
  pageSize: 10
})

const handleSizeChange = (val) => {
    paginationData.pageSize = val
    getListData()
}
const handleCurrentChange = (val) => {
    paginationData.pageNum = val
    getListData()
}


// 表单实例
const formRef = ref()
// 树实例
const treeRef = ref()
// 权限树数据
const permissionData = ref([])
// 弹窗显隐
const dialogFormVisible = ref(false)

// 表单数据
const form = reactive({
  id: '',
  name: '',
  permissions: ''
})

// 表单校验规则
const rules = reactive({
  name: [{ required: true, message: '请输入权限名称', trigger: 'blur' }]
})

// 获取列表
const getListData = () => {
  menuList(paginationData).then(({ data }) => {
    const { list, total } = data.data
    tableData.list = list
    tableData.total = total
  })
}

// 打开弹窗，新建或编辑
const open = (rowData = null) => {
  dialogFormVisible.value = true
  formRef.value?.resetFields()
  treeRef.value?.setCheckedKeys([])

  nextTick(() => {
    if (rowData) {
      Object.assign(form, {
        id: rowData.id,
        name: rowData.name
      })
      treeRef.value?.setCheckedKeys(rowData.permissions || [])
    } else {
      Object.assign(form, {
        id: '',
        name: ''
      })
      treeRef.value?.setCheckedKeys(fixedKeys)
    }
  })
}

// 关闭弹窗前重置状态
const beforeClose = () => {
  dialogFormVisible.value = false
  formRef.value?.resetFields()
  treeRef.value?.setCheckedKeys(fixedKeys)
}

// 提交表单
const confirm = async () => {
  if (!formRef.value) return

  await formRef.value.validate((valid, fields) => {
    if (!valid) {
      console.log('error submit!', fields)
      return
    }

    const permissions = JSON.stringify(treeRef.value.getCheckedKeys())
    userSetMenu({ name: form.name, permissions, id: form.id }).then(({ data }) => {
      if (data.code === 10000) {
        getListData()
        dialogFormVisible.value = false
        formRef.value?.resetFields()
        treeRef.value?.setCheckedKeys(fixedKeys)
      }
    })
  })
}

// 页面初始化
onMounted(() => {
  userGetMenu().then(({ data }) => {
    permissionData.value = setDisabled(data.data)
  })
  getListData()
})
</script>

<style lang="less" scoped>
.btns{
    padding:10px 0 10px 10px;
    background-color: #fff;
}
</style>