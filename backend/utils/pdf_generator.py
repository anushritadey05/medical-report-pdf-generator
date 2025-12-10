from reportlab.lib. pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib. styles import getSampleStyleSheet, ParagraphStyle
from reportlab. lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
import os

def generate_medical_report_pdf(patient_data, lab_results, summary, output_path):
    """
    Generate a professional medical report PDF
    """
    try:
        # Create PDF document
        doc = SimpleDocTemplate(output_path, pagesize=letter,
                                rightMargin=72, leftMargin=72,
                                topMargin=72, bottomMargin=18)
        
        # Container for the 'Flowable' objects
        elements = []
        
        # Styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2C3E50'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#3498DB'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        )
        
        # Title
        title = Paragraph("MEDICAL LABORATORY REPORT", title_style)
        elements.append(title)
        elements.append(Spacer(1, 0.2*inch))
        
        # Report Date
        date_text = f"Report Date: {datetime.now().strftime('%B %d, %Y')}"
        date_para = Paragraph(date_text, styles['Normal'])
        elements.append(date_para)
        elements.append(Spacer(1, 0.3*inch))
        
        # Patient Information Section
        patient_heading = Paragraph("Patient Information", heading_style)
        elements.append(patient_heading)
        
        patient_info = [
            ['Name:', patient_data.get('name', 'N/A')],
            ['Age:', str(patient_data.get('age', 'N/A'))],
            ['Gender:', patient_data.get('gender', 'N/A')],
            ['Phone:', patient_data.get('phone', 'N/A')],
            ['Email:', patient_data.get('email', 'N/A')],
        ]
        
        patient_table = Table(patient_info, colWidths=[2*inch, 4*inch])
        patient_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ECF0F1')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#2C3E50')),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
        ]))
        elements.append(patient_table)
        elements.append(Spacer(1, 0.4*inch))
        
        # Lab Results Section
        lab_heading = Paragraph("Laboratory Test Results", heading_style)
        elements.append(lab_heading)
        
        # Lab results table
        lab_table_data = [['Test Name', 'Value', 'Unit', 'Reference Range', 'Status']]
        
        for item in lab_results:
            status = item.get('status', 'Normal')
            lab_table_data.append([
                item. get('test_name', 'N/A'),
                str(item.get('value', 'N/A')),
                item.get('unit', ''),
                item.get('reference_range', 'N/A'),
                status
            ])
        
        lab_table = Table(lab_table_data, colWidths=[2*inch, 1*inch, 0.8*inch, 1.5*inch, 1*inch])
        
        # Style the lab table
        table_style = [
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498DB')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#BDC3C7')),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8F9FA')])
        ]
        
        # Highlight abnormal results
        for idx, item in enumerate(lab_results, start=1):
            if item.get('status', '').lower() != 'normal':
                table_style.append(('TEXTCOLOR', (4, idx), (4, idx), colors.red))
                table_style. append(('FONTNAME', (4, idx), (4, idx), 'Helvetica-Bold'))
        
        lab_table.setStyle(TableStyle(table_style))
        elements.append(lab_table)
        elements.append(Spacer(1, 0.4*inch))
        
        # Summary Section
        summary_heading = Paragraph("Clinical Summary", heading_style)
        elements.append(summary_heading)
        
        summary_style = ParagraphStyle(
            'Summary',
            parent=styles['Normal'],
            fontSize=11,
            leading=14,
            textColor=colors.HexColor('#34495E'),
            alignment=TA_LEFT
        )
        summary_para = Paragraph(summary. replace('\n', '<br/>'), summary_style)
        elements.append(summary_para)
        elements.append(Spacer(1, 0.5*inch))
        
        # Footer
        footer_text = "This is a computer-generated report.  For medical advice, please consult your physician."
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=9,
            textColor=colors.grey,
            alignment=TA_CENTER,
            fontName='Helvetica-Oblique'
        )
        footer_para = Paragraph(footer_text, footer_style)
        elements.append(footer_para)
        
        # Build PDF
        doc. build(elements)
        
        return {
            'success': True,
            'path': output_path
        }
    
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }