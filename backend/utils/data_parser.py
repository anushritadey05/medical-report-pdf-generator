import pandas as pd
import json

def parse_lab_results(file_path):
    """
    Parse CSV or Excel file containing lab results
    Returns:  dict with parsed data
    """
    try: 
        # Check file extension
        if file_path. endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file_path.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(file_path)
        else:
            raise ValueError("Unsupported file format.  Use CSV or Excel.")
        
        # Convert to dictionary
        lab_data = []
        for _, row in df. iterrows():
            lab_data.append({
                'test_name': row. get('Test Name', row.get('test_name', 'Unknown')),
                'value': row.get('Value', row.get('value', 'N/A')),
                'unit': row.get('Unit', row.get('unit', '')),
                'reference_range':  row.get('Reference Range', row.get('reference_range', '')),
                'status': row.get('Status', row.get('status', 'Normal'))
            })
        
        return {
            'success': True,
            'data':  lab_data,
            'total_tests': len(lab_data)
        }
    
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def validate_lab_data(lab_data):
    """Validate lab results data structure"""
    required_fields = ['test_name', 'value']
    
    for item in lab_data:
        for field in required_fields:
            if field not in item:
                return False, f"Missing required field: {field}"
    
    return True, "Valid"