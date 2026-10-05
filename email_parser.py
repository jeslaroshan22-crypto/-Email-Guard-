import email
from email import policy
import re

def parse_email_headers(eml_file_path):
    # Read the .eml file in binary mode
    with open(eml_file_path, 'rb') as f:
        msg = email.message_from_binary_file(f, policy=policy.default)
    
    print("=" * 50)
    print("  EMAIL FORENSIC HEADER ANALYSIS REPORT")
    print("=" * 50)
    
    # 1. Extract basic headers
    subject = msg.get('Subject', 'No Subject')
    from_address = msg.get('From', 'Unknown Sender')
    return_path = msg.get('Return-Path', 'Not Found')
    auth_results = msg.get('Authentication-Results', 'Not Found')
    
    print(f"📌 Subject      : {subject}")
    print(f"👤 Visible From : {from_address}")
    print(f"🔍 Return-Path  : {return_path}")
    print(f"🛡️ Auth-Results : {auth_results}")
    
    print("\n" + "-" * 50)
    print("🌐 Received Server Chain (Hop-by-Hop):")
    print("-" * 50)
    
    # 2. Extract 'Received' headers (Server transit path)
    received_headers = msg.get_all('Received', [])
    if received_headers:
        for index, hop in enumerate(received_headers, start=1):
            print(f"Hop {index}: {hop.strip()}\n")
    else:
        print("No Received headers found!")

# To test the function (Uncomment the line below and provide your .eml file path)
parse_email_headers("sample_email.eml")
