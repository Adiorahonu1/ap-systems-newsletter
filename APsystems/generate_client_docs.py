"""
AP Systems, Client Document Generator
Usage: python3 generate_client_docs.py /path/to/intake_config.json

Generates Proposal, Contract, and/or Invoice PDFs driven by the intake config.
Replaces generate_proposal.py and generate_contract_invoice.py.
"""

import sys
import json
import os
import datetime

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether, PageBreak
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus.flowables import Flowable

# ── BRAND COLOURS ──────────────────────────────────────────────────────────────
DARK_BG    = colors.HexColor("#0A0E1A")
NAVY       = colors.HexColor("#0D1B2A")
CYAN       = colors.HexColor("#00C8FF")
CYAN_LIGHT = colors.HexColor("#E6F9FF")
VIOLET     = colors.HexColor("#7B5EA7")
WHITE      = colors.white
GREY_TEXT  = colors.HexColor("#6B7280")
LIGHT_GREY = colors.HexColor("#F3F4F6")
MID_GREY   = colors.HexColor("#D1D5DB")
DARK_TEXT  = colors.HexColor("#111827")
GREEN      = colors.HexColor("#10B981")
GREEN_LIGHT= colors.HexColor("#ECFDF5")
AMBER      = colors.HexColor("#F59E0B")

PAGE_W, PAGE_H = letter

# ── CYCLING NODE COLOURS (for flow diagram) ────────────────────────────────────
NODE_COLORS = [
    colors.HexColor("#1E3A5F"),
    CYAN,
    GREEN,
    colors.HexColor("#5B21B6"),
    colors.HexColor("#7C3AED"),
    colors.HexColor("#0F766E"),
]


# ══════════════════════════════════════════════════════════════════════════════
#  SHARED STYLES
# ══════════════════════════════════════════════════════════════════════════════

def proposal_styles():
    return {
        "cover_company": ParagraphStyle("cover_company",
            fontName="Helvetica-Bold", fontSize=11, textColor=CYAN,
            spaceAfter=4, alignment=TA_CENTER, leading=14),
        "cover_title": ParagraphStyle("cover_title",
            fontName="Helvetica-Bold", fontSize=28, textColor=WHITE,
            spaceAfter=10, alignment=TA_CENTER, leading=34),
        "cover_sub": ParagraphStyle("cover_sub",
            fontName="Helvetica", fontSize=13, textColor=colors.HexColor("#CBD5E1"),
            spaceAfter=6, alignment=TA_CENTER, leading=18),
        "cover_meta": ParagraphStyle("cover_meta",
            fontName="Helvetica", fontSize=10, textColor=colors.HexColor("#94A3B8"),
            spaceAfter=4, alignment=TA_CENTER, leading=14),
        "section_label": ParagraphStyle("section_label",
            fontName="Helvetica-Bold", fontSize=8, textColor=CYAN,
            spaceBefore=18, spaceAfter=4, leading=10,
            wordWrap='LTR'),
        "section_heading": ParagraphStyle("section_heading",
            fontName="Helvetica-Bold", fontSize=18, textColor=DARK_TEXT,
            spaceBefore=2, spaceAfter=10, leading=22),
        "body": ParagraphStyle("body",
            fontName="Helvetica", fontSize=11, textColor=DARK_TEXT,
            spaceAfter=10, leading=18),
        "body_bold": ParagraphStyle("body_bold",
            fontName="Helvetica-Bold", fontSize=11, textColor=DARK_TEXT,
            spaceAfter=8, leading=18),
        "bullet": ParagraphStyle("bullet",
            fontName="Helvetica", fontSize=11, textColor=DARK_TEXT,
            spaceAfter=6, leading=17, leftIndent=18, bulletIndent=0),
        "quote": ParagraphStyle("quote",
            fontName="Helvetica-Oblique", fontSize=11, textColor=DARK_TEXT,
            spaceAfter=6, leading=17, leftIndent=20),
        "table_header": ParagraphStyle("table_header",
            fontName="Helvetica-Bold", fontSize=9.5, textColor=WHITE,
            alignment=TA_LEFT, leading=13),
        "table_cell": ParagraphStyle("table_cell",
            fontName="Helvetica", fontSize=10, textColor=DARK_TEXT,
            leading=15),
        "table_cell_bold": ParagraphStyle("table_cell_bold",
            fontName="Helvetica-Bold", fontSize=10, textColor=DARK_TEXT,
            leading=15),
        "price_big": ParagraphStyle("price_big",
            fontName="Helvetica-Bold", fontSize=32, textColor=CYAN,
            alignment=TA_CENTER, leading=38),
        "price_label": ParagraphStyle("price_label",
            fontName="Helvetica-Bold", fontSize=11, textColor=DARK_TEXT,
            alignment=TA_CENTER, leading=15),
        "price_sub": ParagraphStyle("price_sub",
            fontName="Helvetica", fontSize=9.5, textColor=GREY_TEXT,
            alignment=TA_CENTER, leading=14),
        "footer": ParagraphStyle("footer",
            fontName="Helvetica", fontSize=8, textColor=GREY_TEXT,
            alignment=TA_CENTER, leading=11),
        "cta_heading": ParagraphStyle("cta_heading",
            fontName="Helvetica-Bold", fontSize=20, textColor=WHITE,
            alignment=TA_CENTER, leading=26, spaceAfter=8),
        "cta_body": ParagraphStyle("cta_body",
            fontName="Helvetica", fontSize=10.5, textColor=colors.HexColor("#CBD5E1"),
            alignment=TA_CENTER, leading=16, spaceAfter=6),
    }


def contract_styles():
    return {
        "h1": ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=22,
              textColor=DARK_TEXT, leading=28, spaceAfter=6),
        "h2": ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=14,
              textColor=DARK_TEXT, leading=18, spaceBefore=16, spaceAfter=6),
        "h3": ParagraphStyle("h3", fontName="Helvetica-Bold", fontSize=11,
              textColor=DARK_TEXT, leading=15, spaceBefore=8, spaceAfter=4),
        "body": ParagraphStyle("body", fontName="Helvetica", fontSize=10.5,
               textColor=DARK_TEXT, leading=17, spaceAfter=8, alignment=TA_JUSTIFY),
        "body_left": ParagraphStyle("body_left", fontName="Helvetica", fontSize=10.5,
               textColor=DARK_TEXT, leading=17, spaceAfter=8),
        "bold": ParagraphStyle("bold", fontName="Helvetica-Bold", fontSize=10.5,
               textColor=DARK_TEXT, leading=17, spaceAfter=6),
        "small": ParagraphStyle("small", fontName="Helvetica", fontSize=9,
                textColor=GREY_TEXT, leading=13, spaceAfter=4),
        "label": ParagraphStyle("label", fontName="Helvetica-Bold", fontSize=8,
                textColor=CYAN, leading=11, spaceAfter=2),
        "cell": ParagraphStyle("cell", fontName="Helvetica", fontSize=10,
               textColor=DARK_TEXT, leading=14),
        "cell_bold": ParagraphStyle("cell_bold", fontName="Helvetica-Bold", fontSize=10,
               textColor=DARK_TEXT, leading=14),
        "cell_right": ParagraphStyle("cell_right", fontName="Helvetica", fontSize=10,
               textColor=DARK_TEXT, leading=14, alignment=TA_RIGHT),
        "cell_bold_right": ParagraphStyle("cell_bold_right", fontName="Helvetica-Bold",
               fontSize=10, textColor=DARK_TEXT, leading=14, alignment=TA_RIGHT),
        "header_cell": ParagraphStyle("header_cell", fontName="Helvetica-Bold", fontSize=9,
               textColor=WHITE, leading=12),
        "center": ParagraphStyle("center", fontName="Helvetica", fontSize=10.5,
                 textColor=DARK_TEXT, leading=16, alignment=TA_CENTER),
        "center_bold": ParagraphStyle("center_bold", fontName="Helvetica-Bold", fontSize=10.5,
                 textColor=DARK_TEXT, leading=16, alignment=TA_CENTER),
        "footer": ParagraphStyle("footer", fontName="Helvetica", fontSize=8,
                 textColor=GREY_TEXT, leading=11, alignment=TA_CENTER),
        "sig_label": ParagraphStyle("sig_label", fontName="Helvetica", fontSize=9,
                    textColor=GREY_TEXT, leading=12),
        "sig_name": ParagraphStyle("sig_name", fontName="Helvetica-Bold", fontSize=10.5,
                   textColor=DARK_TEXT, leading=15),
    }


# ══════════════════════════════════════════════════════════════════════════════
#  SHARED PAGE CALLBACKS
# ══════════════════════════════════════════════════════════════════════════════

def make_page_cb(doc_title, cfg):
    """Returns a page callback function for headers/footers on contract/invoice pages."""
    provider_email = cfg["provider_email"]
    provider_phone = cfg["provider_phone"]
    provider_company = cfg["provider_company"]

    def on_page(canvas, doc):
        canvas.saveState()
        # Top bar
        canvas.setFillColor(DARK_BG)
        canvas.rect(0, PAGE_H - 34, PAGE_W, 34, fill=1, stroke=0)
        canvas.setFillColor(CYAN)
        canvas.rect(0, PAGE_H - 3, PAGE_W, 3, fill=1, stroke=0)
        canvas.setFillColor(WHITE)
        canvas.setFont("Helvetica-Bold", 8)
        canvas.drawString(0.65*inch, PAGE_H - 21, provider_company.upper())
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.HexColor("#94A3B8"))
        canvas.drawRightString(PAGE_W - 0.65*inch, PAGE_H - 21,
                               f"{doc_title}  |  Confidential")
        # Bottom
        canvas.setFillColor(LIGHT_GREY)
        canvas.rect(0, 0, PAGE_W, 26, fill=1, stroke=0)
        canvas.setFillColor(CYAN)
        canvas.rect(0, 26, PAGE_W, 1, fill=1, stroke=0)
        canvas.setFont("Helvetica", 7.5)
        canvas.setFillColor(GREY_TEXT)
        canvas.drawString(0.65*inch, 9,
                          f"{provider_company}  \u00b7  {provider_email}  \u00b7  {provider_phone}")
        canvas.drawRightString(PAGE_W - 0.65*inch, 9, f"Page {doc.page}")
        canvas.restoreState()
    return on_page


