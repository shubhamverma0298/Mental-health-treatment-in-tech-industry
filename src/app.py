import os
import sys
import pandas as pd
from flask import Flask, request, jsonify, render_template

# --- Add the project root to the Python path ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# ----------------------------------------------------

from src.models.predict import load_model, make_prediction
from src.utils.helpers import helper # Import the helper function

# --- Define constants for the application ---
app = Flask(__name__)
MODEL_PATH = os.path.join('models', 'trained_model.pkl')

# Define the exact column order used during model training
TRAINING_COLUMNS = [
    'Age', 'Gender', 'Country', 'self_employed', 'family_history', 
    'work_interfere', 'no_employees', 'remote_work', 'tech_company', 
    'benefits', 'care_options', 'wellness_program', 'seek_help', 
    'anonymity', 'leave', 'mental_health_consequence', 
    'phys_health_consequence', 'coworkers', 'supervisor', 
    'mental_health_interview', 'phys_health_interview', 
    'mental_vs_physical', 'obs_consequence'
]
# -------------------------------------------

@app.route('/', methods=['GET', 'POST'])
def home():
    prediction_result = None
    error_message = None
    if request.method == 'POST':
        try:
            # Server-side validation for the 'Age' field
            age_str = request.form.get('Age')
            if not age_str:
                raise ValueError("Age is a required field.")
            
            # Get form data using snake_case to match form.html
            age = int(age_str)
            country = int(request.form.get('Country'))
            gender = int(request.form.get('Gender'))
            self_employed = int(request.form.get('self_employed'))
            family_history = int(request.form.get('family_history'))
            work_interfere = int(request.form.get('work_interfere'))
            no_employees = int(request.form.get('no_employees'))
            remote_work = int(request.form.get('remote_work'))
            tech_company = int(request.form.get('tech_company'))
            benefits = int(request.form.get('benefits'))
            care_options = int(request.form.get('care_options'))
            wellness_program = int(request.form.get('wellness_program'))
            seek_help = int(request.form.get('seek_help'))
            anonymity = int(request.form.get('anonymity'))
            leave = int(request.form.get('leave'))
            mental_health_consequence = int(request.form.get('mental_health_consequence'))
            phys_health_consequence = int(request.form.get('phys_health_consequence'))
            coworkers = int(request.form.get('coworkers'))
            supervisor = int(request.form.get('supervisor'))
            mental_health_interview = int(request.form.get('mental_health_interview'))
            phys_health_interview = int(request.form.get('phys_health_interview'))
            mental_vs_physical = int(request.form.get('mental_vs_physical'))
            obs_consequence = int(request.form.get('obs_consequence'))
            
            trained_model = load_model(model_path=MODEL_PATH)
            
            # Create a dictionary for the DataFrame
            feature_dict = {
                'Age': [age], 'Country': [country], 'Gender': [gender], 
                'self_employed': [self_employed], 'family_history': [family_history],
                'work_interfere': [work_interfere], 
                'no_employees': [no_employees], 'remote_work': [remote_work], 
                'tech_company': [tech_company], 'benefits': [benefits], 
                'care_options': [care_options], 'wellness_program': [wellness_program], 
                'seek_help': [seek_help], 'anonymity': [anonymity], 'leave': [leave], 
                'mental_health_consequence': [mental_health_consequence],
                'phys_health_consequence': [phys_health_consequence], 
                'coworkers': [coworkers], 'supervisor': [supervisor],
                'mental_health_interview': [mental_health_interview], 
                'phys_health_interview': [phys_health_interview],
                'mental_vs_physical': [mental_vs_physical], 
                'obs_consequence': [obs_consequence]
            }
            input_data = pd.DataFrame(feature_dict)

            # Reorder columns to match the training order
            input_data = input_data[TRAINING_COLUMNS]
            
            prediction = make_prediction(model=trained_model, input_data=input_data)
            prediction_result = 'Yes' if prediction[0] == 1 else 'No'
        except Exception as e:
            error_message = str(e)
            
    return render_template('form.html', prediction_result=prediction_result, error_message=error_message)
           
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        input_data = pd.DataFrame([data])
        
        # Ensure 'treatment' is not in the prediction data for the API endpoint as well
        if 'treatment' in input_data.columns:
            input_data = input_data.drop(columns=['treatment'])
        
        # Reorder columns for the API endpoint as well
        input_data = input_data[TRAINING_COLUMNS]

        trained_model = load_model(model_path=MODEL_PATH)
        prediction = make_prediction(model=trained_model, input_data=input_data)
        
        result = 'Yes' if prediction[0] == 1 else 'No'
        return jsonify({'prediction': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# The if __name__ == '__main__': block has been removed for production.
# The server will be started by a production server like Gunicorn.
# To run the app locally for development, use the command:
# flask run --host=localhost --port=5000
# or set FLASK_APP=src/app.py and then run flask run
