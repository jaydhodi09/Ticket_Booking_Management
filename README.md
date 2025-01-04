# Ticket Booking Management System

This is a Python-based Ticket Booking Management System that utilizes MySQL for database storage. It allows users to register, log in, search for tickets, book tickets, and view their booking history. Admins can manage tickets, view bookings, generate reports, and clean the database. The system is designed to handle events, tickets, and bookings, with features for both users and administrators.

## Features

### User Features
1. **Register**: Users can create an account by providing their name, email, and password.
2. **Login**: Users can log in using their email and password to access their dashboard.
3. **Search Tickets**: Users can search for tickets by event date or destination.
4. **Book Ticket**: Users can book available tickets by selecting the ticket ID.
5. **View Booking History**: Users can view their booking history, including event name, date, destination, and booking status.

### Admin Features
1. **Admin Login**: Admins can log in using predefined credentials.
2. **Add Ticket**: Admins can add new tickets to the system by specifying event details like name, date, destination, available slots, and price.
3. **Update Ticket**: Admins can modify the details of existing tickets.
4. **Delete Ticket**: Admins can remove tickets from the system.
5. **View Bookings**: Admins can view all bookings with user information, event details, and booking status.
6. **Generate Reports**: Admins can generate daily or weekly reports of bookings and revenue.
7. **Free Database**: Admins can reset the database by truncating all tables, effectively removing all data.

## Database Schema

The system uses three main tables in the MySQL database:

1. **Users**
   - `user_id`: INT (Primary Key)
   - `name`: TEXT
   - `email`: VARCHAR(255) (Unique)
   - `password`: TEXT
   - `created_at`: TIMESTAMP (default: CURRENT_TIMESTAMP)

2. **Tickets**
   - `ticket_id`: INT (Primary Key)
   - `event_name`: TEXT
   - `date`: DATE
   - `destination`: TEXT
   - `available_slots`: INT
   - `price`: REAL

3. **Bookings**
   - `booking_id`: INT (Primary Key)
   - `user_id`: INT (Foreign Key to Users)
   - `ticket_id`: INT (Foreign Key to Tickets)
   - `booking_date`: TIMESTAMP (default: CURRENT_TIMESTAMP)
   - `status`: VARCHAR(225) (default: 'Confirmed')

## Setup and Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>

 
