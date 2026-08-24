from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, Table, TableStyle, Image
from PIL import Image as PILImage

ROOT = Path(r'C:\Users\ASUS\Desktop\面试准备\vue项目\pzadmin')
OUT = ROOT / 'output' / 'pdf' / '李奇骏的简历-修改版.pdf'
OUT.parent.mkdir(parents=True, exist_ok=True)
PHOTO = ROOT / 'tmp' / 'pdfs' / 'resume-photo.png'
RENDER = ROOT / 'tmp' / 'pdfs' / 'original-1.png'
if RENDER.exists():
    PILImage.open(RENDER).crop((110, 120, 292, 300)).save(PHOTO)

pdfmetrics.registerFont(TTFont('SimSun', r'C:\Windows\Fonts\simsun.ttc'))
pdfmetrics.registerFont(TTFont('SimHei', r'C:\Windows\Fonts\simhei.ttf'))
NAVY = colors.HexColor('#33495A')
INK = colors.HexColor('#263746')
MUTED = colors.HexColor('#68727B')
LINE = colors.HexColor('#D7DCE0')
ACCENT = colors.HexColor('#C8AE96')
base = getSampleStyleSheet()
body = ParagraphStyle('body', parent=base['Normal'], fontName='SimSun', fontSize=8.6, leading=12.8, textColor=MUTED)
small = ParagraphStyle('small', parent=body, fontSize=7.8, leading=11.2)
headsmall = ParagraphStyle('headsmall', parent=small, textColor=colors.white)
section = ParagraphStyle('section', parent=body, fontName='SimHei', fontSize=13.5, leading=19, textColor=INK)
title = ParagraphStyle('title', parent=body, fontName='SimHei', fontSize=10.5, leading=15, textColor=INK)
date = ParagraphStyle('date', parent=body, fontName='SimHei', fontSize=9.2, textColor=NAVY)
role = ParagraphStyle('role', parent=body, fontName='SimHei', fontSize=9.2, textColor=NAVY)
bullet = ParagraphStyle('bullet', parent=body, leftIndent=10, firstLineIndent=-8, fontSize=8.4, leading=12.4)
name = ParagraphStyle('name', parent=body, fontName='SimHei', fontSize=24, leading=28, textColor=colors.white)
sub = ParagraphStyle('sub', parent=body, fontName='SimHei', fontSize=10, leading=14, textColor=colors.HexColor('#B8C1C8'))

def P(s, st=body):
    return Paragraph(s, st)

def section_block(s, story):
    t = Table([[P(s, section)]], colWidths=[170*mm])
    t.setStyle(TableStyle([('LINEBELOW',(0,0),(-1,-1),1.1,LINE),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),3)]))
    story += [Spacer(1, 1), t]

def project(d, n, r, items, story):
    t = Table([[P(d, date), P(n, title)]], colWidths=[56*mm,114*mm])
    t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('ALIGN',(1,0),(1,0),'RIGHT'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),('TOPPADDING',(0,0),(-1,-1),3),('BOTTOMPADDING',(0,0),(-1,-1),0)]))
    story += [t, P(r, role)]
    story += [P('&bull; '+x, bullet) for x in items]
    story.append(Spacer(1, 1))

def hf(canvas, doc):
    canvas.saveState()
    if doc.page > 1:
        canvas.setFillColor(NAVY)
        canvas.rect(0, A4[1]-8*mm, A4[0], 8*mm, fill=1, stroke=0)
        canvas.setFillColor(colors.white)
        canvas.setFont('SimSun', 8)
        canvas.drawString(22*mm, A4[1]-5.4*mm, '李奇骏 | 前端开发实习生')
    canvas.setStrokeColor(LINE)
    canvas.line(22*mm, 13*mm, A4[0]-22*mm, 13*mm)
    canvas.setFillColor(MUTED)
    canvas.setFont('SimSun', 8)
    canvas.drawRightString(A4[0]-22*mm, 8*mm, str(doc.page))
    canvas.restoreState()

