#!/bin/sh
sudo apt install python3 -y
sudo apt install python3-venv -y
sudo apt install mariadb-server -y
python3 -m venv ./fmeca-venv
source ./fmeca-venv/bin/activate
pip3 install -r requirements.txt
echo "[Backend] initialization completed."
