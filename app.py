from flask import Flask, request, jsonify, render_template
import joblib
import pandas as pd
from sklearn.tree import DecisionTreeRegressor  

app = Flask(__name__)

import os

current_directory = os.path.dirname(__file__)

model_path = os.path.join(current_directory, 'models', 'mymodel.pkl')

model = joblib.load(model_path)

def calculate_bmi(weight, height):
    """Calculate BMI given weight (kg) and height (cm)."""
    height_m = height / 100  
    bmi = weight / (height_m ** 2)
    return bmi

def diet_recommendation(age, gender, activity_level, bmi):
    """Provide diet recommendations based on age, gender, activity level, and BMI."""
    if gender == 'male':
        if age < 30:
            if bmi < 18.5:
                return "High protein, high calorie diet with healthy fats."
            elif 18.5 <= bmi <= 24.9:
                return "Balanced diet with protein, carbs, and healthy fats."
            else:
                return "Low calorie, high fiber diet with lean protein."
        elif 30 <= age <= 50:
            if bmi < 18.5:
                return "High protein, high calorie diet with moderate fats."
            elif 18.5 <= bmi <= 24.9:
                return "Balanced diet with focus on whole grains, vegetables, and lean protein."
            else:
                return "Low calorie, high fiber diet with lean protein and low carbs."
        else:
            return "High fiber, low fat diet with focus on lean protein and calcium-rich foods."
    else:
        if age < 30:
            if bmi < 18.5:
                return "High protein, high calorie diet with healthy fats."
            elif 18.5 <= bmi <= 24.9:
                return "Balanced diet with protein, carbs, and healthy fats."
            else:
                return "Low calorie, high fiber diet with lean protein."
        elif 30 <= age <= 50:
            if bmi < 18.5:
                return "High protein, high calorie diet with moderate fats."
            elif 18.5 <= bmi <= 24.9:
                return "Balanced diet with focus on whole grains, vegetables, and lean protein."
            else:
                return "Low calorie, high fiber diet with lean protein and low carbs."
        else:
            return "High fiber, low fat diet with focus on lean protein and calcium-rich foods."

def exercise_recommendation(age, activity_level, bmi):
    """Provide exercise recommendations based on age, activity level, and BMI."""
    if activity_level == 'low':
        if bmi < 18.5:
            return "Light activities like walking, yoga, and gentle stretching."
        elif 18.5 <= bmi <= 24.9:
            return "Moderate activities like brisk walking, cycling, and light aerobics."
        else:
            return "Low-impact activities like walking, swimming, and water aerobics."
    elif activity_level == 'moderate':
        if bmi < 18.5:
            return "Moderate activities like jogging, cycling, and aerobics."
        elif 18.5 <= bmi <= 24.9:
            return "Combination of cardio (running, cycling) and strength training."
        else:
            return "Moderate intensity workouts like brisk walking, stationary cycling, and low-impact aerobics."
    else:
        if bmi < 18.5:
            return "Intensive cardio and strength training with adequate rest."
        elif 18.5 <= bmi <= 24.9:
            return "High intensity workouts like HIIT, strength training, and running."
        else:
            return "Combination of low-impact cardio (elliptical, swimming) and strength training."
        

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    data = request.form.to_dict()
    data_df = pd.DataFrame([data])
    
    
    data_df['age'] = data_df['age'].astype(int)
    data_df['height'] = data_df['height'].astype(int)
    data_df['weight'] = data_df['weight'].astype(int)
    data_df['heartrate'] = data_df['heartrate'].astype(int)
    data_df['systolic_bp'] = data_df['systolic_bp'].astype(int)
    data_df['diastolic_bp'] = data_df['diastolic_bp'].astype(int)

    prediction = model.predict(data_df)

    age = int(data['age'])
    gender = data['gender']
    activity_level = data['activity_level']
    weight = int(data['weight'])
    height = int(data['height'])

    bmi = calculate_bmi(weight, height)
    diet = diet_recommendation(age, gender, activity_level, bmi)
    exercise = exercise_recommendation(age, activity_level, bmi)
    
    result = {
        'daily_caloric_intake': int(prediction[0][0]),
        'daily_steps_goal': int(prediction[0][1]),
        'ideal_sleep_duration': int(prediction[0][2]),
        'diet_recommendation': diet,
        'exercise_recommendation': exercise
    }
    
    return render_template('result.html', result=result)