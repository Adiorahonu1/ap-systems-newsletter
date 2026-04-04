"""
AP Systems, Contract & Invoice Generator
Right Away Insurance
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus.flowables import Flowable
import datetime

# ── OUTPUT PATHS ───────────────────────────────────────────────────────────────
CONTRACT_OUT = "/Users/macbook/Documents/new workflows/APsystems/AP_Systems_Contract_RightAway_Insurance.pdf"
INVOICE_OUT  = "/Users/macbook/Documents/new workflows/APsystems/AP_Systems_Invoice_RightAway_Insurance.pdf"

# ── PARTIES ────────────────────────────────────────────────────────────────────
PROVIDER = {
    "company":  "AP Systems",
    "name":     "Onuora Adiorah",
    "address":  "599 Stuyvesant Avenue, Irvington, New Jersey",
    "email":    "adiorahonuora@gmail.com",
    "phone":    "(862) 255-9789",
}
CLIENT = {
    "company":  "Right Away Insurance",
    "contacts": "John & Jahan",
    "email":    "jahan@rightawayinsurance.com",
    "website":  "rightawayinsurance.com",
    "states":   "DC, GA, MD, PA & VA",
}
TODAY      = datetime.date.today()
TODAY_STR  = TODAY.strftime("%B %d, %Y")
DUE_STR    = (TODAY + datetime.timedelta(days=7)).strftime("%B %d, %Y")
INVOICE_NO = f"AP-{TODAY.year}-001"

# ── BRAND COLOURS ──────────────────────────────────────────────────────────────
DARK_BG    = colors.HexColor("#0A0E1A")
NAVY       = colors.HexColor("#0D1B2A")
CYAN       = colors.HexColor("#00C8FF")
CYAN_LIGHT = colors.HexColor("#E6F9FF")
WHITE      = colors.white
GREY_TEXT  = colors.HexColor("#6B7280")
LIGHT_GREY = colors.HexColor("#F3F4F6")
MID_GREY   = colors.HexColor("#D1D5DB")
DARK_TEXT  = colors.HexColor("#111827")
GREEN      = colors.HexColor("#10B981")
GREEN_LIGHT= colors.HexColor("#ECFDF5")
RED_LIGHT  = colors.HexColor("#FEF2F2")

PAGE_W, PAGE_H = letter

# ══════════════════════════════════════════════════════════════════════════════
#  SHARED STYLES
# ══════════════════════════════════════════════════════════════════════════════
def get_styles():
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
def make_page_cb(doc_title):
    def on_page(canvas, doc):
        canvas.saveState()
        # Top bar
        canvas.setFillColor(DARK_BG)
        canvas.rect(0, PAGE_H - 34, PAGE_W, 34, fill=1, stroke=0)
        canvas.setFillColor(CYAN)
        canvas.rect(0, PAGE_H - 3, PAGE_W, 3, fill=1, stroke=0)
        canvas.setFillColor(WHITE)
        canvas.setFont("Helvetica-Bold", 8)
        canvas.drawString(0.65*inch, PAGE_H - 21, "AP SYSTEMS")
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
                          f"AP Systems  ·  {PROVIDER['email']}  ·  {PROVIDER['phone']}")
        canvas.drawRightString(PAGE_W - 0.65*inch, 9, f"Page {doc.page}")
        canvas.restoreState()
    return on_page


# ══════════════════════════════════════════════════════════════════════════════
#  CONTRACT
# ══════════════════════════════════════════════════════════════════════════════
# ── INTERACTIVE FORM FIELD FLOWABLES ──────────────────────────────────────────

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


def build_contract():
    s = get_styles()
    doc = SimpleDocTemplate(
        CONTRACT_OUT, pagesize=letter,
        leftMargin=0.8*inch, rightMargin=0.8*inch,
        topMargin=0.7*inch, bottomMargin=0.55*inch,
    )
    story = []

    # ── Cover header ──────────────────────────────────────────────────────────
    header_data = [[
        Paragraph("AP SYSTEMS", ParagraphStyle("co", fontName="Helvetica-Bold",
            fontSize=18, textColor=WHITE, leading=22)),
        Paragraph("SERVICE AGREEMENT", ParagraphStyle("title", fontName="Helvetica-Bold",
            fontSize=18, textColor=WHITE, leading=22, alignment=TA_RIGHT)),
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
        party_cell("Service Provider", PROVIDER["company"], PROVIDER["name"],
                   PROVIDER["email"], PROVIDER["phone"]),
        party_cell("Client", CLIENT["company"], CLIENT["contacts"],
                   CLIENT["email"], CLIENT["website"]),
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
    story.append(Paragraph(f"Effective Date: <b>{TODAY_STR}</b>", s["small"]))
    story.append(HRFlowable(width="100%", thickness=0.5, color=MID_GREY))
    story.append(Spacer(1, 6))

    # ── Sections ──────────────────────────────────────────────────────────────
    def section(number, title, paragraphs):
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
    scope_items = [
        Paragraph(
            "AP Systems agrees to design, build, and deploy a custom backend automation system "
            "that connects Right Away Insurance's lead capture forms directly to Agency Zoom CRM "
            "and QQ Catalyst (Vertafore) via API integration. The system will be built using the "
            "<b>N8N workflow automation platform</b>.",
            s["body"]),
        Paragraph("<b>The scope of this agreement includes:</b>", s["bold"]),
    ]
    deliverables = [
        "Full N8N workflow build customised to Right Away Insurance's lead form fields and CRM schema",
        "API integration with Agency Zoom and QQ Catalyst (Vertafore products)",
        "Data validation, field mapping, and error handling logic",
        "Controlled testing phase using live API environment before production deployment",
        "Full system walkthrough and handoff documentation upon go-live",
        "30 days of post-launch support for adjustments and bug fixes at no additional charge",
    ]
    for d in deliverables:
        scope_items.append(Paragraph(f"•   {d}", ParagraphStyle("bul", fontName="Helvetica",
            fontSize=10.5, leading=16, leftIndent=14, spaceAfter=5, textColor=DARK_TEXT)))

    scope_items.append(Spacer(1, 6))
    scope_items.append(Paragraph(
        "<b>Out of scope:</b> Any changes to the client's existing CRM configuration, "
        "Agency Zoom account settings, QQ Catalyst account settings, or lead capture form design. "
        "Additional feature requests beyond the agreed scope will require a separate written agreement.",
        s["body"]))

    story.extend(section("1", "Scope of Work", scope_items))

    # 2. Project Timeline
    timeline_data = [
        [Paragraph("Phase", s["header_cell"]),
         Paragraph("Description", s["header_cell"]),
         Paragraph("Duration", s["header_cell"])],
        [Paragraph("Discovery", s["cell_bold"]),
         Paragraph("Field mapping, API access confirmation, logic documentation, "
                   "60-minute working session with client team", s["cell"]),
         Paragraph("Week 1", s["cell"])],
        [Paragraph("Build", s["cell_bold"]),
         Paragraph("N8N workflow construction, API integration, error handling, "
                   "internal testing against live API environments", s["cell"]),
         Paragraph("Weeks 2–3", s["cell"])],
        [Paragraph("Testing & Go-Live", s["cell_bold"]),
         Paragraph("Controlled testing with real data, client walkthrough and approval, "
                   "production deployment", s["cell"]),
         Paragraph("Week 4", s["cell"])],
    ]
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
            "AP Systems will use commercially reasonable efforts to complete the project within "
            "four (4) weeks of receiving the signed agreement and deposit. Timelines are contingent "
            "upon timely provision of API credentials and field documentation by the Client.",
            s["body"]),
        tl_tbl,
    ]
    story.extend(section("2", "Project Timeline", tl_items))

    # 3. Payment Terms
    payment_items = [
        Paragraph(
            "The total fee for the project described in Section 1 is <b>Three Thousand Dollars "
            "($3,000.00 USD)</b>, payable in two equal instalments as follows:",
            s["body"]),
    ]
    pay_data = [
        [Paragraph("Instalment", s["header_cell"]),
         Paragraph("Amount", s["header_cell"]),
         Paragraph("Due", s["header_cell"]),
         Paragraph("Condition", s["header_cell"])],
        [Paragraph("Deposit, Project Start", s["cell_bold"]),
         Paragraph("$1,500.00", s["cell_bold"]),
         Paragraph("Upon signing", s["cell"]),
         Paragraph("Required to begin Discovery phase", s["cell"])],
        [Paragraph("Final Payment, Go-Live", s["cell_bold"]),
         Paragraph("$1,500.00", s["cell_bold"]),
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
    payment_items.append(pay_tbl)
    payment_items.append(Spacer(1, 8))
    payment_items.append(Paragraph("<b>Accepted Payment Methods:</b>", s["bold"]))

    zelle_data = [[
        Paragraph("Bank Transfer (ACH / Wire)", s["cell_bold"]),
        Paragraph("Contact AP Systems for banking details upon agreement signing.", s["cell"]),
    ],[
        Paragraph("Zelle", s["cell_bold"]),
        Paragraph(f"Send to: <b>{PROVIDER['phone']}</b>  or  <b>{PROVIDER['email']}</b>", s["cell"]),
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
    story.extend(section("3", "Payment Terms", payment_items))

    # 4. Data Security & Privacy
    security_items = [
        Paragraph(
            "AP Systems takes the security of client data seriously. The following commitments apply "
            "to all data handled during the performance of this agreement:",
            s["body"]),
    ]
    sec_points = [
        ("No Data Storage",
         "The automation system acts as a transit pipe only. Lead and client data passes through "
         "the N8N environment in real time and is never stored, cached, or logged by AP Systems."),
        ("Encryption in Transit",
         "All data transmitted through the automation layer is encrypted using HTTPS/TLS. "
         "Data is never transmitted over unencrypted channels."),
        ("API Key Security",
         "All integrations use secure, revocable API keys issued directly by Agency Zoom and "
         "QQ Catalyst. The Client retains full control and may revoke access at any time."),
        ("Confidentiality",
         "AP Systems agrees to keep all client data, business information, and system credentials "
         "strictly confidential and will not share them with any third party without written consent."),
        ("Compliance",
         "Because data at rest resides within Agency Zoom and Vertafore systems, not with AP Systems, "
         "the Client's existing compliance frameworks continue to govern stored data."),
    ]
    for title, desc in sec_points:
        security_items.append(Paragraph(f"<b>{title}:</b>  {desc}", s["body"]))
    story.extend(section("4", "Data Security & Confidentiality", security_items))

    # 5. Intellectual Property
    ip_items = [
        Paragraph(
            "Upon receipt of the final payment, the Client owns the automation workflow configuration "
            "and all deliverables produced specifically for this project. AP Systems retains the right "
            "to use general methodologies, tools, and non-client-specific techniques in future projects.",
            s["body"]),
        Paragraph(
            "AP Systems retains no ongoing access to the Client's systems after the project is "
            "complete unless explicitly granted by the Client for support purposes.",
            s["body"]),
    ]
    story.extend(section("5", "Intellectual Property", ip_items))

    # 6. Client Responsibilities
    client_items = [
        Paragraph("The Client agrees to:", s["body"]),
    ]
    client_duties = [
        "Provide valid API credentials for Agency Zoom and QQ Catalyst within 5 business days of signing",
        "Make Jahan (or a designated team member) available for the 60-minute Discovery session",
        "Review and approve the system during the controlled testing phase within 5 business days",
        "Provide timely feedback at each project milestone to avoid delays",
        "Notify AP Systems promptly of any changes to CRM structure or lead form fields",
    ]
    for d in client_duties:
        client_items.append(Paragraph(f"•   {d}", ParagraphStyle("bul2", fontName="Helvetica",
            fontSize=10.5, leading=16, leftIndent=14, spaceAfter=5, textColor=DARK_TEXT)))
    story.extend(section("6", "Client Responsibilities", client_items))

    # 7. Limitation of Liability
    liability_items = [
        Paragraph(
            "AP Systems' total liability under this agreement shall not exceed the total fees paid "
            "by the Client under this agreement. AP Systems is not liable for any indirect, incidental, "
            "or consequential damages, including but not limited to loss of revenue or data, arising "
            "from the use or inability to use the delivered system.",
            s["body"]),
        Paragraph(
            "AP Systems is not responsible for downtime, errors, or data loss caused by third-party "
            "platforms including Agency Zoom, QQ Catalyst, or N8N, or by changes made to those "
            "platforms by their respective vendors after the system go-live date.",
            s["body"]),
    ]
    story.extend(section("7", "Limitation of Liability", liability_items))

    # 8. Termination
    term_items = [
        Paragraph(
            "Either party may terminate this agreement with written notice if the other party "
            "materially breaches any term of this agreement and fails to remedy the breach within "
            "ten (10) business days of receiving written notice.",
            s["body"]),
        Paragraph(
            "If the Client terminates this agreement after the Discovery phase has begun but before "
            "go-live, the $1,500 deposit is non-refundable. If AP Systems is unable to complete the "
            "project due to circumstances within AP Systems' control, the deposit will be refunded in full.",
            s["body"]),
    ]
    story.extend(section("8", "Termination", term_items))

    # 9. Governing Law
    gov_items = [
        Paragraph(
            "This agreement shall be governed by and construed in accordance with the laws of the "
            "State of New Jersey, United States of America. Any disputes arising under this agreement "
            "shall first be attempted to be resolved through good-faith negotiation between the parties.",
            s["body"]),
    ]
    story.extend(section("9", "Governing Law", gov_items))

    # 10. Entire Agreement
    entire_items = [
        Paragraph(
            "This document constitutes the entire agreement between the parties with respect to "
            "the subject matter herein and supersedes all prior discussions, representations, or "
            "agreements. Any amendments must be made in writing and signed by both parties.",
            s["body"]),
    ]
    story.extend(section("10", "Entire Agreement", entire_items))

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

    # Left col: provider (pre-filled, read-only visuals)
    # Right col: client (interactive form fields)
    provider_col = [
        Paragraph("SERVICE PROVIDER", s["label"]),
        Paragraph(PROVIDER["company"], s["sig_name"]),
        Spacer(1, 8),
        # Signature drawing area box
        SigBox(label="Signature", width=2.9*inch, height=52),
        Spacer(1, 8),
        Paragraph("Full Name", s["sig_label"]),
        PrefilledField(PROVIDER["name"], width=2.9*inch, height=22),
        Spacer(1, 6),
        Paragraph("Date", s["sig_label"]),
        PrefilledField(TODAY_STR, width=2.9*inch, height=22),
    ]

    client_col = [
        Paragraph("CLIENT", s["label"]),
        Paragraph(CLIENT["company"], s["sig_name"]),
        Spacer(1, 8),
        # Signature drawing area (PDF sig field)
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
        f"AP Systems  ·  {PROVIDER['address']}  ·  {PROVIDER['email']}  ·  {PROVIDER['phone']}",
        s["footer"]))

    doc.build(story, onFirstPage=make_page_cb("Service Agreement"),
              onLaterPages=make_page_cb("Service Agreement"))
    print(f"✅  Contract saved to:\n   {CONTRACT_OUT}")


# ══════════════════════════════════════════════════════════════════════════════
#  INVOICE
# ══════════════════════════════════════════════════════════════════════════════
def build_invoice():
    s = get_styles()
    doc = SimpleDocTemplate(
        INVOICE_OUT, pagesize=letter,
        leftMargin=0.75*inch, rightMargin=0.75*inch,
        topMargin=0.65*inch, bottomMargin=0.55*inch,
    )
    story = []

    # ── Invoice header ────────────────────────────────────────────────────────
    inv_header = [[
        [
            Paragraph("AP SYSTEMS", ParagraphStyle("invco", fontName="Helvetica-Bold",
                fontSize=22, textColor=WHITE, leading=26)),
            Paragraph(PROVIDER["address"], ParagraphStyle("invaddr", fontName="Helvetica",
                fontSize=9, textColor=colors.HexColor("#94A3B8"), leading=13)),
            Paragraph(PROVIDER["email"], ParagraphStyle("invaddr2", fontName="Helvetica",
                fontSize=9, textColor=colors.HexColor("#94A3B8"), leading=13)),
            Paragraph(PROVIDER["phone"], ParagraphStyle("invaddr3", fontName="Helvetica",
                fontSize=9, textColor=colors.HexColor("#94A3B8"), leading=13)),
        ],
        [
            Paragraph("INVOICE", ParagraphStyle("invtitle", fontName="Helvetica-Bold",
                fontSize=28, textColor=CYAN, leading=32, alignment=TA_RIGHT)),
            Paragraph(f"#{INVOICE_NO}", ParagraphStyle("invnum", fontName="Helvetica-Bold",
                fontSize=13, textColor=WHITE, leading=16, alignment=TA_RIGHT)),
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
    meta_data = [[
        [
            Paragraph("BILL TO", s["label"]),
            Paragraph(CLIENT["company"], s["sig_name"]),
            Paragraph(CLIENT["contacts"], s["cell"]),
            Paragraph(CLIENT["email"], s["cell"]),
            Paragraph(f"States served: {CLIENT['states']}", s["cell"]),
        ],
        [
            Paragraph("INVOICE DETAILS", s["label"]),
            Spacer(1, 4),
            Paragraph(f"Invoice Number:   <b>{INVOICE_NO}</b>", s["cell"]),
            Paragraph(f"Invoice Date:         <b>{TODAY_STR}</b>", s["cell"]),
            Paragraph(f"Payment Due:       <b>{DUE_STR}</b>", s["cell"]),
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
    li_rows = [
        li_header,
        [
            Paragraph("1", s["cell"]),
            [
                Paragraph("<b>AI Lead-to-CRM Automation, Project Deposit</b>", s["cell_bold"]),
                Paragraph(
                    "50% deposit to commence the Discovery & Build phases of the N8N "
                    "workflow automation system. Covers lead form → Agency Zoom CRM → "
                    "QQ Catalyst integration. Full project scope per signed Service Agreement.",
                    ParagraphStyle("li_desc", fontName="Helvetica", fontSize=9,
                                   textColor=GREY_TEXT, leading=13, spaceAfter=0)),
            ],
            Paragraph("1", s["cell"]),
            Paragraph("$1,500.00", s["cell_right"]),
            Paragraph("$1,500.00", s["cell_bold_right"]),
        ],
        [
            Paragraph("2", s["cell"]),
            [
                Paragraph("<b>Final Payment, Go-Live (Billed Separately Upon Completion)</b>",
                          s["cell_bold"]),
                Paragraph(
                    "Remaining 50% balance due upon successful deployment and client approval. "
                    "Includes 30-day post-launch support. Invoice will be issued at go-live.",
                    ParagraphStyle("li_desc2", fontName="Helvetica", fontSize=9,
                                   textColor=GREY_TEXT, leading=13, spaceAfter=0)),
            ],
            Paragraph("1", s["cell"]),
            Paragraph("$1,500.00", s["cell_right"]),
            Paragraph("Billed at\ngo-live", ParagraphStyle("pending", fontName="Helvetica-Oblique",
                fontSize=9, textColor=GREY_TEXT, leading=12, alignment=TA_RIGHT)),
        ],
    ]
    li_tbl = Table(li_rows, colWidths=[0.35*inch, 3.7*inch, 0.4*inch, 1.0*inch, 1.0*inch])
    li_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), NAVY),
        ("BACKGROUND", (0,1), (-1,1), WHITE),
        ("BACKGROUND", (0,2), (-1,2), LIGHT_GREY),
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
    totals_data = [
        [Paragraph("Subtotal (this invoice):", s["cell_right"]),
         Paragraph("$1,500.00", s["cell_bold_right"])],
        [Paragraph("Tax:", s["cell_right"]),
         Paragraph("$0.00", s["cell_right"])],
        [Paragraph("", s["cell_right"]), Paragraph("", s["cell_right"])],
        [Paragraph("<b>AMOUNT DUE NOW</b>",
                   ParagraphStyle("due_label", fontName="Helvetica-Bold", fontSize=13,
                                  textColor=WHITE, alignment=TA_RIGHT, leading=16)),
         Paragraph("<b>$1,500.00</b>",
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
         Paragraph(f"Phone: <b>{PROVIDER['phone']}</b>   or   Email: <b>{PROVIDER['email']}</b>",
                   s["cell"])],
        [Paragraph("Bank Transfer", s["cell_bold"]),
         Paragraph("Contact AP Systems at the email above to receive banking details.",
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
    notes_data = [[
        Paragraph(
            "<b>Note:</b>  This invoice covers the project deposit only. The remaining balance of "
            "$1,500.00 will be invoiced separately upon successful go-live and client approval. "
            "Payment of this deposit confirms acceptance of the Service Agreement and authorises "
            "AP Systems to begin the Discovery phase.",
            ParagraphStyle("note", fontName="Helvetica", fontSize=9.5, textColor=DARK_TEXT,
                           leading=15, spaceAfter=0)),
    ]]
    notes_tbl = Table(notes_data, colWidths=[6.5*inch])
    notes_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#FFFBEB")),
        ("TOPPADDING",  (0,0), (-1,-1), 10),
        ("BOTTOMPADDING",(0,0),(-1,-1), 10),
        ("LEFTPADDING", (0,0), (-1,-1), 12),
        ("RIGHTPADDING",(0,0),(-1,-1), 12),
        ("BOX",         (0,0), (-1,-1), 1, colors.HexColor("#F59E0B")),
    ]))
    story.append(notes_tbl)
    story.append(Spacer(1, 20))

    # ── Footer thank-you ──────────────────────────────────────────────────────
    story.append(HRFlowable(width="100%", thickness=0.5, color=MID_GREY))
    story.append(Spacer(1, 10))
    story.append(Paragraph(
        "Thank you for your business. We look forward to building something valuable for Right Away Insurance.",
        ParagraphStyle("thanks", fontName="Helvetica-Oblique", fontSize=10.5,
                       textColor=GREY_TEXT, leading=15, alignment=TA_CENTER)))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        f"AP Systems  ·  {PROVIDER['address']}  ·  {PROVIDER['email']}  ·  {PROVIDER['phone']}",
        s["footer"]))

    doc.build(story, onFirstPage=make_page_cb("Invoice"),
              onLaterPages=make_page_cb("Invoice"))
    print(f"✅  Invoice saved to:\n   {INVOICE_OUT}")


# ── MAIN ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    build_contract()
    build_invoice()
