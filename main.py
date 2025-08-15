# ================================================
# Project: xuidbweb - UUID-based VPN Config API
# Author: CyberMafiaHQ (https://github.com/CyberMafiaHQ/xuidbweb)
# Description: Simple Python API that returns VLESS or VMess config links
#              based on UUID input. Useful for client-side VPN apps.
# License: MIT
# ================================================

#!/usr/bin/env python3
print("This program running as a service!")
import sqlite3
import json
from datetime import datetime
from flask import Flask, jsonify
import os

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "xuidbweb.conf")

host = "0.0.0.0"
port = 8000

if os.path.exists(CONFIG_PATH):
    with open(CONFIG_PATH, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            key, value = line.split("=", 1)
            key = key.strip().lower()
            value = value.strip()
            if key == "host":
                host = value
            elif key == "port":
                port = int(value)
                
DB_PATH = '/etc/x-ui/x-ui.db'

def get_client_info(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("SELECT settings FROM inbounds")
    rows = c.fetchall()

    found_client = None

    for row in rows:
        settings_json = row[0]
        try:
            settings = json.loads(settings_json)
            clients = settings.get("clients", [])
            for client in clients:
                if client.get('id', '').strip().lower() == user_id.strip().lower():
                    found_client = client
                    break
        except Exception:
            continue
        if found_client:
            break

    if not found_client:
        return {"status": "not_found"}

    email = found_client.get('email')
    expiry_ts = found_client.get('expiryTime', 0)
    expiry_str = (
        datetime.utcfromtimestamp(expiry_ts).strftime('%Y-%m-%d %H:%M:%S')
        if expiry_ts > 0 else "no expiry"
    )
    total_gb = found_client.get('totalGB', 0)
    sub_id = found_client.get('subId')
    enable = found_client.get('enable')

    c.execute("SELECT up, down, total, expiry_time FROM client_traffics WHERE email = ?", (email,))
    traffic_row = c.fetchone()
    if traffic_row:
        upload = traffic_row[0] or 0
        download = traffic_row[1] or 0
        total_bytes = traffic_row[2] or 0
        expire_ts_db = traffic_row[3] or 0
        used_gb = round((upload + download) / (1024 ** 3), 2)
        upload_gb = round(upload / (1024 ** 3), 2)
        download_gb = round(download / (1024 ** 3), 2)
        total_limit_gb = round(total_bytes / (1024 ** 3), 2) if total_bytes > 0 else total_gb
        expiry_str_db = (
            datetime.utcfromtimestamp(expire_ts_db).strftime('%Y-%m-%d %H:%M:%S')
            if expire_ts_db > 0 else expiry_str
        )
    else:
        upload_gb = download_gb = used_gb = 0.0
        total_limit_gb = total_gb
        expiry_str_db = expiry_str
    vless_link = f"vless://{user_id}@[your config here]{email}"
    return {
        "status": "ok",
        "id": user_id,
        "email": email,
        "expire_at": expiry_str_db,
        "total_gb": total_limit_gb,
        "used_gb": used_gb,
        "upload_gb": upload_gb,
        "download_gb": download_gb,
        "sub_id": sub_id,
        "enable": enable,
        "vless_link": vless_link
    }

app = Flask(__name__)

@app.route('/api/user/<uuid>', methods=['GET'])
def api_user(uuid):
    data = get_client_info(uuid)
    return jsonify(data)

@app.route('/api/ping', methods=['GET'])
def ping():
    return jsonify({"status": "ok", "message": "API is working ✅"})

if __name__ == '__main__':
    print(f"Running on {host}:{port}")
    app.run(host=host, port=port)