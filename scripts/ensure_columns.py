import sqlite3
import shutil
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / 'recipes.db'
if not DB.exists():
    print('Database file not found at', DB)
    raise SystemExit(1)

bak = DB.with_suffix('.db.bak')
shutil.copy2(DB, bak)
print('Backup created at', bak)

conn = sqlite3.connect(str(DB))
cur = conn.cursor()

cur.execute("PRAGMA table_info(recipes)")
cols = [row[1] for row in cur.fetchall()]
print('Existing columns:', cols)

changes = []
if 'price' not in cols:
    cur.execute("ALTER TABLE recipes ADD COLUMN price REAL")
    changes.append('price')
if 'sizes' not in cols:
    cur.execute("ALTER TABLE recipes ADD COLUMN sizes TEXT")
    changes.append('sizes')
if 'fillings' not in cols:
    cur.execute("ALTER TABLE recipes ADD COLUMN fillings TEXT")
    changes.append('fillings')

conn.commit()
conn.close()
if changes:
    print('Added columns:', ', '.join(changes))
else:
    print('No changes needed; all columns present')