# ══════════════════════════════════════════════════════════════════════════════
#  PROPOSAL FLOWABLES
# ══════════════════════════════════════════════════════════════════════════════

class ColorBar(Flowable):
    """Full-width horizontal colour bar."""
    def __init__(self, height=4, color=CYAN, width=None):
        Flowable.__init__(self)
        self.bar_height = height
        self.bar_color  = color
        self._width     = width

    def wrap(self, availW, availH):
        self.avail_w = availW
        return (self._width or availW, self.bar_height)

    def draw(self):
        self.canv.setFillColor(self.bar_color)
        self.canv.rect(0, 0, self._width or self.avail_w, self.bar_height, fill=1, stroke=0)


class CoverPage(Flowable):
    """Full dark cover page drawn on canvas, driven by config."""
    def __init__(self, width, height, cfg):
        Flowable.__init__(self)
        self.pg_w = width
        self.pg_h = height
        self.cfg  = cfg

    def wrap(self, *args):
        return (self.pg_w, self.pg_h)

    def draw(self):
        c = self.canv
        w, h = self.pg_w, self.pg_h
        cfg = self.cfg

        # Background
        c.setFillColor(DARK_BG)
        c.rect(0, 0, w, h, fill=1, stroke=0)

        # Accent bar top
        c.setFillColor(CYAN)
        c.rect(0, h - 5, w, 5, fill=1, stroke=0)

        # Left violet accent strip
        c.setFillColor(VIOLET)
        c.rect(0, 0, 6, h - 5, fill=1, stroke=0)

        # Subtle grid lines
        c.setStrokeColor(colors.HexColor("#1E293B"))
        c.setLineWidth(0.5)
        for y in range(0, int(h), 60):
            c.line(0, y, w, y)

        # Company name
        c.setFillColor(CYAN)
        c.setFont("Helvetica-Bold", 11)
        c.drawCentredString(w / 2, h - 80, cfg["provider_company"].upper())

        # Divider under company name
        c.setStrokeColor(CYAN)
        c.setLineWidth(1)
        c.line(w/2 - 60, h - 90, w/2 + 60, h - 90)

        # Main title
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 30)
        c.drawCentredString(w / 2, h - 150, "Automation Proposal")

        c.setFont("Helvetica-Bold", 22)
        c.setFillColor(colors.HexColor("#CBD5E1"))
        c.drawCentredString(w / 2, h - 182, cfg["client_company"])

        # Tagline
        c.setFillColor(colors.HexColor("#94A3B8"))
        c.setFont("Helvetica-Oblique", 12)
        tagline = cfg.get("tagline", "")
        c.drawCentredString(w / 2, h - 215, tagline)

        # Central accent box
        box_y = h - 360
        c.setFillColor(colors.HexColor("#0F172A"))
        c.roundRect(80, box_y, w - 160, 110, 8, fill=1, stroke=0)
        c.setStrokeColor(CYAN)
        c.setLineWidth(0.8)
        c.roundRect(80, box_y, w - 160, 110, 8, fill=0, stroke=1)

        c.setFillColor(CYAN)
        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(w / 2, box_y + 82, "THE CORE PROBLEM WE'RE SOLVING")

        c.setFillColor(WHITE)
        c.setFont("Helvetica", 10)
        pain_points = cfg.get("pain_points", [])
        lines = pain_points[:4]
        for i, line in enumerate(lines):
            c.drawCentredString(w / 2, box_y + 60 - i * 14, line)

        # Flow diagram
        flow_y = h - 440
        nodes = cfg.get("flow_nodes", [])
        node_colors_cycle = [NODE_COLORS[i % len(NODE_COLORS)] for i in range(len(nodes))]
        node_w, node_h, gap = 100, 32, 18
        total_w = len(nodes) * node_w + (len(nodes) - 1) * gap
        start_x = (w - total_w) / 2

        for i, (label, col) in enumerate(zip(nodes, node_colors_cycle)):
            nx = start_x + i * (node_w + gap)
            c.setFillColor(col)
            c.roundRect(nx, flow_y, node_w, node_h, 5, fill=1, stroke=0)
            c.setFillColor(WHITE)
            c.setFont("Helvetica-Bold", 7.5)
            c.drawCentredString(nx + node_w / 2, flow_y + 11, label)
            if i < len(nodes) - 1:
                arrow_x = nx + node_w + 2
                c.setStrokeColor(CYAN)
                c.setLineWidth(1.2)
                c.line(arrow_x, flow_y + node_h / 2, arrow_x + gap - 4, flow_y + node_h / 2)
                # arrowhead
                c.setFillColor(CYAN)
                p = c.beginPath()
                p.moveTo(arrow_x + gap - 4, flow_y + node_h/2 + 4)
                p.lineTo(arrow_x + gap - 4, flow_y + node_h/2 - 4)
                p.lineTo(arrow_x + gap + 2, flow_y + node_h/2)
                p.close()
                c.drawPath(p, fill=1, stroke=0)

        # Meta info
        meta_y = 130
        c.setStrokeColor(colors.HexColor("#1E293B"))
        c.setLineWidth(0.5)
        c.line(80, meta_y + 55, w - 80, meta_y + 55)

        today = datetime.date.today().strftime("%B %d, %Y")
        meta = [
            ("Prepared for:", f"{cfg['client_contacts']}, {cfg['client_company']}"),
            ("Prepared by:",  f"{cfg['provider_name']}, {cfg['provider_company']}"),
            ("Date:",         today),
            ("Valid for:",    "30 Days from Date of Issue"),
        ]
        for i, (lbl, value) in enumerate(meta):
            row_y = meta_y + 35 - i * 16
            c.setFillColor(GREY_TEXT)
            c.setFont("Helvetica", 8)
            c.drawString(100, row_y, lbl)
            c.setFillColor(WHITE)
            c.setFont("Helvetica-Bold", 8)
            c.drawString(230, row_y, value)

        # Bottom bar
        c.setFillColor(CYAN)
        c.rect(0, 0, w, 4, fill=1, stroke=0)

        c.setFillColor(colors.HexColor("#94A3B8"))
        c.setFont("Helvetica", 7.5)
        c.drawCentredString(w / 2, 12,
                            f"Confidential, Prepared exclusively for {cfg['client_company']}")


class CTABox(Flowable):
    """Dark CTA banner."""
    def __init__(self, width, texts):
        Flowable.__init__(self)
        self.box_w  = width
        self.texts  = texts

    def wrap(self, *args):
        return (self.box_w, 140)

    def draw(self):
        c = self.canv
        c.setFillColor(NAVY)
        c.roundRect(0, 0, self.box_w, 130, 8, fill=1, stroke=0)
        c.setStrokeColor(CYAN)
        c.setLineWidth(1)
        c.roundRect(0, 0, self.box_w, 130, 8, fill=0, stroke=1)
        # Left accent
        c.setFillColor(CYAN)
        c.roundRect(0, 0, 5, 130, 8, fill=1, stroke=0)

        y = 100
        for style, text in self.texts:
            if style == "heading":
                c.setFont("Helvetica-Bold", 15)
                c.setFillColor(WHITE)
            elif style == "body":
                c.setFont("Helvetica", 9.5)
                c.setFillColor(colors.HexColor("#CBD5E1"))
            elif style == "cta":
                c.setFont("Helvetica-Bold", 10)
                c.setFillColor(CYAN)
            c.drawString(24, y, text)
            y -= 18


# ── CONTRACT FLOWABLES ─────────────────────────────────────────────────────────

class InputField(Flowable):
    """Clickable text input field the client can type into."""
    def __init__(self, name, tooltip="", width=2.9*inch, height=22, value=""):
        Flowable.__init__(self)
        self.field_name  = name
        self.tooltip     = tooltip
        self.field_width = width
        self.field_height= height
        self.value       = value

    def wrap(self, availW, availH):
        return (self.field_width, self.field_height)

    def draw(self):
        self.canv.acroForm.textfield(
            name        = self.field_name,
            tooltip     = self.tooltip,
            x=0, y=0,
            width       = self.field_width,
            height      = self.field_height,
            value       = self.value,
            fillColor   = colors.HexColor("#F0F9FF"),
            borderColor = CYAN,
            borderWidth = 1,
            fontSize    = 11,
            textColor   = colors.black,
            forceBorder = True,
        )


class PrefilledField(Flowable):
    """Read-only styled box showing pre-filled text (provider side)."""
    def __init__(self, text, width=2.9*inch, height=22):
        Flowable.__init__(self)
        self.text        = text
        self.field_width = width
        self.field_height= height

    def wrap(self, availW, availH):
        return (self.field_width, self.field_height)

    def draw(self):
        c = self.canv
        c.setFillColor(colors.HexColor("#F3F4F6"))
        c.setStrokeColor(MID_GREY)
        c.setLineWidth(0.8)
        c.rect(0, 0, self.field_width, self.field_height, fill=1, stroke=1)
        c.setFillColor(DARK_TEXT)
        c.setFont("Helvetica", 10.5)
        c.drawString(6, 6, self.text)


