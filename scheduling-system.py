from datetime import date
import os

appointments = []  # each item: {'name', 'date', 'time', 'service'}
clients = []       # each item: {'name', 'contact'}

TIME_SLOTS = {
    1: "07:00",
    2: "07:40",
    3: "08:20",
    4: "09:00",
    5: "09:40",
    6: "10:20",
    7: "11:00",
    8: "13:30",
    9: "14:10",
    10: "14:50",
    11: "15:30",
    12: "16:10",
    13: "16:50",
    14: "17:30",
    15: "18:10",
    16: "18:50"
}

FOLDER = "Scheduling Program"
CLIENTS_FILE = os.path.join(FOLDER, 'clients.txt')
SCHEDULE_FILE = os.path.join(FOLDER, 'schedule.txt')

SEPARATOR = '|'
DATE_FORMAT = "%m/%d/%Y"

def clean_text(text):
    return text.replace(SEPARATOR, ',').strip()

def is_slot_taken(time):
    return any(ap['time'] == time for ap in appointments)

def save_clients():
    os.makedirs(FOLDER, exist_ok=True)
    with open(CLIENTS_FILE, 'w', encoding="utf-8") as file:
        for client in clients:
            file.write(f"{client['name']}{SEPARATOR}{client['contact']}\n")

def save_schedule():
    os.makedirs(FOLDER, exist_ok=True)
    with open(SCHEDULE_FILE, 'w', encoding="utf-8") as file:
        for ap in appointments:
            file.write(
                f"{ap['name']}{SEPARATOR}{ap['date']}{SEPARATOR}"
                f"{ap['time']}{SEPARATOR}{ap['service']}\n")

def load_schedule():
    if not os.path.exists(SCHEDULE_FILE):
        return
    with open(SCHEDULE_FILE, 'r', encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line:
                parts = line.split(SEPARATOR)
                if len(parts) == 4:
                    name, day, time, service = parts
                    appointments.append({
                        'name': name,
                        'date': day,
                        'time': time,
                        'service': service
                    })
                else:
                    print(f"Error in {SCHEDULE_FILE}, line ignored: {line}")

def load_clients():
    if not os.path.exists(CLIENTS_FILE):
        return
    with open(CLIENTS_FILE, 'r', encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line:
                parts = line.split(SEPARATOR)
                if len(parts) == 2:
                    name, contact = parts
                    clients.append({'name': name, 'contact': contact})
                else:
                    print(f"Error in {CLIENTS_FILE}, line ignored: {line}")

def register_client(name=None):

    if name is None:
        name = clean_text(input("Enter the client's name: ")).lower()

    if name in [c['name'] for c in clients]:
        print("Client already registered!")
        return

    i = True

    while i:

        contact = input("Enter the phone number: ").replace(" ", "")
        if not contact.isdigit():
            print("Digits only, example: 99 9 99999999")
        else:
            i = False

    print()

    print("Registration complete! See it in > ' [3] View registered clients' < ")

    clients.append({'name': name, 'contact': contact})
    save_clients()

def book_appointment():

    name = clean_text(input("Enter the client's name: ")).lower()
    service = clean_text(input("Enter the desired service: "))

    found = any(c['name'] == name for c in clients)

    if not found:
        answer = input("Name not registered, register now? (y/n) ").lower()

        if answer == 'y':
            register_client(name=name)
        else:
            return print("Please register the client first! ")

    print("-" * 10)
    print()
    show_available_slots()
    print()
    print("-" * 10)

    chosen_time = None
    while chosen_time is None:
        try:
            slot = TIME_SLOTS[int(input(f"Which time slot for {name}?\n>> "))]

            if is_slot_taken(slot):
                print("That time slot is already taken.\n")
            else:
                chosen_time = slot

        except (KeyError, ValueError):
            print("Invalid value, please try again.\n")

    appointments.append({
        'name': name,
        'date': date.today(),
        'time': chosen_time,
        'service': service
    })
    save_schedule()

    print(
        f"Appointment booked for {name} "
        f"at {chosen_time} "
        f"for {service}."
    )

def show_available_slots():

    for number, slot in TIME_SLOTS.items():

        available = not any(ap['time'] == slot for ap in appointments)

        if available:
            print(f"{number} - {slot}")

def view_schedule():
    if not appointments:
        print("No appointments booked.")
        return
    print('-' * 12)
    for ap in appointments:
        print(f"Name: {ap['name']}\n"
              f"Time: {ap['time']}\n"
              f"Date: {ap['date']}\n"
              f"Service: {ap['service']}")
    print('-' * 12)

def cancel_appointment():
    name = clean_text(input("Enter the name of the booked client: ")).lower()

    found = False

    for ap in appointments:
        if ap['name'] == name:
            appointments.remove(ap)
            found = True
            print("Appointment canceled.")
            save_schedule()
            break

    if not found:
        print("Client not found.")

def view_clients():

    if not clients:
        print("No clients registered.")
        return

    print("///////////// Registered Clients //////////////")
    print("\n")
    for client in clients:
        print(f"Name: {client['name']} | Contact: {client['contact']}")

def reschedule():
    if not appointments:
        print("No appointments to change.\n")
        return

    print(f"{'ID':<4}{'NAME':<15}{'DATE':<13}{'TIME':<9}{'SERVICE'}")
    print("-" * 54)

    for index, ap in enumerate(appointments):
        print(
            f"{index:<4}"
            f"{ap['name']:<15}"
            f"{str(ap['date']):<13}"
            f"{ap['time']:<9}"
            f"{ap['service']}")

    try:
        appointment_id = int(input(
            f"From 0 to {len(appointments) - 1}, which one do you want to change? "))
        ap = appointments[appointment_id]
    except (ValueError, IndexError):
        print("Invalid value.")
        return

    print(f"\nClient: {ap['name']}")
    print(f"Current time: {ap['time']}")
    option = input("Do you want to change the time? (y/n) ").lower()

    if option != 'y':
        print("Operation canceled.")
        return

    print()
    show_available_slots()

    try:
        new_slot = int(input("Enter the number of the new time slot: "))
        chosen = TIME_SLOTS[new_slot]
    except (ValueError, KeyError):
        print("Invalid time slot.")
        return

    taken = any(a['time'] == chosen for a in appointments)
    if taken:
        print("That time slot is already taken.")
        return

    ap['time'] = chosen
    print("Appointment changed successfully!")
    save_schedule()

def main(): 


    msg = "Welcome! Scheduling Program started!!"
    print()
    print("=" * len(msg), msg, "=" * len(msg))
    print()
    load_schedule()
    load_clients()
    ok = True
    while ok:

        print("\n=== Scheduling System ===")
        print("1 - Register client")
        print("2 - Book appointment")
        print("3 - View registered clients")
        print("4 - View schedule")
        print("5 - Cancel appointment")
        print("6 - Change appointment")
        print("0 - Exit")

        option = input(">> ")

        if option == '1':
            register_client()
        elif option == '2':
            book_appointment()
        elif option == '3':
            view_clients()
        elif option == '4':
            view_schedule()
        elif option == '5':
            cancel_appointment()
        elif option == '6':
            reschedule()
        elif option == '0':
            print("Shutting down. See you!")
            ok = False
        else:
            print("Invalid option. Please try again.")

main()
