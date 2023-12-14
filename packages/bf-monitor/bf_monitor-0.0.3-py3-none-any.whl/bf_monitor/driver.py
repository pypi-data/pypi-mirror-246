import os
import requests
import time
from pathlib import Path
from .utils import StdTime

def Monitor(url, path):
    path = Path(path)
    assert path.exists(), f"[{path}] doesn't exist"
    previous_snapshot = set()

    def _poll():
        nonlocal previous_snapshot
        if not path.exists(): return 
        snapshot = set(os.listdir(path))
        if snapshot == previous_snapshot: return

        previous_snapshot = snapshot
        print(f"{StdTime.Timestamp()}: changed")
        print(snapshot)
        print("notifying server...")
        res = requests.post(url, json=dict(snapshot=list(snapshot)))
        c, t = res.status_code, res.text
        print(c, t)

    while True:
        try:
            _poll()
            time.sleep(3)
        except KeyboardInterrupt:
            print("killed")
            break