class SigBox(Flowable):
    """Visual signature area box with label."""
    def __init__(self, label, width=2.9*inch, height=52, interactive=False):
        Flowable.__init__(self)
        self.label        = label
        self.field_width  = width
        self.field_height = height
        self.interactive  = interactive

    def wrap(self, availW, availH):
        return (self.field_width, self.field_height)

    def draw(self):
        c = self.canv
        c.setFillColor(colors.HexColor("#FAFAFA"))
        c.setStrokeColor(MID_GREY)
        c.setLineWidth(0.8)
        c.setDash(3, 3)
        c.rect(0, 0, self.field_width, self.field_height, fill=1, stroke=1)
        c.setDash()
        c.setFillColor(GREY_TEXT)
        c.setFont("Helvetica-Oblique", 8)
        c.drawCentredString(self.field_width / 2, self.field_height / 2 - 4,
                            "Sign here (print, sign and scan / or use Adobe Reader)")


# ══════════════════════════════════════════════════════════════════════════════
#  PROPOSAL SECTION BUILDER
# ══════════════════════════════════════════════════════════════════════════════

def proposal_section(s, label, heading, content_fn):
    """Returns list of flowables for one proposal section."""
    items = []
    items.append(Paragraph(label.upper(), s["section_label"]))
    items.append(Paragraph(heading, s["section_heading"]))
    items.append(ColorBar(height=2, color=CYAN, width=40))
    items.append(Spacer(1, 10))
    items.extend(content_fn(s))
    items.append(Spacer(1, 14))
    items.append(HRFlowable(width="100%", thickness=0.5, color=MID_GREY))
    return items


# ══════════════════════════════════════════════════════════════════════════════
#  PROPOSAL CONTENT SECTIONS
# ══════════════════════════════════════════════════════════════════════════════

def proposal_intro_content(s, cfg):
    today = datetime.date.today().strftime("%B %d, %Y")
    return [
        Paragraph(f"Date: {today}", s["body"]),
        Paragraph(f"To: {cfg['client_contacts']}, {cfg['client_company']}", s["body"]),
        Spacer(1, 6),
        Paragraph(
            "Thank you for taking the time to speak with us. What you shared about your daily workflow "
            "was clear, and we believe the solution we are proposing will directly eliminate the bottleneck "
            "your team faces every morning before the workday even begins.",
            s["body"]),
        Paragraph(
            "This proposal outlines a custom automation system designed specifically around your existing "
            "tools and processes, no disruption, no new platforms to learn, no monthly obligations unless "
            "you choose them. Just a system that quietly works in the background so your team doesn't have to.",
            s["body"]),
    ]


def proposal_problem_content(s, cfg):
    items = []
    problem_summary = cfg.get("problem_summary", "")
    items.append(Paragraph(problem_summary, s["body"]))
    items.append(Spacer(1, 6))

    pain_points = cfg.get("pain_points", [])
    pain_data = [
        [Paragraph("The Hidden Cost of Manual Entry", s["table_header"])],
    ]
    for pt in pain_points:
        pain_data.append([Paragraph(pt, s["table_cell"])])

    pain_table = Table(pain_data, colWidths=[5.5 * inch])
    row_bgs = [("BACKGROUND", (0, 0), (-1, 0), NAVY)]
    for idx in range(1, len(pain_data)):
        bg = LIGHT_GREY if idx % 2 == 0 else colors.HexColor("#FEF3C7")
        row_bgs.append(("BACKGROUND", (0, idx), (-1, idx), bg))
    pain_table.setStyle(TableStyle(row_bgs + [
        ("TOPPADDING",    (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING",   (0, 0), (-1, -1), 12),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 12),
    ]))
    items.append(pain_table)
    return items


def proposal_solution_content(s, cfg):
    items = []
    solution_summary = cfg.get("solution_summary", "")
    tools = cfg.get("tools_mentioned", [])
    tools_str = ", ".join(f"<b>{t}</b>" for t in tools) if tools else ""
    items.append(Paragraph(solution_summary, s["body"]))

    contrast_rows = cfg.get("contrast_rows", [])
    contrast_data = [
        [Paragraph("TODAY", s["table_header"]), Paragraph("AFTER " + cfg["provider_company"].upper(), s["table_header"])],
    ]
    for row in contrast_rows:
        contrast_data.append([
            Paragraph(row.get("before", ""), s["table_cell"]),
            Paragraph(row.get("after", ""),  s["table_cell"]),
        ])

    contrast_table = Table(contrast_data, colWidths=[2.75 * inch, 2.75 * inch])
    contrast_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), colors.HexColor("#7F1D1D")),
        ("BACKGROUND", (1, 0), (1, 0), colors.HexColor("#064E3B")),
        ("BACKGROUND", (0, 1), (0, -1), colors.HexColor("#FFF1F2")),
        ("BACKGROUND", (1, 1), (1, -1), colors.HexColor("#ECFDF5")),
        ("TOPPADDING",  (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("GRID", (0, 0), (-1, -1), 0.5, MID_GREY),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    items.append(contrast_table)
    items.append(Spacer(1, 10))

    items.append(Paragraph("<b>How the system works, in plain terms:</b>", s["body_bold"]))
    how_it_works = cfg.get("how_it_works", [])
    for i, b in enumerate(how_it_works, 1):
        items.append(Paragraph(f"<b>{i}.</b>  {b}", s["bullet"]))
    return items


def proposal_timeline_content(s, cfg):
    items = []
    items.append(Paragraph(
        "We run every implementation in focused phases. You will know exactly where things stand "
        "at every stage, no ambiguity, no delays.",
        s["body"]))

    timeline_phases = cfg.get("timeline_phases", [])
    phase_colors = [
        colors.HexColor("#0C2340"),
        colors.HexColor("#0A2E1F"),
        colors.HexColor("#1A0A2E"),
        colors.HexColor("#1A1A0A"),
        colors.HexColor("#0A1A2E"),
    ]

    for idx, phase in enumerate(timeline_phases):
        phase_label = f"Phase {idx + 1}"
        phase_name  = phase.get("name", "")
        phase_time  = phase.get("duration", "")
        phase_desc  = phase.get("description", "")

        data = [[
            Paragraph(f"<b>{phase_label}</b>", s["table_header"]),
            Paragraph(f"<b>{phase_name}</b>", s["table_header"]),
            Paragraph(phase_time, s["table_header"]),
        ],[
            Paragraph("", s["table_cell"]),
            Paragraph(phase_desc, s["table_cell"]),
            Paragraph("", s["table_cell"]),
        ]]
        t = Table(data, colWidths=[0.85*inch, 3.9*inch, 0.75*inch])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), NAVY),
            ("BACKGROUND", (0, 1), (-1, 1), LIGHT_GREY),
            ("SPAN", (1, 1), (2, 1)),
            ("TOPPADDING",  (0, 0), (-1, -1), 7),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ("LEFTPADDING", (0, 0), (-1, -1), 10),
            ("RIGHTPADDING", (0, 0), (-1, -1), 10),
            ("GRID", (0, 0), (-1, -1), 0.5, MID_GREY),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ]))
        items.append(t)
        items.append(Spacer(1, 8))
    return items


