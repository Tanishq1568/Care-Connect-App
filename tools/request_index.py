import sys
import os
# Ensure project root is on sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from app import app
app.testing = True
with app.test_client() as c:
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        }
        r = c.get('/index', headers=headers)
        print('STATUS', r.status_code)
        text = r.get_data(as_text=True)
        print('LEN', len(text))
        print(text[:2000])
    except Exception:
        import traceback
        traceback.print_exc()