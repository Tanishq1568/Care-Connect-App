from flask import Flask, render_template, request, jsonify, send_from_directory
import json
import os
import traceback
from werkzeug.exceptions import HTTPException

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
# REQUEST-LEVEL LOGGING
# ---------------------------
@app.before_request
def _log_request():
    # append each incoming request to render_error.log for quick diagnostics
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        log_path = os.path.join(base_dir, 'render_error.log')
        with open(log_path, 'a', encoding='utf-8') as lf:
            lf.write('\n' + ('-'*60) + '\n')
            ua = request.headers.get('User-Agent', '')
            lf.write(f"Incoming: {request.method} {request.path} from {request.remote_addr} UA: {ua}\n")
    except Exception as e:
        print('Failed to write request log:', e)

# ---------------------------
# SAFE FAVICON (SERVE STATIC)
# ---------------------------
@app.route('/favicon.ico')
def favicon():
    try:
        # Serve the favicon from static/img/favicon.ico if present
        favicon_dir = os.path.join(app.static_folder, 'img')
        return send_from_directory(favicon_dir, 'favicon.ico', mimetype='image/vnd.microsoft.icon')
    except Exception as e:
        print("Favicon serve failed:", e)
        traceback.print_exc()
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
# SAFE TEMPLATE RENDER HELPER (WITH LOGGING)
# ---------------------------
def safe_render(template, **context):
    """Render templates but log and record any exceptions with request context.

    This centralizes template error handling so we consistently write useful
    diagnostics to `render_error.log` (template name, request method/path, user-agent)
    and return a safe fallback or a helpful message in debug mode.
    """
    try:
        return render_template(template, **context)
    except Exception as e:
        tb = traceback.format_exc()
        print(f"Template render failed for {template}:", e)
        print(tb)

        # Prepare paths early so we can always attempt to log
        base_dir = os.path.dirname(os.path.abspath(__file__))
        log_path = os.path.join(base_dir, 'render_error.log')

        # Save the traceback to a log file for easier inspection, including request context
        try:
            with open(log_path, 'a', encoding='utf-8') as lf:
                lf.write('\n' + ('='*80) + '\n')
                lf.write(f'Template: {template}\n')
                try:
                    lf.write(f'Request: {request.method} {request.path}\n')
                    lf.write(f'User-Agent: {request.headers.get("User-Agent", "")}\n')
                except Exception:
                    lf.write('Request: <no request context>\n')
                lf.write(tb)
        except Exception as log_exc:
            print('Failed to write render_error.log:', log_exc)
            # Attempt backup log
            try:
                backup_path = os.path.join(base_dir, 'render_error_backup.log')
                with open(backup_path, 'a', encoding='utf-8') as blf:
                    blf.write('\n' + ('='*80) + '\n')
                    blf.write(f'Template: {template}\n')
                    try:
                        blf.write(f'Request: {request.method} {request.path}\n')
                    except Exception:
                        blf.write('Request: <no request context>\n')
                    blf.write(tb)
            except Exception as backup_exc:
                print('Failed to write backup render log:', backup_exc)

        # If running in debug mode, include traceback in the response for faster debugging
        try:
            if app.debug and request.remote_addr in ('127.0.0.1', '::1'):
                return f"Template error rendering {template}: {e}\n\n{tb}", 500
        except Exception:
            pass

        # For the index page, always return a minimal hardcoded fallback HTML so users don't see raw error text
        try:
            if template == 'index.html':
                fallback_html = ("<html><head><title>CareConnect</title></head>"
                                 "<body><h1>CareConnect</h1>"
                                 "<p>We encountered an internal error rendering the homepage; "
                                 "we're serving a temporary fallback while we fix this.</p>"
                                 "</body></html>")
                return fallback_html, 200
        except Exception:
            pass

        return f"Template error rendering {template}: check server logs (see render_error.log)", 500


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
    # Log that we entered the index handler
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        log_path = os.path.join(base_dir, 'render_error.log')
        with open(log_path, 'a', encoding='utf-8') as lf:
            lf.write('\n' + ('-'*60) + '\n')
            lf.write(f'INDEX_HANDLER_ENTER: {request.method} {request.path} from {request.remote_addr}\n')
    except Exception:
        pass

    # Immediate override: allow forcing index fallback via env var for trouble-shooting
    try:
        if os.environ.get('FORCE_INDEX_FALLBACK'):
            try:
                with open(log_path, 'a', encoding='utf-8') as lf:
                    lf.write('INDEX_HANDLER: FORCE_INDEX_FALLBACK enabled -> sending static fallback\n')
            except Exception:
                pass
            try:
                return send_from_directory(app.static_folder, 'fallback_index.html')
            except Exception:
                try:
                    with open(log_path, 'a', encoding='utf-8') as lf:
                        lf.write('INDEX_HANDLER: static fallback send_from_directory failed, trying template fallback\n')
                except Exception:
                    pass
                return render_template('fallback_index.html'), 200

    except Exception:
        pass

    # First: if startup detected index is broken, serve a static fallback page directly
    try:
        if globals().get('INDEX_BROKEN'):
            try:
                with open(log_path, 'a', encoding='utf-8') as lf:
                    lf.write('INDEX_HANDLER: INDEX_BROKEN -> sending static fallback\n')
            except Exception:
                pass
            # send static fallback file to avoid any template rendering
            try:
                return send_from_directory(app.static_folder, 'fallback_index.html')
            except Exception:
                try:
                    with open(log_path, 'a', encoding='utf-8') as lf:
                        lf.write('INDEX_HANDLER: static fallback send_from_directory failed, trying template fallback\n')
                except Exception:
                    pass
                return render_template('fallback_index.html'), 200
    except Exception as e:
        try:
            with open(log_path, 'a', encoding='utf-8') as lf:
                lf.write(f'INDEX_HANDLER_STARTUP_CHECK_EXCEPTION: {e}\n')
        except Exception:
            pass

    # Normal flow: attempt to render template safely
    result = safe_render('index.html')
    try:
        with open(log_path, 'a', encoding='utf-8') as lf:
            lf.write('INDEX_HANDLER_EXIT: safe_render returned\n')
    except Exception:
        pass
    return result


