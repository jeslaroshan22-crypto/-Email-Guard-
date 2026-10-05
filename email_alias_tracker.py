
import json
import os
import csv
from datetime import datetime

# Database file to store our aliases inside 3_Alias_Tracker folder
DB_FILE = "alias_database.json"

def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def create_alias():
    service_name = input("Enter the service name (e.g., Daraz LK, PickMe): ")
    real_email = input("Enter your real email address: ")
    
    username = service_name.lower().replace(" ", "_")
    masked_email = f"{username}_safe_mask@emailguard.local"
    
    data = load_data()
    
    data[masked_email] = {
        "service": service_name,
        "real_email": real_email,
        "status": "Active",       # Status to track active/blocked
        "hit_count": 0,          # Hit counter for incoming emails
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    save_data(data)
    print(f"\n✅ Masked Email Generated for {service_name}:")
    print(f"   {masked_email} --> Forwarding to: {real_email}\n")

def check_alias_leak():
    incoming_to_address = input("Enter the incoming email address to simulate a received email: ")
    data = load_data()
    
    if incoming_to_address in data:
        if data[incoming_to_address]["status"] == "Blocked":
            print(f"\n🚫 BLOCKED: Email to {incoming_to_address} was blocked because this alias is deactivated!\n")
            return
            
        # Increase hit count
        data[incoming_to_address]["hit_count"] += 1
        save_data(data)
        
        service = data[incoming_to_address]["service"]
        hits = data[incoming_to_address]["hit_count"]
        print(f"\n🚨 ALERT: Email received via service: **{service}**!")
        print(f"   Total emails received on this alias: {hits}")
        print(f"   The address {incoming_to_address} was targeted or leaked.\n")
    else:
        print("\n✅ Safe: Address not found in database.\n")

# Option to Deactivate or Block an Alias
def toggle_alias_status():
    address = input("Enter the masked email address to block/activate: ")
    data = load_data()
    
    if address in data:
        current_status = data[address]["status"]
        if current_status == "Active":
            data[address]["status"] = "Blocked"
            print(f"\n🔒 Success: Alias {address} has been BLOCKED/Deactivated.\n")
        else:
            data[address]["status"] = "Active"
            print(f"\n🔓 Success: Alias {address} has been ACTIVATED again.\n")
        save_data(data)
    else:
        print("\n❌ Error: Address not found in database.\n")

# Option to Export Database to CSV Report
def export_to_csv():
    data = load_data()
    if not data:
        print("\nNo data available to export!\n")
        return
        
    csv_file = "alias_security_report.csv"
    with open(csv_file, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Masked Email", "Service Name", "Real Email", "Status", "Hit Count", "Created At"])
        
        for email_addr, details in data.items():
            writer.writerow([
                email_addr,
                details["service"],
                details["real_email"],
                details["status"],
                details["hit_count"],
                details["created_at"]
            ])
            
    print(f"\n📁 Success! Report exported successfully as '{csv_file}' in your project folder.\n")

# --- Interactive Menu ---
while True:
    print("--- EMAIL MASKING & LEAK TRACKER (ADVANCED) ---")
    print("1. Create New Masked Alias")
    print("2. Simulate Incoming Email (Leak/Hit Check)")
    print("3. Block / Deactivate an Alias")
    print("4. Export Report to CSV")
    print("5. Exit")
    
    choice = input("Enter your choice (1-5): ")
    
    if choice == '1':
        create_alias()
    elif choice == '2':
        check_alias_leak()
    elif choice == '3':
        toggle_alias_status()
    elif choice == '4':
        export_to_csv()
    elif choice == '5':
        print("Exiting... Thank you!")
        break
    else:
        print("❌ Invalid choice! Please try again.\n")