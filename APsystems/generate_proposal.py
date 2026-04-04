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
import datetime

OUTPUT = "/Users/macbook/Documents/new workflows/APsystems/AP_Systems_Proposal_RightAway_Insurance.pdf"

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
AMBER      = colors.HexColor("#F59E0B")

# ── STYLES ─────────────────────────────────────────────────────────────────────
def styles():
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

# ── HELPER FLOWABLES ───────────────────────────────────────────────────────────
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
    """Full dark cover page drawn on canvas."""
    def __init__(self, width, height):
        Flowable.__init__(self)
        self.pg_w = width
        self.pg_h = height

    def wrap(self, *args):
        return (self.pg_w, self.pg_h)

    def draw(self):
        c = self.canv
        w, h = self.pg_w, self.pg_h

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
        c.drawCentredString(w / 2, h - 80, "AP SYSTEMS")

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
        c.drawCentredString(w / 2, h - 182, "Right Away Insurance")

        # Tagline
        c.setFillColor(colors.HexColor("#94A3B8"))
        c.setFont("Helvetica-Oblique", 12)
        c.drawCentredString(w / 2, h - 215, "Seamless Lead-to-CRM Automation, Built Around Your Workflow")

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
        lines = [
            "Every morning, Jahan manually imports leads captured overnight ",
            "5 to 12 entries, every single day, before the real work begins.",
            "That is hours of avoidable manual work every week,",
            "and every delayed entry is a lead that waits longer to be contacted.",
        ]
        for i, line in enumerate(lines):
            c.drawCentredString(w / 2, box_y + 60 - i * 14, line)

        # Flow diagram
        flow_y = h - 440
        nodes = ["Lead Captured", "N8N Automation", "Agency Zoom CRM", "QQ Catalyst"]
        colors_n = [colors.HexColor("#1E3A5F"), CYAN, GREEN, colors.HexColor("#5B21B6")]
        node_w, node_h, gap = 100, 32, 18
        total_w = len(nodes) * node_w + (len(nodes) - 1) * gap
        start_x = (w - total_w) / 2

        for i, (label, col) in enumerate(zip(nodes, colors_n)):
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
            ("Prepared for:", "John & Jahan, Right Away Insurance"),
            ("Prepared by:", "Onuora Adiorah, AP Systems"),
            ("Date:", today),
            ("Valid for:", "30 Days from Date of Issue"),
        ]
        for i, (label, value) in enumerate(meta):
            row_y = meta_y + 35 - i * 16
            c.setFillColor(GREY_TEXT)
            c.setFont("Helvetica", 8)
            c.drawString(100, row_y, label)
            c.setFillColor(WHITE)
            c.setFont("Helvetica-Bold", 8)
            c.drawString(230, row_y, value)

        # Bottom bar
        c.setFillColor(CYAN)
        c.rect(0, 0, w, 4, fill=1, stroke=0)

        c.setFillColor(colors.HexColor("#94A3B8"))
        c.setFont("Helvetica", 7.5)
        c.drawCentredString(w / 2, 12, "Confidential, Prepared exclusively for Right Away Insurance")


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


# ── SECTION BUILDER ────────────────────────────────────────────────────────────
def section(s, label, heading, content_fn):
    """Returns list of flowables for one section."""
    items = []
    items.append(Paragraph(label.upper(), s["section_label"]))
    items.append(Paragraph(heading, s["section_heading"]))
    items.append(ColorBar(height=2, color=CYAN, width=40))
    items.append(Spacer(1, 10))
    items.extend(content_fn(s))
    items.append(Spacer(1, 14))
    items.append(HRFlowable(width="100%", thickness=0.5, color=MID_GREY))
    return items


# ── CONTENT SECTIONS ───────────────────────────────────────────────────────────

