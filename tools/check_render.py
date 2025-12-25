import sys
import os
import traceback
# Ensure parent directory (project root) is on sys.path so app can be imported
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from app import app
from flask import render_template

ctx = app.test_request_context()
ctx.push()
try:
    html = render_template('index.html')
    print('RENDER_OK')
except Exception:
    print('RENDER_EXCEPTION')
    traceback.print_exc()
finally:
    ctx.pop()