# ---------------------------
# EMERGENCY MODULE
# ---------------------------
@app.route('/emergency')
def emergency():
    return safe_render('Emergency.html')

# Backwards-compatible endpoint used by templates (some templates use 'emergency_index')
# Register the same view under the expected endpoint name so url_for('emergency_index') works
try:
    app.add_url_rule('/emergency', endpoint='emergency_index', view_func=emergency)
except AssertionError:
    # If endpoint already exists, ignore
    pass

# Backwards-compatible aliases will be registered later (after view functions are defined).

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
        # If the form sent a single comma-separated string, split it
        if len(symptoms) == 1 and isinstance(symptoms[0], str) and ',' in symptoms[0]:
            symptoms = [s.strip() for s in symptoms[0].split(',') if s.strip()]
        result = detect_disease(symptoms)
    return safe_render("HealthDetector.html", result=result)


# JSON API for AJAX requests from the client-side health detector
@app.route('/api/health_detector', methods=['POST'])
def api_health_detector():
    data = request.get_json(silent=True) or {}
    symptoms = data.get('symptoms')
    if symptoms is None:
        # also accept form-encoded POST
        symptoms = request.form.getlist('symptoms')
    # normalize string input
    if isinstance(symptoms, str):
        symptoms = [s.strip() for s in symptoms.split(',') if s.strip()]
    if not isinstance(symptoms, list):
        symptoms = []
    result = detect_disease(symptoms)
    return jsonify({'result': result})


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


# ---------------------------
# BACKWARDS-COMPATIBLE ENDPOINT ALIASES (REGISTERED LAST)
# ---------------------------
aliases = [
    ('/health_detector', 'health_detector_index', health_detector),
    ('/health_recommendation', 'health_recommendation_index', health_recommendation),
    ('/JoinCareConnect', 'join_care_connect', join),
    ('/PollutionMap', 'pollution_map', pollution),
]
for url, endpoint, view in aliases:
    try:
        app.add_url_rule(url, endpoint=endpoint, view_func=view)
    except AssertionError:
        pass


# ---------------------------
# DEBUG: expose render log in debug mode
# ---------------------------
import html as _html

@app.route('/__debug/render_log')
def _render_log():
    try:
        # Allow access when running locally (from 127.0.0.1 or ::1) even if debug is off,
        # to make it easier to fetch logs when debugging locally.
        if not app.debug:
            if request.remote_addr not in ('127.0.0.1', '::1'):
                return "Not available", 403
        base_dir = os.path.dirname(os.path.abspath(__file__))
        log_path = os.path.join(base_dir, 'render_error.log')
        with open(log_path, 'r', encoding='utf-8') as lf:
            data = lf.read()
        # Return last 10000 chars to avoid huge responses
        return f"<pre>{_html.escape(data[-10000:])}</pre>", 200
    except FileNotFoundError:
        return "No render log found", 404
    except Exception as e:
        print('Error reading render log:', e)
        traceback.print_exc()
        return "Error reading render log", 500


