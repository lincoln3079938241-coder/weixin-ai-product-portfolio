from __future__ import annotations

import os
from pathlib import Path

from reportlab.lib.colors import Color, HexColor, white
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader


SITE = Path(__file__).resolve().parents[1]
ASSETS = SITE / "assets"
PORTFOLIO_PDF = ASSETS / "Chen-Weixin-AI-Product-Portfolio.pdf"
CONCEPT_PDF = ASSETS / "DriveMate-Concept-Proposal.pdf"
PORTFOLIO_EN_PDF = ASSETS / "Chen-Weixin-AI-Product-Portfolio-EN.pdf"
CONCEPT_EN_PDF = ASSETS / "DriveMate-Concept-EN.pdf"

SITE_URL = "https://lincoln3079938241-coder.github.io/weixin-ai-product-portfolio/"
SITE_EN_URL = f"{SITE_URL}en/"

PAGE_W, PAGE_H = landscape(A4)
MARGIN = 38

INK = HexColor("#10212B")
MUTED = HexColor("#5D6D75")
LINE = HexColor("#D7E1E4")
PAPER = HexColor("#F7FAF9")
CYAN = HexColor("#00A8A8")
BLUE = HexColor("#175C73")
LIME = HexColor("#C8EF5B")
PALE = HexColor("#EAF4F3")
WARM = HexColor("#F2F6E9")
GOLD_BG = HexColor("#FFF1B8")
GOLD = HexColor("#6A4D00")


def register_fonts() -> None:
    font_dir = Path(os.environ["WINDIR"]) / "Fonts"
    pdfmetrics.registerFont(TTFont("MSYH", font_dir / "msyh.ttc"))
    pdfmetrics.registerFont(TTFont("MSYH-Bold", font_dir / "msyhbd.ttc"))


def wrap_text(text: str, font: str, size: float, max_width: float) -> list[str]:
    lines: list[str] = []
    for paragraph in text.split("\n"):
        if not paragraph:
            lines.append("")
            continue
        if " " in paragraph:
            current_words: list[str] = []
            for word in paragraph.split():
                candidate = " ".join([*current_words, word])
                if current_words and pdfmetrics.stringWidth(candidate, font, size) > max_width:
                    lines.append(" ".join(current_words))
                    current_words = [word]
                else:
                    current_words.append(word)
            if current_words:
                lines.append(" ".join(current_words))
            continue
        current = ""
        for char in paragraph:
            candidate = current + char
            if current and pdfmetrics.stringWidth(candidate, font, size) > max_width:
                lines.append(current)
                current = char
            else:
                current = candidate
        if current:
            lines.append(current)
    return lines


def text_block(
    c: canvas.Canvas,
    text: str,
    x: float,
    top: float,
    width: float,
    *,
    font: str = "MSYH",
    size: float = 9.2,
    leading: float | None = None,
    color=INK,
    max_lines: int | None = None,
) -> float:
    leading = leading or size * 1.55
    lines = wrap_text(text, font, size, width)
    if max_lines is not None:
        lines = lines[:max_lines]
    c.setFont(font, size)
    c.setFillColor(color)
    y = top
    for line in lines:
        c.drawString(x, y, line)
        y -= leading
    return y


def title(c: canvas.Canvas, kicker: str, heading: str, subtitle: str = "") -> float:
    c.setFillColor(CYAN)
    c.setFont("MSYH-Bold", 7.5)
    c.drawString(MARGIN, PAGE_H - 34, kicker)
    c.setFillColor(INK)
    c.setFont("MSYH-Bold", 28)
    c.drawString(MARGIN, PAGE_H - 74, heading)
    y = PAGE_H - 94
    if subtitle:
        y = text_block(c, subtitle, MARGIN, y, PAGE_W - 2 * MARGIN, size=9.5, color=MUTED, max_lines=2)
    return y - 8


def footer(c: canvas.Canvas, page_no: int, total: int, label: str = "陈蔚昕 · AI产品经理作品集") -> None:
    c.setStrokeColor(LINE)
    c.line(MARGIN, 24, PAGE_W - MARGIN, 24)
    c.setFont("MSYH", 6.8)
    c.setFillColor(MUTED)
    c.drawString(MARGIN, 11, label)
    c.drawRightString(PAGE_W - MARGIN, 11, f"{page_no:02d} / {total:02d}")


def card(c: canvas.Canvas, x: float, y: float, w: float, h: float, fill=white, stroke=LINE, radius=10) -> None:
    c.setFillColor(fill)
    c.setStrokeColor(stroke)
    c.roundRect(x, y, w, h, radius, fill=1, stroke=1)


def card_text(
    c: canvas.Canvas,
    x: float,
    y: float,
    w: float,
    h: float,
    label: str,
    heading: str,
    body: str,
    *,
    fill=white,
    label_color=CYAN,
) -> None:
    card(c, x, y, w, h, fill=fill)
    c.setFont("MSYH-Bold", 6.7)
    c.setFillColor(label_color)
    c.drawString(x + 12, y + h - 17, label)
    c.setFont("MSYH-Bold", 10.5)
    c.setFillColor(INK)
    c.drawString(x + 12, y + h - 37, heading)
    text_block(c, body, x + 12, y + h - 54, w - 24, size=7.8, leading=11.8, color=MUTED, max_lines=4)


def card_text_en(
    c: canvas.Canvas,
    x: float,
    y: float,
    w: float,
    h: float,
    label: str,
    heading: str,
    body: str,
    *,
    fill=white,
    label_color=CYAN,
    heading_size: float = 9.2,
    body_size: float = 7.2,
    body_lines: int = 4,
) -> None:
    card(c, x, y, w, h, fill=fill)
    c.setFont("MSYH-Bold", 6.4)
    c.setFillColor(label_color)
    c.drawString(x + 12, y + h - 17, label)
    heading_bottom = text_block(
        c,
        heading,
        x + 12,
        y + h - 34,
        w - 24,
        font="MSYH-Bold",
        size=heading_size,
        leading=heading_size * 1.18,
        color=INK,
        max_lines=2,
    )
    text_block(
        c,
        body,
        x + 12,
        heading_bottom - 4,
        w - 24,
        size=body_size,
        leading=body_size * 1.42,
        color=MUTED,
        max_lines=body_lines,
    )


def pill(c: canvas.Canvas, text: str, x: float, y: float, *, fill=PALE, color=BLUE, h: float = 20) -> float:
    w = pdfmetrics.stringWidth(text, "MSYH", 7.2) + 18
    c.setFillColor(fill)
    c.setStrokeColor(fill)
    c.roundRect(x, y, w, h, h / 2, fill=1, stroke=0)
    c.setFillColor(color)
    c.setFont("MSYH", 7.2)
    c.drawCentredString(x + w / 2, y + 6.2, text)
    return w


def link_button(c: canvas.Canvas, label: str, url: str, x: float, y: float, w: float) -> None:
    c.setFillColor(INK)
    c.setStrokeColor(INK)
    c.roundRect(x, y, w, 27, 7, fill=1, stroke=1)
    c.setFillColor(white)
    c.setFont("MSYH-Bold", 8)
    c.drawCentredString(x + w / 2, y + 9, label)
    c.linkURL(url, (x, y, x + w, y + 27), relative=0)


def flow(c: canvas.Canvas, items: list[str], x: float, y: float, w: float, *, h: float = 32) -> None:
    gap = 12
    item_w = (w - gap * (len(items) - 1)) / len(items)
    for idx, item in enumerate(items):
        xi = x + idx * (item_w + gap)
        c.setFillColor(PALE if idx < len(items) - 1 else WARM)
        c.setStrokeColor(LINE)
        c.roundRect(xi, y, item_w, h, 7, fill=1, stroke=1)
        c.setFillColor(INK)
        c.setFont("MSYH-Bold", 7.4)
        c.drawCentredString(xi + item_w / 2, y + 11.2, item)
        if idx < len(items) - 1:
            c.setStrokeColor(CYAN)
            c.setLineWidth(1.3)
            c.line(xi + item_w + 2, y + h / 2, xi + item_w + gap - 2, y + h / 2)
            c.line(xi + item_w + gap - 5, y + h / 2 + 3, xi + item_w + gap - 2, y + h / 2)
            c.line(xi + item_w + gap - 5, y + h / 2 - 3, xi + item_w + gap - 2, y + h / 2)


