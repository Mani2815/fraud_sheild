"""
Feature 7: PDF Forensic Report Generator
Generates a professional cybersecurity incident report PDF.
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from datetime import datetime
import io
import re


# ── COLOUR PALETTE ──
C_BLACK   = colors.HexColor('#0a0a08')
C_AMBER   = colors.HexColor('#f5a623')
C_HIGH    = colors.HexColor('#ff3d5a')
C_MEDIUM  = colors.HexColor('#ff8c00')
C_LOW     = colors.HexColor('#00c896')
C_SURFACE = colors.HexColor('#161614')
C_BORDER  = colors.HexColor('#2a2a25')
C_TEXT    = colors.HexColor('#1a1a18')
C_MUTED   = colors.HexColor('#555550')
C_WHITE   = colors.white


def risk_color(risk_level):
    return {'HIGH': C_HIGH, 'MEDIUM': C_MEDIUM, 'LOW': C_LOW}.get(risk_level, C_MUTED)


def strip_html(text):
    return re.sub(r'<[^>]+>', '', text)


def generate_pdf_report(result):
    """
    Generate a forensic PDF report from analysis result dict.
    Returns bytes of the PDF.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=20*mm, rightMargin=20*mm,
        topMargin=18*mm, bottomMargin=18*mm
    )

    styles = getSampleStyleSheet()
    w = A4[0] - 40*mm  # usable width

    # ── CUSTOM STYLES ──
    def S(name, **kw):
        base = kw.pop('base', 'Normal')
        s = ParagraphStyle(name, parent=styles[base], **kw)
        return s

    title_style   = S('Title2',   fontSize=26, textColor=C_BLACK,   fontName='Helvetica-Bold',  spaceAfter=2,   leading=30)
    sub_style     = S('Sub',      fontSize=8,  textColor=C_MUTED,   fontName='Helvetica',       spaceAfter=0,   letterSpacing=1.5)
    section_style = S('Section',  fontSize=8,  textColor=C_AMBER,   fontName='Helvetica-Bold',  spaceBefore=14, spaceAfter=6, letterSpacing=2)
    body_style    = S('Body2',    fontSize=9.5,textColor=C_TEXT,    fontName='Helvetica',       leading=15,     spaceAfter=6)
    mono_style    = S('Mono',     fontSize=8.5,textColor=C_TEXT,    fontName='Courier',         leading=14,     spaceAfter=4)
    caption_style = S('Caption',  fontSize=7.5,textColor=C_MUTED,   fontName='Helvetica',       spaceAfter=2)
    flag_style    = S('Flag',     fontSize=8,  textColor=C_HIGH,    fontName='Courier-Bold',    spaceAfter=3)

    story = []
    rc = risk_color(result['risk_level'])
    now = datetime.now()

    # ══ HEADER BANNER ══
    header_data = [[
        Paragraph('<b>FRAUDSHIELD</b>', S('H1', fontSize=18, textColor=C_WHITE, fontName='Helvetica-Bold')),
        Paragraph('FORENSIC INCIDENT REPORT', S('H2', fontSize=8, textColor=C_AMBER, fontName='Helvetica-Bold', letterSpacing=2)),
    ]]
    header_table = Table(header_data, colWidths=[w*0.6, w*0.4])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_BLACK),
        ('VALIGN',     (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 14),
        ('BOTTOMPADDING', (0,0), (-1,-1), 14),
        ('LEFTPADDING', (0,0), (0,-1), 14),
        ('RIGHTPADDING', (-1,0), (-1,-1), 14),
        ('ALIGN',  (1,0), (1,-1), 'RIGHT'),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 6))

    # ══ META ROW ══
    meta_data = [[
        Paragraph(f'REPORT ID: FS-{now.strftime("%Y%m%d")}-{abs(hash(result["message"]))%9999:04d}', caption_style),
        Paragraph(f'GENERATED: {now.strftime("%d %b %Y  %H:%M:%S")}', caption_style),
        Paragraph(f'CLASSIFICATION: {result["risk_level"]} RISK', S('CM', fontSize=7.5, textColor=rc, fontName='Helvetica-Bold', spaceAfter=2)),
    ]]
    meta_table = Table(meta_data, colWidths=[w/3, w/3, w/3])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f5f4f0')),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (0,-1), 10),
        ('RIGHTPADDING', (-1,0), (-1,-1), 10),
        ('ALIGN', (2,0), (2,-1), 'RIGHT'),
        ('BOX', (0,0), (-1,-1), 0.5, C_BORDER),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 12))

    # ══ THREAT VERDICT ══
    story.append(Paragraph('01 // THREAT VERDICT', section_style))
    story.append(HRFlowable(width=w, thickness=0.5, color=C_BORDER, spaceAfter=8))

    verdict_data = [[
        Paragraph(f'{result["risk_level"]} RISK', S('VL', fontSize=36, textColor=rc, fontName='Helvetica-Bold', leading=38)),
        Table([
            [Paragraph('FINAL THREAT SCORE', caption_style)],
            [Paragraph(f'{result["final_score"]}<font size="14" color="#999"> / 100</font>', S('FS', fontSize=32, textColor=rc, fontName='Helvetica-Bold', leading=34))],
        ], colWidths=[w*0.35]),
        Table([
            [Paragraph('RULE ENGINE', caption_style), Paragraph('AI CLASSIFIER', caption_style)],
            [Paragraph(str(result['rule_score']), S('RS', fontSize=22, textColor=colors.HexColor('#7b5ea7'), fontName='Helvetica-Bold')),
             Paragraph(str(result['ai_score']),   S('AS', fontSize=22, textColor=C_AMBER, fontName='Helvetica-Bold'))],
            [Paragraph('/ 100', caption_style), Paragraph('/ 100', caption_style)],
        ], colWidths=[w*0.175, w*0.175]),
    ]]
    verdict_table = Table(verdict_data, colWidths=[w*0.28, w*0.36, w*0.36])
    verdict_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#fafaf8')),
        ('BOX', (0,0), (-1,-1), 1, rc),
        ('LINEBEFORE', (1,0), (1,-1), 0.5, C_BORDER),
        ('LINEBEFORE', (2,0), (2,-1), 0.5, C_BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 14),
        ('BOTTOMPADDING', (0,0), (-1,-1), 14),
        ('LEFTPADDING', (0,0), (0,-1), 16),
        ('LEFTPADDING', (1,0), (1,-1), 16),
        ('LEFTPADDING', (2,0), (2,-1), 16),
    ]))
    story.append(verdict_table)
    story.append(Spacer(1, 14))

    # ══ ANALYST REPORT ══
    story.append(Paragraph('02 // ANALYST REPORT', section_style))
    story.append(HRFlowable(width=w, thickness=0.5, color=C_BORDER, spaceAfter=8))
    story.append(Paragraph(result['explanation'], body_style))
    story.append(Spacer(1, 10))

    # ══ DETECTED SIGNALS ══
    story.append(Paragraph('03 // DETECTED THREAT SIGNALS', section_style))
    story.append(HRFlowable(width=w, thickness=0.5, color=C_BORDER, spaceAfter=8))

    if result['detected_phrases']:
        phrase_rows = []
        for i, phrase in enumerate(result['detected_phrases'], 1):
            phrase_rows.append([
                Paragraph(f'{i:02d}', S('N', fontSize=8, textColor=C_MUTED, fontName='Courier')),
                Paragraph(f'▸  {phrase}', flag_style),
                Paragraph('FLAGGED', S('F', fontSize=7, textColor=C_HIGH, fontName='Helvetica-Bold', letterSpacing=1)),
            ])
        phrase_table = Table(phrase_rows, colWidths=[12*mm, w - 32*mm, 20*mm])
        phrase_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#fff8f8')),
            ('ROWBACKGROUNDS', (0,0), (-1,-1), [colors.white, colors.HexColor('#fff4f4')]),
            ('TOPPADDING',    (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('LEFTPADDING',   (0,0), (0,-1), 10),
            ('LEFTPADDING',   (1,0), (1,-1), 8),
            ('ALIGN', (2,0), (2,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#ffcccc')),
            ('LINEBELOW', (0,0), (-1,-2), 0.3, colors.HexColor('#ffdddd')),
        ]))
        story.append(phrase_table)
    else:
        story.append(Paragraph('◎  No suspicious keywords detected.', S('OK', fontSize=9, textColor=C_LOW, fontName='Helvetica')))

    story.append(Spacer(1, 14))

    # ══ ORIGINAL MESSAGE ══
    story.append(Paragraph('04 // ORIGINAL MESSAGE (FORENSIC TRANSCRIPT)', section_style))
    story.append(HRFlowable(width=w, thickness=0.5, color=C_BORDER, spaceAfter=8))
    clean_msg = strip_html(result['message'])
    msg_data = [[Paragraph(clean_msg, mono_style)]]
    msg_table = Table(msg_data, colWidths=[w])
    msg_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#0f0f0d')),
        ('TOPPADDING', (0,0), (-1,-1), 12),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ('BOX', (0,0), (-1,-1), 1, C_AMBER),
    ]))
    # Override text colour for dark background
    msg_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#0f0f0d')),
        ('TEXTCOLOR', (0,0), (-1,-1), C_WHITE),
        ('TOPPADDING', (0,0), (-1,-1), 12),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ('BOX', (0,0), (-1,-1), 1, C_AMBER),
    ]))
    story.append(msg_table)
    story.append(Spacer(1, 14))

    # ══ SAFETY RECOMMENDATIONS ══
    story.append(Paragraph('05 // SAFETY RECOMMENDATIONS', section_style))
    story.append(HRFlowable(width=w, thickness=0.5, color=C_BORDER, spaceAfter=8))

    tips = [
        ('01', 'Never share OTP, PIN, password, or CVV with anyone — including bank employees.'),
        ('02', 'Always call back on official numbers from the bank\'s website, not numbers in the SMS.'),
        ('03', 'Urgency is a weapon. Pause, verify, and never act under pressure from a message.'),
        ('04', 'Check URLs character by character. Fake sites use subtle typos like "sbi-secure.in".'),
        ('05', 'Report fraud to cybercrime.gov.in or call the national helpline 1930 immediately.'),
    ]
    if result['risk_level'] == 'HIGH':
        tips.append(('⚠', 'This message is HIGH RISK. Do NOT click any links or share any personal data.'))

    tip_rows = [[
        Paragraph(n, S('TN', fontSize=8, textColor=C_AMBER, fontName='Courier-Bold')),
        Paragraph(t, S('TT', fontSize=9, textColor=C_TEXT, fontName='Helvetica', leading=13)),
    ] for n, t in tips]

    tip_table = Table(tip_rows, colWidths=[10*mm, w - 10*mm])
    tip_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (0,-1), 4),
        ('LINEBELOW', (0,0), (-1,-2), 0.3, C_BORDER),
    ]))
    story.append(tip_table)
    story.append(Spacer(1, 20))

    # ══ FOOTER LINE ══
    story.append(HRFlowable(width=w, thickness=1, color=C_BLACK, spaceAfter=6))
    footer_data = [[
        Paragraph('FRAUDSHIELD INTELLIGENCE SYSTEM — EDUCATIONAL USE ONLY', caption_style),
        Paragraph('cybercrime.gov.in  |  Helpline: 1930', S('FC', fontSize=7.5, textColor=C_MUTED, fontName='Helvetica', spaceAfter=2, alignment=TA_RIGHT)),
    ]]
    footer_table = Table(footer_data, colWidths=[w*0.65, w*0.35])
    footer_table.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP')]))
    story.append(footer_table)

    doc.build(story)
    buffer.seek(0)
    return buffer.read()