def intro_content(s):
    today = datetime.date.today().strftime("%B %d, %Y")
    return [
        Paragraph(f"Date: {today}", s["body"]),
        Paragraph("To: John & Jahan, Right Away Insurance", s["body"]),
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


def problem_content(s):
    items = []
    items.append(Paragraph(
        "Right now, every lead captured after hours by your AI assistant sits in a queue. "
        "Each morning, that data has to be manually moved, entry by entry, into Agency Zoom and QQ Catalyst. "
        "On a busy day, that is <b>12 individual imports before 9am</b>.",
        s["body"]))
    items.append(Spacer(1, 6))

    pain_data = [
        [Paragraph("The Hidden Cost of Manual Entry", s["table_header"])],
        [Paragraph("5–12 manual data imports every morning", s["table_cell"])],
        [Paragraph("Delayed CRM updates mean slower response time to warm leads", s["table_cell"])],
        [Paragraph("Team attention pulled away from revenue-generating tasks", s["table_cell"])],
        [Paragraph("Human error risk on every import, wrong field, missed field, duplicate entry", s["table_cell"])],
        [Paragraph("Lead momentum lost between capture and first contact", s["table_cell"])],
    ]
    pain_table = Table(pain_data, colWidths=[5.5 * inch])
    pain_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("BACKGROUND", (0, 1), (-1, 1), colors.HexColor("#FEF3C7")),
        ("BACKGROUND", (0, 2), (-1, 2), LIGHT_GREY),
        ("BACKGROUND", (0, 3), (-1, 3), colors.HexColor("#FEF3C7")),
        ("BACKGROUND", (0, 4), (-1, 4), LIGHT_GREY),
        ("BACKGROUND", (0, 5), (-1, 5), colors.HexColor("#FEF3C7")),
        ("TOPPADDING",  (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [LIGHT_GREY, colors.HexColor("#FEF3C7")]),
    ]))
    items.append(pain_table)
    items.append(Spacer(1, 10))
    items.append(Paragraph(
        "<i>\"The team doesn't want to pay for something during months the system just runs, "
        "and we already pay for Agency Zoom, QQ Catalyst, and multiple other platforms.\"</i>",
        s["quote"]))
    items.append(Paragraph(" John, Right Away Insurance (paraphrased from our conversation)", s["footer"]))
    items.append(Spacer(1, 6))
    items.append(Paragraph(
        "We heard that. This proposal is structured to respect exactly that concern.",
        s["body_bold"]))
    return items


def solution_content(s):
    items = []
    items.append(Paragraph(
        "We will build a backend automation system using <b>N8N</b>, a powerful workflow automation "
        "platform, that connects your lead capture forms directly to Agency Zoom and QQ Catalyst via API. "
        "No agentic AI, no black-box processing. Just a clean, reliable data pipe.",
        s["body"]))

    contrast_data = [
        [Paragraph("TODAY", s["table_header"]), Paragraph("AFTER AP SYSTEMS", s["table_header"])],
        [Paragraph("Lead captured overnight by AI assistant", s["table_cell"]),
         Paragraph("Lead captured overnight by AI assistant", s["table_cell"])],
        [Paragraph("Jahan manually imports 5–12 entries each morning", s["table_cell"]),
         Paragraph("Data transfers automatically, zero manual input", s["table_cell"])],
        [Paragraph("CRM updated hours after lead was captured", s["table_cell"]),
         Paragraph("CRM updated in seconds, while lead is still warm", s["table_cell"])],
        [Paragraph("Risk of missed fields or duplicate entries", s["table_cell"]),
         Paragraph("Consistent, validated data transfer every time", s["table_cell"])],
        [Paragraph("Team starts day with administrative tasks", s["table_cell"]),
         Paragraph("Team starts day ready to close, pipeline already loaded", s["table_cell"])],
    ]
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
    bullets = [
        "A lead submits their information through your capture form or AI assistant.",
        "N8N intercepts the data the moment it is submitted.",
        "The system validates, formats, and routes the data to Agency Zoom and QQ Catalyst simultaneously.",
        "Your CRM is updated in seconds, no human required.",
        "The data is never stored by our system. It moves through, like a pipe, and that is all.",
    ]
    for i, b in enumerate(bullets, 1):
        items.append(Paragraph(f"<b>{i}.</b>  {b}", s["bullet"]))
    return items


def timeline_content(s):
    items = []
    items.append(Paragraph(
        "We run every implementation in three focused phases. You will know exactly where things stand "
        "at every stage, no ambiguity, no delays.",
        s["body"]))
    phases = [
        ("Phase 1", "Discovery & Mapping", "Week 1",
         "We document every data point your lead forms capture, map the exact fields in Agency Zoom and QQ Catalyst, "
         "confirm API access, and define the logic for any conditional routing (e.g. different lead types go to different pipelines)."),
        ("Phase 2", "Build & Configuration", "Weeks 2–3",
         "Backend automation is built, tested internally against live API environments, error handling is configured, "
         "and all data transformation logic is finalized. You will receive a walkthrough before we proceed to testing."),
        ("Phase 3", "Controlled Testing & Go-Live", "Week 4",
         "We run a controlled testing period using real data in a staging environment. Any edge cases are resolved before "
         "production deployment. Final sign-off from your team, then the system goes live."),
    ]
    phase_colors = [colors.HexColor("#0C2340"), colors.HexColor("#0A2E1F"), colors.HexColor("#1A0A2E")]

    for phase_label, phase_name, phase_time, phase_desc in phases:
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


