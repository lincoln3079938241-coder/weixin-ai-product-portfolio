# 陈蔚昕 · AI产品经理作品集

面向“AI产品经理 / AI创新产品”校招岗位的公开作品集，包含：

- Auto-LifeOS：AI Agent 饮食建议与家庭库存管理公开 Demo；
- 2027届秋招岗位雷达：数据自动化、规则筛选与信息管理产品；
- DriveMate：AI+汽车多Agent、多模态与Physical AI创新产品概念方案（未开发上线）；
- 7页 PDF 作品集与2页 DriveMate 概念 PDF。

## 本轮证据增强

- Auto-LifeOS 与秋招雷达各收录4张来自公开运行界面的真实截图；
- 三个案例均补充 Key Product Decisions，先说明用户问题与取舍，再说明实现；
- 两个可运行项目补充 Synthetic Usability Evaluation，明确为模拟角色与任务，不冒充真实用户研究；
- Auto-LifeOS 增加 A/B-style Prototype Comparison，明确不是线上A/B测试；
- DriveMate 增加三个高约束汽车场景、可切换静态低保真原型、多模态产品架构及分阶段VLA路线。

网页截图均有替代文本，可点击查看原图；布局适配桌面与手机。PDF中的项目、Demo、邮箱及下载链接均为可点击链接。

## 在线项目

- Auto-LifeOS Demo：https://auto-lifeos-demo.streamlit.app/
- Auto-LifeOS GitHub：https://github.com/lincoln3079938241-coder/auto-lifeos-demo
- 秋招雷达 Demo：https://shanghai-2027-job-radar-demo.streamlit.app/
- 秋招雷达 GitHub：https://github.com/lincoln3079938241-coder/shanghai-2027-job-radar-demo

## 本地预览

这是无后端、无构建步骤的静态网站。可直接打开 `index.html`，或使用任意静态文件服务器预览。

重新生成PDF：

```powershell
python scripts/generate_pdfs.py
```

## 真实性边界

- 不虚构技术、用户数量、真实访谈、业务效果、VLA能力或不存在的模型API调用；
- Auto-LifeOS 公开版强制使用 Mock Provider；
- 秋招雷达不包含 Agent、大模型、智能推荐或岗位成功率预测；
- DriveMate 明确标记为 Concept Proposal / 创新产品概念方案，未开发上线。
- DriveMate 静态原型不连接真实车辆、视觉传感器、VLA模型或外部API。

## 安全

仓库不应包含 `.env`、API Key、Token、Cookie、Session、个人数据库或原始招聘数据。公开联系邮箱为 `Lincoln3079938241@163.com`；不公开手机号、出生年月、政治面貌或其他非必要个人信息。
