#!/bin/bash
set -e

SERVICE_NAME="xuidbweb"
INSTALL_DIR="/etc/$SERVICE_NAME"
MAIN_FILE="main.py"
CONF_FILE="xuidbweb.conf"
PYTHON_PATH=$(which python3)

read -p "Enter host [default 0.0.0.0]: " HOST
HOST=${HOST:-0.0.0.0}

read -p "Enter port [default 8000]: " PORT
PORT=${PORT:-8000}

echo "[*] Creating $INSTALL_DIR..."
sudo mkdir -p "$INSTALL_DIR"

if [ ! -f "$MAIN_FILE" ]; then
    echo "[!] $MAIN_FILE not found!"
    exit 1
fi
sudo cp "$MAIN_FILE" "$INSTALL_DIR/"
sudo chmod 700 "$INSTALL_DIR"
sudo chmod 700 "$INSTALL_DIR/$MAIN_FILE"

echo "[*] Creating config file..."
sudo tee "$INSTALL_DIR/$CONF_FILE" > /dev/null <<EOL
host=$HOST
port=$PORT
EOL
sudo chmod 600 "$INSTALL_DIR/$CONF_FILE"

SERVICE_FILE="/etc/systemd/system/$SERVICE_NAME.service"
echo "[*] Creating service..."
sudo tee "$SERVICE_FILE" > /dev/null <<EOL
[Unit]
Description=$SERVICE_NAME - VPN User Info API (UUID-Based)
After=network.target

[Service]
ExecStart=$PYTHON_PATH $INSTALL_DIR/$MAIN_FILE
Restart=always
User=root
WorkingDirectory=$INSTALL_DIR
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOL

sudo systemctl daemon-reload
sudo systemctl enable "$SERVICE_NAME"
sudo systemctl start "$SERVICE_NAME"

echo "[+] Installed! Running on $HOST:$PORT"