def proposal_investment_content(s, cfg):
    items = []
    total_price    = cfg.get("total_price", 0)
    deposit_amount = cfg.get("deposit_amount", 0)
    final_amount   = cfg.get("final_payment_amount", 0)


    price_label_text = f"ONE-TIME PROJECT FEE"
    price_big_text   = f"${total_price:,.0f}"
    what_included    = cfg.get("what_is_included", [])
    included_summary = " \u00b7 ".join(what_included[:3]) if what_included else ""

    price_data = [
        [Paragraph(price_label_text, s["price_label"])],
        [Paragraph(price_big_text, s["price_big"])],
        [Paragraph(included_summary, s["price_sub"])],
    ]
    price_table = Table(price_data, colWidths=[5.5 * inch])
    price_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), CYAN_LIGHT),
        ("TOPPADDING",  (0, 0), (-1, -1), 14),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
        ("LEFTPADDING", (0, 0), (-1, -1), 20),
        ("RIGHTPADDING", (0, 0), (-1, -1), 20),
        ("LINEBELOW", (0, 0), (-1, 0), 1, CYAN),
        ("BOX", (0, 0), (-1, -1), 1.5, CYAN),
        ("ROUNDEDCORNERS", [8]),
    ]))
    items.append(price_table)
    items.append(Spacer(1, 14))

    items.append(Paragraph(f"<b>What is included in the ${total_price:,.0f}:</b>", s["body_bold"]))
    for item in what_included:
        items.append(Paragraph(f"\u2713  {item}", s["bullet"]))

    tool_costs = cfg.get("tool_costs", [])
    if tool_costs:
        items.append(Spacer(1, 10))
        items.append(Paragraph(
            "<b>Tool Costs (Provided by Client):</b>",
            s["body_bold"]))
        items.append(Paragraph(
            "All tool and platform costs are covered directly by the client. "
            "AP Systems handles the setup, configuration, and integration. "
            "The estimates below are provided so you can plan accordingly before the project begins.",
            s["body"]))
        items.append(Spacer(1, 6))
        tool_cost_header = [
            Paragraph("Tool", s["table_header"]),
            Paragraph("Purpose", s["table_header"]),
            Paragraph("Est. Cost", s["table_header"]),
        ]
        tool_cost_rows = [tool_cost_header]
        for i, row in enumerate(tool_costs):
            bg = LIGHT_GREY if i % 2 == 0 else colors.white
            tool_cost_rows.append([
                Paragraph(row.get("tool", ""), s["table_cell_bold"]),
                Paragraph(row.get("purpose", ""), s["table_cell"]),
                Paragraph(row.get("cost", ""), s["table_cell_bold"]),
            ])
        tool_cost_table = Table(tool_cost_rows, colWidths=[1.5*inch, 2.8*inch, 1.2*inch])
        style_cmds = [
            ("BACKGROUND", (0, 0), (-1, 0), NAVY),
            ("TOPPADDING",  (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#2A3A5A")),
        ]
        for i in range(1, len(tool_cost_rows)):
            bg = LIGHT_GREY if i % 2 == 1 else colors.white
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), bg))
        tool_cost_table.setStyle(TableStyle(style_cmds))
        items.append(tool_cost_table)

    items.append(Spacer(1, 10))
    items.append(Paragraph("<b>Ongoing Support (Optional, Never Mandatory):</b>", s["body_bold"]))
    items.append(Paragraph(
        "After the 30-day post-launch period, ongoing maintenance and updates are available on an "
        "<b>as-needed basis</b>. You pay only when you need something changed. There is no mandatory "
        "monthly retainer. If the system runs without issue, which it is designed to, your cost "
        "after the initial build is zero.",
        s["body"]))

    items.append(Spacer(1, 10))
    payment_data = [
        [Paragraph("Payment Schedule", s["table_header"]),
         Paragraph("Amount", s["table_header"]),
         Paragraph("Timing", s["table_header"])],
        [Paragraph("Deposit, Discovery & Build Start", s["table_cell"]),
         Paragraph(f"${deposit_amount:,.0f}", s["table_cell_bold"]),
         Paragraph("Upon agreement", s["table_cell"])],
        [Paragraph("Final Payment, Go-Live Sign-Off", s["table_cell"]),
         Paragraph(f"${final_amount:,.0f}", s["table_cell_bold"]),
         Paragraph("Upon successful deployment", s["table_cell"])],
    ]
    payment_table = Table(payment_data, colWidths=[2.8*inch, 1.2*inch, 1.5*inch])
    payment_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("BACKGROUND", (0, 1), (-1, 1), LIGHT_GREY),
        ("BACKGROUND", (0, 2), (-1, 2), colors.HexColor("#F0FDF4")),
        ("TOPPADDING",  (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("GRID", (0, 0), (-1, -1), 0.5, MID_GREY),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    items.append(payment_table)
    return items


def proposal_security_content(s, cfg):
    items = []
    items.append(Paragraph(
        "You asked the right questions about data security, and we take this seriously.",
        s["body_bold"]))

    security_points = [
        ("No Data Storage",
         "Our automation system acts purely as a pipe. Data passes through the automation layer "
         "in transit and is never stored, cached, or logged by our system. "
         "It moves from your lead sources to your CRM and nowhere else."),
        ("Encrypted in Transit",
         "All data transferred through the automation layer is encrypted using HTTPS/TLS, the same standard "
         "used by banks and financial platforms. Data is never transmitted over unencrypted channels."),
        ("API Key Security",
         "All integrations use secure, revocable API keys issued by your platforms. "
         "You retain full control, you can revoke access at any time without contacting us."),
        ("Vendor-Level Compliance",
         "Because the data lives in your CRM systems, not ours, their existing "
         "compliance frameworks continue to govern the data at rest."),
        ("Liability Coverage",
         "We are happy to provide documentation on our liability position and discuss any specific "
         "coverage requirements your business has before signing. This can be addressed directly."),
    ]

    for title, desc in security_points:
        data = [[Paragraph(f"<b>{title}</b>", s["table_cell_bold"])],
                [Paragraph(desc, s["table_cell"])]]
        t = Table(data, colWidths=[5.5 * inch])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#EFF6FF")),
            ("BACKGROUND", (0, 1), (-1, 1), LIGHT_GREY),
            ("TOPPADDING",  (0, 0), (-1, -1), 7),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ("LEFTPADDING", (0, 0), (-1, -1), 12),
            ("RIGHTPADDING", (0, 0), (-1, -1), 12),
            ("LINEAFTER", (0, 0), (0, -1), 2, CYAN),
            ("BOX", (0, 0), (-1, -1), 0.5, MID_GREY),
        ]))
        items.append(t)
        items.append(Spacer(1, 6))
    return items


def proposal_why_us_content(s, cfg):
    items = []
    differentiators = [
        ("Built Around Your Stack",
         "We are not asking you to change your existing platforms or tools. "
         "This system wraps around what you already use."),
        ("No Black-Box AI",
         "This is not an agentic AI system making decisions with your data. "
         "It is a deterministic automation, every action is defined, predictable, and auditable."),
        ("Outcome-Focused, Not Feature-Focused",
         f"We are not selling you a platform. We are solving a specific problem for {cfg['client_company']}: "
         "the manual work that costs your team time every single day."),
        ("No Subscription Pressure",
         "You raised this concern directly. Our model respects it. You pay once, you own the outcome. "
         "Support is available when you need it, not billed whether you use it or not."),
        ("Transparent Process",
         f"{cfg.get('timeline_weeks', 4)} weeks. {len(cfg.get('timeline_phases', []))} phases. "
         "You will know what is happening at every stage before we move forward."),
    ]
    for title, desc in differentiators:
        items.append(Paragraph(f"<b>{title}</b>", s["body_bold"]))
        items.append(Paragraph(desc, s["body"]))
        items.append(Spacer(1, 2))
    return items


def proposal_next_steps_content(s, cfg):
    items = []
    items.append(Paragraph(
        "You mentioned you want to research before responding, that is completely fair, "
        "and we encourage it. When you are ready, the path forward is simple and low-risk.",
        s["body"]))
    items.append(Spacer(1, 8))

    deposit_amount = cfg.get("deposit_amount", 0)
    client_contacts = cfg.get("client_contacts", "your team")
    provider_name   = cfg.get("provider_name", "")
    client_company  = cfg.get("client_company", "")

    steps = [
        (
            "Step 1, Reply to Confirm Interest",
            "ACTION: Reply to this email or contact us directly.",
            f"Let us know you want to move forward. No commitment yet, just a confirmation "
            f"that the terms in this proposal work for {client_company}.",
        ),
        (
            "Step 2, Sign the Project Agreement",
            "ACTION: Review and sign the project agreement.",
            "We will send a short agreement covering the scope, timeline, and payment terms outlined "
            "in this proposal. No surprises, it reflects exactly what is written here.",
        ),
        (
            f"Step 3, Submit the ${deposit_amount:,.0f} Deposit",
            "ACTION: Submit the first payment to begin the Discovery phase.",
            f"Once the deposit is received, we will schedule the Discovery session with {client_contacts} within "
            f"48 hours. The final payment is only due when the system is live and approved by your team.",
        ),
        (
            f"Step 4, Discovery Session with {client_contacts}",
            "ACTION: Join a working session with the AP Systems team.",
            "We will map every lead form field to the exact CRM fields, confirm API access, "
            "and document any conditional routing logic. This is the only significant time commitment "
            "required from your team during the entire build.",
        ),
        (
            "Step 5, We Build, Test, and Go Live",
            "ACTION: Review and approve the system during controlled testing.",
            "You will receive a walkthrough at the end of the build phase before we touch your "
            "live environment. Once you approve, the system goes into production. "
            "From that point forward, no manual imports, no morning data entry.",
        ),
    ]

    step_bg = [colors.HexColor("#F0F9FF"), LIGHT_GREY]
    for i, (title, action, desc) in enumerate(steps):
        action_style = ParagraphStyle("action",
            fontName="Helvetica-Bold", fontSize=9, textColor=GREEN,
            leading=13, spaceAfter=3)
        num_style = ParagraphStyle("num2", fontName="Helvetica-Bold", fontSize=16,
                   textColor=WHITE, alignment=TA_CENTER, leading=20)
        data = [[
            Paragraph(str(i + 1), num_style),
            [Paragraph(title, s["body_bold"]),
             Paragraph(action, action_style),
             Paragraph(desc, s["table_cell"])],
        ]]
        t = Table(data, colWidths=[0.45*inch, 5.05*inch])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (0, 0), CYAN if i == 0 else NAVY),
            ("BACKGROUND", (1, 0), (1, 0), step_bg[i % 2]),
            ("TOPPADDING",  (0, 0), (-1, -1), 10),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ("LEFTPADDING", (0, 0), (-1, -1), 10),
            ("RIGHTPADDING", (0, 0), (-1, -1), 10),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("BOX", (0, 0), (-1, -1), 0.5, MID_GREY),
        ]))
        items.append(t)
        items.append(Spacer(1, 6))

    items.append(Spacer(1, 6))
    timeline_weeks = cfg.get("timeline_weeks", 4)
    items.append(Paragraph(
        f"That is it. Five steps. {timeline_weeks} weeks. And your team never manually enters lead data again.",
        ParagraphStyle("close_line", fontName="Helvetica-Bold", fontSize=11,
                       textColor=DARK_TEXT, leading=16, alignment=TA_CENTER)
    ))
    return items


# ── PROPOSAL PAGE CALLBACKS ────────────────────────────────────────────────────

