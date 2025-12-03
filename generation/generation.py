"""Generación de hosts, logs y mantenimientos.

Reglas:
- hosts: hostname codifica país y entorno. Ej: LPIRL001
- logs: id_log,id_host,timestamp,request_type,response_time_ms,status_code,user
- maintenance: id_maintenance,id_host,date,type,duration_min,technician,notes

Las notas de mantenimiento intentan usar 'ollama' si está instalado; si no, se generan frases simples.
"""
import pandas as pd
import numpy as np
import random
import datetime
from pathlib import Path
from config.config import NUM_HOSTS, RANDOM_SEED

random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)

COUNTRIES = ["Ireland", "Italy", "Germany", "Chile", "Spain", "USA"]
OSS = ["Linux", "AIX", "Solaris", "Windows"]
ENV = ["Production", "Testing", "Development"]
REQUEST_TYPES = ["GET", "POST", "PUT", "DELETE"]
STATUS_CODES = [200, 201, 400, 401, 403, 404, 500]
MAINT_TYPES = ["Patch", "Incident", "Upgrade", "Security", "Network"]


def gen_logs(hosts_df, per_host_mean=200):
    logs = []
    start = datetime.datetime(2024, 1, 1, 0, 0, 0)
    end = datetime.datetime(2025, 10, 1, 0, 0, 0)
    for idx, row in hosts_df.iterrows():

        n = max(10, int(abs(int(random.gauss(per_host_mean, per_host_mean * 0.5)))))
        for _ in range(n):
            ts = start + datetime.timedelta(seconds=random.randint(0, int((end - start).total_seconds())))
            req = random.choices(REQUEST_TYPES, weights=[0.7, 0.15, 0.1, 0.05])[0]
            base = 100 if row['environment'] == 'Production' else 200
            
            resp = max(1, int(np.random.exponential(scale=base) + random.gauss(0, 50)))
            status = random.choices(STATUS_CODES, weights=[0.7, 0.05, 0.03, 0.03, 0.02, 0.15, 0.02])[0]
            user = f"user{random.randint(1, 999):03d}"
            logs.append({
                "id_host": int(idx) +1,
                "timestamp": ts.strftime('%Y-%m-%d %H:%M:%S'),
                "request_type": req,
                "response_time_ms": int(resp),
                "status_code": int(status),
                "user": user
            })
    return pd.DataFrame(logs)

def generate_note_with_ollama_stub():
    
    try:
        import ollama
        response = ollama.chat(model='phi', messages=[{
            'role': 'user',
            'content': (
                "Generate exactly short maintenance notes. "
                "Each note must be one sentence, under 12 words. "
                "No numbering or extra text. Example: 'Server rebooted successfully.'"
            )
        }])
        content = response.get('message', {}).get('content', '')
        
        note = content.strip().split('\n')[0]
        return note[:200]
    except Exception:
        opts = [
            "Server rebooted successfully.",
            "Applied security patch and verified.",
            "Replaced faulty NIC and tested connectivity.",
            "Updated TLS certificates.",
            "Performed kernel update and rebooted.",
            "Adjusted firewall rules.",
            "Checked disk health; replaced failing disk.",
            "Database service restarted after crash."
        ]
        return random.choice(opts)

def gen_maintenance(hosts_df, mean_per_host=3):
    maint = []
    start = datetime.datetime(2024, 1, 1)
    end = datetime.datetime(2025, 10, 1)

    for idx_host, row in hosts_df.iterrows():
        n = int(np.random.poisson(lam=mean_per_host))
        n = max(0, n)
        if n == 0:
            n = random.randint(0, 3)

        for _ in range(n):
            date = start + datetime.timedelta(seconds=random.randint(0, int((end - start).total_seconds())))
            mtype = random.choice(MAINT_TYPES)
            duration = random.randint(5, 420)
            tech = f"tech{random.randint(1, 50):03d}"
            notes = generate_note_with_ollama_stub()

            maint.append({
                "id_host": int(idx_host) + 1,  
                "date": date.strftime('%Y-%m-%d %H:%M:%S'),
                "type": mtype,
                "duration_min": int(duration),
                "technician": tech,
                "notes": notes
            })
    return pd.DataFrame(maint)



