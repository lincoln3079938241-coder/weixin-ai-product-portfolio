# 陈蔚昕 · AI产品经理作品集

以 AI Product Manager 为主要岗位定位，覆盖 Generative AI、AI Innovation、Data Products 与 AI Solutions / Product Operations 能力方向的中英双语公开作品集。

## 在线入口

| 内容 | 中文 | English |
| --- | --- | --- |
| 作品集网站 | https://lincoln3079938241-coder.github.io/weixin-ai-product-portfolio/ | https://lincoln3079938241-coder.github.io/weixin-ai-product-portfolio/en/ |
| DriveMate 页面 | https://lincoln3079938241-coder.github.io/weixin-ai-product-portfolio/drivemate.html | https://lincoln3079938241-coder.github.io/weixin-ai-product-portfolio/en/drivemate.html |
| 作品集 PDF | `assets/Chen-Weixin-AI-Product-Portfolio.pdf` | `assets/Chen-Weixin-AI-Product-Portfolio-EN.pdf` |
| DriveMate PDF | `assets/DriveMate-Concept-Proposal.pdf` | `assets/DriveMate-Concept-EN.pdf` |

中文与英文页面均为可独立访问的静态 HTML，并通过顶部语言按钮互相切换。英文页面复用根目录 `styles.css` 与 `assets/`，适配 GitHub Pages 子目录路径。

## 项目内容

- Auto-LifeOS：AI Agent 饮食建议与家庭库存管理公开 Demo；公开版使用 Mock Provider。
- 2027 Graduate Job Radar / 2027届秋招岗位雷达：数据自动化、规则筛选与信息管理产品；公开版使用脱敏样例数据。
- DriveMate：AI+汽车、多Agent、多模态与 Physical AI 方向的概念方案和静态低保真原型；未开发上线，也未连接真实车辆、传感器、VLA 模型或外部 API。
- 中英文 7 页作品集 PDF 与中英文 2 页 DriveMate 概念 PDF。

网页收录来自当前公开 Demo 的真实运行截图。部分截图界面仍为中文；英文页面提供英文标题、caption、alt 与 aria 文本，不声称截图来自英文 Demo。

## 文件结构

```text
.
├── index.html
├── drivemate.html
├── en/
│   ├── index.html
│   └── drivemate.html
├── styles.css
├── assets/
│   ├── Chen-Weixin-AI-Product-Portfolio.pdf
│   ├── Chen-Weixin-AI-Product-Portfolio-EN.pdf
│   ├── DriveMate-Concept-Proposal.pdf
│   ├── DriveMate-Concept-EN.pdf
│   └── screenshots/
└── scripts/
    ├── generate_pdfs.py
    └── check_static.py
```

## 本地预览与检查

网站无后端、无前端框架、无构建步骤。可直接打开 `index.html`，也可使用任意静态文件服务器预览。

重新生成全部中英文 PDF：

```powershell
python scripts/generate_pdfs.py
```

检查四个 HTML 页面、CSS、截图、本地链接与四个 PDF：

```powershell
python scripts/check_static.py
```

## 在线项目

- Auto-LifeOS Demo：https://auto-lifeos-demo.streamlit.app/
- Auto-LifeOS GitHub：https://github.com/lincoln3079938241-coder/auto-lifeos-demo
- 2027 Graduate Job Radar Demo：https://shanghai-2027-job-radar-demo.streamlit.app/
- 2027 Graduate Job Radar GitHub：https://github.com/lincoln3079938241-coder/shanghai-2027-job-radar-demo

## 真实性边界

- 不虚构技术、用户数量、真实访谈、业务效果、转化率、VLA 能力或不存在的模型 API 调用。
- Synthetic Usability Evaluation 是模拟画像和任务路径推演，不是真实用户研究。
- A/B-style Prototype Comparison 是概念方案比较，不是线上 A/B Test。
- Auto-LifeOS 公开版使用 Mock Provider。
- 2027 Graduate Job Radar 使用脱敏样例数据，不代表企业当前实时招聘状态，也不预测岗位成功率。
- DriveMate 是 Concept Proposal 与 Static Prototype，不连接真实车辆、视觉传感器、VLA 模型、车控接口或外部 API。

## 安全

仓库不应包含 `.env`、API Key、Token、Cookie、Session、个人数据库或原始招聘数据。公开联系邮箱为 `Lincoln3079938241@163.com`；不公开手机号、出生年月、政治面貌或其他非必要个人信息。
