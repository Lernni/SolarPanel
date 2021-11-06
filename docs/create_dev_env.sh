#/bin/sh

# Abhängigkeiten installieren
sudo apt-get install -y python3-pip nodejs npm

# SolarModule einrichten
cd ../src/solar_module
python3 -m venv ./.venv
source ./.venv/bin/activate
pip3 install -r requirements.txt
deactivate
cd ../../docs

# WebSocket einrichten
cd ../src/web_socket/
npm install
cd ../../docs

# Frontend einrichten
cd ../src/frontend/
npm install
npm audit fix
cd ../../docs