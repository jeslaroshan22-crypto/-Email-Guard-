
import re
import os
import hashlib
import requests
import tkinter as tk
from tkinter import filedialog

# VirusTotal API Key (Inghe ungaludaiya free VirusTotal API key-ai potrukkalam)
VT_API_KEY = "YOUR_VIRUSTOTAL_API_KEY_HERE"

def calculate_file_hash(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def check_virustotal(file_hash):
    if VT_API_KEY == "YOUR_VIRUSTOTAL_API_KEY_HERE":
        return "API Key not configured (Skipped online check)"
    
    headers = {"x-apikey": VT_API_KEY}
    url = f"https://www.virustotal.com/api/v3/files/{file_hash}"
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            stats = response.json()["data"]["attributes"]["last_analysis_stats"]
            malicious_count = stats.get("malicious", 0)
            if malicious_count > 0:
                return f"🔴 MALICIOUS! Flagged by {malicious_count} antivirus engines on VirusTotal."
            else:
                return "🟢 CLEAN! No security vendors flagged this file on VirusTotal."
        elif response.status_code == 404:
            return "🟡 File hash not found in VirusTotal database (Unknown/New file)."
    except Exception:
        return "❌ Error connecting to VirusTotal API."
    
    return "Check completed."

def inspect_content(email_body, attachment_path=""):
    risk_score = 0
    alerts = []
    
    # 1. Phishing Keyword Scanner
    phishing_keywords = ["urgent", "verify your account", "password reset", "bank account suspended", "click here", "claim prize"]
    found_keywords = [kw for kw in phishing_keywords if kw in email_body.lower()]
    
    if found_keywords:
        risk_score += 40
        alerts.append(f"🚨 Phishing Keywords Detected: {found_keywords}")
        
    # 2. Malicious URL / Link Extractor
    urls = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', email_body)
    if urls:
        alerts.append(f"🔗 Links Extracted: {urls}")
        for url in urls:
            if re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', url):
                risk_score += 50
                alerts.append(f"⚠️ Suspicious IP-based URL: {url}")
                
    # 3. Advanced Attachment Hash & VirusTotal Check
    if attachment_path and os.path.exists(attachment_path):
        file_name = os.path.basename(attachment_path)
        file_hash = calculate_file_hash(attachment_path)
        alerts.append(f"📦 Attachment: {file_name}")
        alerts.append(f"🔑 SHA-256 Hash: {file_hash}")
        
        vt_result = check_virustotal(file_hash)
        alerts.append(f"🛡️ VirusTotal Status: {vt_result}")
        
        if "MALICIOUS" in vt_result:
            risk_score += 80
    
    # --- Final Report ---
    print("\n--- ADVANCED CONTENT & MALWARE INSPECTION REPORT ---")
    for alert in alerts:
        print(f"  {alert}")
        
    print(f"\nFinal Content Risk Score: {risk_score}/100")
    if risk_score >= 50:
        print("🔴 STATUS: HIGH RISK / MALICIOUS THREAT DETECTED!\n")
    else:
        print("🟢 STATUS: LOW RISK / CLEAN CONTENT\n")

def main():
    while True:
        print("--- CONTENT & MALWARE INSPECTOR ---")
        print("1. Select Email File & Check Attachment")
        print("2. Type Email Body Manually")
        print("3. Exit")
        
        choice = input("Enter choice (1-3): ")
        if choice == '1':
            root = tk.Tk()
            root.withdraw()
            file_path = filedialog.askopenfilename(title="Select Email File")
            if file_path:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    body = f.read()
                
                has_attachment = input("Do you want to test an attachment file for VirusTotal check? (y/n): ")
                att_path = ""
                if has_attachment.lower() == 'y':
                    att_path = filedialog.askopenfilename(title="Select Attachment File to Scan")
                    
                inspect_content(body, att_path)
        elif choice == '2':
            body = input("Enter email body: ")
            inspect_content(body)
        elif choice == '3':
            break

if __name__ == "__main__":
    main()