# ---------------------------
# TEMPORARY: open render log route (requires key) -- remove before production
# ---------------------------
@app.route('/__debug/render_log_open')
def _render_log_open():
    """Return render_error.log if the correct key is supplied. This is a temporary
    helper for environments where running shell commands is inconvenient. The key
    defaults to 'dev_debug' but can be overridden with the RENDER_LOG_KEY env var.
    """
    try:
        expected = os.environ.get('RENDER_LOG_KEY', 'dev_debug')
        key = request.args.get('key')
        if key != expected:
            return "Forbidden", 403
        base_dir = os.path.dirname(os.path.abspath(__file__))
        log_path = os.path.join(base_dir, 'render_error.log')
        with open(log_path, 'r', encoding='utf-8') as lf:
            data = lf.read()
        return f"<pre>{_html.escape(data[-20000:])}</pre>", 200
    except FileNotFoundError:
        return "No render log found", 404
    except Exception as e:
        print('Error reading open render log:', e)
        traceback.print_exc()
        return "Error reading render log", 500


@app.route('/__debug/index_diag')
def _index_diag():
    # Local-only diagnostic endpoint to return environment/runtime info helpful for debugging /index
    if request.remote_addr not in ('127.0.0.1', '::1'):
        return "Not available", 403
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        tmpl_path = os.path.join(base_dir, 'templates', 'index.html')
        fallback_tmpl = os.path.join(base_dir, 'templates', 'fallback_index.html')
        static_fallback = os.path.join(base_dir, 'static', 'fallback_index.html')
        info = {
            'INDEX_BROKEN': bool(globals().get('INDEX_BROKEN')),
            'app_debug': bool(app.debug),
            'template_exists': os.path.exists(tmpl_path),
            'template_size': os.path.getsize(tmpl_path) if os.path.exists(tmpl_path) else None,
            'fallback_template_exists': os.path.exists(fallback_tmpl),
            'static_fallback_exists': os.path.exists(static_fallback),
            'static_folder': app.static_folder,
            'template_folder': app.template_folder,
            'endpoints': sorted([e.endpoint for e in app.url_map.iter_rules()]),
        }
        return jsonify(info)
    except Exception as e:
        tb = traceback.format_exc()
        print('Index diag failed:', e)
        print(tb)
        return jsonify({'error': 'diag failed', 'traceback': tb}), 500


# ---------------------------
# DEBUG: validate index rendering (local-only)
# ---------------------------
@app.route('/__debug/validate_index')
def _validate_index():
    # Restrict to localhost so we don't leak internals in production
    if request.remote_addr not in ('127.0.0.1', '::1'):
        return "Not available", 403
    try:
        html = render_template('index.html')
        return "VALID_RENDER", 200
    except Exception as e:
        tb = traceback.format_exc()
        print('Index validation render failed:', e)
        print(tb)
        # Write the traceback to the render log for inspection
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            log_path = os.path.join(base_dir, 'render_error.log')
            with open(log_path, 'a', encoding='utf-8') as lf:
                lf.write('\n' + ('='*80) + '\n')
                lf.write('Validation render failed: index.html\n')
                lf.write(f'Request: {request.method} {request.path}\n')
                lf.write(tb)
        except Exception as log_exc:
            print('Failed to write validation to render_error.log:', log_exc)

        if app.debug:
            return f"VALIDATION_FAILED:\n{tb}", 500
        return "VALIDATION_FAILED, see render_error.log", 500

# ---------------------------
# DEBUG: local index diagnostic (returns traceback and saves it to render_error.log)
# ---------------------------
@app.route('/__debug/index_diag')
def index_diag():
    # Restrict to localhost
    if request.remote_addr not in ('127.0.0.1', '::1'):
        return "Not available", 403
    try:
        html = render_template('index.html')
        return jsonify({'status': 'ok', 'length': len(html)}), 200
    except Exception as e:
        tb = traceback.format_exc()
        print('Index diagnostic failed:', e)
        print(tb)
        # write to log
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            log_path = os.path.join(base_dir, 'render_error.log')
            with open(log_path, 'a', encoding='utf-8') as lf:
                lf.write('\n' + ('='*80) + '\n')
                lf.write('Diagnostic render failed: index.html\n')
                lf.write(f'Request: {request.method} {request.path}\n')
                lf.write(tb)
        except Exception as log_exc:
            print('Failed to write diagnostic to render_error.log:', log_exc)

        if app.debug:
            return tb, 500
        return jsonify({'status': 'error', 'error': str(e), 'traceback': tb[-4000:]}), 500

# ---------------------------
# STARTUP: proactively check index template rendering and record failures
# ---------------------------
INDEX_BROKEN = False
try:
    ctx = app.test_request_context()
    ctx.push()
    try:
        # Attempt a dry run render of index.html to catch syntax errors or template-time errors early
        render_template('index.html')
    finally:
        ctx.pop()
