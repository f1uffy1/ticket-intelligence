import random
import pandas as pd
import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, HRFlowable, KeepTogether
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from datetime import datetime, timedelta


# Generating fake data to use for analysis
cats = ["Password Reset", "Hardware Failure", "Software Install",
        "Network Issue", "Email Problem", "Printer Issue", "Account Lockout"]
techs = ["John Smith", "Maria Garcia", "Devon Lee", "Sara Kim"]
pri = ["Low", "Medium", "High", "Critical"]

random.seed(99)
ticket_rows = []
base = datetime(2024, 1, 1)

for i in range(500):
    created = base + timedelta(days=random.randint(0, 364))
    hrs = random.randint(1, 72)
    ticket_rows.append({
        "Ticket ID": f"TKT-{1000+i}",
        "Category": random.choice(cats),
        "Priority": random.choice(pri),
        "Technician": random.choice(techs),
        "Created": created,
        "Resolved": created + timedelta(hours=hrs),
        "Resolution Hours": hrs
    })

df = pd.DataFrame(ticket_rows)
top_issues = df["Category"].value_counts().head(5)
avg_res = df.groupby("Category")["Resolution Hours"].mean().round(1).sort_values(ascending=False)
by_day = df["Created"].dt.day_name().value_counts()
by_tech = df.groupby("Technician")["Resolution Hours"].mean().round(1).sort_values()

# chart settings
plt.rcParams.update({
    "font.family": "sans-serif",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.3,
    "axes.titlesize": 11,
    "axes.titleweight": "bold"
})

def savefig(fig, name):
    fig.savefig(name, bbox_inches="tight", dpi=150)
    plt.close(fig)

fig, ax = plt.subplots(figsize=(6, 3))
top_issues.plot(kind="barh", ax=ax, color="#2E4B8F")
ax.set_title("Top 5 Most Common Issues")
ax.set_xlabel("Number of Tickets")
for b in ax.patches:
    ax.text(b.get_width() + 0.5, b.get_y() + b.get_height()/2,
            str(int(b.get_width())), va='center', fontsize=9, color='#333333')
savefig(fig, "chart_top_issues.png")

fig, ax = plt.subplots(figsize=(6, 3))
avg_res.plot(kind="barh", ax=ax, color="#C0392B")
ax.set_title("Avg Resolution Time by Category (Hours)")
ax.set_xlabel("Hours")
for b in ax.patches:
    ax.text(b.get_width() + 0.2, b.get_y() + b.get_height()/2,
            f'{b.get_width():.1f}h', va='center', fontsize=9, color='#333333')
savefig(fig, "chart_resolution.png")

fig, ax = plt.subplots(figsize=(6, 3))
by_day.plot(kind="bar", ax=ax, color="#27AE60")
ax.set_title("Ticket Volume by Day of Week")
ax.set_ylabel("Tickets")
ax.tick_params(axis='x', rotation=45)
for b in ax.patches:
    ax.text(b.get_x() + b.get_width()/2, b.get_height() + 0.5,
            str(int(b.get_height())), ha='center', fontsize=9, color='#333333')
savefig(fig, "chart_days.png")

# tech chart - flipped to barh so the names werent overlapping
fig, ax = plt.subplots(figsize=(6, 2.5))
by_tech.plot(kind="barh", ax=ax, color="#8E44AD")
ax.set_title("Avg Resolution Time by Technician (Hours)")
ax.set_xlabel("Hours")
for b in ax.patches:
    ax.text(b.get_width() + 0.2, b.get_y() + b.get_height()/2,
            f'{b.get_width():.1f}h', va='center', fontsize=9, color='#333333')
savefig(fig, "chart_tech.png")


styles = getSampleStyleSheet()

h_style = ParagraphStyle("h", fontSize=22, fontName="Helvetica-Bold",
    textColor=colors.white, alignment=TA_CENTER, spaceAfter=4)

sh_style = ParagraphStyle("sh", fontSize=10, fontName="Helvetica",
    textColor=colors.white, alignment=TA_CENTER)

sec_style = ParagraphStyle("sec", fontSize=13, fontName="Helvetica-Bold",
    textColor=colors.HexColor("#2E4B8F"), spaceBefore=14, spaceAfter=6)

foot_style = ParagraphStyle("foot", fontSize=8, fontName="Helvetica",
    textColor=colors.grey, alignment=TA_CENTER)


doc = SimpleDocTemplate("Ticket_Intelligence_Report.pdf", pagesize=letter,
    rightMargin=50, leftMargin=50, topMargin=40, bottomMargin=50)

el = []

