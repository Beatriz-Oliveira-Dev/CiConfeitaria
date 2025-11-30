import sys
import os
import traceback

# Ensure project root is on sys.path so 'from app import app' works
HERE = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(HERE, '..'))
sys.path.insert(0, PROJECT_ROOT)

from app import app

try:
    with app.test_client() as c:
        resp = c.get('/')
        print('STATUS', resp.status_code)
        print(resp.get_data(as_text=True))
except Exception:
    traceback.print_exc()