def investment_content(s):
    items = []
    items.append(Paragraph(
        "During our conversation, you were clear: you don't want ongoing obligations for a system "
        "that simply runs. We respected that immediately, and this proposal reflects it.",
        s["body"]))

    # Price card
    price_data = [
        [Paragraph("ONE-TIME PROJECT FEE", s["price_label"])],
        [Paragraph("$3,000", s["price_big"])],
        [Paragraph("Full build · API integration · testing · go-live", s["price_sub"])],
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

    what_included = [
        "Complete N8N workflow build, custom to your lead forms and CRM fields",
        "API integration with Agency Zoom and QQ Catalyst (Vertafore products)",
        "Data validation and error handling logic",
        "4-week implementation (discovery → build → test → go-live)",
        "Full walkthrough and handoff documentation",
        "30 days post-launch support for any adjustments at no additional charge",
    ]
    items.append(Paragraph("<b>What is included in the $3,000:</b>", s["body_bold"]))
    for item in what_included:
        items.append(Paragraph(f"✓  {item}", s["bullet"]))

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
        [Paragraph("Payment Schedule", s["table_header"]), Paragraph("Amount", s["table_header"]), Paragraph("Timing", s["table_header"])],
        [Paragraph("Deposit, Discovery & Build Start", s["table_cell"]), Paragraph("$1,500", s["table_cell_bold"]), Paragraph("Upon agreement", s["table_cell"])],
        [Paragraph("Final Payment, Go-Live Sign-Off", s["table_cell"]), Paragraph("$1,500", s["table_cell_bold"]), Paragraph("Upon successful deployment", s["table_cell"])],
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


def security_content(s):
    items = []
    items.append(Paragraph(
        "You asked the right questions about data security, and we take this seriously.",
        s["body_bold"]))

    security_points = [
        ("No Data Storage",
         "Our automation system acts purely as a pipe. Data passes through N8N in transit and is never stored, "
         "cached, or logged by our system. It moves from your lead forms to your CRM and nowhere else."),
        ("Encrypted in Transit",
         "All data transferred through the automation layer is encrypted using HTTPS/TLS, the same standard "
         "used by banks and financial platforms. Data is never transmitted over unencrypted channels."),
        ("API Key Security",
         "All integrations use secure, revocable API keys issued by Agency Zoom and QQ Catalyst. "
         "You retain full control, you can revoke access at any time without contacting us."),
        ("Vendor-Level Compliance",
         "Because the data lives in your Agency Zoom and Vertafore systems, not ours, their existing "
         "compliance frameworks (SOC 2, HIPAA considerations, etc.) continue to govern the data at rest."),
        ("Liability Coverage",
         "We are happy to provide documentation on our liability position and discuss any specific "
         "coverage requirements your agency has before signing. This can be addressed directly."),
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


def why_us_content(s):
    items = []
    differentiators = [
        ("Built Around Your Stack",
         "We are not asking you to change your CRM, your management system, or your capture tools. "
         "This system wraps around what you already use."),
        ("No Black-Box AI",
         "This is not an agentic AI system making decisions with your data. "
         "It is a deterministic automation, every action is defined, predictable, and auditable."),
        ("Outcome-Focused, Not Feature-Focused",
         "We are not selling you a platform. We are solving a specific problem: "
         "manual data entry that costs your team time every single morning."),
        ("No Subscription Pressure",
         "You raised this concern directly. Our model respects it. You pay once, you own the outcome. "
         "Support is available when you need it, not billed whether you use it or not."),
        ("Transparent Process",
         "Four weeks. Three phases. You will know what is happening at every stage before we move forward."),
    ]
    for title, desc in differentiators:
        items.append(Paragraph(f"<b>{title}</b>", s["body_bold"]))
        items.append(Paragraph(desc, s["body"]))
        items.append(Spacer(1, 2))
    return items


def next_steps_content(s):
    items = []
    items.append(Paragraph(
        "You mentioned you want to research N8N before responding, that is completely fair, "
        "and we encourage it. When you are ready, the path forward is simple and low-risk.",
        s["body"]))
    items.append(Spacer(1, 8))

    steps = [
        (
            "Step 1, Reply to Confirm Interest",
            "ACTION: Reply to this email or contact Onuora directly.",
            "Let us know you want to move forward. No commitment yet, just a confirmation "
            "that the terms in this proposal work for Right Away Insurance.",
        ),
        (
            "Step 2, Sign the Project Agreement",
            "ACTION: Review and sign the one-page project agreement.",
            "We will send a short agreement covering the scope, timeline, and payment terms outlined "
            "in this proposal. No surprises, it reflects exactly what is written here.",
        ),
        (
            "Step 3, Submit the $1,500 Deposit",
            "ACTION: Submit the first payment to begin the Discovery phase.",
            "Once the deposit is received, we will schedule the Discovery session with Jahan within "
            "48 hours. The second $1,500 is only due when the system is live and approved by your team.",
        ),
        (
            "Step 4, Discovery Session with Jahan (60 minutes)",
            "ACTION: Jahan joins a 60-minute working session with the AP Systems team.",
            "We will map every lead form field to the exact Agency Zoom and QQ Catalyst fields, "
            "confirm API access, and document any conditional routing logic. This is the only "
            "significant time commitment required from your team during the entire build.",
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
        cell_content = [
            Paragraph(title, s["body_bold"]),
            Paragraph(action, action_style),
            Paragraph(desc, s["table_cell"]),
        ]
        from reportlab.platypus import ListFlowable
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
    items.append(Paragraph(
        "That is it. Five steps. Four weeks. And your team never manually enters lead data again.",
        ParagraphStyle("close_line", fontName="Helvetica-Bold", fontSize=11,
                       textColor=DARK_TEXT, leading=16, alignment=TA_CENTER)
    ))
    return items


# ── PAGE TEMPLATE (header/footer on body pages) ────────────────────────────────
PAGE_W, PAGE_H = letter

def on_page(canvas, doc):
    canvas.saveState()
    # Top bar
    canvas.setFillColor(DARK_BG)
    canvas.rect(0, PAGE_H - 36, PAGE_W, 36, fill=1, stroke=0)
    canvas.setFillColor(CYAN)
    canvas.rect(0, PAGE_H - 3, PAGE_W, 3, fill=1, stroke=0)
    canvas.setFillColor(WHITE)
    canvas.setFont("Helvetica-Bold", 8)
    canvas.drawString(0.65 * inch, PAGE_H - 22, "AP SYSTEMS")
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#94A3B8"))
    canvas.drawRightString(PAGE_W - 0.65 * inch, PAGE_H - 22,
                           "Automation Proposal, Right Away Insurance  |  Confidential")
    # Bottom bar
    canvas.setFillColor(LIGHT_GREY)
    canvas.rect(0, 0, PAGE_W, 28, fill=1, stroke=0)
    canvas.setFillColor(CYAN)
    canvas.rect(0, 28, PAGE_W, 1, fill=1, stroke=0)
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(GREY_TEXT)
    canvas.drawString(0.65 * inch, 10, "AP Systems  ·  adiorahonuora@gmail.com  ·  (862) 255-9789")
    canvas.drawRightString(PAGE_W - 0.65 * inch, 10, f"Page {doc.page}")
    canvas.restoreState()


# ── BUILD PDF ──────────────────────────────────────────────────────────────────
def draw_cover(canvas, doc):
    """Draw cover page directly on the canvas (page 1)."""
    cp = CoverPage(PAGE_W, PAGE_H)
    cp.canv = canvas
    canvas.saveState()
    cp.draw()
    canvas.restoreState()


def build():
    doc = SimpleDocTemplate(
        OUTPUT,
        pagesize=letter,
        leftMargin=0.65 * inch,
        rightMargin=0.65 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.55 * inch,
    )

    s = styles()
    story = []

    # Reserve page 1 for cover (drawn in onFirstPage callback)
    story.append(PageBreak())

    # ── Body pages ─────────────────────────────────────────────────────────────
    body_sections = [
        ("Letter of Introduction", "A Personal Note Before We Begin", intro_content),
        ("The Challenge",          "What Is Costing Your Team Time Every Day", problem_content),
        ("The Solution",           "A Clean Automation Pipeline Built For Your Workflow", solution_content),
        ("Implementation Timeline","What Happens, Week by Week", timeline_content),
        ("Your Investment",        "Transparent, Fair, and Commitment-Free", investment_content),
        ("Data Security",          "How We Protect Your Clients' Information", security_content),
        ("Why AP Systems",         "What Makes This Different", why_us_content),
        ("Next Steps",             "How We Get Started, When You Are Ready", next_steps_content),
    ]

    for label, heading, fn in body_sections:
        story.extend(section(s, label, heading, fn))
        story.append(Spacer(1, 10))

    # ── Closing CTA ────────────────────────────────────────────────────────────
    story.append(Spacer(1, 10))
    story.append(CTABox(
        PAGE_W - 1.3 * inch,
        [
            ("heading", "Let's get Right Away Insurance running on autopilot."),
            ("body",    "Reply to this proposal, or contact Onuora directly to confirm your interest."),
            ("body",    "Discovery can begin within 48 hours of your deposit."),
            ("cta",     "Onuora Adiorah  |  AP Systems  |  adiorahonuora@gmail.com  |  (862) 255-9789"),
        ]
    ))

    story.append(Spacer(1, 20))
    story.append(Paragraph(
        "This proposal is valid for 30 days from the date of issue. "
        "All terms are subject to a signed project agreement.",
        s["footer"]))

    doc.build(story, onFirstPage=draw_cover, onLaterPages=on_page)
    print(f"✅  Proposal saved to:\n   {OUTPUT}")


if __name__ == "__main__":
    build()
