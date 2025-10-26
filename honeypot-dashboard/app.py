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

app = Flask(__name__)

# Path to Cowrie logs
COWRIE_LOG_PATH = "/home/cowrie/cowrie/var/log/cowrie/cowrie.json"


def parse_cowrie_logs():
    """Parse Cowrie JSON logs and extract relevant data (robust to string durations)."""
    data = {
        'total_connections': 0,
        'total_login_attempts': 0,
        'successful_logins': 0,
        'failed_logins': 0,
        'usernames': [],
        'passwords': [],
        'commands': [],
        'ips': [],
        'timeline': [],
        'sessions': []
    }

    if not os.path.exists(COWRIE_LOG_PATH):
        return data

    try:
        with open(COWRIE_LOG_PATH, 'r') as f:
            for line in f:
                try:
                    entry = json.loads(line.strip())
                except json.JSONDecodeError:
                    continue

                event_id = entry.get('eventid')

                # New connection
                if event_id == 'cowrie.session.connect':
                    data['total_connections'] += 1
                    data['ips'].append(entry.get('src_ip', 'unknown'))
                    data['timeline'].append({
                        'timestamp': entry.get('timestamp'),
                        'event': 'connection'
                    })

                # Login success
                elif event_id == 'cowrie.login.success':
                    data['successful_logins'] += 1
                    data['total_login_attempts'] += 1
                    data['usernames'].append(entry.get('username', 'unknown'))
                    data['passwords'].append(entry.get('password', 'unknown'))
                    data['timeline'].append({
                        'timestamp': entry.get('timestamp'),
                        'event': 'login_success',
                        'username': entry.get('username')
                    })

                # Login failed
                elif event_id == 'cowrie.login.failed':
                    data['failed_logins'] += 1
                    data['total_login_attempts'] += 1
                    data['usernames'].append(entry.get('username', 'unknown'))
                    data['passwords'].append(entry.get('password', 'unknown'))

                # Command input
                elif event_id == 'cowrie.command.input':
                    cmd = entry.get('input', '')
                    if cmd:
                        data['commands'].append(cmd)
                        data['timeline'].append({
                            'timestamp': entry.get('timestamp'),
                            'event': 'command',
                            'command': cmd
                        })

                # Session closed
                elif event_id == 'cowrie.session.closed':
                    raw_duration = entry.get('duration', 0)
                    try:
                        duration = float(raw_duration)
                    except (TypeError, ValueError):
                        duration = 0.0
                    data['sessions'].append({
                        'duration': duration,
                        'timestamp': entry.get('timestamp')
                    })

    except Exception as e:
        print(f"Error reading logs: {e}")

    return data


def get_statistics():
    """Generate statistics from parsed logs."""
    data = parse_cowrie_logs()

    # Top usernames
    username_counts = Counter(data['usernames'])
    top_usernames = [{'name': k, 'count': v} for k, v in username_counts.most_common(10)]

    # Top passwords
    password_counts = Counter(data['passwords'])
    top_passwords = [{'name': k, 'count': v} for k, v in password_counts.most_common(10)]

    # Top commands
    command_counts = Counter(data['commands'])
    top_commands = [{'name': k, 'count': v} for k, v in command_counts.most_common(10)]

    # Top IPs
    ip_counts = Counter(data['ips'])
    top_ips = [{'ip': k, 'count': v} for k, v in ip_counts.most_common(10)]

    # Timeline (group by hour)
    timeline_by_hour = {}
    for event in data['timeline']:
        if event.get('timestamp'):
            hour = event['timestamp'][:13]  # YYYY-MM-DDTHH
            timeline_by_hour[hour] = timeline_by_hour.get(hour, 0) + 1
    timeline_data = [{'time': k, 'count': v} for k, v in sorted(timeline_by_hour.items())]

    # Average session duration (safe)
    durations = [float(s.get('duration', 0.0)) for s in data['sessions'] if s.get('duration') is not None]
    avg_session_duration = sum(durations) / len(durations) if durations else 0.0

    stats = {
        'summary': {
            'total_connections': data['total_connections'],
            'total_login_attempts': data['total_login_attempts'],
            'successful_logins': data['successful_logins'],
            'failed_logins': data['failed_logins'],
            'unique_ips': len(set(data['ips'])),
            'unique_usernames': len(set(data['usernames'])),
            'unique_passwords': len(set(data['passwords'])),
            'total_commands': len(data['commands']),
            'avg_session_duration': round(avg_session_duration, 2)
        },
        'top_usernames': top_usernames,
        'top_passwords': top_passwords,
        'top_commands': top_commands,
        'top_ips': top_ips,
        'timeline': timeline_data
    }

    return stats


@app.route('/')
def index():
    """Serve the dashboard HTML."""
    return render_template('dashboard.html')


@app.route('/api/stats')
def api_stats():
    """API endpoint for statistics."""
    stats = get_statistics()
    return jsonify(stats)


if __name__ == '__main__':
    os.makedirs('templates', exist_ok=True)

    print("=" * 60)
    print("Cowrie Honeypot Dashboard")
    print("=" * 60)
    print("Starting server on http://0.0.0.0:5000")
    print("Access from your browser at: http://localhost:5000")
    print("Or from Windows: http://10.0.2.15:5000")
    print("=" * 60)

    app.run(host='0.0.0.0', port=5000, debug=True)
