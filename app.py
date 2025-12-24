from flask import Flask, render_template, request, jsonify, send_from_directory, abort
import json
import os
from data import disease_rules

app = Flask(
    __name__,
    static_folder='static',
    static_url_path='/static',
    template_folder='templates'
)

# ---------------------------
# FAVICON FIX (IMPORTANT)
# ---------------------------
@app.route('/favicon.ico')
def favicon():
    return "", 204


# ---------------------------
# SAFE JSON LOADING
# ---------------------------
try:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(base_dir, 'emergency_data.json')
    with open(json_path) as f:
        emergency_data = json.load(f)
except Exception as e:
    emergency_data = {}
    print("Error loading emergency data:", e)


# ---------------------------
# AUTH / HOME ROUTES
# ---------------------------
@app.route('/')
def login_page():
    return render_template('Login.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    return jsonify({"message": f"Login successful for user: {username}"})


@app.route('/index')
def index():
    return render_template('index.html')


# ---------------------------
# EMERGENCY MODULE
# ---------------------------
@app.route('/emergency')
def emergency_index():
    return render_template('Emergency.html')


@app.route('/get_emergency_steps', methods=['POST'])
def get_emergency_steps():
    data = request.json
    emergency_type = data.get("emergency")
    steps = emergency_data.get(emergency_type, ["No information available."])
    return jsonify({"steps": steps})


@app.route('/get_emergency_list')
def get_emergency_list():
    return jsonify({"emergencies": list(emergency_data.keys())})


# ---------------------------
# HEALTH DETECTOR MODULE
# ---------------------------
@app.route("/health_detector", methods=["GET", "POST"])
def health_detector_index():
    if request.method == "POST":
        symptoms = request.form.getlist("symptoms")
        predicted_disease = detect_disease(symptoms)
        return render_template("HealthDetector.html", result=predicted_disease)

    return render_template("HealthDetector.html", result=None)


def detect_disease(symptoms):
    best_match = None
    max_match_count = 0

    symptoms_lower = [symptom.lower() for symptom in symptoms]

    for disease, rules in disease_rules.items():
        rules_lower = [rule.lower() for rule in rules]
        match_count = len(set(rules_lower) & set(symptoms_lower))

        if match_count > max_match_count and match_count > 0:
            max_match_count = match_count
            best_match = disease

    return best_match if best_match else "Could not determine a disease. Please consult a doctor."


# ---------------------------
# HEALTH RECOMMENDATION MODULE
# ---------------------------
@app.route('/health_recommendation', methods=['GET', 'POST'])
def health_recommendation_index():
    if request.method == 'POST':
        age = int(request.form['age'])
        weight = float(request.form['weight'])
        height = float(request.form['height'])
        activity_level = request.form['activity_level']

        recommendations = get_health_recommendation(
            age, weight, height, activity_level
        )
        return render_template(
            'HealthRecommendation.html',
            recommendations=recommendations
        )

    return render_template('HealthRecommendation.html', recommendations=None)


def get_health_recommendation(age, weight, height, activity_level):
    bmi = weight / ((height / 100) ** 2)
    recommendations = []

    if bmi < 18.5:
        recommendations.append("You are underweight.")
        recommendations.append("Diet: High-protein and calorie-dense food.")
        recommendations.append("Exercise: Strength training recommended.")
    elif 18.5 <= bmi < 24.9:
        recommendations.append("Your weight is normal.")
        recommendations.append("Diet: Balanced nutrition.")
        recommendations.append("Exercise: Cardio + strength training.")
    elif 25 <= bmi < 29.9:
        recommendations.append("You are overweight.")
        recommendations.append("Diet: Low-carb, high-fiber food.")
        recommendations.append("Exercise: Daily cardio + strength training.")
    else:
        recommendations.append("You are obese.")
        recommendations.append("Diet: Reduce sugar and processed foods.")
        recommendations.append("Exercise: Start with low-impact workouts.")

    if activity_level == "low":
        recommendations.append("Increase daily movement.")
    elif activity_level == "moderate":
        recommendations.append("Maintain current activity level.")
    else:
        recommendations.append("Excellent activity level. Keep it up!")

    recommendations.append("Hydration: 2–3 liters water daily.")
    recommendations.append("Sleep: 7–9 hours recommended.")
    recommendations.append("Stress: Practice meditation or yoga.")

    return recommendations


# ---------------------------
# NAVIGATION ROUTES
# ---------------------------
@app.route('/CareContribution')
def care_contribution():
    return render_template('contribution.html')


@app.route('/Appointment')
def appointment():
    return render_template('booking.html')


@app.route('/JoinCareConnect')
def join_care_connect():
    return render_template('connect.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/Reviews')
def reviews():
    return render_template('reviews.html')


@app.route('/Blog')
def blog():
    return render_template('blog-single.html')


@app.route('/PollutionMap')
def pollution_map():
    return render_template('404.html')


@app.route('/Reminder')
def reminder():
    return render_template('404.html')
