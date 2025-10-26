ls
sudo apt update
sudo apt install -y git python3-virtualenv libssl-dev libffi-dev build-essential libpython3-dev python3-minimal authbind virtualenv
sudo adduser --disabled-password cowrie
sudo su - cowrie
sudo apt install -y python3.12-venv
sudo su - cowrie
sudo netstat -tulpn | grep 2222
ss -tulpn | grep 2222
ss -tulpn | grep 22
exit
sudo aptt update && sudo apt upgrade -y
sudo apt update && sudo apt upgrade -y
ping -c 3 8.8.8.8
ping -c 3 google.com
exit
sudo shutdown -h now
exit
sudo su - cowrie
Sudo su - cowrie
cd ~/cowrie
ls
cd ~/cowrie
sudo shutdown -h now
ls
sudo apt install -y sshpass
chmod +x simulate_attacks.py
ls
cd honeypot-dashboard/
ls
sudo apt install -y sshpass
chmod +x simulate_attacks.py
nano app.py
#!/usr/bin/env python3
"""
Cowrie Honeypot Dashboard
Visualizes attack data from Cowrie JSON logs
"""
from flask import Flask, render_template, jsonify
import json
import os
from datetime import datetime
from collections import Counter
import glob
app = Flask(__name__)
# Path to Cowrie logs
COWRIE_LOG_PATH = "/home/cowrie/cowrie/var/log/cowrie/cowrie.json"
def parse_cowrie_logs():
def get_statistics():
@app.route('/')
def index():
@app.route('/api/stats')
def api_stats():
if __name__ == '__main__':
    os.makedirs('templates', exist_ok=True)
ls
nano templates/dashboard.html
ls
mkdir templates
nano templates/dashboard.html
pip3 install flask
chmod +x app.py
ls
sudo apt install python3-pip
python3 app.py
pip3 install flask
sudo apt install python3-venv python3-full -y
python3 -m venv dashboard-env
ls
source dashboard-env/bin/activate
pip install flask
python3 app.py
sudo su - cowrie
sudo chmod 644 /home/cowrie/cowrie/var/log/cowrie/cowrie.json
ssh -p 2223 jak@127.0.0.1
ls
ssh -p 2223 jak@127.0.0.1
ssh -p 2223 jak@127.0.0.1)
ssh -p 2223 jak@127.0.0.1
exit
