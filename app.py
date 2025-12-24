from flask import Flask, render_template, request, jsonify
import json
import os

# ---------------------------
# SAFE IMPORT FOR DISEASE RULES
# ---------------------------
try:
    from data import disease_rules
except Exception as e:
    disease_rules = {}
    print("Disease rules load failed:", e)

app = Flask(
    __name__,
    static_folder='static',
    template_folder='templates'
)

# ---------------------------
# SAFE FAVICON (NO CRASH)
# ---------------------------
@app.route('/favicon.ico')
def favicon():
    return '', 204


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
    print("Emergency JSON load failed:", e)


# ---------------------------
# SAFE TEMPLATE RENDER HELPER
# ---------------------------
def safe_render(template, **context):
    try:
        return render_template(template, **context)
    except Exception as e:
        return f"Template error: {template} not found", 500


# ---------------------------
# ROUTES
# ---------------------------
@app.route('/')
def login_page():
    return safe_render('Login.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    return jsonify({"message": f"Login successful for {username}"})


@app.route('/index')
def index():
    return safe_render('index.html')


# ---------------------------
# EMERGENCY MODULE
# ---------------------------
@app.route('/emergency')
def emergency():
    return safe_render('Emergency.html')


@app.route('/get_emergency_steps', methods=['POST'])
def get_emergency_steps():
    data = request.json or {}
    emergency_type = data.get("emergency")
    steps = emergency_data.get(emergency_type, ["No data available"])
    return jsonify({"steps": steps})


@app.route('/get_emergency_list')
def get_emergency_list():
    return jsonify({"emergencies": list(emergency_data.keys())})


# ---------------------------
# HEALTH DETECTOR
# ---------------------------
@app.route("/health_detector", methods=["GET", "POST"])
def health_detector():
    result = None
    if request.method == "POST":
        symptoms = request.form.getlist("symptoms")
        result = detect_disease(symptoms)
    return safe_render("HealthDetector.html", result=result)


def detect_disease(symptoms):
    symptoms = [s.lower() for s in symptoms]

    best_match = None
    max_match = 0

    for disease, rules in disease_rules.items():
        match = len(set(symptoms) & set([r.lower() for r in rules]))
        if match > max_match:
            max_match = match
            best_match = disease

    return best_match or "Consult a doctor"


# ---------------------------
# HEALTH RECOMMENDATION
# ---------------------------
@app.route('/health_recommendation', methods=['GET', 'POST'])
def health_recommendation():
    if request.method == 'POST':
        try:
            age = int(request.form['age'])
            weight = float(request.form['weight'])
            height = float(request.form['height'])
            activity = request.form['activity_level']
            rec = get_recommendation(age, weight, height, activity)
            return safe_render('HealthRecommendation.html', recommendations=rec)
        except:
            return "Invalid input", 400

    return safe_render('HealthRecommendation.html', recommendations=None)


def get_recommendation(age, weight, height, activity):
    bmi = weight / ((height / 100) ** 2)
    return [f"Your BMI is {round(bmi, 2)}"]


# ---------------------------
# NAVIGATION ROUTES
# ---------------------------
@app.route('/CareContribution')
def care_contribution():
    return safe_render('contribution.html')


@app.route('/Appointment')
def appointment():
    return safe_render('booking.html')


@app.route('/JoinCareConnect')
def join():
    return safe_render('connect.html')


@app.route('/contact')
def contact():
    return safe_render('contact.html')


@app.route('/Reviews')
def reviews():
    return safe_render('reviews.html')


@app.route('/Blog')
def blog():
    return safe_render('blog-single.html')


@app.route('/PollutionMap')
def pollution():
    return safe_render('404.html')


@app.route('/Reminder')
def reminder():
    return safe_render('404.html')