def make_proposal_on_page(cfg):
    """Returns the header/footer callback for proposal body pages."""
    provider_email   = cfg["provider_email"]
    provider_phone   = cfg["provider_phone"]
    provider_company = cfg["provider_company"]
    client_company   = cfg["client_company"]

    def on_page(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(DARK_BG)
        canvas.rect(0, PAGE_H - 36, PAGE_W, 36, fill=1, stroke=0)
        canvas.setFillColor(CYAN)
        canvas.rect(0, PAGE_H - 3, PAGE_W, 3, fill=1, stroke=0)
        canvas.setFillColor(WHITE)
        canvas.setFont("Helvetica-Bold", 8)
        canvas.drawString(0.65 * inch, PAGE_H - 22, provider_company.upper())
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.HexColor("#94A3B8"))
        canvas.drawRightString(PAGE_W - 0.65 * inch, PAGE_H - 22,
                               f"Automation Proposal, {client_company}  |  Confidential")
        canvas.setFillColor(LIGHT_GREY)
        canvas.rect(0, 0, PAGE_W, 28, fill=1, stroke=0)
        canvas.setFillColor(CYAN)
        canvas.rect(0, 28, PAGE_W, 1, fill=1, stroke=0)
        canvas.setFont("Helvetica", 7.5)
        canvas.setFillColor(GREY_TEXT)
        canvas.drawString(0.65 * inch, 10,
                          f"{provider_company}  \u00b7  {provider_email}  \u00b7  {provider_phone}")
        canvas.drawRightString(PAGE_W - 0.65 * inch, 10, f"Page {doc.page}")
        canvas.restoreState()
    return on_page


def make_proposal_draw_cover(cfg):
    """Returns the first-page callback that draws the cover."""
    def draw_cover(canvas, doc):
        cp = CoverPage(PAGE_W, PAGE_H, cfg)
        cp.canv = canvas
        canvas.saveState()
        cp.draw()
        canvas.restoreState()
    return draw_cover


# ══════════════════════════════════════════════════════════════════════════════
#  BUILD PROPOSAL
# ══════════════════════════════════════════════════════════════════════════════

def build_proposal(cfg):
    sanitized  = cfg["client_name_sanitized"]
    output_dir = cfg["output_dir"]
    output_path = os.path.join(output_dir, f"AP_Systems_Proposal_{sanitized}.pdf")

    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=0.65 * inch,
        rightMargin=0.65 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.55 * inch,
    )

    s = proposal_styles()
    story = []

    # Reserve page 1 for cover (drawn in onFirstPage callback)
    story.append(PageBreak())

    # Helper that curries cfg into each content function
    def make_content(fn):
        def wrapped(style):
            return fn(style, cfg)
        return wrapped

    body_sections = [
        ("Letter of Introduction",   "A Personal Note Before We Begin",
         make_content(proposal_intro_content)),
        ("The Challenge",            "What Is Costing Your Team Time Every Day",
         make_content(proposal_problem_content)),
        ("The Solution",             "A Clean Automation Pipeline Built For Your Workflow",
         make_content(proposal_solution_content)),
        ("Implementation Timeline",  "What Happens, Week by Week",
         make_content(proposal_timeline_content)),
        ("Your Investment",          "Transparent, Fair, and Commitment-Free",
         make_content(proposal_investment_content)),
        ("Data Security",            "How We Protect Your Clients' Information",
         make_content(proposal_security_content)),
        ("Why " + cfg["provider_company"], "What Makes This Different",
         make_content(proposal_why_us_content)),
        ("Next Steps",               "How We Get Started, When You Are Ready",
         make_content(proposal_next_steps_content)),
    ]

    for label, heading, fn in body_sections:
        story.extend(proposal_section(s, label, heading, fn))
        story.append(Spacer(1, 10))

    # Closing CTA
    story.append(Spacer(1, 10))
    story.append(CTABox(
        PAGE_W - 1.3 * inch,
        [
            ("heading", f"Let's get {cfg['client_company']} running on autopilot."),
            ("body",    "Reply to this proposal, or contact us directly to confirm your interest."),
            ("body",    "Discovery can begin within 48 hours of your deposit."),
            ("cta",     f"{cfg['provider_name']}  |  {cfg['provider_company']}  |  "
                        f"{cfg['provider_email']}  |  {cfg['provider_phone']}"),
        ]
    ))

    story.append(Spacer(1, 20))
    story.append(Paragraph(
        "This proposal is valid for 30 days from the date of issue. "
        "All terms are subject to a signed project agreement.",
        s["footer"]))

    doc.build(story,
              onFirstPage=make_proposal_draw_cover(cfg),
              onLaterPages=make_proposal_on_page(cfg))
    print(f"Proposal saved to:\n   {output_path}")


# ══════════════════════════════════════════════════════════════════════════════
#  BUILD CONTRACT
# ══════════════════════════════════════════════════════════════════════════════

