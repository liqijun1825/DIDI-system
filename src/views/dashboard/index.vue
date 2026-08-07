<template>
  <div class="control-container">
    <panel-head :route="route" />
    <div class="card">
      <div class="user">
        <el-card class="user-card">
          <template #header>
            <div class="card-header">
              <el-image :src="user.user_img" />
              <span>{{ user.user_name }}</span>
            </div>
          </template>
          <div class="user-info">
            <div>当前权限：{{ user.permission }}</div>
            <div>登录的ip：{{ user.ip }}</div>
          </div>
        </el-card>
      </div>
      <el-card class="serive-list">
        <div class="serive-item" v-for="(item, index) in types" :key="index">
          <div class="img-box" :style="{ 'background-color': color[index % color.length] }">
            <img :src="imgs[index % imgs.length]" alt="" />
          </div>
          <div class="text">
            <div class="num">{{ item.num }}</div>
            <div class="name">{{ item.state }}</div>
          </div>
        </div>
      </el-card>
    </div>

    <div class="content">
      <div class="echart-title">订单数</div>
      <div class="echart" ref="echart"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import * as echarts from 'echarts'
import { getControlData } from '../../api'
import { useRoute } from 'vue-router'
import dzfImg from '../../assets/dzf.png'
import dfwImg from '../../assets/dfw.png'
import ywcImg from '../../assets/ywc.png'
import yqxImg from '../../assets/yqx.png'

const route = useRoute()
const echart = ref()

const user = ref({
  user_img: '',
  user_name: '',
  permission: '',
  ip: ''
})

const types = ref([])
const typeList = ref([])

const imgs = [dzfImg, dfwImg, ywcImg, yqxImg]
const color = ['#F05050', '#7266BA', '#23B7E5', '#27C24C']

const normalizeUser = (raw = {}) => ({
  user_img: raw.user_img || raw.avatar || raw.userImg || '',
  user_name: raw.user_name || raw.name || raw.nickName || raw.userName || '',
  permission: raw.permission || raw.permissionName || raw.role || '',
  ip: raw.ip || raw.login_ip || raw.loginIp || ''
})

const normalizeTypes = (raw = []) => {
  if (!Array.isArray(raw)) return []
  return raw.map(item => ({
    state: item.state || item.name || '',
    num: Number(item.num ?? item.count ?? 0)
  }))
}

const normalizeTypeList = (raw = []) => {
  if (!Array.isArray(raw)) return []
  return raw.map(item => ({
    date: item.date || item.day || '',
    order_sum: Number(item.order_sum ?? item.orderCount ?? item.num ?? 0),
    order_money: Number(item.order_money ?? item.orderAmount ?? item.money ?? 0)
  }))
}

const initEchart = () => {
  if (!echart.value || !typeList.value.length) return

  const options = {
    grid: {
      left: 40,
      bottom: 10,
      right: 40,
      top: 30,
      containLabel: true
    },
    color: ['#67CEBC'],
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'line'
      },
      formatter: (params) => {
        const item = typeList.value[params[0].dataIndex] || {}
        return `${params[0].seriesName}: ${params[0].data}<br />总金额: ${item.order_money}`
      }
    },
    legend: {
      data: ['订单数']
    },
    xAxis: {
      type: 'category',
      data: typeList.value.map(item => item.date),
      axisLine: { show: true, lineStyle: { width: 2, color: '#67CEBC' } },
      axisLabel: {
        color: '#999'
      },
      axisTick: false
    },
    yAxis: {
      type: 'value',
      axisLabel: {
        color: '#999'
      },
      axisLine: { show: true, lineStyle: { color: '#999' } },
      splitLine: {
        show: true
      }
    },
    series: [
      {
        name: '订单数',
        type: 'line',
        data: typeList.value.map(item => item.order_sum),
        symbolSize: 8,
        smooth: true,
        itemStyle: {
          color: '#67CEBC'
        }
      }
    ]
  }

  const myChart = echarts.init(echart.value)
  myChart.setOption(options)

  const observer = new ResizeObserver(() => {
    myChart.resize()
  })

  observer.observe(echart.value)
}

const getData = async () => {
  const res = await getControlData()
  const data = res?.data?.data

  if (!data) return

  user.value = normalizeUser(data.user || {})
  types.value = normalizeTypes(data.types || [])
  typeList.value = normalizeTypeList(data.typeList || [])

  await nextTick()
  initEchart()
}

onMounted(() => {
  getData()
})
</script>

<style lang="less" scoped>
.card {
  display: flex;
}
.user {
  margin: 20px 0;
  width: 45%;
  .user-card {
    .card-header {
      display: flex;
      .el-image {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        margin: 5px;
      }
      span {
        line-height: 120px;
        font-size: 28px;
        font-weight: bold;
      }
    }
    .user-info {
      color: #666;
      line-height: 30px;
    }
  }
}
.serive-list {
  background-color: #fff;
  margin: 20px;
  min-height: 269px;
  width: 50%;
  margin-bottom: 40px;
  ::v-deep(.el-card__body) {
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap;
    align-content: flex-start;
    gap: 12px 0;
    padding: 18px;

    .serive-item {
      width: 50%;
      min-height: 90px;
      display: flex;
      justify-content: center;
      align-items: center;
      .img-box {
        width: 74px;
        height: 74px;
        text-align: center;
        margin-right: 10px;
        border-radius: 5px;
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
        img {
          display: block;
          width: 54px;
          height: 54px;
          border-radius: 5px;
          object-fit: contain;
        }
      }

      .num {
        font-size: 25px;
        line-height: 40px;
        font-weight: bold;
      }
      .name {
        font-size: 14px;
      }
    }
  }
}
.content {
  padding: 10px;
  background-color: #fff;
  width: 95%;
  position: relative;
  .echart-title {
    position: absolute;
    top: 16px;
    left: 50%;
    transform: translateX(-50%);
    font-size: 18px;
    font-weight: 700;
    color: #333;
    z-index: 2;
    pointer-events: none;
  }
  .echart {
    height: 400px;
  }
}
</style>
