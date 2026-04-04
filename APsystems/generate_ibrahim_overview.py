"""
AP Systems — Service Overview PDF Generator
Client: Ibrahim Yilla
Run: python3 generate_ibrahim_overview.py
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether, PageBreak
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus.flowables import Flowable

# ── BRAND COLOURS ───────────────────────────────────────────────────────────
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
OUTPUT_DIR = "/Users/macbook/Documents/new workflows/APsystems/clients/Ibrahim Yilla Company"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "AP_Systems_ServiceOverview_Ibrahim_Yilla.pdf")

# ── FLOWABLES ───────────────────────────────────────────────────────────────

class FullPageBackground(Flowable):
    """Dark background fill for cover page."""
    def __init__(self, color=DARK_BG):
        super().__init__()
        self.color = color
        self.width = PAGE_W
        self.height = PAGE_H

    def draw(self):
        self.canv.setFillColor(self.color)
        self.canv.rect(-inch, -inch, PAGE_W + 2*inch, PAGE_H + 2*inch, fill=1, stroke=0)


class CoverPage(Flowable):
    """Full dark cover page drawn directly on canvas."""
    def __init__(self, client_name, date):
        super().__init__()
        self.client_name = client_name
        self.date = date
        self.width = PAGE_W
        self.height = PAGE_H

    def wrap(self, *args):
        return (PAGE_W, PAGE_H)

    def draw(self):
        c = self.canv
        w, h = PAGE_W, PAGE_H

        # Background
        c.setFillColor(DARK_BG)
        c.rect(0, 0, w, h, fill=1, stroke=0)

        # Top cyan accent bar
        c.setFillColor(CYAN)
        c.rect(0, h - 6, w, 6, fill=1, stroke=0)

        # Subtle diagonal overlay
        c.setFillColorRGB(0, 0.78, 1, alpha=0.03)
        p = c.beginPath()
        p.moveTo(0, h * 0.4)
        p.lineTo(w * 0.6, h)
        p.lineTo(w, h)
        p.lineTo(w, h * 0.55)
        p.close()
        c.drawPath(p, fill=1, stroke=0)

        # AP SYSTEMS label
        c.setFillColor(CYAN)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(0.65*inch, h - 0.75*inch, "AP SYSTEMS")

        # Divider line
        c.setStrokeColor(VIOLET)
        c.setLineWidth(1)
        c.line(0.65*inch, h - 0.9*inch, 2.5*inch, h - 0.9*inch)

        # Main headline
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 30)
        c.drawString(0.65*inch, h - 1.9*inch, "Your AI Growth System")

        c.setFillColor(CYAN)
        c.setFont("Helvetica-Bold", 30)
        c.drawString(0.65*inch, h - 2.45*inch, "A Service Overview")

        # Subtitle
        c.setFillColor(GREY_TEXT)
        c.setFont("Helvetica", 12)
        subtitle = "A look at what's possible when your business runs on intelligent automation"
        c.drawString(0.65*inch, h - 3.05*inch, subtitle)

        # Client name block
        c.setFillColor(NAVY)
        c.roundRect(0.65*inch, h - 4.2*inch, 3.8*inch, 0.9*inch, 8, fill=1, stroke=0)
        c.setFillColor(GREY_TEXT)
        c.setFont("Helvetica", 9)
        c.drawString(0.9*inch, h - 3.55*inch, "PREPARED FOR")
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(0.9*inch, h - 3.85*inch, self.client_name)

        # Flow diagram: nodes across bottom third
        nodes = ["Lead Captured", "Funnel + Quiz", "CRM + Nurture", "Appointment Booked"]
        node_colors = [
            colors.HexColor("#1E3A5F"),
            CYAN,
            GREEN,
            colors.HexColor("#5B21B6"),
        ]
        node_w = 1.3 * inch
        node_h = 0.55 * inch
        gap = 0.35 * inch
        total_w = len(nodes) * node_w + (len(nodes) - 1) * gap
        start_x = (w - total_w) / 2
        node_y = 2.2 * inch

        for i, (label, nc) in enumerate(zip(nodes, node_colors)):
            nx = start_x + i * (node_w + gap)
            c.setFillColor(nc)
            c.roundRect(nx, node_y, node_w, node_h, 6, fill=1, stroke=0)
            c.setFillColor(WHITE)
            c.setFont("Helvetica-Bold", 8)
            text_width = c.stringWidth(label, "Helvetica-Bold", 8)
            c.drawString(nx + (node_w - text_width) / 2, node_y + 0.2 * inch, label)

            if i < len(nodes) - 1:
                arrow_x = nx + node_w + gap / 2
                c.setFillColor(GREY_TEXT)
                c.setFont("Helvetica", 10)
                c.drawString(arrow_x - 0.05*inch, node_y + 0.18*inch, "→")

        # Date + footer
        c.setFillColor(GREY_TEXT)
        c.setFont("Helvetica", 9)
        c.drawString(0.65*inch, 1.3*inch, f"Prepared by Onuora Adiorah  |  AP Systems  |  {self.date}")
        c.setStrokeColor(GREY_TEXT)
        c.setLineWidth(0.5)
        c.line(0.65*inch, 1.5*inch, w - 0.65*inch, 1.5*inch)
        c.drawString(0.65*inch, 1.1*inch, "adiorahonuora@gmail.com  |  (862) 255-9789")


class SectionHeader(Flowable):
    """Cyan-accented section header bar."""
    def __init__(self, number, title, subtitle=""):
        super().__init__()
        self.number = number
        self.title = title
        self.subtitle = subtitle
        self.width = PAGE_W - 1.3*inch

    def wrap(self, *args):
        return (self.width, 1.1*inch)

    def draw(self):
        c = self.canv
        w = self.width

        # Background
        c.setFillColor(DARK_BG)
        c.roundRect(0, 0, w, 1.05*inch, 8, fill=1, stroke=0)

        # Left cyan bar
        c.setFillColor(CYAN)
        c.roundRect(0, 0, 0.18*inch, 1.05*inch, 4, fill=1, stroke=0)

        # Number badge
        c.setFillColor(VIOLET)
        c.circle(0.5*inch, 0.525*inch, 0.18*inch, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 9)
        num_w = c.stringWidth(str(self.number), "Helvetica-Bold", 9)
        c.drawString(0.5*inch - num_w/2, 0.49*inch, str(self.number))

        # Title
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(0.78*inch, 0.62*inch, self.title)

        # Subtitle
        if self.subtitle:
            c.setFillColor(CYAN)
            c.setFont("Helvetica", 9)
            c.drawString(0.78*inch, 0.34*inch, self.subtitle)


class ROIBox(Flowable):
    """Green ROI highlight box."""
    def __init__(self, text, width):
        super().__init__()
        self._text = text
        self.box_width = width

    def wrap(self, *args):
        return (self.box_width, 1.0*inch)

    def draw(self):
        c = self.canv
        c.setFillColor(GREEN_LIGHT)
        c.roundRect(0, 0, self.box_width, 0.95*inch, 6, fill=1, stroke=0)
        c.setStrokeColor(GREEN)
        c.setLineWidth(1.5)
        c.roundRect(0, 0, self.box_width, 0.95*inch, 6, fill=0, stroke=1)

        # Icon
        c.setFillColor(GREEN)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(0.18*inch, 0.58*inch, "LONG-TERM ROI")

        c.setFillColor(DARK_TEXT)
        c.setFont("Helvetica", 9)
        # Wrap text manually
        words = self._text.split()
        lines = []
        line = ""
        for word in words:
            test = (line + " " + word).strip()
            if c.stringWidth(test, "Helvetica", 9) < self.box_width - 0.36*inch:
                line = test
            else:
                lines.append(line)
                line = word
        if line:
            lines.append(line)

        y = 0.38*inch
        for ln in lines[:3]:
            c.drawString(0.18*inch, y, ln)
            y -= 0.16*inch


# ── STYLES ──────────────────────────────────────────────────────────────────

def make_styles():
    return {
        "intro": ParagraphStyle("intro", fontName="Helvetica", fontSize=11,
                                leading=18, textColor=DARK_TEXT, spaceAfter=8),
        "intro_bold": ParagraphStyle("intro_bold", fontName="Helvetica-Bold", fontSize=12,
                                     leading=18, textColor=DARK_TEXT, spaceAfter=6),
        "label": ParagraphStyle("label", fontName="Helvetica-Bold", fontSize=9,
                                leading=13, textColor=CYAN, spaceAfter=4, spaceBefore=14),
        "body": ParagraphStyle("body", fontName="Helvetica", fontSize=10,
                               leading=16, textColor=DARK_TEXT, spaceAfter=6),
        "bullet": ParagraphStyle("bullet", fontName="Helvetica", fontSize=10,
                                 leading=16, textColor=DARK_TEXT, leftIndent=14,
                                 spaceAfter=3, bulletIndent=0),
        "footer": ParagraphStyle("footer", fontName="Helvetica", fontSize=8,
                                 leading=12, textColor=GREY_TEXT, alignment=TA_CENTER),
        "cover_tag": ParagraphStyle("cover_tag", fontName="Helvetica-Bold", fontSize=10,
                                    leading=14, textColor=WHITE),
        "next_head": ParagraphStyle("next_head", fontName="Helvetica-Bold", fontSize=20,
                                    leading=26, textColor=DARK_BG, spaceAfter=12),
        "next_body": ParagraphStyle("next_body", fontName="Helvetica", fontSize=11,
                                    leading=18, textColor=DARK_TEXT, spaceAfter=8),
    }


def draw_cover_on_canvas(canvas, doc):
    """Draw the cover page directly on the canvas (called via onFirstPage)."""
    canvas.saveState()
    c = canvas
    w, h = PAGE_W, PAGE_H

    c.setFillColor(DARK_BG)
    c.rect(0, 0, w, h, fill=1, stroke=0)

    c.setFillColor(CYAN)
    c.rect(0, h - 6, w, 6, fill=1, stroke=0)

    c.setFillColor(CYAN)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(0.65*inch, h - 0.75*inch, "AP SYSTEMS")

    c.setStrokeColor(VIOLET)
    c.setLineWidth(1)
    c.line(0.65*inch, h - 0.9*inch, 2.5*inch, h - 0.9*inch)

    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 30)
    c.drawString(0.65*inch, h - 1.9*inch, "Your AI Growth System")

    c.setFillColor(CYAN)
    c.setFont("Helvetica-Bold", 30)
    c.drawString(0.65*inch, h - 2.45*inch, "A Service Overview")

    c.setFillColor(GREY_TEXT)
    c.setFont("Helvetica", 12)
    c.drawString(0.65*inch, h - 3.05*inch,
                 "A look at what's possible when your business runs on intelligent automation")

    c.setFillColor(NAVY)
    c.roundRect(0.65*inch, h - 4.2*inch, 3.8*inch, 0.9*inch, 8, fill=1, stroke=0)
    c.setFillColor(GREY_TEXT)
    c.setFont("Helvetica", 9)
    c.drawString(0.9*inch, h - 3.55*inch, "PREPARED FOR")
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(0.9*inch, h - 3.85*inch, "Ibrahim Yilla")

    nodes = ["Lead Captured", "Funnel + Quiz", "CRM + Nurture", "Appointment Booked"]
    node_colors_list = [
        colors.HexColor("#1E3A5F"), CYAN, GREEN, colors.HexColor("#5B21B6"),
    ]
    node_w = 1.3 * inch
    node_h = 0.55 * inch
    gap = 0.35 * inch
    total_w = len(nodes) * node_w + (len(nodes) - 1) * gap
    start_x = (w - total_w) / 2
    node_y = 2.2 * inch

    for i, (label, nc) in enumerate(zip(nodes, node_colors_list)):
        nx = start_x + i * (node_w + gap)
        c.setFillColor(nc)
        c.roundRect(nx, node_y, node_w, node_h, 6, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 8)
        text_width = c.stringWidth(label, "Helvetica-Bold", 8)
        c.drawString(nx + (node_w - text_width) / 2, node_y + 0.2 * inch, label)
        if i < len(nodes) - 1:
            arrow_x = nx + node_w + gap / 2
            c.setFillColor(GREY_TEXT)
            c.setFont("Helvetica", 10)
            c.drawString(arrow_x - 0.05*inch, node_y + 0.18*inch, "\u2192")

    c.setFillColor(GREY_TEXT)
    c.setFont("Helvetica", 9)
    c.drawString(0.65*inch, 1.3*inch,
                 "Prepared by Onuora Adiorah  |  AP Systems  |  April 2, 2026")
    c.setStrokeColor(GREY_TEXT)
    c.setLineWidth(0.5)
    c.line(0.65*inch, 1.5*inch, w - 0.65*inch, 1.5*inch)
    c.drawString(0.65*inch, 1.1*inch, "adiorahonuora@gmail.com  |  (862) 255-9789")

    canvas.restoreState()


def footer_cb(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(GREY_TEXT)
    canvas.setFont("Helvetica", 8)
    page_num = doc.page
    canvas.drawString(0.65*inch, 0.5*inch, "AP Systems  |  adiorahonuora@gmail.com  |  (862) 255-9789")
    canvas.drawRightString(PAGE_W - 0.65*inch, 0.5*inch, f"Page {page_num}")
    canvas.setStrokeColor(MID_GREY)
    canvas.setLineWidth(0.5)
    canvas.line(0.65*inch, 0.65*inch, PAGE_W - 0.65*inch, 0.65*inch)
    canvas.restoreState()


# ── SERVICE DATA ─────────────────────────────────────────────────────────────

SERVICES = [
    {
        "number": 1,
        "title": "Social Media Optimization",
        "subtitle": "Facebook + Instagram",
        "what": (
            "We audit and restructure your Facebook and Instagram pages to function as active "
            "lead generation tools rather than passive content boards. This includes profile "
            "optimization, call-to-action setup, trust signals, and content alignment that "
            "attracts your ideal client automatically."
        ),
        "problem": (
            "Right now, your social pages exist but they are not working for you. Every day "
            "potential clients visit your pages, get no clear direction, and leave. That is "
            "revenue walking out the door silently."
        ),
        "benefits": [
            "More inbound leads from your existing audience without increasing ad spend",
            "A stronger first impression for every referral who checks you out online",
            "A consistent trust signal that builds credibility before you even speak",
            "Page structure that guides visitors toward taking action",
        ],
        "roi": (
            "Over 12 months, every post, ad, and referral click lands somewhere that works. "
            "Optimized pages compound quietly and become your most cost-effective lead source."
        ),
    },
    {
        "number": 2,
        "title": "Lead Funnel + Qualification Quiz",
        "subtitle": "Capture and sort your best prospects automatically",
        "what": (
            "A step-by-step online flow that captures visitor interest, asks smart qualifying "
            "questions, and segments leads based on where they are in the decision process. "
            "Warm leads go straight to your calendar. Cold leads enter a nurture sequence. "
            "You only talk to people who are ready."
        ),
        "problem": (
            "Every lead you get today requires a manual discovery conversation just to find out "
            "if they are worth your time. That process is costing you hours each week and it "
            "does not scale."
        ),
        "benefits": [
            "Qualifies leads automatically before they ever reach you",
            "Segments prospects by need, urgency, and fit",
            "Feeds only warm, ready leads directly to your calendar",
            "Runs 24 hours a day, 7 days a week without your involvement",
        ],
        "roi": (
            "You stop spending time on leads who are not ready and start focusing entirely on "
            "prospects with intent. Your conversion rate increases and your time per client drops."
        ),
    },
    {
        "number": 3,
        "title": "CRM Setup + Lead Routing",
        "subtitle": "A centralized engine for your entire pipeline",
        "what": (
            "A centralized system where every lead lands, gets tagged, scored, and automatically "
            "routed to the right follow-up workflow. No more spreadsheets, no more sticky notes, "
            "no more leads falling through the cracks. Your pipeline becomes fully visible and "
            "fully managed."
        ),
        "problem": (
            "Without a CRM, leads live in your head, your phone, and scattered follow-up "
            "attempts. Some get followed up three times, others get forgotten. There is no "
            "system tracking who is where and what happens next."
        ),
        "benefits": [
            "Every lead captured and tracked from first touch to close",
            "Automatic tagging and routing based on lead behavior",
            "Full visibility into your pipeline at a glance",
            "Never lose a lead to poor follow-up timing again",
        ],
        "roi": (
            "At scale, this becomes the operating system of your business. You can see exactly "
            "where revenue is sitting and what it takes to move it forward."
        ),
    },
    {
        "number": 4,
        "title": "AI Nurture Sequences",
        "subtitle": "Email + SMS follow-up that runs automatically",
        "what": (
            "Intelligent, pre-built message sequences that go out automatically based on where "
            "a lead is in your funnel. Educational content, trust-building messages, and "
            "well-timed prompts that move people from curious to committed without you "
            "lifting a finger."
        ),
        "problem": (
            "Most of your revenue is sitting in the follow-up you have not done yet. Leads who "
            "said they would think about it, annual review clients who drifted, referrals who "
            "expressed interest and then went quiet. Manual follow-up is inconsistent and "
            "most of these people never hear from you again."
        ),
        "benefits": [
            "Automated follow-up that feels personal and timely",
            "Re-engages cold leads who previously went quiet",
            "Builds trust before the first conversation even starts",
            "Consistent messaging delivered at scale across your entire list",
        ],
        "roi": (
            "The businesses that follow up best win the most. This turns follow-up into a "
            "system rather than a task, and recovers revenue you are currently leaving behind."
        ),
    },
    {
        "number": 5,
        "title": "Appointment Booking Automation",
        "subtitle": "Let your calendar fill itself",
        "what": (
            "An automated booking system connected directly to your calendar that allows "
            "qualified leads to schedule themselves at the right time. Automatic confirmations, "
            "reminders, and pre-meeting information reduce no-shows and keep your schedule "
            "running clean."
        ),
        "problem": (
            "Right now you schedule appointments manually, often going back and forth over "
            "timing within 24 to 48 hours of meeting someone. That process creates friction "
            "for the client and consumes time you could spend doing higher-value work."
        ),
        "benefits": [
            "Leads book directly into your calendar without back-and-forth",
            "Automatic reminders that reduce no-shows significantly",
            "Frees 1 to 2 hours of your day spent on scheduling logistics",
            "Professional booking experience that builds confidence before the meeting",
        ],
        "roi": (
            "More appointments booked per week at a fraction of the effort. Your time goes "
            "toward client conversations and closes, not calendar management."
        ),
    },
    {
        "number": 6,
        "title": "Digital Presence",
        "subtitle": "Your 24/7 sales representative online",
        "what": (
            "A professional, conversion-optimized landing page that clearly communicates who "
            "you are, what you do, and why clients should work with you. Integrated with your "
            "funnel, your booking system, and your CRM so that every visitor has a clear, "
            "frictionless path to becoming a lead."
        ),
        "problem": (
            "You mentioned you do not currently have a website. That means referrals who look "
            "you up online find nothing official. Ads have nowhere authoritative to send traffic. "
            "And social media does the heavy lifting it was never built to do alone."
        ),
        "benefits": [
            "Instant credibility with every referral, lead, and prospect who looks you up",
            "Captures leads passively while you are busy doing other work",
            "Integrates with your entire AI system seamlessly",
            "Positions you as a serious, established professional in your market",
        ],
        "roi": (
            "Every ad, every referral, every social post now has a professional destination. "
            "Traffic you were previously losing gets converted into contacts in your system."
        ),
    },
]


# ── BUILD ─────────────────────────────────────────────────────────────────────

def build_pdf():
    doc = SimpleDocTemplate(
        OUTPUT_FILE,
        pagesize=letter,
        leftMargin=0.65*inch,
        rightMargin=0.65*inch,
        topMargin=0.85*inch,
        bottomMargin=0.85*inch,
    )

    styles = make_styles()
    story = []

    # Page 1 is the cover, drawn entirely via draw_cover_on_canvas callback.
    # Start the story with a PageBreak so content begins on page 2.
    story.append(PageBreak())

    # ── INTRODUCTION ──
    story.append(Spacer(1, 0.3*inch))

    intro_header_data = [["INTRODUCTION"]]
    intro_header_table = Table(intro_header_data, colWidths=[PAGE_W - 1.3*inch])
    intro_header_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), DARK_BG),
        ("TEXTCOLOR", (0, 0), (-1, -1), CYAN),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("ROUNDEDCORNERS", [6, 6, 6, 6]),
    ]))
    story.append(intro_header_table)
    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph("Ibrahim,", styles["intro_bold"]))
    story.append(Paragraph(
        "It was great speaking with you. What you have built is impressive — a business running "
        "on genuine relationships, physical presence, and real client trust. That foundation is "
        "rare and it is worth protecting.",
        styles["intro"]
    ))
    story.append(Paragraph(
        "The opportunity in front of you is simple: everything you are doing manually today can "
        "run automatically, at scale, without losing the personal touch that makes your business "
        "work. You do not need to replace anything. You need to add systems underneath what "
        "already works.",
        styles["intro"]
    ))
    story.append(Paragraph(
        "This document outlines the six areas where AI can make the biggest difference for "
        "your business. There is no commitment here. Review what resonates with you, and we "
        "will build the right plan together from there.",
        styles["intro"]
    ))
    story.append(Spacer(1, 0.15*inch))

    story.append(Paragraph(
        "What I saw on our call:",
        styles["intro_bold"]
    ))
    highlights = [
        "Your client acquisition is entirely manual and capped by your personal bandwidth",
        "Leads are being generated but there is no system catching and nurturing them",
        "Your social media presence exists but is not optimized to generate inbound interest",
        "Back-end admin work is consuming time that should go toward closing and serving clients",
        "You have no digital home base for referrals and traffic to land on",
    ]
    for h in highlights:
        story.append(Paragraph(f"\u2022   {h}", styles["bullet"]))

    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph(
        "Each of the following pages addresses one of these areas directly.",
        styles["intro"]
    ))
    story.append(PageBreak())

    # ── SERVICE PAGES ──
    content_width = PAGE_W - 1.3*inch

    for svc in SERVICES:
        story.append(SectionHeader(svc["number"], svc["title"], svc["subtitle"]))
        story.append(Spacer(1, 0.18*inch))

        story.append(Paragraph("WHAT IT IS", styles["label"]))
        story.append(Paragraph(svc["what"], styles["body"]))

        story.append(Paragraph("THE PROBLEM IT SOLVES", styles["label"]))
        story.append(Paragraph(svc["problem"], styles["body"]))

        story.append(Paragraph("KEY BENEFITS", styles["label"]))
        for b in svc["benefits"]:
            row = Table(
                [[
                    Paragraph("\u2022", ParagraphStyle("dot", fontName="Helvetica-Bold",
                                                       fontSize=14, textColor=CYAN, leading=16)),
                    Paragraph(b, styles["body"])
                ]],
                colWidths=[0.2*inch, content_width - 0.2*inch],
            )
            row.setStyle(TableStyle([
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
            ]))
            story.append(row)

        story.append(Spacer(1, 0.12*inch))
        story.append(ROIBox(svc["roi"], content_width))
        story.append(PageBreak())

    # ── NEXT STEPS ──
    story.append(Spacer(1, 0.4*inch))

    next_bg = Table(
        [[Paragraph("What Happens Next", styles["next_head"])]],
        colWidths=[content_width],
    )
    next_bg.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), CYAN_LIGHT),
        ("LEFTPADDING", (0, 0), (-1, -1), 18),
        ("RIGHTPADDING", (0, 0), (-1, -1), 18),
        ("TOPPADDING", (0, 0), (-1, -1), 20),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 20),
        ("ROUNDEDCORNERS", [8, 8, 8, 8]),
    ]))
    story.append(next_bg)
    story.append(Spacer(1, 0.25*inch))

    story.append(Paragraph(
        "This document is a starting point, not a contract.",
        ParagraphStyle("ns_bold", fontName="Helvetica-Bold", fontSize=13,
                       leading=18, textColor=DARK_TEXT, spaceAfter=10)
    ))
    story.append(Paragraph(
        "Take a look at the six services and identify what feels most relevant to where your "
        "business is right now. You do not need to pick everything at once. Some clients start "
        "with one or two services and build from there. Others come in wanting the full system.",
        styles["next_body"]
    ))
    story.append(Paragraph(
        "Once you know what interests you, we get on a proper discovery call, I scope it "
        "precisely for your business, and I send you a formal proposal with a clear deliverable, "
        "timeline, and investment. No guesswork, no surprises.",
        styles["next_body"]
    ))

    story.append(Spacer(1, 0.2*inch))

    steps = [
        ("1", "Review this document and note what resonates most"),
        ("2", "We meet on Tuesday as planned"),
        ("3", "I scope your specific solution and send a formal proposal"),
        ("4", "We build and launch your AI system"),
    ]

    for num, step in steps:
        row = Table(
            [[
                Table([[Paragraph(num, ParagraphStyle("sn", fontName="Helvetica-Bold",
                                                      fontSize=11, textColor=WHITE,
                                                      alignment=TA_CENTER, leading=14))]],
                      colWidths=[0.3*inch],
                      rowHeights=[0.3*inch],
                      style=TableStyle([
                          ("BACKGROUND", (0, 0), (-1, -1), CYAN),
                          ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                          ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                          ("ROUNDEDCORNERS", [4, 4, 4, 4]),
                          ("TOPPADDING", (0, 0), (-1, -1), 2),
                          ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                      ])),
                Paragraph(step, ParagraphStyle("st", fontName="Helvetica", fontSize=11,
                                               leading=16, textColor=DARK_TEXT))
            ]],
            colWidths=[0.45*inch, content_width - 0.45*inch],
        )
        row.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]))
        story.append(row)

    story.append(Spacer(1, 0.35*inch))
    story.append(HRFlowable(width=content_width, thickness=1, color=MID_GREY))
    story.append(Spacer(1, 0.2*inch))

    contact = Table(
        [[
            Paragraph(
                "<b>Onuora Adiorah</b><br/>AI Consultant, AP Systems<br/>"
                "adiorahonuora@gmail.com<br/>(862) 255-9789",
                ParagraphStyle("ct", fontName="Helvetica", fontSize=10,
                               leading=16, textColor=DARK_TEXT)
            ),
            Paragraph(
                "<b>Ready to talk?</b><br/>Reply to the email this came with<br/>"
                "or book directly using the Calendly<br/>link I'll send you.",
                ParagraphStyle("ct2", fontName="Helvetica", fontSize=10,
                               leading=16, textColor=DARK_TEXT, alignment=TA_RIGHT)
            ),
        ]],
        colWidths=[content_width * 0.5, content_width * 0.5],
    )
    contact.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    story.append(contact)

    # ── BUILD ──
    doc.build(story, onFirstPage=draw_cover_on_canvas, onLaterPages=footer_cb)
    print(f"Generated: {OUTPUT_FILE}")


if __name__ == "__main__":
    build_pdf()
