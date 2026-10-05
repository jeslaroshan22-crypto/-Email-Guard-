
import re
import requests

def get_ip_geolocation(ip_address):
    try:
        # Using free ip-api.com service to track IP location
        response = requests.get(f"http://ip-api.com/json/{ip_address}", timeout=5)
        data = response.json()
        if data.get("status") == "success":
            country = data.get("country", "Unknown")
            isp = data.get("isp", "Unknown")
            return country, isp
    except Exception:
        pass
    # Always return 2 values to prevent unpacking error
    return "Unknown", "Unknown"

def analyze_email_risk():
    print("--- EMAIL RISK SCORING & IP INTELLIGENCE ---")
    
    spf_status = input("Enter SPF Status (Pass/Fail): ").strip().capitalize()
    dkim_status = input("Enter DKIM Status (Pass/Fail): ").strip().capitalize()
    dmarc_status = input("Enter DMARC Status (Pass/Fail): ").strip().capitalize()
    sender_ip = input("Enter Sender IP Address (e.g., 8.8.8.8): ").strip()
    
    risk_score = 0
    
    # 1. Domain Authentication Checks
    if spf_status != "Pass":
        risk_score += 30
    if dkim_status != "Pass":
        risk_score += 30
    if dmarc_status != "Pass":
        risk_score += 40
        
    # 2. IP Geolocation Lookup
    country, isp = "Unknown", "Unknown"
    if sender_ip:
        print(f"\n[+] Fetching Threat Intelligence for IP: {sender_ip}...")
        country, isp = get_ip_geolocation(sender_ip)
        
    # --- Final Risk Report ---
    print("\n--- RISK SCORING & INTELLIGENCE REPORT ---")
    print(f"  SPF Authentication : {spf_status}")
    print(f"  DKIM Authentication: {dkim_status}")
    print(f"  DMARC Authentication: {dmarc_status}")
    print(f"  Sender IP Location : {country} (ISP: {isp})")
    
    print(f"\nFinal Domain Risk Score: {risk_score}/100")
    
    if risk_score >= 70:
        print("🔴 STATUS: HIGH RISK / SPOOFED DOMAIN DETECTED!\n")
    elif risk_score > 0:
        print("🟡 STATUS: MEDIUM RISK / WARNINGS FOUND\n")
    else:
        print("🟢 STATUS: LOW RISK / AUTHENTIC EMAIL\n")

if __name__ == "__main__":
    analyze_email_risk()