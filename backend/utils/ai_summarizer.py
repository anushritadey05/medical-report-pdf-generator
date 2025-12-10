import openai
import os

def generate_summary(lab_results, patient_info):
    """
    Generate AI summary of lab results (Optional - requires OpenAI API key)
    Falls back to basic summary if API key not available
    """
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key: 
        # Fallback:  Basic summary without AI
        return generate_basic_summary(lab_results, patient_info)
    
    try:
        openai.api_key = api_key
        
        # Prepare prompt
        lab_text = "\n".join([
            f"{item['test_name']}: {item['value']} {item. get('unit', '')} (Ref: {item.get('reference_range', 'N/A')})"
            for item in lab_results
        ])
        
        prompt = f"""
        Patient: {patient_info. get('name', 'Unknown')}, Age: {patient_info.get('age', 'N/A')}, Gender: {patient_info.get('gender', 'N/A')}
        
        Lab Results: 
        {lab_text}
        
        Please provide a brief medical summary of these lab results, highlighting any abnormal values and their potential significance.
        Keep it professional and concise.
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a medical assistant helping to summarize lab results. "},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        print(f"AI Summary Error: {e}")
        return generate_basic_summary(lab_results, patient_info)


def generate_basic_summary(lab_results, patient_info):
    """Generate a basic summary without AI"""
    abnormal_count = sum(1 for item in lab_results if item. get('status', '').lower() != 'normal')
    total_tests = len(lab_results)
    
    summary = f"Lab Report Summary for {patient_info.get('name', 'Patient')}\n\n"
    summary += f"Total Tests Performed: {total_tests}\n"
    summary += f"Abnormal Results: {abnormal_count}\n"
    summary += f"Normal Results: {total_tests - abnormal_count}\n\n"
    
    if abnormal_count > 0:
        summary += "Abnormal Test Results:\n"
        for item in lab_results:
            if item.get('status', '').lower() != 'normal':
                summary += f"- {item['test_name']}: {item['value']} {item.get('unit', '')} "
                summary += f"(Expected: {item.get('reference_range', 'N/A')})\n"
    else:
        summary += "All test results are within normal ranges."
    
    return summary