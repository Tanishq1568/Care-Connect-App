from flask import Flask, render_template, request, jsonify, send_from_directory, abort
import json
import os
from data import disease_rules

app = Flask(__name__, 
           static_folder='static', 
           static_url_path='/static',
           template_folder='templates')

@app.route('/')
def login_page():
    return render_template('Login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    # Add authentication logic here
    return jsonify({"message": "Login successful for user: {}".format(username)})

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/static/img/favicon.ico')
def favicon():
    # Robust favicon serving: use absolute paths and handle exceptions to avoid 500 errors
    try:
        static_root = app.static_folder if os.path.isabs(app.static_folder) else os.path.join(app.root_path, app.static_folder)
        img_dir = os.path.join(static_root, 'img')
        ico_path = os.path.join(img_dir, 'favicon.ico')
        png_path = os.path.join(img_dir, 'favicon.ico')
        if os.path.exists(ico_path):
            return send_from_directory(img_dir, 'favicon.ico', mimetype='image/vnd.microsoft.icon')
        if os.path.exists(png_path):
            return send_from_directory(img_dir, 'favicon.png', mimetype='image/png')
    except Exception:
        app.logger.exception("Error serving favicon")
    # If file not found or error occurred, return 404 so we don't return a 500
    abort(404)

# Emergency Module
with open('emergency_data.json') as f:
    emergency_data = json.load(f)

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

# Health Detector Module
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
    
    # Convert all submitted symptoms to lowercase for case-insensitive matching
    symptoms_lower = [symptom.lower() for symptom in symptoms]

    for disease, rules in disease_rules.items():
        # Convert disease rules to lowercase for comparison
        rules_lower = [rule.lower() for rule in rules]
        match_count = len(set(rules_lower) & set(symptoms_lower))

        if match_count > max_match_count and match_count > 0:
            max_match_count = match_count
            best_match = disease

    return best_match if best_match else "Could not determine a disease. Please consult a doctor."

# Health Recommendation Module
@app.route('/health_recommendation', methods=['GET', 'POST'])
def health_recommendation_index():
    if request.method == 'POST':
        age = int(request.form['age'])
        weight = float(request.form['weight'])
        height = float(request.form['height'])
        activity_level = request.form['activity_level']
        
        recommendations = get_health_recommendation(age, weight, height, activity_level)
        return render_template('HealthRecommendation.html', recommendations=recommendations)
    
    return render_template('HealthRecommendation.html', recommendations=None)

def get_health_recommendation(age, weight, height, activity_level):
    bmi = weight / ((height / 100) ** 2)
    recommendations = []

    if bmi < 18.5:
        recommendations.append("You are underweight.")
        recommendations.append("Diet: Consider a high-protein and calorie-dense diet with nuts, dairy, lean meats, and whole grains.")
        recommendations.append("Exercise: Focus on strength training to build muscle mass. Avoid excessive cardio.")
    elif 18.5 <= bmi < 24.9:
        recommendations.append("Your weight is normal.")
        recommendations.append("Diet: Maintain a balanced diet with lean proteins, whole grains, vegetables, and healthy fats.")
        recommendations.append("Exercise: Incorporate a mix of cardio, strength training, and flexibility exercises.")
    elif 25 <= bmi < 29.9:
        recommendations.append("You are overweight.")
        recommendations.append("Diet: Focus on a low-carb, high-fiber diet with more vegetables, lean proteins, and whole grains.")
        recommendations.append("Exercise: Engage in at least 30 minutes of cardio (running, cycling, swimming) and strength training.")
    else:
        recommendations.append("You are in the obese category.")
        recommendations.append("Diet: Reduce sugar and processed foods. Consider a structured weight-loss program with professional guidance.")
        recommendations.append("Exercise: Start with low-impact exercises like walking and gradually include strength training.")
    
    if activity_level == "low":
        recommendations.append("Activity: Increase your physical activity with daily walks, yoga, or home workouts. Aim for at least 30 minutes of movement daily.")
    elif activity_level == "moderate":
        recommendations.append("Activity: Maintain a moderate exercise routine with a mix of cardio, strength training, and flexibility exercises.")
    else:
        recommendations.append("Activity: Great job on staying active! Keep pushing your limits with varied workouts and proper recovery.")
    
    recommendations.append("Hydration: Ensure you drink at least 2-3 liters of water daily.")
    recommendations.append("Sleep: Aim for 7-9 hours of quality sleep to support overall health.")
    recommendations.append("Stress Management: Practice meditation, deep breathing, or hobbies to keep stress levels in check.")

    return recommendations

# Add routes for all navigation links
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
    return render_template('404.html')  # Placeholder - using 404.html as we don't have a specific template for this

@app.route('/Reminder')
def reminder():
    return render_template('404.html')  # Placeholder - using 404.html as we don't have a specific template for this

if __name__ == '__main__':
    app.run(debug=True)