def image_fit(c: canvas.Canvas, path: Path, x: float, y: float, w: float, h: float) -> None:
    card(c, x, y, w, h, fill=white)
    image = ImageReader(str(path))
    iw, ih = image.getSize()
    scale = min((w - 12) / iw, (h - 12) / ih)
    dw, dh = iw * scale, ih * scale
    c.drawImage(image, x + (w - dw) / 2, y + (h - dh) / 2, width=dw, height=dh, mask="auto")


def bullets(c: canvas.Canvas, items: list[str], x: float, top: float, width: float, *, size=8.3, leading=13.5) -> float:
    y = top
    for item in items:
        c.setFillColor(CYAN)
        c.circle(x + 3, y - 3, 2, fill=1, stroke=0)
        y = text_block(c, item, x + 12, y, width - 12, size=size, leading=leading, color=INK)
        y -= 3
    return y


def page_one(c: canvas.Canvas) -> None:
    c.setFillColor(PAPER)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    c.setFillColor(CYAN)
    c.rect(0, 0, 8, PAGE_H, fill=1, stroke=0)
    c.setFillColor(CYAN)
    c.setFont("MSYH-Bold", 8)
    c.drawString(MARGIN, PAGE_H - 46, "AI PRODUCT MANAGER PORTFOLIO")
    c.setFillColor(INK)
    c.setFont("MSYH-Bold", 43)
    c.drawString(MARGIN, PAGE_H - 112, "陈蔚昕")
    c.setFillColor(BLUE)
    c.setFont("MSYH-Bold", 21)
    c.drawString(MARGIN, PAGE_H - 148, "AI产品经理｜生成式AI与AI创新")
    text_block(
        c,
        "具备AI Agent、数据产品和独立应用开发经验，能够完成用户问题识别、产品方案设计、Demo搭建、测试评估与迭代落地。",
        MARGIN,
        PAGE_H - 185,
        455,
        size=12,
        leading=20,
        color=MUTED,
    )
    link_button(c, "查看 GitHub", "https://github.com/lincoln3079938241-coder", MARGIN, 176, 118)
    link_button(c, "Auto-LifeOS Demo", "https://auto-lifeos-demo.streamlit.app/", MARGIN + 130, 176, 142)
    link_button(c, "秋招雷达 Demo", "https://shanghai-2027-job-radar-demo.streamlit.app/", MARGIN + 284, 176, 132)
    c.setFillColor(MUTED)
    c.setFont("MSYH", 7.2)
    c.drawString(MARGIN, 151, "作品集只使用仓库可验证信息，不虚构模型调用、用户规模、访谈或业务效果。")

    rx, ry, rw, rh = 532, 102, 270, 390
    card(c, rx, ry, rw, rh, fill=white)
    c.setFillColor(INK)
    c.setFont("MSYH-Bold", 15)
    c.drawString(rx + 20, ry + rh - 32, "能力地图")
    capabilities = [
        "AI产品设计", "用户场景拆解", "Agent工作流", "RAG与生成式AI理解",
        "原型与Demo开发", "数据分析与效果评估", "AI Coding辅助开发",
    ]
    py = ry + rh - 66
    for item in capabilities:
        c.setFillColor(CYAN)
        c.circle(rx + 24, py + 2, 2.5, fill=1, stroke=0)
        c.setFillColor(INK)
        c.setFont("MSYH-Bold", 8.7)
        c.drawString(rx + 36, py - 2, item)
        c.setStrokeColor(LINE)
        c.line(rx + 20, py - 12, rx + rw - 20, py - 12)
        py -= 37
    c.setFillColor(INK)
    c.roundRect(rx + 18, ry + 18, rw - 36, 54, 10, fill=1, stroke=0)
    c.setFillColor(LIME)
    c.setFont("MSYH-Bold", 7)
    c.drawString(rx + 30, ry + 54, "FOCUS")
    c.setFillColor(white)
    c.setFont("MSYH-Bold", 10)
    c.drawString(rx + 30, ry + 35, "AI Agent × 数据产品 × AI+汽车")
    footer(c, 1, 7)


def page_auto_product(c: canvas.Canvas) -> None:
    y = title(c, "01 / CORE CASE · AI AGENT", "Auto-LifeOS", "把饮食需求变成经过规则校验、双阶段确认和库存事务更新的可执行流程。")
    cw = (PAGE_W - 2 * MARGIN - 20) / 3
    card_text(c, MARGIN, y - 104, cw, 94, "用户问题", "建议与库存脱节", "用户得到一道菜后，仍需自行核对库存、过期状态、忌口与实际用量。")
    card_text(c, MARGIN + cw + 10, y - 104, cw, 94, "产品目标", "让建议可执行", "需求经过检索、方案生成和确定性校验，只有双确认后才触发库存事务。")
    card_text(c, MARGIN + (cw + 10) * 2, y - 104, cw, 94, "公开边界", "默认Mock，无私密Key", "公开版不调用GPT/Qwen；全部用户、库存、知识与实验数据为synthetic/sample。")

    sy = y - 338
    shot_w, shot_h = 188, 101
    image_fit(c, ASSETS / "screenshots" / "auto-01-home.jpg", MARGIN, sy + 108, shot_w, shot_h)
    image_fit(c, ASSETS / "screenshots" / "auto-02-result.jpg", MARGIN + 197, sy + 108, shot_w, shot_h)
    image_fit(c, ASSETS / "screenshots" / "auto-03-confirm.jpg", MARGIN, sy, shot_w, shot_h)
    image_fit(c, ASSETS / "screenshots" / "auto-04-update.jpg", MARGIN + 197, sy, shot_w, shot_h)
    c.setFillColor(MUTED)
    c.setFont("MSYH", 6.8)
    c.drawString(MARGIN + 8, sy - 12, "公开Demo真实界面：输入 → 方案 → 第二阶段确认 → 库存事务结果")

    c.setFillColor(INK)
    c.setFont("MSYH-Bold", 12)
    c.drawString(445, y - 132, "核心功能")
    bullets(
        c,
        [
            "LangGraph节点编排、条件路由、校验重试与异常回退",
            "TF-IDF知识检索与结构化MealPlan",
            "库存、过敏、忌口、过期、单位和数量规则校验",
            "方案确认 + 实际用量确认的双阶段确认",
            "SQLite原子库存事务、审计记录与撤销",
        ],
        445,
        y - 155,
        345,
        size=8.2,
        leading=13,
    )
    px = 445
    for txt in ["61 公开版测试", "27 核心测试", "28 演示菜谱"]:
        px += pill(c, txt, px, sy + 30, fill=WARM, color=BLUE) + 7
    c.setFont("MSYH-Bold", 9)
    c.setFillColor(INK)
    c.drawString(MARGIN, 66, "用户流程")
    flow(c, ["需求输入", "意图理解", "检索与生成", "规则校验", "双确认", "库存事务", "追踪与回退"], MARGIN, 34, PAGE_W - 2 * MARGIN, h=28)
    c.linkURL("https://auto-lifeos-demo.streamlit.app/", (PAGE_W - 180, PAGE_H - 82, PAGE_W - MARGIN, PAGE_H - 46), relative=0)
    footer(c, 2, 7)


