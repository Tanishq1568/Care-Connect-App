import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from app import app
app.testing = True
with app.test_client() as c:
    r = c.get('/__debug/index_diag')
    print('STATUS', r.status_code)
    print(r.get_data(as_text=True)[:4000])