doc = BaseDocTemplate(str(OUT), pagesize=A4, leftMargin=22*mm, rightMargin=22*mm, topMargin=13*mm, bottomMargin=11*mm)
doc.addPageTemplates([PageTemplate(id='resume', frames=[Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='f')], onPage=hf)])
story = []
photo = Image(str(PHOTO), width=35*mm, height=39*mm) if PHOTO.exists() else Spacer(35*mm,39*mm)
head = Table([[photo, [P('李奇骏', name), P('前端开发实习生', sub), Spacer(1,2*mm), P('电话：19857869584　　邮箱：2562227040@qq.com', headsmall), P('男　　本科在读　　四川农业大学　　预计 2028 年毕业', headsmall)]]], colWidths=[43*mm,127*mm], rowHeights=[45*mm])
head.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),NAVY),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),('BOX',(0,0),(0,0),1.2,ACCENT)]))
story += [head, Spacer(1,2)]
section_block('求职意向', story)
t = Table([[P('<b>意向岗位：</b>前端开发实习生'), P('<b>意向城市：</b>不限'), P('<b>求职类型：</b>日常实习')]], colWidths=[66*mm,52*mm,52*mm])
t.setStyle(TableStyle([('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),5),('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),0)]))
story.append(t)
section_block('教育经历', story)
t = Table([[P('2024.01 - 2028.01',date),P('四川农业大学',title)],[P('计算机科学与技术 | 本科'),P('核心课程：数据结构、计算机网络、C/C++、Python',small)]], colWidths=[56*mm,114*mm])
t.setStyle(TableStyle([('ALIGN',(1,0),(1,-1),'RIGHT'),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),2)]))
story.append(t)
section_block('项目经历', story)
project('2026.03 - 至今','陪诊服务平台（pzadmin + pzH5）','前端开发 | 个人项目 | Vue 3 全栈联调',[
    '<b>项目概述：</b>面向陪诊业务搭建用户端 H5 与运营后台，覆盖“服务选择 - 创建订单 - 订单跟踪 - 后台处理”的完整业务链路。',
    '<b>用户端 pzH5：</b>使用 Vue 3、Vite、Vant、Vue Router 开发移动端页面，实现首页医院/服务选择、预约下单、订单列表、订单详情、个人中心与登录认证。',
    '<b>管理端 pzadmin：</b>使用 Element Plus、Vuex、Vue Router、ECharts 实现控制台数据看板、管理员管理、角色权限组、陪诊师管理和订单状态维护。',
    '<b>工程实践：</b>统一封装 Axios 请求、请求/响应拦截器与异常提示，基于 Token 和路由守卫实现登录态校验；根据后端菜单权限动态注册路由并生成树形菜单，支持按角色控制页面访问。',
    '<b>个人贡献：</b>独立完成前后台核心页面、接口联调、组件交互与样式适配，梳理订单状态流转和权限数据结构，提升项目的可维护性与业务闭环完整度。'
], story)
project('2026.03 - 2026.05','多模态野生动物智能检测系统','前端 / 推理服务开发 | 核心开发者',[
    '<b>系统架构：</b>基于 FastAPI 搭建视频、音频上传与分析服务，使用 StreamingResponse 持续返回加载、预处理、推理和完成状态，前端实时展示进度。',
    '<b>多模态推理：</b>参与 VideoMAE 视频编码器、AST 音频编码器与 MBT Transformer 融合链路，完成 16 帧视频采样、音频 Mel 频谱预处理和滑动窗口推理。',
    '<b>结果可视化：</b>使用 Chart.js 展示活动类别分布与物种置信度，使用 Leaflet 展示监测节点，使用 Three.js 绘制物种 3D 线框模型，并将 JSON 帧级结果与视频时间轴同步。',
    '<b>业务能力：</b>支持物种识别、活动分类和多标签动作识别，设计异常回退与置信度阈值处理，提升推理结果的可解释性和交互反馈。',
    '<b>项目成果：</b>项目获中国计算机设计大赛四川省三等奖，负责前端指挥中心界面、推理服务联调和多版本迭代优化。'
], story)
section_block('校园经历', story)
project('2025.09 - 2026.07','IOT 全栈工作室','前端负责人',[
    '统筹多人前端小组开发，协调后端与硬件组需求，拆分任务并跟进交付。',
    '推动统一接口文档、PR 提交和每日短会机制，减少前后端对接错误，完成 2 项校内实训项目。'
], story)
section_block('相关技能', story)
story += [P('<b>前端：</b>JavaScript、HTML5、CSS3、Vue 3、Vue Router、Vuex、Vite、Element Plus、Vant、Chart.js、Leaflet、Three.js、Axios、Less'),
          P('<b>后端与 AI：</b>Python、FastAPI、PyTorch、OpenCV、librosa、Transformers、VideoMAE、AST、Transformer/MBT、多模态推理'),
          P('<b>工程与基础：</b>Git/Gitee、HTTP、响应式布局、路由与权限控制、接口联调、组件化开发、C/C++、数据结构'),
          P('<b>开发方式：</b>重视代码规范、组件复用和交互细节，熟悉使用 AI 工具辅助检索、调试与重构，并进行人工验证。')]
story.append(P('<b>荣誉证书：</b>计算机三级　　大学英语四级　　中国计算机设计大赛四川省三等奖'))
doc.build(story)
print(OUT)