def page_auto_evaluation(c: canvas.Canvas) -> None:
    y = title(c, "01 / CORE CASE · DECISIONS & EVALUATION", "Auto-LifeOS：为什么这样设计", "模型或Mock只提出方案；确定性规则、双确认与数据库事务控制可执行性和副作用。")
    bw = (PAGE_W - 2 * MARGIN - 24) / 3
    card_text(c, MARGIN, y - 118, bw, 108, "PROVIDER / MOCK", "提出结构化方案", "理解需求、组织检索证据并输出候选MealPlan；不拥有库存写权限。", fill=PALE)
    card_text(c, MARGIN + bw + 12, y - 118, bw, 108, "RULES", "控制可执行性", "Pydantic与Python检查过敏、忌口、过期、单位、数量和营养范围。", fill=PALE)
    card_text(c, MARGIN + (bw + 12) * 2, y - 118, bw, 108, "TRANSACTION", "控制副作用", "双确认后由SQLite原子事务更新；失败整体回滚，成功结果可撤销。", fill=WARM)
    panel_y, panel_h = y - 346, 208
    card(c, MARGIN, panel_y, 365, panel_h, fill=white)
    c.setFillColor(CYAN); c.setFont("MSYH-Bold", 7); c.drawString(MARGIN + 14, panel_y + panel_h - 20, "KEY PRODUCT DECISIONS")
    c.setFillColor(INK); c.setFont("MSYH-Bold", 11); c.drawString(MARGIN + 14, panel_y + panel_h - 42, "四个决定构成可演示闭环")
    bullets(c, [
        "规则校验独立于生成：可解释、可回归，避免模型直接决定安全边界。",
        "两阶段确认：先确认方案，再按实际用量确认库存副作用。",
        "事务更新可撤销：把失败回滚与误操作恢复做成产品能力。",
        "公开版默认Mock：无需私密Key，且不把稳定演示包装成真实LLM调用。",
    ], MARGIN + 14, panel_y + panel_h - 66, 336, size=7.3, leading=11)
    card(c, 416, panel_y, 387, panel_h, fill=white)
    c.setFillColor(CYAN); c.setFont("MSYH-Bold", 7); c.drawString(430, panel_y + panel_h - 20, "SYNTHETIC USABILITY EVALUATION")
    c.setFillColor(INK); c.setFont("MSYH-Bold", 11); c.drawString(430, panel_y + panel_h - 42, "模拟任务，不是真实用户研究")
    personas = [
        "独居上班族｜晚餐20分钟内完成｜关注步骤与库存是否够",
        "健身用户｜高蛋白低脂｜关注营养解释与份量可调",
        "过敏用户｜排除花生｜关注禁忌是否在确认前被拦截",
        "家庭库存管理者｜多人共用｜关注实际用量、撤销与审计",
    ]
    bullets(c, personas, 430, panel_y + panel_h - 66, 355, size=7.2, leading=10.8)
    card(c, MARGIN, 34, PAGE_W - 2 * MARGIN, 86, fill=INK, stroke=INK)
    c.setFillColor(LIME); c.setFont("MSYH-Bold", 7); c.drawString(MARGIN + 14, 98, "PROTOTYPE COMPARISON · NOT A LIVE A/B TEST")
    c.setFillColor(white); c.setFont("MSYH-Bold", 9.5); c.drawString(MARGIN + 14, 78, "方案A：一步确认、信息密度低  vs  方案B：双阶段确认、展示库存变化与撤销")
    text_block(c, "最终选择方案B：虽然多一次确认，但能降低库存误更新风险，并让规则校验和事务结果对用户可见。自动化测试覆盖路由、规则边界、双确认、事务原子性、撤销与会话隔离；公开版仍无真实用户访谈或线上A/B结果。", MARGIN + 14, 59, PAGE_W - 2 * MARGIN - 28, size=7.2, leading=10.5, color=HexColor("#C6D3D8"), max_lines=3)
    footer(c, 3, 7)


def page_radar(c: canvas.Canvas) -> None:
    y = title(c, "02 / 0→1 DATA PRODUCT", "2027届秋招岗位雷达", "从分散招聘入口到可追溯、可筛选、可复核的岗位信息清单。")
    radar_y = y - 252
    image_fit(c, ASSETS / "screenshots" / "radar-01-home.jpg", MARGIN, radar_y + 116, 190, 108)
    image_fit(c, ASSETS / "screenshots" / "radar-02-filter.jpg", MARGIN + 200, radar_y + 116, 190, 108)
    image_fit(c, ASSETS / "screenshots" / "radar-03-sources.jpg", MARGIN, radar_y, 190, 108)
    image_fit(c, ASSETS / "screenshots" / "radar-04-quality.jpg", MARGIN + 200, radar_y, 190, 108)
    c.setFont("MSYH", 6.8)
    c.setFillColor(MUTED)
    c.drawString(MARGIN + 8, y - 268, "公开Demo真实界面：首页 · 筛选 · 来源核验 · 数据质量")
    c.setFillColor(INK)
    c.setFont("MSYH-Bold", 12)
    c.drawString(450, y - 5, "用户问题与产品价值")
    problems = [
        ("痛点", "跨平台搜索成本高", "企业官网、公共就业服务和高校网站入口分散。"),
        ("痛点", "信息分散，容易遗漏", "地点、方向、阶段和专业限制缺少统一字段。"),
        ("数据问题", "来源与状态不透明", "转载可能重复或过时，需要保留来源和更新时间。"),
        ("产品价值", "一次整理，持续筛选", "将公开线索转为结构化清单，降低重复劳动。"),
    ]
    py = y - 35
    for label, heading, body in problems:
        card_text(c, 450, py - 69, 352, 62, label, heading, body, fill=white)
        py -= 70
    c.setFont("MSYH-Bold", 9)
    c.setFillColor(INK)
    c.drawString(MARGIN, 95, "数据流程")
    flow(c, ["公开入口", "合规采集/导入", "清洗标准化", "去重变更", "规则筛选", "质量提示", "来源回查"], MARGIN, 62, PAGE_W - 2 * MARGIN, h=27)
    c.setFillColor(GOLD_BG)
    c.setStrokeColor(GOLD_BG)
    c.roundRect(MARGIN, 32, PAGE_W - 2 * MARGIN, 21, 7, fill=1, stroke=0)
    c.setFont("MSYH", 7.2)
    c.setFillColor(GOLD)
    c.drawString(MARGIN + 10, 39, "能力边界：数据自动化、规则筛选、信息管理与产品化展示；不包含Agent、大模型、智能推荐或岗位成功率预测。")
    footer(c, 4, 7)


