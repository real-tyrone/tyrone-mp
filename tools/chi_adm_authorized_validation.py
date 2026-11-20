from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
def authorized_current(path):
    path=str(path).replace('\\','/')
    if path.startswith(str(ROOT).replace('\\','/')+'/'):path=path[len(str(ROOT))+1:]
    records=json.loads((ROOT/'tools/chi_adm_authorized_migrations.json').read_text(encoding='utf-8'))
    entry=records.get(path)
    return bool(entry and entry['reason'] and hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==entry['sha256'])
