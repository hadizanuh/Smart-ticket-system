import json
import uuid
from datetime import datetime
import os

# ----CONFIGURATION----
TICKET_FILE = 'tickets.json'
FAQ_FILE = 'faq.json'       #Changed to relative path

#-------FUNCTIONS-----

def load_tickets():      
    """Loads Ticket from the jason file.Handles filr not found and other errors"""
    try:
        if os.path.exists(TICKET_FILE):     #check if the file exists
            with open(TICKET_FILE, 'r') as f:
                return json.load(f)          
        else:
            return[]           # Return an empty list if the file does not exist
    except (json.JSONDecodeError, OSError) as e:
        print(f"Error: Could no load tickets. Returning an empty list. Error Details: {e}")
        return[]            # Return an empty list on error, and inform the user
    
def save_tickets(tickets):
    """Saves Ticket to the JSON file. Handles Potential Error"""
    try:
        with open(TICKET_FILE, 'w') as f:
            json.dump(tickets, f, indent=4)
    except (OSError, TypeError) as e:
        print(f"Error saving tickets: {e}")

def load_faq():
    """LoadsFAQs from the JSON file. Handles file not found and other errors."""
    try:
        if os.path.exists(FAQ_FILE):   # Check if the file exists
            with open(FAQ_FILE, 'r', encoding='utf-8') as f:  # Added encoding
                return json.load(f)
        else:
            return {}    # Return empty dict if file does not exist
    except (json.JSONDecodeError, OSError) as e:
        print(f"Error: Could not load FAQs. Returning an empty dictionary. Error Details: {e}")
        return {}  # Return an empty dict on error
    
def auto_reply(message):
    """Provides an automated response based on keywords in the message."""
    faqs = load_faq()
    if not faqs:
        return None # Return None if no FAQs are loaded.
    for keyword, reply in faqs.items():
        if keyword.lower() in message.lower():
            return reply
    return None

def assign_team(message):
    """Assigns a support team based on keywords in the message."""

    if "billing" in message.lower():
        return "Finance Team"
    elif "login" in message.lower() or "password" in message.lower():
        return "Tech Support"
    elif "refund" in message.lower():
        return "Customer Service"
    else:
        return "General Support"
    
def create_ticket():
    """Creates a new support ticket."""

    name = input("Enter your name: ")
    message = input("Describe your issue: ")
    ticket_id = str(uuid.uuid4())[:8]
    team = assign_team(message)
    reply = auto_reply(message)

    ticket = {
        "id": ticket_id,
        "name": name,
        "message": message,
        "team": team,
        "status": "open",
        "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    tickets = load_tickets()
    tickets.append(ticket)
    save_tickets(tickets)

    print(f"\nTicket Created! ID: {ticket_id}")
    print(f"Assigned Team: {team}")
    if reply:
        print(f"Auto-Reply: {reply}")
    else:
        print("No Auto-Reply Available.")

def view_tickets():
    """Displays all support tickets."""

    tickets = load_tickets()
    if not tickets:
        print("No tickets found.")
        return  # Early return for empty ticket list
    
    print("\n---Tickets---") # Added a header for better output
    for ticket in tickets:
        print("-" * 40)
        for key, value in ticket.items():
            print(f"{key.capitalize()}: {value}") #Iterate through the ticket dictionary, and print keys and values.


def main():
    """Main function to run the support ticket system."""
    while True:
        print("\n--- Smart Support Ticket System ---")
        print("1. Create a new ticket")
        print("2. View all tickets")
        print("3. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            create_ticket()
        elif choice == '2':
            view_tickets()
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid Choice. Try Again.")

if __name__ == '__main__':
    main()   