import os
import io
import sys
import django

sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from reports.models import Report
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_RIGHT, TA_CENTER
import arabic_reshaper
from bidi.algorithm import get_display

# Register Arabic Font
font_path = 'C:/Windows/Fonts/arial.ttf'
if not os.path.exists(font_path):
    font_path = 'C:/Windows/Fonts/tahoma.ttf'

pdfmetrics.registerFont(TTFont('ArabicFont', font_path))

def ar(text):
    if not text:
        return ""
    return get_display(arabic_reshaper.reshape(str(text)))

report = Report.objects.first()
print("Testing PDF generation for report:", report.report_number)

buffer = io.BytesIO()
doc = SimpleDocTemplate(
    buffer, pagesize=A4,
    rightMargin=2*cm, leftMargin=2*cm,
    topMargin=2*cm, bottomMargin=2*cm
)

styles = getSampleStyleSheet()
title_style = ParagraphStyle(
    'RTLTitle', parent=styles['Title'],
    fontName='ArabicFont',
    alignment=TA_CENTER, fontSize=20, spaceAfter=15,
    textColor=colors.HexColor('#1A5276')
)
normal_arabic = ParagraphStyle(
    'RTLNormal', parent=styles['Normal'],
    fontName='ArabicFont',
    alignment=TA_RIGHT, fontSize=10,
    textColor=colors.HexColor('#2C3E50')
)

story = []
story.append(Paragraph(ar('تقرير ميداني شامل'), title_style))
story.append(Spacer(1, 0.5*cm))

gps_text = f"{report.latitude}, {report.longitude}" if report.has_gps else ar('غير محدد')

info_data = [
    [ar('رقم التقرير'), report.report_number],
    [ar('الموظف الميداني'), ar(report.user.get_full_name() or report.user.username)],
    [ar('الوحدة'), ar(report.unit.name if report.unit else 'غير محدد')],
    [ar('نوع الموقع'), ar(report.location_type.name if report.location_type else 'غير محدد')],
    [ar('الموقع'), ar(report.location.name if report.location else 'غير محدد')],
    [ar('إحداثيات الموقع (GPS)'), gps_text],
    [ar('تاريخ الإنشاء'), report.created_at.strftime('%Y-%m-%d %H:%M')],
]
info_table = Table(info_data, colWidths=[5*cm, 12*cm])
info_table.setStyle(TableStyle([
    ('FONTNAME', (0, 0), (-1, -1), 'ArabicFont'),
    ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#1A5276')),
    ('TEXTCOLOR', (0, 0), (0, -1), colors.white),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ('ROWBACKGROUNDS', (1, 0), (1, -1), [colors.white, colors.HexColor('#EBF5FB')]),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
]))
story.append(info_table)
story.append(Spacer(1, 0.8*cm))

# Location photo if present
if report.location_photo:
    try:
        if os.path.exists(report.location_photo.path):
            story.append(Paragraph(ar('صورة تحديد الموقع:'), ParagraphStyle('Sub', parent=normal_arabic, fontSize=12, textColor=colors.HexColor('#1A5276'))))
            story.append(Spacer(1, 0.2*cm))
            story.append(RLImage(report.location_photo.path, width=10*cm, height=6.5*cm))
            story.append(Spacer(1, 0.5*cm))
    except Exception as e:
        print("Location photo exception:", e)

# Notes & Items
items = report.items.select_related('note', 'work_type').prefetch_related('images')
for item_num, item in enumerate(items, 1):
    wt_name = item.work_type.name if item.work_type else 'غير محدد'
    note_text = item.note.text if item.note else ''
    classification = item.work_classification or 'لا يوجد'

    if note_text:
        header_raw = f"{item_num}. {note_text} | نوع العمل: {wt_name} | تصنيف: {classification}"
    else:
        header_raw = f"{item_num}. نوع العمل: {wt_name} | تصنيف: {classification}"

    story.append(Paragraph(
        ar(header_raw),
        ParagraphStyle('NoteTitle', parent=normal_arabic,
                       fontSize=11, alignment=TA_RIGHT,
                       textColor=colors.HexColor('#1A5276'),
                       spaceAfter=6, spaceBefore=10)
    ))

    images = list(item.images.all())
    if images:
        img_width = 8*cm
        img_height = 5.5*cm
        row_imgs = []
        for img_obj in images:
            try:
                if os.path.exists(img_obj.image.path):
                    row_imgs.append(RLImage(img_obj.image.path, width=img_width, height=img_height))
            except Exception as e:
                print("Image error:", e)

        for i in range(0, len(row_imgs), 2):
            row = row_imgs[i:i+2]
            if len(row) == 1:
                row.append('')
            img_table = Table([row], colWidths=[8.5*cm, 8.5*cm])
            img_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ]))
            story.append(img_table)
            story.append(Spacer(1, 0.3*cm))

doc.build(story)
pdf_data = buffer.getvalue()
print("Generated PDF size:", len(pdf_data), "bytes")
with open("test_output.pdf", "wb") as f:
    f.write(pdf_data)
print("Saved to test_output.pdf successfully!")
