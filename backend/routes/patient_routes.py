from flask import Blueprint, request, jsonify
from models.patient import db, Patient

patient_bp = Blueprint('patient', __name__)

@patient_bp.route('/patients', methods=['GET'])
def get_patients():
    """Get all patients"""
    try:
        patients = Patient.query.all()
        return jsonify({
            'success': True,
            'patients': [patient.to_dict() for patient in patients]
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error':  str(e)}), 500


@patient_bp.route('/patients/<int:patient_id>', methods=['GET'])
def get_patient(patient_id):
    """Get single patient by ID"""
    try: 
        patient = Patient.query. get_or_404(patient_id)
        return jsonify({
            'success': True,
            'patient': patient.to_dict()
        }), 200
    except Exception as e: 
        return jsonify({'success': False, 'error': str(e)}), 404


@patient_bp.route('/patients', methods=['POST'])
def create_patient():
    """Create new patient"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'age', 'gender']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        patient = Patient(
            name=data['name'],
            age=data['age'],
            gender=data['gender'],
            phone=data.get('phone', ''),
            email=data. get('email', ''),
            address=data.get('address', ''),
            medical_history=data.get('medical_history', '')
        )
        
        db.session.add(patient)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'patient': patient.to_dict(),
            'message': 'Patient created successfully'
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@patient_bp.route('/patients/<int:patient_id>', methods=['PUT'])
def update_patient(patient_id):
    """Update patient information"""
    try:
        patient = Patient.query.get_or_404(patient_id)
        data = request.get_json()
        
        # Update fields
        patient.name = data.get('name', patient.name)
        patient.age = data.get('age', patient.age)
        patient.gender = data.get('gender', patient.gender)
        patient.phone = data.get('phone', patient.phone)
        patient.email = data.get('email', patient.email)
        patient.address = data.get('address', patient.address)
        patient.medical_history = data.get('medical_history', patient.medical_history)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'patient': patient.to_dict(),
            'message': 'Patient updated successfully'
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error':  str(e)}), 500


@patient_bp.route('/patients/<int:patient_id>', methods=['DELETE'])
def delete_patient(patient_id):
    """Delete patient"""
    try: 
        patient = Patient.query. get_or_404(patient_id)
        db.session. delete(patient)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message':  'Patient deleted successfully'
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500