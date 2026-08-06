DIDI陪诊后台管理系统（DIDI-system）
一个基于Vue 3 + Vite + Element Plus构建的、高效现代化的陪诊业务后台管理系统。系统包含权限管理、陪护师管理、订单管理、控制台统计等核心业务功能。

🛠️技术栈

构建工具：vite

前端框架：Vue 3(SFC组合式API)

路由管理：Vue Router 4

状态管理：Vuex

UI组件库：Element Plus

网络请求：Axios (封装统一拦截器与响应处理)

✨ 核心功能模块
登录与鉴权（Auth & Login）

用户登录验证与Token状态保持

动态路由生成与菜单权限控制

系统与权限管理（系统与权限管理）

管理员管理( /auth/admin)：管理员账号列表、角色分配与账号管理

权限组/菜单配置( /auth/group)：角色组配置、树形菜单权限勾选与绑定

陪诊业务管理（VPPZ Business Management）

陪护师管理( /vppz/staff)：陪护师人员信息维护、服务状态管理及新增/编辑

订单管理( /vppz/order)：陪诊订单列表展示、订单状态变更及服务接收

控制台仪表盘（Dashboard）

业务数据概览、可视化统计与快捷入口

📂 项目目录结构
纯文本
DIDI-system/
├── public/                 # 静态资源文件
├── src/
│   ├── api/                # API 接口统一管理
│   │   └── index.js
│   ├── assets/             # 资源文件 (图片、图标等)
│   ├── components/         # 公用组件
│   │   ├── aside.vue       # 侧边栏菜单组件
│   │   ├── navHeader.vue   # 顶部导航栏组件
│   │   ├── panelHead.vue   # 面板头部组件
│   │   └── treeMenu.vue    # 递归树形菜单组件
│   ├── router/             # Vue Router 路由配置
│   ├── store/              # 状态管理 (菜单状态、用户信息等)
│   ├── utils/              # 工具函数 (Axios 拦截器封装等)
│   │   └── request.js
│   ├── views/              # 视图页面
│   │   ├── auth/           # 权限管理 (admin / group)
│   │   ├── dashboard/      # 控制台/仪表盘
│   │   ├── login/          # 登录页
│   │   ├── vppz/           # 陪诊业务 (order / staff)
│   │   └── Main.vue        # 主页面布局框架
│   ├── App.vue             # 根组件
│   ├── main.js             # 入口文件
│   └── style.css           # 全局样式
├── index.html              # HTML 模板
├── package.json            # 项目依赖配置
└── vite.config.js          # Vite 配置文件


🚀 快速开始
1.环境准备

保证您的开发环境中已安装：

Node.js（>= 16.0.0）

npm或pnpm/yarn

2.安装依赖

npm install
# 或使用 pnpm
pnpm install
3.本地开发运行
npm run dev
启动成功后，在浏览器访问控制台输出的本地地址（默认通常为http://localhost:5173）。

4. 项目储备建设

npm run build
文件夹完成后，将在根目录下生成dist文件夹，用于生产环境部署。

📝 开发规范与建议
VS Code 推荐插件：Vue - Volar(已在.vscode/extensions.json中配置)。

组件命名：公共组件统一放置于src/components/，页面级视图放置于src/views/。

接口调用：统一在src/api/中按模块导出请求函数，网络拦截逻辑在src/utils/request.js中维护。