except Exception as e:
    INDEX_BROKEN = True
    tb = traceback.format_exc()
    print('Startup: index.html validation failed:', e)
    print(tb)
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        log_path = os.path.join(base_dir, 'render_error.log')
        with open(log_path, 'a', encoding='utf-8') as lf:
            lf.write('\n' + ('='*80) + '\n')
            lf.write('Startup validation failed: index.html\n')
            lf.write(tb)
    except Exception as log_exc:
        print('Failed to write startup validation to render_error.log:', log_exc)

# If INDEX_BROKEN is True, `index()` will serve the fallback instead of attempting to render the broken template

# GLOBAL ERROR HANDLER
# ---------------------------
@app.errorhandler(Exception)
def handle_exception(e):
    # If it's an HTTPException (404, 400, etc.), let Flask handle the response normally
    if isinstance(e, HTTPException):
        print("HTTP exception occurred:", e)
        return e

    # Log full traceback and write to render_error.log for diagnosis
    tb = traceback.format_exc()
    print("Unhandled Exception:", e)
    print(tb)
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        log_path = os.path.join(base_dir, 'render_error.log')
        with open(log_path, 'a', encoding='utf-8') as lf:
            lf.write('\n' + ('='*80) + '\n')
            lf.write(f'Unhandled exception on request: {request.method} {request.path}\n')
            lf.write(tb)
    except Exception as log_exc:
        print('Failed to write render_error.log:', log_exc)

    # If the client expects JSON or this is an API endpoint, return JSON-formatted error
    accept = request.headers.get('Accept', '')
    wants_json = request.is_json or 'application/json' in accept or request.path.startswith('/api')
    if wants_json:
        try:
            return jsonify({'error': 'Internal Server Error'}), 500
        except Exception:
            return "Internal Server Error", 500

    # For typical browser HTML requests, prefer serving a safe fallback to avoid a blank 500 page
    try:
        is_html = 'text/html' in accept or request.path in ('/', '/index')
    except Exception:
        is_html = False

    if is_html:
        # Try to render a simple fallback homepage instead of returning 500
        try:
            return render_template('fallback_index.html'), 200
        except Exception as fb_e:
            print('Fallback render failed in global handler:', fb_e)
            traceback.print_exc()
            try:
                with open(log_path, 'a', encoding='utf-8') as lf:
                    lf.write('\nFallback render in handler failed:\n')
                    lf.write(traceback.format_exc())
            except Exception:
                pass
            # As a final measure, return a minimal hardcoded fallback so the site remains usable
            try:
                fallback_html = ("<html><head><title>CareConnect</title></head>"
                                 "<body><h1>CareConnect</h1>"
                                 "<p>We encountered an internal error; "
                                 "a temporary fallback is being served while we fix it.</p>"
                                 "</body></html>")
                return fallback_html, 200
            except Exception:
                pass

    # In debug mode return traceback in response for immediate feedback
    try:
        if app.debug:
            return f"Unhandled exception: {e}\n\n{tb}", 500
    except Exception:
        pass

    return "Internal Server Error", 500


# ---------------------------
# WSGI-LEVEL EXCEPTION LOGGER (app-wide)
# ---------------------------
class WSGIErrorLogger:
    """Wrap the WSGI app to catch exceptions that occur before Flask's handlers
    and ensure we record full diagnostics (environ, headers, traceback) to a log.
    """
    def __init__(self, inner_app):
        self.inner_app = inner_app

    def __call__(self, environ, start_response):
        try:
            return self.inner_app(environ, start_response)
        except Exception as e:
            import traceback
            tb = traceback.format_exc()
            print("WSGI-level exception caught:", e)
            print(tb)
            try:
                base_dir = os.path.dirname(os.path.abspath(__file__))
                log_path = os.path.join(base_dir, 'render_error.log')
                with open(log_path, 'a', encoding='utf-8') as lf:
                    lf.write('\n' + ('='*80) + '\n')
                    lf.write('WSGI-level Exception on request\n')
                    # Basic request info
                    lf.write(f"REQUEST_METHOD: {environ.get('REQUEST_METHOD')}\n")
                    lf.write(f"PATH_INFO: {environ.get('PATH_INFO')}\n")
                    lf.write(f"QUERY_STRING: {environ.get('QUERY_STRING')}\n")
                    lf.write(f"REMOTE_ADDR: {environ.get('REMOTE_ADDR')}\n")
                    lf.write(f"HTTP_USER_AGENT: {environ.get('HTTP_USER_AGENT')}\n")
                    lf.write(f"HTTP_ACCEPT: {environ.get('HTTP_ACCEPT')}\n")
                    lf.write(tb)
            except Exception as log_exc:
                print('Failed to write WSGI-level log:', log_exc)
            # Re-raise so server sends a 500 as expected
            raise

# Install the wrapper
try:
    app.wsgi_app = WSGIErrorLogger(app.wsgi_app)
except Exception as wrap_exc:
    print('Failed to install WSGIErrorLogger:', wrap_exc)
