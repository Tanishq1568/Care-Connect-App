import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from app import app
app.testing = True
resources = ['/static/css/style.css','/static/js/main.js','/favicon.ico','/index']
with app.test_client() as c:
    for r in resources:
        resp = c.get(r)
        print(r, resp.status_code, 'len', len(resp.get_data()))
        if resp.status_code != 200:
            print('BODY:', resp.get_data(as_text=True)[:500])