def drive_page_one(c: canvas.Canvas, page_no: int, total: int, *, concept_only=False) -> None:
    y = title(c, "03 / CONCEPT PROPOSAL · 未开发上线", "DriveMate", "面向城市通勤、家庭出行和长途驾驶用户的多Agent、多模态智能出行与车况助手。")
    c.setFillColor(GOLD_BG)
    c.setStrokeColor(GOLD_BG)
    c.roundRect(PAGE_W - 245, PAGE_H - 72, 207, 23, 10, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.setFont("MSYH-Bold", 7.2)
    c.drawCentredString(PAGE_W - 141.5, PAGE_H - 64, "Concept Proposal / 点击查看静态原型")
    c.linkURL(
        "https://lincoln3079938241-coder.github.io/weixin-ai-product-portfolio/drivemate.html",
        (PAGE_W - 245, PAGE_H - 72, PAGE_W - 38, PAGE_H - 49),
        relative=0,
    )
    pw = (PAGE_W - 2 * MARGIN - 24) / 4
    pains = [
        ("痛点01", "行程信息分散", "地图、天气、日程与同行人安排彼此割裂。"),
        ("痛点02", "车况难以理解", "电量、胎压和维保状态缺少普通用户可理解的解释。"),
        ("痛点03", "补能无法统筹", "路线、充电站、停留时间和到达目标需要联合规划。"),
        ("痛点04", "缺少连续执行", "传统语音交互难以完成跨工具复合任务。"),
    ]
    for idx, p in enumerate(pains):
        card_text(c, MARGIN + idx * (pw + 8), y - 91, pw, 82, *p)
    card(c, MARGIN, y - 296, 230, 184, fill=INK, stroke=INK)
    c.setFillColor(LIME)
    c.setFont("MSYH-Bold", 7)
    c.drawString(MARGIN + 16, y - 140, "ORCHESTRATOR")
    c.setFillColor(white)
    c.setFont("MSYH-Bold", 14)
    c.drawString(MARGIN + 16, y - 168, "DriveMate 主Agent")
    text_block(
        c,
        "拆解任务、协调专业Agent、选择工具、汇总事实与推断，并在关键操作前请求用户确认。",
        MARGIN + 16,
        y - 193,
        195,
        size=8.3,
        leading=13.2,
        color=HexColor("#C5D2D7"),
    )
    agents = [
        ("出行规划Agent", "地图 / 交通 / 天气"),
        ("车辆状态解释Agent", "电量 / 胎压 / 维保"),
        ("补能规划Agent", "续航 / 充电站 / 停留"),
        ("日程与提醒Agent", "日历 / 出发提醒"),
        ("应急支持Agent", "异常解释 / 专业服务"),
    ]
    ax, ay, aw, ah = 285, y - 190, 247, 76
    for idx, (name, tools) in enumerate(agents):
        row, col = divmod(idx, 2)
        xi = ax + col * (aw + 10)
        yi = ay - row * (ah + 8)
        if idx == 4:
            xi, yi, aw2 = ax, ay - 2 * (ah + 8), 504
        else:
            aw2 = aw
        card(c, xi, yi, aw2, ah, fill=white)
        c.setFillColor(INK)
        c.setFont("MSYH-Bold", 9.2)
        c.drawString(xi + 12, yi + 45, name)
        c.setFillColor(MUTED)
        c.setFont("MSYH", 7.5)
        c.drawString(xi + 12, yi + 23, tools)
    layer_w = (PAGE_W - 2 * MARGIN - 16) / 3
    layers = [
        ("多模态输入", "语音/文本 · 车况 · 地图天气 · 内外视觉概念输入"),
        ("主Agent编排", "任务拆解 · 工具聚合 · 事实/推断分离 · 风险分级"),
        ("安全输出", "可解释计划 · 数据时间 · 待确认动作 · 专业服务建议"),
    ]
    for idx, (head, body) in enumerate(layers):
        xi = MARGIN + idx * (layer_w + 8)
        card(c, xi, 32, layer_w, 68, fill=PALE if idx < 2 else WARM)
        c.setFillColor(CYAN); c.setFont("MSYH-Bold", 6.5); c.drawString(xi + 10, 82, f"LAYER {idx + 1}")
        c.setFillColor(INK); c.setFont("MSYH-Bold", 8.5); c.drawString(xi + 10, 65, head)
        text_block(c, body, xi + 10, 49, layer_w - 20, size=6.5, leading=9.2, color=MUTED, max_lines=2)
    c.setFillColor(GOLD); c.setFont("MSYH", 6.2)
    c.drawRightString(PAGE_W - MARGIN, 108, "静态概念：未接入摄像头、车辆传感器、真实VLA模型或车控接口")
    footer(c, page_no, total, "DriveMate · Concept Proposal" if concept_only else "陈蔚昕 · AI产品经理作品集")


def drive_page_two(c: canvas.Canvas, page_no: int, total: int, *, concept_only=False) -> None:
    y = title(c, "03 / CONCEPT PROPOSAL · SCENARIOS & ROADMAP", "DriveMate：高约束场景、安全与VLA路线", "所有车辆、地图、天气、日历、视觉和充电站能力均为拟议范围，不代表已经接入API或模型。")
    c.linkURL(
        "https://lincoln3079938241-coder.github.io/weixin-ai-product-portfolio/drivemate.html",
        (MARGIN, PAGE_H - 132, PAGE_W - MARGIN, PAGE_H - 46),
        relative=0,
    )
    sw = (PAGE_W - 2 * MARGIN - 16) / 3
    scenarios = [
        ("场景01", "暴雨积水 · 机场接人", "合并天气、路况与续航；不判断水深，不指导涉水。"),
        ("场景02", "家庭长途 · 上海至杭州", "围绕午餐日程、老人儿童休息与补能候选反推出发。"),
        ("场景03", "胎压异常 · 安全处置", "暂停长途规划，优先停车检查与专业服务入口。"),
    ]
    for idx, item in enumerate(scenarios):
        card_text(c, MARGIN + idx * (sw + 8), y - 91, sw, 80, *item, fill=white)
    panel_y, panel_h = y - 229, 122
    card(c, MARGIN, panel_y, 365, panel_h, fill=white)
    c.setFillColor(CYAN); c.setFont("MSYH-Bold", 7); c.drawString(MARGIN + 14, panel_y + panel_h - 18, "SAFETY BOUNDARY")
    bullets(c, ["不执行高风险车控；关键操作需确认", "事实、过期数据与模型推断分层展示", "异常优先停车检查或联系专业服务", "工具缺失时说明缺口，不补造事实"], MARGIN + 14, panel_y + panel_h - 39, 335, size=7.1, leading=10.5)
    card(c, 416, panel_y, 387, panel_h, fill=white)
    c.setFillColor(CYAN); c.setFont("MSYH-Bold", 7); c.drawString(430, panel_y + panel_h - 18, "PLANNED EVALUATION · NOT RESULTS")
    mx, my = 430, panel_y + panel_h - 46
    for metric in ["任务完成率", "工具调用准确率", "信息事实性", "用户确认次数", "响应时间", "用户满意度", "高风险错误率"]:
        mw = pill(c, metric, mx, my, fill=PALE, color=BLUE, h=18)
        mx += mw + 6
        if mx > 746:
            mx = 430
            my -= 25
    c.setFillColor(MUTED); c.setFont("MSYH", 6.4); c.drawString(430, panel_y + 12, "以上为概念验证指标，并非已取得的线上结果。")

    c.setFillColor(INK); c.setFont("MSYH-Bold", 10); c.drawString(MARGIN, panel_y - 23, "静态低保真页面示意")
    wx, wy, ww, wh = MARGIN, 115, PAGE_W - 2 * MARGIN, 112
    card(c, wx, wy, ww, wh, fill=PAPER, stroke=INK, radius=12)
    card(c, wx + 10, wy + 10, 185, wh - 20, fill=white)
    c.setFillColor(CYAN); c.setFont("MSYH-Bold", 6.5); c.drawString(wx + 22, wy + wh - 29, "VEHICLE & CONTEXT")
    for idx, line in enumerate(["电量 68% · 示例", "天气 暴雨预警 · 示例", "胎压 正常 · 示例"]):
        c.setFillColor(INK); c.setFont("MSYH", 7); c.drawString(wx + 22, wy + wh - 48 - idx * 17, line)
    main_x = wx + 205
    card(c, main_x, wy + 10, ww - 215, wh - 20, fill=white)
    c.setFillColor(INK); c.setFont("MSYH-Bold", 9); c.drawString(main_x + 13, wy + wh - 28, "暴雨积水条件下的机场接人计划")
    c.setFillColor(MUTED); c.setFont("MSYH", 6.6); c.drawString(main_x + 13, wy + wh - 46, "建议提前25分钟出发 · 主干高架优先 · 保留20%续航余量")
    c.setFillColor(GOLD_BG); c.roundRect(main_x + 13, wy + 34, ww - 243, 24, 6, fill=1, stroke=0)
    c.setFillColor(GOLD); c.setFont("MSYH", 6.3); c.drawString(main_x + 23, wy + 43, "高风险：无法判断水深；只提示绕行，不指导涉水。")
    c.setFillColor(INK); c.roundRect(main_x + 13, wy + 10, ww - 243, 18, 5, fill=1, stroke=0)
    c.setFillColor(white); c.setFont("MSYH-Bold", 6.3); c.drawCentredString(main_x + (ww - 217) / 2, wy + 16, "确认写入提醒草案（静态示意）")

    c.setFillColor(INK); c.setFont("MSYH-Bold", 9); c.drawString(MARGIN, 91, "Physical AI / VLA 分阶段路线")
    stages = [
        ("0 当前", "静态概念与合成场景"),
        ("1 只读沙盒", "授权车辆数据与工具评测"),
        ("2 多模态理解", "离线视觉—语言风险评测"),
        ("3 受控行动", "封闭环境、低风险、人工确认"),
    ]
    stage_w = (PAGE_W - 2 * MARGIN - 18) / 4
    for idx, (head, body) in enumerate(stages):
        xi = MARGIN + idx * (stage_w + 6)
        card(c, xi, 35, stage_w, 46, fill=PALE if idx else white)
        c.setFillColor(CYAN if idx else MUTED); c.setFont("MSYH-Bold", 6.5); c.drawString(xi + 9, 65, head)
        c.setFillColor(INK); c.setFont("MSYH", 6.2); c.drawString(xi + 9, 48, body)
    footer(c, page_no, total, "DriveMate · Concept Proposal" if concept_only else "陈蔚昕 · AI产品经理作品集")


def page_method(c: canvas.Canvas) -> None:
    y = title(c, "PRODUCT METHOD · CONTACT", "我的产品方法", "用可验证的MVP缩短“想法”和“证据”之间的距离。")
    flow(c, ["发现问题", "定义用户场景", "制定MVP", "搭建Demo", "测试评估", "bad case分析", "迭代优化"], MARGIN, y - 53, PAGE_W - 2 * MARGIN, h=36)
    methods = [
        ("01", "发现问题", "先确认用户为什么被现状阻塞。"),
        ("02", "定义用户与场景", "明确谁、何时、在什么约束下使用。"),
        ("03", "制定MVP", "保留最短闭环与清晰安全边界。"),
        ("04", "搭建Demo", "把关键流程做成可交互原型。"),
        ("05", "测试与评估", "用任务、规则与结果指标验证。"),
        ("06", "bad case分析", "按失败类型定位产品或系统问题。"),
        ("07", "迭代优化", "回归测试后再进入下一轮。"),
    ]
    mw = (PAGE_W - 2 * MARGIN - 18) / 4
    for idx, item in enumerate(methods):
        row, col = divmod(idx, 4)
        x = MARGIN + col * (mw + 6)
        yy = y - 158 - row * 92
        card_text(c, x, yy, mw, 82, item[0], item[1], item[2], fill=white)
    card(c, MARGIN, 48, PAGE_W - 2 * MARGIN, 118, fill=INK, stroke=INK)
    c.setFillColor(LIME)
    c.setFont("MSYH-Bold", 7)
    c.drawString(MARGIN + 18, 143, "CONTACT & LINKS")
    c.setFillColor(white)
    c.setFont("MSYH-Bold", 15)
    c.drawString(MARGIN + 18, 117, "期待一起把AI能力做成可用产品")
    c.setFont("MSYH", 8)
    c.setFillColor(HexColor("#C5D2D7"))
    c.drawString(MARGIN + 18, 94, "陈蔚昕 · AI产品经理｜生成式AI与AI创新")
    links = [
        ("GitHub", "https://github.com/lincoln3079938241-coder"),
        ("Auto-LifeOS", "https://auto-lifeos-demo.streamlit.app/"),
        ("秋招雷达", "https://shanghai-2027-job-radar-demo.streamlit.app/"),
        ("公开邮箱", "mailto:Lincoln3079938241@163.com"),
    ]
    lx = 390
    for label, url in links:
        c.setFillColor(HexColor("#20343E"))
        c.roundRect(lx, 85, 94, 37, 8, fill=1, stroke=0)
        c.setFillColor(white)
        c.setFont("MSYH-Bold", 7.5)
        c.drawCentredString(lx + 47, 99, label)
        c.linkURL(url, (lx, 85, lx + 94, 122), relative=0)
        lx += 101
    c.setFillColor(HexColor("#9FB1B8"))
    c.setFont("MSYH", 6.4)
    c.drawString(390, 67, "仅公开求职邮箱，不展示手机号或其他非必要个人信息。")
    footer(c, 7, 7)


def footer_en(c: canvas.Canvas, page_no: int, total: int, label: str = "WEIXIN CHEN · AI Product Manager Portfolio") -> None:
    footer(c, page_no, total, label)


def page_one_en(c: canvas.Canvas) -> None:
    c.setFillColor(PAPER)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    c.setFillColor(CYAN)
    c.rect(0, 0, 8, PAGE_H, fill=1, stroke=0)
    c.setFont("MSYH-Bold", 8)
    c.drawString(MARGIN, PAGE_H - 46, "AI PRODUCT MANAGER PORTFOLIO")
    c.setFillColor(INK)
    c.setFont("MSYH-Bold", 38)
    c.drawString(MARGIN, PAGE_H - 112, "WEIXIN CHEN")
    c.setFillColor(BLUE)
    c.setFont("MSYH-Bold", 16.5)
    c.drawString(MARGIN, PAGE_H - 148, "AI Product Manager | Generative AI & AI Innovation")
    text_block(
        c,
        "AI product portfolio covering agent workflows, data products, and independently developed prototypes. Experienced in identifying user problems, defining solutions, building functional demos, evaluating product behavior, and iterating with evidence.",
        MARGIN,
        PAGE_H - 181,
        445,
        size=10.5,
        leading=16,
        color=MUTED,
        max_lines=5,
    )
    buttons = [
        ("English website", SITE_EN_URL, 111),
        ("GitHub", "https://github.com/lincoln3079938241-coder", 92),
        ("Auto-LifeOS", "https://auto-lifeos-demo.streamlit.app/", 112),
        ("Job Radar", "https://shanghai-2027-job-radar-demo.streamlit.app/", 102),
    ]
    bx = MARGIN
    for label, url, width in buttons:
        link_button(c, label, url, bx, 162, width)
        bx += width + 9
    c.setFillColor(MUTED)
    c.setFont("MSYH", 7)
    c.drawString(MARGIN, 139, "Claims are limited to repository-verifiable evidence. No fabricated users, interviews, model calls, or business outcomes.")

    rx, ry, rw, rh = 532, 102, 270, 390
    card(c, rx, ry, rw, rh, fill=white)
    c.setFillColor(INK)
    c.setFont("MSYH-Bold", 15)
    c.drawString(rx + 20, ry + rh - 32, "Capability Map")
    capabilities = [
        "AI Product Design",
        "User Scenario Definition",
        "Agent Workflow Design",
        "RAG & Generative AI",
        "Prototype & Demo Development",
        "Data Analysis & Evaluation",
        "AI-Assisted Development",
    ]
    py = ry + rh - 66
    for item in capabilities:
        c.setFillColor(CYAN)
        c.circle(rx + 24, py + 2, 2.5, fill=1, stroke=0)
        c.setFillColor(INK)
        c.setFont("MSYH-Bold", 8.3)
        c.drawString(rx + 36, py - 2, item)
        c.setStrokeColor(LINE)
        c.line(rx + 20, py - 12, rx + rw - 20, py - 12)
        py -= 37
    c.setFillColor(INK)
    c.roundRect(rx + 18, ry + 18, rw - 36, 54, 10, fill=1, stroke=0)
    c.setFillColor(LIME)
    c.setFont("MSYH-Bold", 7)
    c.drawString(rx + 30, ry + 54, "FOCUS")
    c.setFillColor(white)
    c.setFont("MSYH-Bold", 9.2)
    c.drawString(rx + 30, ry + 35, "AI agents × data products × automotive AI")
    footer_en(c, 1, 7)


def page_auto_product_en(c: canvas.Canvas) -> None:
    y = title(c, "01 / CORE CASE · AI AGENT", "Auto-LifeOS", "Turns a meal request into an executable workflow with validation, two-stage confirmation, and transactional inventory updates.")
    cw = (PAGE_W - 2 * MARGIN - 20) / 3
    card_text_en(c, MARGIN, y - 104, cw, 94, "USER PROBLEM", "Advice ignores inventory", "Users still verify stock, expiry, dietary restrictions, and actual quantities.")
    card_text_en(c, MARGIN + cw + 10, y - 104, cw, 94, "PRODUCT GOAL", "Make advice executable", "Retrieval and deterministic rules run before two confirmations authorize an inventory transaction.")
    card_text_en(c, MARGIN + (cw + 10) * 2, y - 104, cw, 94, "PUBLIC BOUNDARY", "Mock Provider, no private key", "The public demo does not call GPT or Qwen; user, inventory, knowledge, and test data are synthetic or sample data.")

    sy = y - 338
    shot_w, shot_h = 188, 101
    image_fit(c, ASSETS / "screenshots" / "auto-01-home.jpg", MARGIN, sy + 108, shot_w, shot_h)
    image_fit(c, ASSETS / "screenshots" / "auto-02-result.jpg", MARGIN + 197, sy + 108, shot_w, shot_h)
    image_fit(c, ASSETS / "screenshots" / "auto-03-confirm.jpg", MARGIN, sy, shot_w, shot_h)
    image_fit(c, ASSETS / "screenshots" / "auto-04-update.jpg", MARGIN + 197, sy, shot_w, shot_h)
    c.setFillColor(MUTED)
    c.setFont("MSYH", 6.4)
    c.drawString(MARGIN + 8, sy - 12, "Public demo screens: request - plan - second confirmation - inventory transaction result")

    c.setFillColor(INK)
    c.setFont("MSYH-Bold", 12)
    c.drawString(445, y - 132, "Core product behavior")
    bullets(
        c,
        [
            "LangGraph node orchestration, conditional routing, validation retry, and exception fallback",
            "TF-IDF knowledge retrieval with a structured MealPlan",
            "Deterministic checks for allergies, exclusions, expiry, units, and quantities",
            "Two-stage confirmation for the plan and actual quantities",
            "Atomic SQLite inventory transactions, audit records, and undo",
        ],
        445,
        y - 155,
        345,
        size=7.4,
        leading=11.2,
    )
    px = 445
    for txt in ["61 public tests", "27 core tests", "28 demo recipes"]:
        px += pill(c, txt, px, sy + 30, fill=WARM, color=BLUE) + 7
    c.setFont("MSYH-Bold", 9)
    c.setFillColor(INK)
    c.drawString(MARGIN, 66, "User flow")
    flow(c, ["Request", "Intent", "Retrieve", "Validate", "Confirm twice", "Transaction", "Trace & undo"], MARGIN, 34, PAGE_W - 2 * MARGIN, h=28)
    c.linkURL("https://auto-lifeos-demo.streamlit.app/", (PAGE_W - 180, PAGE_H - 82, PAGE_W - MARGIN, PAGE_H - 46), relative=0)
    footer_en(c, 2, 7)


def page_auto_evaluation_en(c: canvas.Canvas) -> None:
    y = title(c, "01 / CORE CASE · DECISIONS & EVALUATION", "Auto-LifeOS: Product Decisions", "The provider proposes a plan; deterministic rules, confirmation, and database transactions control execution and side effects.")
    bw = (PAGE_W - 2 * MARGIN - 24) / 3
    card_text_en(c, MARGIN, y - 118, bw, 108, "PROVIDER / MOCK", "Propose a structured plan", "Interpret the request, organize retrieval evidence, and output a candidate MealPlan without inventory write access.", fill=PALE)
    card_text_en(c, MARGIN + bw + 12, y - 118, bw, 108, "RULES", "Control executability", "Pydantic and Python check allergies, exclusions, expiry, units, quantities, and nutrition ranges.", fill=PALE)
    card_text_en(c, MARGIN + (bw + 12) * 2, y - 118, bw, 108, "TRANSACTION", "Control side effects", "After two confirmations, SQLite updates atomically. Failures roll back and successful results support undo.", fill=WARM)
    panel_y, panel_h = y - 346, 208
    card(c, MARGIN, panel_y, 365, panel_h, fill=white)
    c.setFillColor(CYAN); c.setFont("MSYH-Bold", 7); c.drawString(MARGIN + 14, panel_y + panel_h - 20, "KEY PRODUCT DECISIONS")
    c.setFillColor(INK); c.setFont("MSYH-Bold", 11); c.drawString(MARGIN + 14, panel_y + panel_h - 42, "Four decisions create the demo loop")
    bullets(c, [
        "Keep validation outside generation so safety boundaries remain explainable and regression-testable.",
        "Confirm the plan first, then confirm actual quantities before any inventory side effect.",
        "Make updates atomic and reversible, treating recovery as a product capability.",
        "Use a Mock Provider in public so the demo is stable without claiming a live model call.",
    ], MARGIN + 14, panel_y + panel_h - 66, 336, size=7, leading=10.5)
    card(c, 416, panel_y, 387, panel_h, fill=white)
    c.setFillColor(CYAN); c.setFont("MSYH-Bold", 7); c.drawString(430, panel_y + panel_h - 20, "SYNTHETIC USABILITY EVALUATION")
    c.setFillColor(INK); c.setFont("MSYH-Bold", 11); c.drawString(430, panel_y + panel_h - 42, "Task walkthroughs, not user research")
    personas = [
        "Single professional | quick meal | checks process clarity and available stock",
        "Fitness-focused user | high protein | checks rationale and adjustable portions",
        "User with allergies | exclude peanuts | checks that rules block conflicts early",
        "Household inventory owner | shared use | checks quantities, audit trail, and undo",
    ]
    bullets(c, personas, 430, panel_y + panel_h - 66, 355, size=6.9, leading=10.2)
    card(c, MARGIN, 34, PAGE_W - 2 * MARGIN, 86, fill=INK, stroke=INK)
    c.setFillColor(LIME); c.setFont("MSYH-Bold", 7); c.drawString(MARGIN + 14, 98, "PROTOTYPE COMPARISON · NOT A LIVE A/B TEST")
    c.setFillColor(white); c.setFont("MSYH-Bold", 9); c.drawString(MARGIN + 14, 78, "Version A: one confirmation, low detail  vs  Version B: two confirmations, inventory preview, and undo")
    text_block(c, "Version B is the selected direction. It adds one confirmation but makes validation and inventory effects visible. Automated tests cover routing, rule boundaries, confirmation, transaction atomicity, undo, and session isolation. There are no real-user interviews or live A/B results.", MARGIN + 14, 59, PAGE_W - 2 * MARGIN - 28, size=6.9, leading=10.2, color=HexColor("#C6D3D8"), max_lines=3)
    footer_en(c, 3, 7)


def page_radar_en(c: canvas.Canvas) -> None:
    y = title(c, "02 / 0->1 DATA PRODUCT", "2027 Graduate Job Radar", "Turns fragmented recruitment entry points into a traceable, filterable, and reviewable job-information list.")
    radar_y = y - 252
    image_fit(c, ASSETS / "screenshots" / "radar-01-home.jpg", MARGIN, radar_y + 116, 190, 108)
    image_fit(c, ASSETS / "screenshots" / "radar-02-filter.jpg", MARGIN + 200, radar_y + 116, 190, 108)
    image_fit(c, ASSETS / "screenshots" / "radar-03-sources.jpg", MARGIN, radar_y, 190, 108)
    image_fit(c, ASSETS / "screenshots" / "radar-04-quality.jpg", MARGIN + 200, radar_y, 190, 108)
    c.setFont("MSYH", 6.4)
    c.setFillColor(MUTED)
    c.drawString(MARGIN + 8, y - 268, "Public demo screens: home · filters · source verification · data quality")
    c.setFillColor(INK)
    c.setFont("MSYH-Bold", 12)
    c.drawString(450, y - 5, "User problem and product value")
    problems = [
        ("PAIN POINT", "High search cost", "Company, public-employment, and university entry points are scattered."),
        ("PAIN POINT", "Details are easy to miss", "Location, function, stage, and degree limits lack consistent fields."),
        ("DATA PROBLEM", "Source status is unclear", "Reposts may be duplicated or stale; source and time must remain visible."),
        ("PRODUCT VALUE", "Structure once, filter often", "Convert public leads into a structured list and reduce repeated work."),
    ]
    py = y - 35
    for label, heading, body in problems:
        card_text_en(c, 450, py - 69, 352, 62, label, heading, body, body_size=6.7, body_lines=2)
        py -= 70
    c.setFont("MSYH-Bold", 9)
    c.setFillColor(INK)
    c.drawString(MARGIN, 95, "Data flow")
    flow(c, ["Public sources", "Collect/import", "Normalize", "Deduplicate", "Rule filters", "Quality notice", "Source review"], MARGIN, 62, PAGE_W - 2 * MARGIN, h=27)
    c.setFillColor(GOLD_BG)
    c.setStrokeColor(GOLD_BG)
    c.roundRect(MARGIN, 32, PAGE_W - 2 * MARGIN, 21, 7, fill=1, stroke=0)
    c.setFont("MSYH", 6.7)
    c.setFillColor(GOLD)
    c.drawString(MARGIN + 10, 39, "Boundary: data automation, rule-based filtering, information management, and product presentation - no agent, LLM, recommendation, or success score.")
    c.linkURL("https://shanghai-2027-job-radar-demo.streamlit.app/", (PAGE_W - 180, PAGE_H - 82, PAGE_W - MARGIN, PAGE_H - 46), relative=0)
    footer_en(c, 4, 7)


def drive_page_one_en(c: canvas.Canvas, page_no: int, total: int, *, concept_only=False) -> None:
    y = title(c, "03 / CONCEPT PROPOSAL · NOT LAUNCHED", "DriveMate", "A multi-agent, multimodal mobility and vehicle-status assistant for commuters, families, and long-distance drivers.")
    c.setFillColor(GOLD_BG)
    c.setStrokeColor(GOLD_BG)
    c.roundRect(PAGE_W - 245, PAGE_H - 72, 207, 23, 10, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.setFont("MSYH-Bold", 7.2)
    c.drawCentredString(PAGE_W - 141.5, PAGE_H - 64, "Concept Proposal / Open static prototype")
    c.linkURL(f"{SITE_EN_URL}drivemate.html", (PAGE_W - 245, PAGE_H - 72, PAGE_W - 38, PAGE_H - 49), relative=0)
    pw = (PAGE_W - 2 * MARGIN - 24) / 4
    pains = [
        ("PAIN 01", "Fragmented trip context", "Maps, weather, schedule, and passenger needs are handled separately."),
        ("PAIN 02", "Vehicle status is opaque", "Battery, tire pressure, and maintenance data need plain-language explanation."),
        ("PAIN 03", "Charging is hard to coordinate", "Route, stations, stop duration, and arrival goals must be planned together."),
        ("PAIN 04", "Compound tasks break apart", "Traditional voice flows struggle to coordinate work across several tools."),
    ]
    for idx, p in enumerate(pains):
        card_text_en(c, MARGIN + idx * (pw + 8), y - 91, pw, 82, *p, heading_size=8.2, body_size=6.5, body_lines=3)
    card(c, MARGIN, y - 296, 230, 184, fill=INK, stroke=INK)
    c.setFillColor(LIME)
    c.setFont("MSYH-Bold", 7)
    c.drawString(MARGIN + 16, y - 140, "ORCHESTRATOR")
    c.setFillColor(white)
    c.setFont("MSYH-Bold", 14)
    c.drawString(MARGIN + 16, y - 168, "DriveMate Orchestrator")
    text_block(c, "Decomposes the task, coordinates specialist agents, selects tools, separates facts from inference, and asks for confirmation before key actions.", MARGIN + 16, y - 193, 195, size=7.7, leading=12, color=HexColor("#C5D2D7"), max_lines=6)
    agents = [
        ("Trip Planning Agent", "map / traffic / weather"),
        ("Vehicle Status Agent", "battery / tires / maintenance"),
        ("Charging Agent", "range / stations / stop time"),
        ("Schedule Agent", "calendar / departure reminder"),
        ("Emergency Support Agent", "exception explanation / service"),
    ]
    ax, ay, aw, ah = 285, y - 190, 247, 76
    for idx, (name, tools) in enumerate(agents):
        row, col = divmod(idx, 2)
        xi = ax + col * (aw + 10)
        yi = ay - row * (ah + 8)
        if idx == 4:
            xi, yi, aw2 = ax, ay - 2 * (ah + 8), 504
        else:
            aw2 = aw
        card(c, xi, yi, aw2, ah, fill=white)
        c.setFillColor(INK)
        c.setFont("MSYH-Bold", 8.8)
        c.drawString(xi + 12, yi + 45, name)
        c.setFillColor(MUTED)
        c.setFont("MSYH", 7.1)
        c.drawString(xi + 12, yi + 23, tools)
    layer_w = (PAGE_W - 2 * MARGIN - 16) / 3
    layers = [
        ("Multimodal inputs", "voice/text · vehicle status · map/weather · conceptual visual input"),
        ("Agent orchestration", "task split · tool aggregation · fact/inference separation · risk tiering"),
        ("Safe outputs", "explainable plan · timestamps · confirmation · professional service"),
    ]
    for idx, (head, body) in enumerate(layers):
        xi = MARGIN + idx * (layer_w + 8)
        card(c, xi, 32, layer_w, 68, fill=PALE if idx < 2 else WARM)
        c.setFillColor(CYAN); c.setFont("MSYH-Bold", 6.5); c.drawString(xi + 10, 82, f"LAYER {idx + 1}")
        c.setFillColor(INK); c.setFont("MSYH-Bold", 8.5); c.drawString(xi + 10, 65, head)
        text_block(c, body, xi + 10, 49, layer_w - 20, size=6.3, leading=9.2, color=MUTED, max_lines=2)
    c.setFillColor(GOLD); c.setFont("MSYH", 6.2)
    c.drawRightString(PAGE_W - MARGIN, 108, "Static concept: no camera, vehicle sensor, real VLA model, or vehicle-control integration")
    c.setFillColor(BLUE)
    c.setFont("MSYH-Bold", 6.5)
    c.drawString(MARGIN, 108, "English portfolio")
    c.linkURL(SITE_EN_URL, (MARGIN, 104, MARGIN + 78, 116), relative=0)
    footer_en(c, page_no, total, "DriveMate · Concept Proposal" if concept_only else "WEIXIN CHEN · AI Product Manager Portfolio")


def drive_page_two_en(c: canvas.Canvas, page_no: int, total: int, *, concept_only=False) -> None:
    y = title(c, "03 / CONCEPT PROPOSAL · SCENARIOS & ROADMAP", "DriveMate: Scenarios, Safety, and VLA Roadmap", "All vehicle, map, weather, calendar, vision, and charging capabilities are proposed scope - not integrated APIs or models.")
    c.linkURL(f"{SITE_EN_URL}drivemate.html", (MARGIN, PAGE_H - 132, PAGE_W - MARGIN, PAGE_H - 46), relative=0)
    sw = (PAGE_W - 2 * MARGIN - 16) / 3
    scenarios = [
        ("SCENARIO 01", "Heavy Rain & Flooding", "Combine weather, route, and range. Do not assess water depth or instruct driving through water."),
        ("SCENARIO 02", "Family Road Trip", "Work backward from lunch, passenger breaks, and charging alternatives to a departure plan."),
        ("SCENARIO 03", "Abnormal Tire Pressure", "Pause trip planning and prioritize safe inspection and professional service options."),
    ]
    for idx, item in enumerate(scenarios):
        card_text_en(c, MARGIN + idx * (sw + 8), y - 91, sw, 80, *item, fill=white, heading_size=8.6, body_size=6.5, body_lines=3)
    panel_y, panel_h = y - 229, 122
    card(c, MARGIN, panel_y, 365, panel_h, fill=white)
    c.setFillColor(CYAN); c.setFont("MSYH-Bold", 7); c.drawString(MARGIN + 14, panel_y + panel_h - 18, "SAFETY BOUNDARY")
    bullets(c, ["No high-risk vehicle control; confirm key actions", "Separate facts, stale data, and model inference", "Prioritize safe inspection or professional support", "State information gaps instead of inventing facts"], MARGIN + 14, panel_y + panel_h - 39, 335, size=7, leading=10.4)
    card(c, 416, panel_y, 387, panel_h, fill=white)
    c.setFillColor(CYAN); c.setFont("MSYH-Bold", 7); c.drawString(430, panel_y + panel_h - 18, "PLANNED EVALUATION · NOT RESULTS")
    mx, my = 430, panel_y + panel_h - 46
    for metric in ["Task completion", "Tool-call accuracy", "Factual consistency", "Confirmation count", "Response time", "User satisfaction", "High-risk error rate"]:
        mw = pill(c, metric, mx, my, fill=PALE, color=BLUE, h=18)
        mx += mw + 6
        if mx > 746:
            mx = 430
            my -= 25
    c.setFillColor(MUTED); c.setFont("MSYH", 6.4); c.drawString(430, panel_y + 12, "These are proposed concept metrics, not deployed-product results.")

    c.setFillColor(INK); c.setFont("MSYH-Bold", 10); c.drawString(MARGIN, panel_y - 23, "Static low-fidelity interface")
    wx, wy, ww, wh = MARGIN, 115, PAGE_W - 2 * MARGIN, 112
    card(c, wx, wy, ww, wh, fill=PAPER, stroke=INK, radius=12)
    card(c, wx + 10, wy + 10, 185, wh - 20, fill=white)
    c.setFillColor(CYAN); c.setFont("MSYH-Bold", 6.5); c.drawString(wx + 22, wy + wh - 29, "VEHICLE & CONTEXT")
    for idx, line in enumerate(["Battery 68% · sample", "Weather: heavy rain · sample", "Tire pressure: normal · sample"]):
        c.setFillColor(INK); c.setFont("MSYH", 7); c.drawString(wx + 22, wy + wh - 48 - idx * 17, line)
    main_x = wx + 205
    card(c, main_x, wy + 10, ww - 215, wh - 20, fill=white)
    c.setFillColor(INK); c.setFont("MSYH-Bold", 9); c.drawString(main_x + 13, wy + wh - 28, "Heavy Rain & Flooding · Airport Pickup")
    c.setFillColor(MUTED); c.setFont("MSYH", 6.6); c.drawString(main_x + 13, wy + wh - 46, "Leave 25 minutes early · prefer elevated roads · retain 20% range")
    c.setFillColor(GOLD_BG); c.roundRect(main_x + 13, wy + 34, ww - 243, 24, 6, fill=1, stroke=0)
    c.setFillColor(GOLD); c.setFont("MSYH", 6.3); c.drawString(main_x + 23, wy + 43, "High risk: cannot assess water depth; recommend rerouting only.")
    c.setFillColor(INK); c.roundRect(main_x + 13, wy + 10, ww - 243, 18, 5, fill=1, stroke=0)
    c.setFillColor(white); c.setFont("MSYH-Bold", 6.3); c.drawCentredString(main_x + (ww - 217) / 2, wy + 16, "Confirm reminder draft · static demo")

    c.setFillColor(INK); c.setFont("MSYH-Bold", 9); c.drawString(MARGIN, 91, "Physical AI / VLA staged roadmap")
    stages = [
        ("0 CURRENT", "Static concept and synthetic scenarios"),
        ("1 READ-ONLY", "Authorized vehicle data and tool evaluation"),
        ("2 MULTIMODAL", "Offline vision-language risk evaluation"),
        ("3 CONTROLLED", "Closed setting, low risk, human confirmation"),
    ]
    stage_w = (PAGE_W - 2 * MARGIN - 18) / 4
    for idx, (head, body) in enumerate(stages):
        xi = MARGIN + idx * (stage_w + 6)
        card(c, xi, 35, stage_w, 46, fill=PALE if idx else white)
        c.setFillColor(CYAN if idx else MUTED); c.setFont("MSYH-Bold", 6.5); c.drawString(xi + 9, 65, head)
        text_block(c, body, xi + 9, 48, stage_w - 18, size=6.1, leading=8.5, color=INK, max_lines=2)
    footer_en(c, page_no, total, "DriveMate · Concept Proposal" if concept_only else "WEIXIN CHEN · AI Product Manager Portfolio")


def page_method_en(c: canvas.Canvas) -> None:
    y = title(c, "PRODUCT METHOD · CONTACT", "Product Method", "Use a verifiable MVP to shorten the distance between an idea and product evidence.")
    flow(c, ["Discover", "Define scenario", "Scope MVP", "Build demo", "Evaluate", "Analyze bad cases", "Iterate"], MARGIN, y - 53, PAGE_W - 2 * MARGIN, h=36)
    methods = [
        ("01", "Discover the problem", "Identify why users are blocked by the current state."),
        ("02", "Define the scenario", "Specify the user, moment, and constraints."),
        ("03", "Scope the MVP", "Keep the shortest loop and explicit safety boundaries."),
        ("04", "Build the demo", "Turn the critical flow into operable evidence."),
        ("05", "Evaluate", "Test tasks, rules, and outcomes."),
        ("06", "Analyze bad cases", "Classify failures to locate product or system issues."),
        ("07", "Iterate", "Run regression checks before the next cycle."),
    ]
    mw = (PAGE_W - 2 * MARGIN - 18) / 4
    for idx, item in enumerate(methods):
        row, col = divmod(idx, 4)
        x = MARGIN + col * (mw + 6)
        yy = y - 158 - row * 92
        card_text_en(c, x, yy, mw, 82, item[0], item[1], item[2], fill=white, heading_size=8.5, body_size=6.8, body_lines=3)
    card(c, MARGIN, 48, PAGE_W - 2 * MARGIN, 118, fill=INK, stroke=INK)
    c.setFillColor(LIME)
    c.setFont("MSYH-Bold", 7)
    c.drawString(MARGIN + 18, 143, "CONTACT & LINKS")
    c.setFillColor(white)
    c.setFont("MSYH-Bold", 14)
    c.drawString(MARGIN + 18, 117, "Let's turn AI capabilities into useful products")
    c.setFont("MSYH", 8)
    c.setFillColor(HexColor("#C5D2D7"))
    c.drawString(MARGIN + 18, 94, "WEIXIN CHEN · AI Product Manager | Generative AI & AI Innovation")
    links = [
        ("Website", SITE_EN_URL),
        ("GitHub", "https://github.com/lincoln3079938241-coder"),
        ("Auto-LifeOS", "https://auto-lifeos-demo.streamlit.app/"),
        ("Job Radar", "https://shanghai-2027-job-radar-demo.streamlit.app/"),
        ("Email", "mailto:Lincoln3079938241@163.com"),
    ]
    lx = 388
    for label, url in links:
        c.setFillColor(HexColor("#20343E"))
        c.roundRect(lx, 85, 75, 37, 8, fill=1, stroke=0)
        c.setFillColor(white)
        c.setFont("MSYH-Bold", 7)
        c.drawCentredString(lx + 37.5, 99, label)
        c.linkURL(url, (lx, 85, lx + 75, 122), relative=0)
        lx += 81
    c.setFillColor(HexColor("#9FB1B8"))
    c.setFont("MSYH", 6.4)
    c.drawString(388, 67, "Public recruitment email only. No phone number or unnecessary personal data is included.")
    footer_en(c, 7, 7)


def build_portfolio() -> None:
    c = canvas.Canvas(str(PORTFOLIO_PDF), pagesize=(PAGE_W, PAGE_H), pageCompression=1)
    c.setTitle("陈蔚昕 - AI产品经理作品集")
    c.setAuthor("陈蔚昕 / Weixin Chen")
    for fn in [
        page_one,
        page_auto_product,
        page_auto_evaluation,
        page_radar,
        lambda cv: drive_page_one(cv, 5, 7),
        lambda cv: drive_page_two(cv, 6, 7),
        page_method,
    ]:
        fn(c)
        c.showPage()
    c.save()


def build_concept() -> None:
    c = canvas.Canvas(str(CONCEPT_PDF), pagesize=(PAGE_W, PAGE_H), pageCompression=1)
    c.setTitle("DriveMate - Concept Proposal")
    c.setAuthor("陈蔚昕 / Weixin Chen")
    drive_page_one(c, 1, 2, concept_only=True)
    c.showPage()
    drive_page_two(c, 2, 2, concept_only=True)
    c.showPage()
    c.save()


def build_portfolio_en() -> None:
    c = canvas.Canvas(str(PORTFOLIO_EN_PDF), pagesize=(PAGE_W, PAGE_H), pageCompression=1)
    c.setTitle("WEIXIN CHEN - AI Product Manager Portfolio")
    c.setAuthor("WEIXIN CHEN")
    c.setSubject("AI product management portfolio")
    for fn in [
        page_one_en,
        page_auto_product_en,
        page_auto_evaluation_en,
        page_radar_en,
        lambda cv: drive_page_one_en(cv, 5, 7),
        lambda cv: drive_page_two_en(cv, 6, 7),
        page_method_en,
    ]:
        fn(c)
        c.showPage()
    c.save()


def build_concept_en() -> None:
    c = canvas.Canvas(str(CONCEPT_EN_PDF), pagesize=(PAGE_W, PAGE_H), pageCompression=1)
    c.setTitle("DriveMate - Concept Proposal")
    c.setAuthor("WEIXIN CHEN")
    c.setSubject("Automotive AI product concept")
    drive_page_one_en(c, 1, 2, concept_only=True)
    c.showPage()
    drive_page_two_en(c, 2, 2, concept_only=True)
    c.showPage()
    c.save()


if __name__ == "__main__":
    register_fonts()
    ASSETS.mkdir(parents=True, exist_ok=True)
    build_portfolio()
    build_concept()
    build_portfolio_en()
    build_concept_en()
    print(PORTFOLIO_PDF)
    print(CONCEPT_PDF)
    print(PORTFOLIO_EN_PDF)
    print(CONCEPT_EN_PDF)
