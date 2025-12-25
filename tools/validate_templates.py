import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from app import app
from flask import render_template
import traceback

failures = []
with app.test_request_context():
    for root, dirs, files in os.walk(os.path.join(os.path.dirname(__file__), '..', 'templates')):
        for f in files:
            if not f.endswith('.html'):
                continue
            tpl = os.path.relpath(os.path.join(root, f), os.path.join(os.path.dirname(__file__), '..', 'templates'))
            tpl = tpl.replace('\\', '/')
            try:
                render_template(tpl)
                print('OK', tpl)
            except Exception as e:
                print('FAIL', tpl, type(e).__name__, str(e)[:200])
                failures.append((tpl, traceback.format_exc()))

if failures:
    print('\nSUMMARY: Failures detected:')
    for tpl, tb in failures:
        print('---', tpl)
        print(tb)
else:
    print('\nAll templates rendered successfully (in test context).')