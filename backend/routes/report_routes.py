from flask import Blueprint, request, jsonify, send_file
from models.patient import db, Patient, Report
from utils.data_parser import parse_lab_results
from utils.ai_summarizer import generate_summary
from utils.pdf_generator import generate_medical_report_pdf
import os
import json
from datetime import datetime

report_bp = Blueprint('report', __name__)

# Ensure uploads and reports directories exist
UPLOAD_FOLDER = 'uploads'
REPORTS_FOLDER = 'reports'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORTS_FOLDER, exist_ok=True)


@report_bp.route('/upload-lab-results', methods=['POST'])
def upload_lab_results():
    """Upload and parse lab results file (CSV/Excel)"""
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '': 
            return jsonify({'success':  False, 'error': 'No file selected'}), 400
        
        # Save file
        filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{file.filename}"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # Parse lab results
        parsed_data = parse_lab_results(filepath)
        
        if not parsed_data['success']:
            return jsonify(parsed_data), 400
        
        return jsonify(parsed_data), 200
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@report_bp.route('/generate-report', methods=['POST'])
def generate_report():
    """Generate PDF report for a patient"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if 'patient_id' not in data or 'lab_results' not in data: 
            return jsonify({
                'success': False,
                'error': 'Missing patient_id or lab_results'
            }), 400
        
        patient_id = data['patient_id']
        lab_results = data['lab_results']
        
        # Get patient data
        patient = Patient.query. get_or_404(patient_id)
        patient_data = patient.to_dict()
        
        # Generate summary
        summary = generate_summary(lab_results, patient_data)
        
        # Generate PDF
        pdf_filename = f"report_{patient_id}_{datetime. now().strftime('%Y%m%d%H%M%S')}.pdf"
        pdf_path = os.path.join(REPORTS_FOLDER, pdf_filename)
        
        pdf_result = generate_medical_report_pdf(patient_data, lab_results, summary, pdf_path)
        
        if not pdf_result['success']:
            return jsonify(pdf_result), 500
        
        # Save report to database
        report = Report(
            patient_id=patient_id,
            report_type='Lab Results',
            lab_results=json.dumps(lab_results),
            summary=summary,
            pdf_path=pdf_path
        )
        
        db. session.add(report)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'report':  report.to_dict(),
            'summary': summary,
            'pdf_url': f'/api/reports/download/{report.id}',
            'message': 'Report generated successfully'
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@report_bp.route('/reports/<int:patient_id>', methods=['GET'])
def get_patient_reports(patient_id):
    """Get all reports for a patient"""
    try:
        reports = Report.query.filter_by(patient_id=patient_id).all()
        return jsonify({
            'success': True,
            'reports': [report. to_dict() for report in reports]
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@report_bp.route('/reports/download/<int:report_id>', methods=['GET'])
def download_report(report_id):
    """Download PDF report"""
    try:
        report = Report.query.get_or_404(report_id)
        
        if not os.path.exists(report.pdf_path):
            return jsonify({
                'success': False,
                'error': 'PDF file not found'
            }), 404
        
        return send_file(report.pdf_path, as_attachment=True, download_name=f'medical_report_{report_id}.pdf')
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500