def build_contract(cfg):
    sanitized   = cfg["client_name_sanitized"]
    output_dir  = cfg["output_dir"]
    output_path = os.path.join(output_dir, f"AP_Systems_Contract_{sanitized}.pdf")

    today     = datetime.date.today()
    today_str = today.strftime("%B %d, %Y")

    s = contract_styles()
    doc = SimpleDocTemplate(
        output_path, pagesize=letter,
        leftMargin=0.8*inch, rightMargin=0.8*inch,
        topMargin=0.7*inch, bottomMargin=0.55*inch,
    )
    story = []

    provider_company = cfg["provider_company"]
    provider_name    = cfg["provider_name"]
    provider_email   = cfg["provider_email"]
    provider_phone   = cfg["provider_phone"]
    provider_address = cfg["provider_address"]

    client_company  = cfg["client_company"]
    client_contacts = cfg["client_contacts"]
    client_email    = cfg["client_email"]
    client_website  = cfg.get("client_website", "")

    total_price    = cfg.get("total_price", 0)
    deposit_amount = cfg.get("deposit_amount", 0)
    final_amount   = cfg.get("final_payment_amount", 0)
    timeline_weeks = cfg.get("timeline_weeks", 4)

    # ── Cover header ──────────────────────────────────────────────────────────
    header_data = [[
        Paragraph(provider_company.upper(), ParagraphStyle("co",
            fontName="Helvetica-Bold", fontSize=18, textColor=WHITE, leading=22)),
        Paragraph("SERVICE AGREEMENT", ParagraphStyle("title",
            fontName="Helvetica-Bold", fontSize=18, textColor=WHITE,
            leading=22, alignment=TA_RIGHT)),
    ]]
    header_tbl = Table(header_data, colWidths=[3*inch, 3.8*inch])
    header_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), DARK_BG),
        ("TOPPADDING",  (0,0), (-1,-1), 16),
        ("BOTTOMPADDING",(0,0),(-1,-1), 16),
        ("LEFTPADDING", (0,0), (-1,-1), 16),
        ("RIGHTPADDING",(0,0),(-1,-1), 16),
        ("LINEBELOW",   (0,0), (-1,-1), 3, CYAN),
        ("VALIGN",      (0,0), (-1,-1), "MIDDLE"),
    ]))
    story.append(header_tbl)
    story.append(Spacer(1, 18))

    # ── Parties block ─────────────────────────────────────────────────────────
    def party_cell(role, company, name, email, extra=""):
        lines = [
            Paragraph(role.upper(), s["label"]),
            Paragraph(f"<b>{company}</b>", s["bold"]),
            Paragraph(name, s["cell"]),
            Paragraph(email, s["cell"]),
        ]
        if extra:
            lines.append(Paragraph(extra, s["cell"]))
        return lines

    parties_data = [[
        party_cell("Service Provider", provider_company, provider_name,
                   provider_email, provider_phone),
        party_cell("Client", client_company, client_contacts,
                   client_email, client_website),
    ]]
    parties_tbl = Table(parties_data, colWidths=[3.3*inch, 3.3*inch])
    parties_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (0,0), colors.HexColor("#EFF6FF")),
        ("BACKGROUND", (1,0), (1,0), colors.HexColor("#F0FDF4")),
        ("TOPPADDING",  (0,0), (-1,-1), 12),
        ("BOTTOMPADDING",(0,0),(-1,-1), 12),
        ("LEFTPADDING", (0,0), (-1,-1), 14),
        ("RIGHTPADDING",(0,0),(-1,-1), 14),
        ("BOX",         (0,0), (0,0), 1, CYAN),
        ("BOX",         (1,0), (1,0), 1, GREEN),
        ("VALIGN",      (0,0), (-1,-1), "TOP"),
    ]))
    story.append(parties_tbl)
    story.append(Spacer(1, 8))
    story.append(Paragraph(f"Effective Date: <b>{today_str}</b>", s["small"]))
    story.append(HRFlowable(width="100%", thickness=0.5, color=MID_GREY))
    story.append(Spacer(1, 6))

    # ── Section helper ────────────────────────────────────────────────────────
    def contract_section(number, title, paragraphs):
        items = []
        items.append(KeepTogether([
            Paragraph(f"{number}.  {title}", s["h2"]),
            HRFlowable(width=40, thickness=2, color=CYAN),
            Spacer(1, 6),
        ]))
        for p in paragraphs:
            items.append(p)
        return items

    # 1. Scope of Work
    scope_deliverables = cfg.get("scope_deliverables", [])
    out_of_scope       = cfg.get("out_of_scope", "")
    tools_mentioned    = cfg.get("tools_mentioned", [])

    scope_items = [
        Paragraph(
            f"{provider_company} agrees to design, build, and deploy a custom backend automation system "
            f"for {client_company} per the agreed project scope. "
            f"The system will be built using the <b>N8N workflow automation platform</b>.",
            s["body"]),
        Paragraph("<b>The scope of this agreement includes:</b>", s["bold"]),
    ]
    for d in scope_deliverables:
        scope_items.append(Paragraph(f"\u2022   {d}", ParagraphStyle("bul",
            fontName="Helvetica", fontSize=10.5, leading=16,
            leftIndent=14, spaceAfter=5, textColor=DARK_TEXT)))
    scope_items.append(Spacer(1, 6))
    scope_items.append(Paragraph(
        f"<b>Out of scope:</b> {out_of_scope}",
        s["body"]))
    story.extend(contract_section("1", "Scope of Work", scope_items))

    # 2. Project Timeline
    timeline_phases = cfg.get("timeline_phases", [])
    timeline_data   = [
        [Paragraph("Phase", s["header_cell"]),
         Paragraph("Description", s["header_cell"]),
         Paragraph("Duration", s["header_cell"])],
    ]
    for phase in timeline_phases:
        timeline_data.append([
            Paragraph(phase.get("name", ""), s["cell_bold"]),
            Paragraph(phase.get("description", ""), s["cell"]),
            Paragraph(phase.get("duration", ""), s["cell"]),
        ])
    tl_tbl = Table(timeline_data, colWidths=[1.1*inch, 4.1*inch, 1.0*inch])
    tl_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), NAVY),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [LIGHT_GREY, WHITE]),
        ("TOPPADDING",  (0,0), (-1,-1), 8),
        ("BOTTOMPADDING",(0,0),(-1,-1), 8),
        ("LEFTPADDING", (0,0), (-1,-1), 10),
        ("GRID",        (0,0), (-1,-1), 0.4, MID_GREY),
        ("VALIGN",      (0,0), (-1,-1), "TOP"),
    ]))
    tl_items = [
        Paragraph(
            f"{provider_company} will use commercially reasonable efforts to complete the project within "
            f"{timeline_weeks} weeks of receiving the signed agreement and deposit. Timelines are contingent "
            "upon timely provision of API credentials and field documentation by the Client.",
            s["body"]),
        tl_tbl,
    ]
    story.extend(contract_section("2", "Project Timeline", tl_items))

    # 3. Payment Terms
    payment_items = [
        Paragraph(
            f"The total fee for the project described in Section 1 is <b>"
            f"{'${:,.2f} USD'.format(total_price)}</b>, payable as follows:",
            s["body"]),
    ]

    payment_structure = cfg.get("payment_structure", "split")
    if payment_structure == "split":
        pay_data = [
            [Paragraph("Instalment", s["header_cell"]),
             Paragraph("Amount", s["header_cell"]),
             Paragraph("Due", s["header_cell"]),
             Paragraph("Condition", s["header_cell"])],
            [Paragraph("Deposit, Project Start", s["cell_bold"]),
             Paragraph(f"${deposit_amount:,.2f}", s["cell_bold"]),
             Paragraph("Upon signing", s["cell"]),
             Paragraph("Required to begin Discovery phase", s["cell"])],
            [Paragraph("Final Payment, Go-Live", s["cell_bold"]),
             Paragraph(f"${final_amount:,.2f}", s["cell_bold"]),
             Paragraph("Upon go-live approval", s["cell"]),
             Paragraph("Due after client approves the live system", s["cell"])],
        ]
        pay_tbl = Table(pay_data, colWidths=[1.8*inch, 1.0*inch, 1.3*inch, 2.1*inch])
        pay_tbl.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), NAVY),
            ("BACKGROUND", (0,1), (-1,1), colors.HexColor("#FFF7ED")),
            ("BACKGROUND", (0,2), (-1,2), GREEN_LIGHT),
            ("TOPPADDING",  (0,0), (-1,-1), 8),
            ("BOTTOMPADDING",(0,0),(-1,-1), 8),
            ("LEFTPADDING", (0,0), (-1,-1), 10),
            ("GRID",        (0,0), (-1,-1), 0.4, MID_GREY),
            ("VALIGN",      (0,0), (-1,-1), "TOP"),
        ]))
    else:
        pay_data = [
            [Paragraph("Payment", s["header_cell"]),
             Paragraph("Amount", s["header_cell"]),
             Paragraph("Due", s["header_cell"])],
            [Paragraph("Full Project Fee", s["cell_bold"]),
             Paragraph(f"${total_price:,.2f}", s["cell_bold"]),
             Paragraph("Upon signing", s["cell"])],
        ]
        pay_tbl = Table(pay_data, colWidths=[2.5*inch, 1.3*inch, 2.4*inch])
        pay_tbl.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), NAVY),
            ("BACKGROUND", (0,1), (-1,1), GREEN_LIGHT),
            ("TOPPADDING",  (0,0), (-1,-1), 8),
            ("BOTTOMPADDING",(0,0),(-1,-1), 8),
            ("LEFTPADDING", (0,0), (-1,-1), 10),
            ("GRID",        (0,0), (-1,-1), 0.4, MID_GREY),
            ("VALIGN",      (0,0), (-1,-1), "TOP"),
        ]))

    payment_items.append(pay_tbl)
    payment_items.append(Spacer(1, 8))
    payment_items.append(Paragraph("<b>Accepted Payment Methods:</b>", s["bold"]))

    zelle_data = [[
        Paragraph("Bank Transfer (ACH / Wire)", s["cell_bold"]),
        Paragraph(f"Contact {provider_company} for banking details upon agreement signing.", s["cell"]),
    ],[
        Paragraph("Zelle", s["cell_bold"]),
        Paragraph(f"Send to: <b>{provider_phone}</b>  or  <b>{provider_email}</b>", s["cell"]),
    ]]
    zelle_tbl = Table(zelle_data, colWidths=[1.8*inch, 4.4*inch])
    zelle_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), CYAN_LIGHT),
        ("BACKGROUND", (0,1), (-1,1), LIGHT_GREY),
        ("TOPPADDING",  (0,0), (-1,-1), 8),
        ("BOTTOMPADDING",(0,0),(-1,-1), 8),
        ("LEFTPADDING", (0,0), (-1,-1), 10),
        ("GRID",        (0,0), (-1,-1), 0.4, MID_GREY),
        ("VALIGN",      (0,0), (-1,-1), "MIDDLE"),
    ]))
    payment_items.append(zelle_tbl)
    payment_items.append(Spacer(1, 6))
    payment_items.append(Paragraph(
        "There is <b>no mandatory monthly retainer or subscription fee</b> associated with this agreement. "
        "Ongoing support after the 30-day post-launch period is available on an as-needed basis and "
        "will be quoted separately upon request.",
        s["body"]))
    story.extend(contract_section("3", "Payment Terms", payment_items))

    # 4. Data Security & Privacy
    security_items = [
        Paragraph(
            f"{provider_company} takes the security of client data seriously. The following commitments apply "
            "to all data handled during the performance of this agreement:",
            s["body"]),
    ]
    sec_points = [
        ("No Data Storage",
         "The automation system acts as a transit pipe only. Lead and client data passes through "
         "the automation environment in real time and is never stored, cached, or logged by "
         f"{provider_company}."),
        ("Encryption in Transit",
         "All data transmitted through the automation layer is encrypted using HTTPS/TLS. "
         "Data is never transmitted over unencrypted channels."),
        ("API Key Security",
         "All integrations use secure, revocable API keys issued directly by your platforms. "
         "The Client retains full control and may revoke access at any time."),
        ("Confidentiality",
         f"{provider_company} agrees to keep all client data, business information, and system credentials "
         "strictly confidential and will not share them with any third party without written consent."),
        ("Compliance",
         f"Because data at rest resides within the Client's platforms, not with {provider_company}, "
         "the Client's existing compliance frameworks continue to govern stored data."),
    ]
    for title, desc in sec_points:
        security_items.append(Paragraph(f"<b>{title}:</b>  {desc}", s["body"]))
    story.extend(contract_section("4", "Data Security & Confidentiality", security_items))

    # 5. Intellectual Property
    ip_items = [
        Paragraph(
            "Upon receipt of the final payment, the Client owns the automation workflow configuration "
            f"and all deliverables produced specifically for this project. {provider_company} retains the right "
            "to use general methodologies, tools, and non-client-specific techniques in future projects.",
            s["body"]),
        Paragraph(
            f"{provider_company} retains no ongoing access to the Client's systems after the project is "
            "complete unless explicitly granted by the Client for support purposes.",
            s["body"]),
    ]
    story.extend(contract_section("5", "Intellectual Property", ip_items))

    # 6. Client Responsibilities
    client_responsibilities = cfg.get("client_responsibilities", [])
    client_items = [
        Paragraph("The Client agrees to:", s["body"]),
    ]
    for d in client_responsibilities:
        client_items.append(Paragraph(f"\u2022   {d}", ParagraphStyle("bul2",
            fontName="Helvetica", fontSize=10.5, leading=16,
            leftIndent=14, spaceAfter=5, textColor=DARK_TEXT)))
    story.extend(contract_section("6", "Client Responsibilities", client_items))

    # 7. Limitation of Liability
    liability_items = [
        Paragraph(
            f"{provider_company}'s total liability under this agreement shall not exceed the total fees paid "
            f"by the Client under this agreement. {provider_company} is not liable for any indirect, incidental, "
            "or consequential damages, including but not limited to loss of revenue or data, arising "
            "from the use or inability to use the delivered system.",
            s["body"]),
        Paragraph(
            f"{provider_company} is not responsible for downtime, errors, or data loss caused by third-party "
            "platforms or by changes made to those platforms by their respective vendors after the "
            "system go-live date.",
            s["body"]),
    ]
    story.extend(contract_section("7", "Limitation of Liability", liability_items))

    # 8. Termination
    term_items = [
        Paragraph(
            "Either party may terminate this agreement with written notice if the other party "
            "materially breaches any term of this agreement and fails to remedy the breach within "
            "ten (10) business days of receiving written notice.",
            s["body"]),
        Paragraph(
            f"If the Client terminates this agreement after the Discovery phase has begun but before "
            f"go-live, the ${deposit_amount:,.2f} deposit is non-refundable. If {provider_company} is unable to complete the "
            f"project due to circumstances within {provider_company}'s control, the deposit will be refunded in full.",
            s["body"]),
    ]
    story.extend(contract_section("8", "Termination", term_items))

    # 9. Governing Law
    gov_items = [
        Paragraph(
            "This agreement shall be governed by and construed in accordance with the laws of the "
            "State of New Jersey, United States of America. Any disputes arising under this agreement "
            "shall first be attempted to be resolved through good-faith negotiation between the parties.",
            s["body"]),
    ]
    story.extend(contract_section("9", "Governing Law", gov_items))

    # 10. Entire Agreement
    entire_items = [
        Paragraph(
            "This document constitutes the entire agreement between the parties with respect to "
            "the subject matter herein and supersedes all prior discussions, representations, or "
            "agreements. Any amendments must be made in writing and signed by both parties.",
            s["body"]),
    ]
    story.extend(contract_section("10", "Entire Agreement", entire_items))

    # ── Signature block ───────────────────────────────────────────────────────
    story.append(Spacer(1, 16))
    story.append(HRFlowable(width="100%", thickness=1, color=MID_GREY))
    story.append(Spacer(1, 12))
    story.append(Paragraph("SIGNATURES", ParagraphStyle("sig_head",
        fontName="Helvetica-Bold", fontSize=12, textColor=DARK_TEXT, leading=16,
        alignment=TA_CENTER, spaceAfter=4)))
    story.append(Paragraph(
        "By signing below, both parties agree to the terms of this Service Agreement.",
        ParagraphStyle("sig_sub", fontName="Helvetica", fontSize=9, textColor=GREY_TEXT,
                       alignment=TA_CENTER, leading=13, spaceAfter=16)))

    provider_col = [
        Paragraph("SERVICE PROVIDER", s["label"]),
        Paragraph(provider_company, s["sig_name"]),
        Spacer(1, 8),
        SigBox(label="Signature", width=2.9*inch, height=52),
        Spacer(1, 8),
        Paragraph("Full Name", s["sig_label"]),
        PrefilledField(provider_name, width=2.9*inch, height=22),
        Spacer(1, 6),
        Paragraph("Date", s["sig_label"]),
        PrefilledField(today_str, width=2.9*inch, height=22),
    ]

    client_col = [
        Paragraph("CLIENT", s["label"]),
        Paragraph(client_company, s["sig_name"]),
        Spacer(1, 8),
        SigBox(label="Signature", width=2.9*inch, height=52),
        Spacer(1, 8),
        Paragraph("Full Name  (click to type)", s["sig_label"]),
        InputField("client_name", tooltip="Enter your full legal name",
                   width=2.9*inch, height=22),
        Spacer(1, 6),
        Paragraph("Date  (click to type)", s["sig_label"]),
        InputField("client_date", tooltip="Enter today's date",
                   width=2.9*inch, height=22),
    ]

    sig_data = [[provider_col, Spacer(1,1), client_col]]
    sig_tbl = Table(sig_data, colWidths=[3.0*inch, 0.4*inch, 3.0*inch])
    sig_tbl.setStyle(TableStyle([
        ("VALIGN",       (0,0), (-1,-1), "TOP"),
        ("TOPPADDING",   (0,0), (-1,-1), 0),
        ("BOTTOMPADDING",(0,0), (-1,-1), 0),
        ("LEFTPADDING",  (0,0), (-1,-1), 0),
        ("RIGHTPADDING", (0,0), (-1,-1), 0),
    ]))
    story.append(sig_tbl)
    story.append(Spacer(1, 14))
    story.append(Paragraph(
        "By typing your name in the fields above, you acknowledge that this constitutes "
        "a legally binding electronic signature under applicable e-signature laws.",
        ParagraphStyle("esig_note", fontName="Helvetica-Oblique", fontSize=8.5,
                       textColor=GREY_TEXT, leading=13, alignment=TA_CENTER)))
    story.append(Spacer(1, 10))
    story.append(Paragraph(
        f"{provider_company}  \u00b7  {provider_address}  \u00b7  {provider_email}  \u00b7  {provider_phone}",
        s["footer"]))

    doc.build(story,
              onFirstPage=make_page_cb("Service Agreement", cfg),
              onLaterPages=make_page_cb("Service Agreement", cfg))
    print(f"Contract saved to:\n   {output_path}")


