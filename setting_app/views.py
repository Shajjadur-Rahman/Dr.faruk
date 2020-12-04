from django.shortcuts import render

import os
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, inch, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Frame
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from django.http import HttpResponse


def download_pdf_file(request):

    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'
    buffer = BytesIO()


    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30,
                            bottomMargin=18)
    doc.pagesize = landscape(A4)
    elements = []
    fontdiractory = "/vendors/webfonts/"
    pdfmetrics.registerFont(TTFont('bangla', os.path.join(fontdiractory, 'fa-solid-900.ttf')))
    styles = getSampleStyleSheet()
    style_centre = ParagraphStyle(name='centre', parent=styles['Heading2'],fontName='bangla', alignment=TA_CENTER)

    p = Paragraph("গণপ্রজাতন্ত্রী বাংলাদেশ", style_centre)
    elements.append(p)
    p = Paragraph("UEO Office", style_centre)
    elements.append(p)
    p = Paragraph("Upazilla: "+'Tongipara'+ " District: "+'Gopalgonj', style_centre)
    elements.append(p)

    data = [
        ['Govt. Primary School','','','','','','',''],
        ['Ebtedaiye Madrasha','','','','','','',''],
        ['গণপ্রজাতন্ত্রী বাংলাদেশ','','','','','','',''],
        ['Primary school','','','','','','',''],
        ['Primary school','','','','','','',''],
        ['Primary school','','','','','','','']
    ]

    # TODO: Get this line right instead of just copying it from the docs
    style = TableStyle([('ALIGN', (1, 1), (-2, -2), 'RIGHT'),
                        ('TEXTCOLOR', (1, 1), (-2, -2), colors.red),
                        ('VALIGN', (0, 0), (0, -1), 'TOP'),
                        ('TEXTCOLOR', (0, 0), (0, -1), colors.blue),
                        ('ALIGN', (0, -1), (-1, -1), 'CENTER'),
                        ('VALIGN', (0, -1), (-1, -1), 'MIDDLE'),
                        ('TEXTCOLOR', (0, -1), (-1, -1), colors.green),
                        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                        ])

    data2 = [[Paragraph(cell, style_centre) for cell in row] for row in data]
    t = Table(data2)
    t.setStyle(style)
    elements.append(t)

    doc.build(elements)
    response.write(buffer.getvalue())
    buffer.close()
    return response