hdr = Table([
    [Paragraph("Help Desk Ticket Intelligence Report", h_style)],
    [Paragraph(f"Annual Analysis Report &nbsp;|&nbsp; January – December 2024 &nbsp;|&nbsp; Generated: {datetime.now().strftime('%B %d, %Y')}", sh_style)]
], colWidths=[515])
hdr.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#2E4B8F")),
    ("BACKGROUND", (0,1), (-1,1), colors.HexColor("#1A3060")),
    ("TOPPADDING", (0,0), (-1,0), 18),
    ("BOTTOMPADDING", (0,0), (-1,0), 10),
    ("TOPPADDING", (0,1), (-1,1), 6),
    ("BOTTOMPADDING", (0,1), (-1,1), 14),
    ("ROUNDEDCORNERS", [6]),
]))
el.append(hdr)
el.append(Spacer(1, 20))

ms = ParagraphStyle("ms", fontSize=10, fontName="Helvetica", alignment=TA_CENTER, leading=16)
summary = Table([
    [Paragraph("<b>EXECUTIVE SUMMARY</b>", ParagraphStyle("s", fontSize=11,
        fontName="Helvetica-Bold", textColor=colors.HexColor("#2E4B8F"))), "", "", ""],
    [
        Paragraph(f"<b>500</b><br/>Total Tickets", ms),
        Paragraph(f"<b>37.8 hrs</b><br/>Avg Resolution", ms),
        Paragraph(f"<b>{top_issues.index[0]}</b><br/>Top Issue", ms),
        Paragraph(f"<b>{by_day.index[0]}</b><br/>Busiest Day", ms),
    ]
], colWidths=[128, 128, 128, 128])
summary.setStyle(TableStyle([
    ("SPAN", (0,0), (3,0)),
    ("BACKGROUND", (0,0), (3,0), colors.HexColor("#EEF2FF")),
    ("BACKGROUND", (0,1), (3,1), colors.HexColor("#F8F9FF")),
    ("BOX", (0,0), (-1,-1), 1, colors.HexColor("#2E4B8F")),
    ("LINEBELOW", (0,0), (3,0), 1, colors.HexColor("#2E4B8F")),
    ("TOPPADDING", (0,0), (-1,-1), 10),
    ("BOTTOMPADDING", (0,0), (-1,-1), 10),
    ("ALIGN", (0,1), (-1,-1), "CENTER"),
    ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
]))
el.append(summary)
el.append(Spacer(1, 20))

def section(title, img, h=180):
    return KeepTogether([
        Paragraph(title, sec_style),
        HRFlowable(width="100%", thickness=1, color=colors.HexColor("#2E4B8F")),
        Spacer(1, 8),
        Image(img, width=480, height=h),
        Spacer(1, 16),
    ])

el.append(section("Top 5 Recurring Issues", "chart_top_issues.png"))
el.append(section("Resolution Time by Category", "chart_resolution.png"))
el.append(section("Ticket Volume by Day of Week", "chart_days.png"))
el.append(section("Technician Performance", "chart_tech.png"))

top_issue = top_issues.index[0]
slowest = avg_res.index[0]
busiest = by_day.index[0]
best = by_tech.index[0]

el.append(Paragraph("Recommendations", sec_style))
el.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#2E4B8F")))
el.append(Spacer(1, 8))

recs = Table([
    ["01", f"Create a self-service KB article for '{top_issue}' — currently the #1 issue by volume."],
    ["02", f"Investigate '{slowest}' delays — averaging {avg_res[slowest]} hours, highest of any category."],
    ["03", f"Increase staffing on {busiest}s — busiest day of the week."],
    ["04", f"Use {best}'s workflow as a training baseline — lowest avg resolution time on the team."],
], colWidths=[35, 480])
recs.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (0,-1), colors.HexColor("#2E4B8F")),
    ("TEXTCOLOR", (0,0), (0,-1), colors.white),
    ("ALIGN", (0,0), (0,-1), "CENTER"),
    ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ("FONTNAME", (0,0), (0,-1), "Helvetica-Bold"),
    ("FONTSIZE", (0,0), (0,-1), 11),
    ("FONTNAME", (1,0), (1,-1), "Helvetica"),
    ("FONTSIZE", (1,0), (1,-1), 10),
    ("TOPPADDING", (0,0), (-1,-1), 10),
    ("BOTTOMPADDING", (0,0), (-1,-1), 10),
    ("LEFTPADDING", (1,0), (1,-1), 12),
    ("ROWBACKGROUNDS", (1,0), (1,-1), [colors.HexColor("#F0F4FF"), colors.HexColor("#FAFAFA")]),
    ("BOX", (0,0), (-1,-1), 1, colors.HexColor("#CCCCCC")),
    ("LINEBELOW", (0,0), (-1,-2), 0.5, colors.HexColor("#DDDDDD")),
]))
el.append(recs)
el.append(Spacer(1, 30))

el.append(HRFlowable(width="100%", thickness=0.5, color=colors.grey))
el.append(Spacer(1, 6))
el.append(Paragraph("Ticket Intelligence System &nbsp;|&nbsp; Internal IT Report &nbsp;|&nbsp; Confidential", foot_style))

doc.build(el)
print("done")