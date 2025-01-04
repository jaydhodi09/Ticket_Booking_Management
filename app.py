import mysql.connector
from tabulate import tabulate
import datetime

# Database setup
connection = mysql.connector.connect(
    host='localhost',
    database='ticket',
    user='root',
    password='67936793'
)
cursor = connection.cursor()

# Table creation
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name TEXT,
    email VARCHAR(255),
    password TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS tickets (
    ticket_id INT AUTO_INCREMENT PRIMARY KEY,
    event_name TEXT,
    date DATE,
    destination TEXT,
    available_slots INT,
    price REAL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS bookings (
    booking_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    ticket_id INT,
    booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(225) DEFAULT 'Confirmed',
    FOREIGN KEY(user_id) REFERENCES users(user_id),
    FOREIGN KEY(ticket_id) REFERENCES tickets(ticket_id)
)
''')

connection.commit()

# Helper functions
def print_table(data, headers):
    if data:
        print(tabulate(data, headers=headers, tablefmt='grid'))
    else:
        print("No records found.")

def register_user():
    name = input("Enter your name: ")
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    try:
        cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, password))
        connection.commit()
        print("Registration successful!")
    except mysql.connector.IntegrityError:
        print("Email already registered.")

def login_user():
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
    user = cursor.fetchone()
    if user:
        print(f"Welcome, {user[1]}!")
        user_panel(user[0])
    else:
        print("Invalid email or password.")

def user_panel(user_id):
    while True:
        print("\n--- User Panel ---")
        print("1. Search Tickets")
        print("2. Book Ticket")
        print("3. View Booking History")
        print("4. Logout")
        choice = input("Enter your choice: ")

        if choice == '1':
            search_tickets()
        elif choice == '2':
            book_ticket(user_id)
        elif choice == '3':
            view_booking_history(user_id)
        elif choice == '4':
            break
        else:
            print("Invalid choice. Try again.")

def search_tickets():
    print("\n--- Search Tickets ---")
    print("1. By Date")
    print("2. By Destination")
    choice = input("Enter your choice: ")

    if choice == '1':
        date = input("Enter date (YYYY-MM-DD): ")
        cursor.execute("SELECT * FROM tickets WHERE date = %s", (date,))
    elif choice == '2':
        destination = input("Enter destination: ")
        cursor.execute("SELECT * FROM tickets WHERE destination LIKE %s", (f"%{destination}%",))
    else:
        print("Invalid choice.")
        return

    tickets = cursor.fetchall()
    print_table(tickets, headers=["ID", "Event Name", "Date", "Destination", "Available Slots", "Price"])

def book_ticket(user_id):
    ticket_id = input("Enter Ticket ID to book: ")
    cursor.execute("SELECT available_slots FROM tickets WHERE ticket_id = %s", (ticket_id,))
    ticket = cursor.fetchone()

    if ticket and ticket[0] > 0:
        cursor.execute("INSERT INTO bookings (user_id, ticket_id) VALUES (%s, %s)", (user_id, ticket_id))
        cursor.execute("UPDATE tickets SET available_slots = available_slots - 1 WHERE ticket_id = %s", (ticket_id,))
        connection.commit()
        print("Ticket booked successfully!")
    else:
        print("Invalid Ticket ID or no slots available.")

def view_booking_history(user_id):
    cursor.execute("""
        SELECT b.booking_id, t.event_name, t.date, t.destination, b.booking_date, b.status
        FROM bookings b
        JOIN tickets t ON b.ticket_id = t.ticket_id
        WHERE b.user_id = %s
    """, (user_id,))
    bookings = cursor.fetchall()
    print_table(bookings, headers=["Booking ID", "Event Name", "Date", "Destination", "Booking Date", "Status"])


def admin_login():

    name = input("Enter your name: ")
    password = input("Enter your password: ")
    
    if(name=='jay' and  password=='6793'):
        return admin_panel()
    else:
        print("Invalid name or password.")    

def admin_panel():
    while True:
        print("\n--- Admin Panel ---")
        print("1. Add Ticket")
        print("2. Update Ticket")
        print("3. Delete Ticket")
        print("4. View Bookings")
        print("5. Generate Reports")
        print("6. Free Database")
        print("7. Logout")
        choice = input("Enter your choice: ")

        if choice == '1':
            add_ticket()
        elif choice == '2':
            update_ticket()
        elif choice == '3':
            delete_ticket()
        elif choice == '4':
            view_bookings()
        elif choice == '5':
            generate_reports()
        elif choice== '6':
            free_reports()    
        elif choice == '7':
            break
        else:
            print("Invalid choice. Try again.")

def add_ticket():
    event_name = input("Enter event name: ")
    date = input("Enter date (YYYY-MM-DD): ")
    destination = input("Enter destination: ")
    available_slots = int(input("Enter available slots: "))
    price = float(input("Enter price: "))
    cursor.execute("INSERT INTO tickets (event_name, date, destination, available_slots, price) VALUES (%s, %s, %s, %s, %s)",
                   (event_name, date, destination, available_slots, price))
    connection.commit()
    print("Ticket added successfully!")

def update_ticket():
    ticket_id = input("Enter Ticket ID to update: ")
    event_name = input("Enter new event name: ")
    date = input("Enter new date (YYYY-MM-DD): ")
    destination = input("Enter new destination: ")
    available_slots = int(input("Enter new available slots: "))
    price = float(input("Enter new price: "))
    cursor.execute("""
        UPDATE tickets
        SET event_name = %s, date = %s, destination = %s, available_slots = %s, price = %s
        WHERE ticket_id = %s
    """, (event_name, date, destination, available_slots, price, ticket_id))
    connection.commit()
    print("Ticket updated successfully!")

def delete_ticket():
    ticket_id = input("Enter Ticket ID to delete: ")
    cursor.execute("DELETE FROM tickets WHERE ticket_id = %s", (ticket_id,))
    connection.commit()
    print("Ticket deleted successfully!")

def view_bookings():
    cursor.execute("""
        SELECT b.booking_id, u.name, t.event_name, t.date, t.destination, b.booking_date, b.status
        FROM bookings b
        JOIN users u ON b.user_id = u.user_id
        JOIN tickets t ON b.ticket_id = t.ticket_id
    """)
    bookings = cursor.fetchall()
    print_table(bookings, headers=["Booking ID", "User Name", "Event Name", "Date", "Destination", "Booking Date", "Status"])

def generate_reports():
    print("\n--- Generate Reports ---")
    print("1. Daily Report")
    print("2. Weekly Report")
    choice = input("Enter your choice: ")

    if choice == '1':
        date = input("Enter date (YYYY-MM-DD): ")
        cursor.execute("""
            SELECT COUNT(*), SUM(t.price)
            FROM bookings b
            JOIN tickets t ON b.ticket_id = t.ticket_id
            WHERE DATE(b.booking_date) = %s
        """, (date,))
    elif choice == '2':
        start_date = input("Enter start date (YYYY-MM-DD): ")
        end_date = input("Enter end date (YYYY-MM-DD): ")
        cursor.execute("""
            SELECT COUNT(*), SUM(t.price)
            FROM bookings b
            JOIN tickets t ON b.ticket_id = t.ticket_id
            WHERE DATE(b.booking_date) BETWEEN %s AND %s
        """, (start_date, end_date))
    else:
        print("Invalid choice.")
        return

    report = cursor.fetchone()
    print(f"Total Bookings: {report[0]}, Total Revenue: {report[1]}")

def free_reports():
    try:
        
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        tables = ['users', 'tickets', 'bookings']
        for table in tables:
            cursor.execute(f"TRUNCATE TABLE {table}")
        
        connection.commit()
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        
        print("All tables have been truncated and the database is now free.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")    

# Main function
def main():
    while True:
        print("\n--- Ticket Booking System ---")
        print("1. Register")
        print("2. Login")
        print("3. Admin Login")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            register_user()
        elif choice == '2':
            login_user()
        elif choice == '3':
            admin_login()
        elif choice == '4':
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == '__main__':
    main()