# ══════════════════════════════════════════════════════════════════════════════
#  BUILD INVOICE
# ══════════════════════════════════════════════════════════════════════════════

def build_invoice(cfg):
    sanitized   = cfg["client_name_sanitized"]
    output_dir  = cfg["output_dir"]
    output_path = os.path.join(output_dir, f"AP_Systems_Invoice_{sanitized}.pdf")

    today     = datetime.date.today()
    today_str = today.strftime("%B %d, %Y")
    due_str   = (today + datetime.timedelta(days=7)).strftime("%B %d, %Y")

    provider_company = cfg["provider_company"]
    provider_name    = cfg["provider_name"]
    provider_address = cfg["provider_address"]
    provider_email   = cfg["provider_email"]
    provider_phone   = cfg["provider_phone"]

    client_company  = cfg["client_company"]
    client_contacts = cfg["client_contacts"]
    client_email    = cfg["client_email"]
    client_states   = cfg.get("client_states", "")

    invoice_number    = cfg.get("invoice_number", f"AP-{today.year}-001")
    invoice_line_items = cfg.get("invoice_line_items", [])
    deposit_amount    = cfg.get("deposit_amount", 0)

    s = contract_styles()
    doc = SimpleDocTemplate(
        output_path, pagesize=letter,
        leftMargin=0.75*inch, rightMargin=0.75*inch,
        topMargin=0.65*inch, bottomMargin=0.55*inch,
    )
    story = []

    # ── Invoice header ────────────────────────────────────────────────────────
    inv_header = [[
        [
            Paragraph(provider_company.upper(), ParagraphStyle("invco",
                fontName="Helvetica-Bold", fontSize=22, textColor=WHITE, leading=26)),
            Paragraph(provider_address, ParagraphStyle("invaddr",
                fontName="Helvetica", fontSize=9, textColor=colors.HexColor("#94A3B8"), leading=13)),
            Paragraph(provider_email, ParagraphStyle("invaddr2",
                fontName="Helvetica", fontSize=9, textColor=colors.HexColor("#94A3B8"), leading=13)),
            Paragraph(provider_phone, ParagraphStyle("invaddr3",
                fontName="Helvetica", fontSize=9, textColor=colors.HexColor("#94A3B8"), leading=13)),
        ],
        [
            Paragraph("INVOICE", ParagraphStyle("invtitle",
                fontName="Helvetica-Bold", fontSize=28, textColor=CYAN,
                leading=32, alignment=TA_RIGHT)),
            Paragraph(f"#{invoice_number}", ParagraphStyle("invnum",
                fontName="Helvetica-Bold", fontSize=13, textColor=WHITE,
                leading=16, alignment=TA_RIGHT)),
        ],
    ]]
    inv_hdr_tbl = Table(inv_header, colWidths=[3.5*inch, 3.25*inch])
    inv_hdr_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), DARK_BG),
        ("TOPPADDING",  (0,0), (-1,-1), 18),
        ("BOTTOMPADDING",(0,0),(-1,-1), 18),
        ("LEFTPADDING", (0,0), (-1,-1), 16),
        ("RIGHTPADDING",(0,0),(-1,-1), 16),
        ("VALIGN",      (0,0), (-1,-1), "TOP"),
        ("LINEBELOW",   (0,0), (-1,-1), 3, CYAN),
    ]))
    story.append(inv_hdr_tbl)
    story.append(Spacer(1, 20))

    # ── Invoice meta + Bill To ────────────────────────────────────────────────
    bill_to_lines = [
        Paragraph("BILL TO", s["label"]),
        Paragraph(client_company, s["sig_name"]),
        Paragraph(client_contacts, s["cell"]),
        Paragraph(client_email, s["cell"]),
    ]
    if client_states:
        bill_to_lines.append(Paragraph(f"States served: {client_states}", s["cell"]))

    meta_data = [[
        bill_to_lines,
        [
            Paragraph("INVOICE DETAILS", s["label"]),
            Spacer(1, 4),
            Paragraph(f"Invoice Number:   <b>{invoice_number}</b>", s["cell"]),
            Paragraph(f"Invoice Date:         <b>{today_str}</b>", s["cell"]),
            Paragraph(f"Payment Due:       <b>{due_str}</b>", s["cell"]),
            Paragraph("Status:                    <b>Due on Receipt</b>", s["cell"]),
        ],
    ]]
    meta_tbl = Table(meta_data, colWidths=[3.4*inch, 3.35*inch])
    meta_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (0,0), colors.HexColor("#F0F9FF")),
        ("BACKGROUND", (1,0), (1,0), LIGHT_GREY),
        ("TOPPADDING",  (0,0), (-1,-1), 12),
        ("BOTTOMPADDING",(0,0),(-1,-1), 12),
        ("LEFTPADDING", (0,0), (-1,-1), 14),
        ("BOX",         (0,0), (0,0), 1, CYAN),
        ("BOX",         (1,0), (1,0), 0.5, MID_GREY),
        ("VALIGN",      (0,0), (-1,-1), "TOP"),
    ]))
    story.append(meta_tbl)
    story.append(Spacer(1, 24))

    # ── Line items ────────────────────────────────────────────────────────────
    li_header = [
        Paragraph("#", s["header_cell"]),
        Paragraph("Description", s["header_cell"]),
        Paragraph("Qty", s["header_cell"]),
        Paragraph("Unit Price", s["header_cell"]),
        Paragraph("Amount", s["header_cell"]),
    ]
    li_rows = [li_header]

    row_bgs = [("BACKGROUND", (0,0), (-1,0), NAVY)]
    for idx, item in enumerate(invoice_line_items):
        row_color = WHITE if idx % 2 == 0 else LIGHT_GREY
        row_bgs.append(("BACKGROUND", (0, idx+1), (-1, idx+1), row_color))

        unit_price = item.get("unit_price", 0)
        amount_display = item.get("amount_display", "")
        qty = item.get("qty", 1)

        if unit_price and unit_price > 0:
            unit_price_str = f"${unit_price:,.2f}"
        else:
            unit_price_str = amount_display if amount_display else ""

        li_desc_style = ParagraphStyle(f"li_desc_{idx}", fontName="Helvetica", fontSize=9,
                                       textColor=GREY_TEXT, leading=13, spaceAfter=0)
        li_rows.append([
            Paragraph(str(item.get("number", idx+1)), s["cell"]),
            [
                Paragraph(f"<b>{item.get('title', '')}</b>", s["cell_bold"]),
                Paragraph(item.get("description", ""), li_desc_style),
            ],
            Paragraph(str(qty), s["cell"]),
            Paragraph(unit_price_str, s["cell_right"]),
            Paragraph(amount_display, s["cell_bold_right"]) if unit_price and unit_price > 0
            else Paragraph(amount_display, ParagraphStyle(f"pending_{idx}",
                fontName="Helvetica-Oblique", fontSize=9, textColor=GREY_TEXT,
                leading=12, alignment=TA_RIGHT)),
        ])

    li_tbl = Table(li_rows, colWidths=[0.35*inch, 3.7*inch, 0.4*inch, 1.0*inch, 1.0*inch])
    li_tbl.setStyle(TableStyle(row_bgs + [
        ("TOPPADDING",  (0,0), (-1,-1), 9),
        ("BOTTOMPADDING",(0,0),(-1,-1), 9),
        ("LEFTPADDING", (0,0), (-1,-1), 8),
        ("RIGHTPADDING",(0,0),(-1,-1), 8),
        ("GRID",        (0,0), (-1,-1), 0.4, MID_GREY),
        ("VALIGN",      (0,0), (-1,-1), "TOP"),
        ("LINEBELOW",   (0,-1), (-1,-1), 1.5, DARK_TEXT),
    ]))
    story.append(li_tbl)
    story.append(Spacer(1, 8))

    # ── Totals ────────────────────────────────────────────────────────────────
    amount_due = deposit_amount if deposit_amount else cfg.get("total_price", 0)
    totals_data = [
        [Paragraph("Subtotal (this invoice):", s["cell_right"]),
         Paragraph(f"${amount_due:,.2f}", s["cell_bold_right"])],
        [Paragraph("Tax:", s["cell_right"]),
         Paragraph("$0.00", s["cell_right"])],
        [Paragraph("", s["cell_right"]), Paragraph("", s["cell_right"])],
        [Paragraph("<b>AMOUNT DUE NOW</b>",
                   ParagraphStyle("due_label", fontName="Helvetica-Bold", fontSize=13,
                                  textColor=WHITE, alignment=TA_RIGHT, leading=16)),
         Paragraph(f"<b>${amount_due:,.2f}</b>",
                   ParagraphStyle("due_amt", fontName="Helvetica-Bold", fontSize=13,
                                  textColor=WHITE, alignment=TA_RIGHT, leading=16))],
    ]
    totals_tbl = Table(totals_data, colWidths=[4.75*inch, 1.5*inch])
    totals_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,3), (-1,3), NAVY),
        ("TOPPADDING",  (0,0), (-1,-1), 6),
        ("BOTTOMPADDING",(0,0),(-1,-1), 6),
        ("LEFTPADDING", (0,0), (-1,-1), 8),
        ("RIGHTPADDING",(0,0),(-1,-1), 8),
        ("LINEABOVE",   (0,3), (-1,3), 1.5, CYAN),
        ("VALIGN",      (0,0), (-1,-1), "MIDDLE"),
    ]))
    story.append(totals_tbl)
    story.append(Spacer(1, 24))

    # ── Payment instructions ──────────────────────────────────────────────────
    story.append(Paragraph("PAYMENT INSTRUCTIONS", s["label"]))
    story.append(Spacer(1, 4))
    pay_inst = [
        [Paragraph("Zelle", s["cell_bold"]),
         Paragraph(f"Phone: <b>{provider_phone}</b>   or   Email: <b>{provider_email}</b>",
                   s["cell"])],
        [Paragraph("Bank Transfer", s["cell_bold"]),
         Paragraph(f"Contact {provider_company} at the email above to receive banking details.",
                   s["cell"])],
    ]
    pay_tbl = Table(pay_inst, colWidths=[1.3*inch, 5.15*inch])
    pay_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), CYAN_LIGHT),
        ("BACKGROUND", (0,1), (-1,1), LIGHT_GREY),
        ("TOPPADDING",  (0,0), (-1,-1), 9),
        ("BOTTOMPADDING",(0,0),(-1,-1), 9),
        ("LEFTPADDING", (0,0), (-1,-1), 12),
        ("GRID",        (0,0), (-1,-1), 0.4, MID_GREY),
        ("VALIGN",      (0,0), (-1,-1), "MIDDLE"),
        ("LINEAFTER",   (0,0), (0,-1), 1.5, CYAN),
    ]))
    story.append(pay_tbl)
    story.append(Spacer(1, 14))

    # ── Notes ─────────────────────────────────────────────────────────────────
    final_balance = cfg.get("final_payment_amount", 0)
    notes_text = (
        f"<b>Note:</b>  This invoice covers the project deposit only. "
        f"The remaining balance of ${final_balance:,.2f} will be invoiced separately "
        "upon successful go-live and client approval. "
        f"Payment of this deposit confirms acceptance of the Service Agreement and authorises "
        f"{provider_company} to begin the Discovery phase."
    ) if cfg.get("payment_structure") == "split" else (
        f"<b>Note:</b>  This invoice covers the full project fee. "
        "Payment confirms acceptance of the Service Agreement."
    )

    notes_data = [[
        Paragraph(notes_text, ParagraphStyle("note", fontName="Helvetica", fontSize=9.5,
                                             textColor=DARK_TEXT, leading=15, spaceAfter=0)),
    ]]
    notes_tbl = Table(notes_data, colWidths=[6.5*inch])
    notes_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#FFFBEB")),
        ("TOPPADDING",  (0,0), (-1,-1), 10),
        ("BOTTOMPADDING",(0,0),(-1,-1), 10),
        ("LEFTPADDING", (0,0), (-1,-1), 12),
        ("RIGHTPADDING",(0,0),(-1,-1), 12),
        ("BOX",         (0,0), (-1,-1), 1, AMBER),
    ]))
    story.append(notes_tbl)
    story.append(Spacer(1, 20))

    # ── Footer thank-you ──────────────────────────────────────────────────────
    story.append(HRFlowable(width="100%", thickness=0.5, color=MID_GREY))
    story.append(Spacer(1, 10))
    story.append(Paragraph(
        f"Thank you for your business. We look forward to building something valuable for {client_company}.",
        ParagraphStyle("thanks", fontName="Helvetica-Oblique", fontSize=10.5,
                       textColor=GREY_TEXT, leading=15, alignment=TA_CENTER)))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        f"{provider_company}  \u00b7  {provider_address}  \u00b7  {provider_email}  \u00b7  {provider_phone}",
        s["footer"]))

    doc.build(story,
              onFirstPage=make_page_cb("Invoice", cfg),
              onLaterPages=make_page_cb("Invoice", cfg))
    print(f"Invoice saved to:\n   {output_path}")


# ══════════════════════════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 generate_client_docs.py /path/to/intake_config.json")
        sys.exit(1)

    config_path = sys.argv[1]
    if not os.path.isfile(config_path):
        print(f"Error: config file not found: {config_path}")
        sys.exit(1)

    with open(config_path, "r", encoding="utf-8") as f:
        cfg = json.load(f)

    os.makedirs(cfg["output_dir"], exist_ok=True)

    generated = []

    if cfg.get("generate_proposal", True):
        build_proposal(cfg)
        generated.append("Proposal")

    if cfg.get("generate_contract", True):
        build_contract(cfg)
        generated.append("Contract")

    if cfg.get("generate_invoice", True):
        build_invoice(cfg)
        generated.append("Invoice")

    if generated:
        print(f"\nAll done. Generated: {', '.join(generated)}")
    else:
        print("No documents were generated. Check generate_proposal/contract/invoice flags in your config.")


if __name__ == "__main__":
    main()
