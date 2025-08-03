# 🔐 VPN User Info API (UUID-Based)

This is a simple REST API built with Python (Flask) to serve VPN user subscription information based on a UUID from X-UI(https://github.com/MHSanaei/3x-ui) database.

## 📌 Overview

Users send their UUID via the API endpoint, and receive a JSON response containing:

- ✅ Account status
- 📩 Email
- 📅 Expiration date
- 📊 Used, uploaded, and downloaded data (in GB)
- 🔗 VLESS or VMess connection link

## 🚀 How to Use

### Request:

```
GET /api/user/<uuid>
```

### Example:

```
GET https://api.vpnserver.com.com/api/user/ec**********************-d7fc889e01d3
```

### Sample Response:

```json
{
  "download_gb": 5.38,
  "email": "User1",
  "enable": true,
  "expire_at": "13/06/2025",
  "id": "ec**********************-d7fc889e01d3",
  "status": "ok",
  "sub_id": "vomdl85bpz0zjtho",
  "total_gb": 0,
  "upload_gb": 0.15,
  "used_gb": 5.53,
  "vless_link": "vless://ec**********************-d7fc889e01d3@vpn.server.com:443?...#User1"
}
```

## ⚙️ Installation

1. Clone the repo:

```bash
git clone https://github.com/CyberMafiaHQ/xuidbweb.git
cd xuidbweb
```

2. Install dependencies:

```bash
pip install flask
```

3. Run the server:

```bash
python main.py
```

---

## 📝 Notes

- This API is stateless and works solely by querying with UUIDs.
- You can connect it to a database or JSON file depending on your needs.
- Designed to work perfectly with custom VPN Android apps.


Made with ❤️ by Shadow Commander
