import sys
import os
import traceback
# Ensure project root (parent directory) is on sys.path so local modules can be imported
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
try:
    import app
    print('IMPORT_OK', repr(app))
except Exception:
    print('IMPORT_EXCEPTION')
    traceback.print_exc()