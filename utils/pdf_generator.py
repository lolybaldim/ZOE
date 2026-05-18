from datetime import date
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import cm
import io


def generate_patient_report(user, patient, consultations, appointments, medications):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)

    styles = getSampleStyleSheet()
    primary = colors.HexColor("#0EA5E9")
    dark = colors.HexColor("#1E293B")

    title_style = ParagraphStyle("Title", parent=styles["Title"],
                                 textColor=primary, fontSize=24, spaceAfter=4)
    heading_style = ParagraphStyle("Heading", parent=styles["Heading2"],
                                   textColor=dark, fontSize=13, spaceBefore=14, spaceAfter=6)
    body_style = styles["Normal"]

    story = []

    # Header
    story.append(Paragraph("ZOE Health Report", title_style))
    story.append(Paragraph("AI Health Access Platform", styles["Normal"]))
    story.append(Spacer(1, 0.4*cm))
    story.append(Paragraph(f"Generated: {date.today().strftime('%B %d, %Y')}", styles["Normal"]))
    story.append(Spacer(1, 0.6*cm))

    # Patient info
    story.append(Paragraph("Patient Information", heading_style))
    info_data = [
        ["Name", user.full_name],
        ["Email", user.email],
        ["Blood Type", patient.blood_type or "—"],
        ["Allergies", patient.allergies or "None reported"],
        ["Chronic Conditions", patient.chronic_conditions or "None reported"],
        ["Emergency Contact", patient.emergency_contact_name or "—"],
    ]
    t = Table(info_data, colWidths=[5*cm, 12*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#F1F5F9")),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ("PADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(t)
    story.append(Spacer(1, 0.4*cm))

    # Recent consultations
    story.append(Paragraph("AI Consultations", heading_style))
    if consultations:
        for c in consultations[:10]:
            story.append(Paragraph(
                f"<b>{c.created_at.strftime('%Y-%m-%d %H:%M')}</b> — Urgency: <b>{c.urgency_level}</b>",
                body_style
            ))
            story.append(Paragraph(f"Symptoms: {c.symptoms[:200]}", body_style))
            story.append(Spacer(1, 0.2*cm))
    else:
        story.append(Paragraph("No consultations recorded.", body_style))

    # Appointments
    story.append(Paragraph("Appointment History", heading_style))
    if appointments:
        appt_data = [["Date", "Time", "Reason", "Status"]]
        for a in appointments[:15]:
            appt_data.append([str(a.date), str(a.time)[:5], a.reason[:40], a.status.title()])
        t2 = Table(appt_data, colWidths=[3.5*cm, 2.5*cm, 9*cm, 3*cm])
        t2.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), primary),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
            ("PADDING", (0, 0), (-1, -1), 5),
        ]))
        story.append(t2)
    else:
        story.append(Paragraph("No appointments recorded.", body_style))

    # Medications
    story.append(Paragraph("Current Medications", heading_style))
    if medications:
        for m in medications:
            story.append(Paragraph(f"• <b>{m.name}</b> — {m.dosage} ({m.frequency})", body_style))
    else:
        story.append(Paragraph("No active medications.", body_style))

    story.append(Spacer(1, 1*cm))
    story.append(Paragraph(
        "⚕ This report is for reference only. Always consult a qualified healthcare professional for medical advice.",
        ParagraphStyle("Disclaimer", parent=body_style, textColor=colors.gray, fontSize=8)
    ))

    doc.build(story)
    buffer.seek(0)
    return buffer
