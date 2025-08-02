# Train Ticket Booking System

This is a simple Python project I built for booking train tickets using a MySQL database. It runs in the terminal and allows users to book, cancel, and view tickets. The project mainly focuses on using Python with MySQL for backend operations.

---

What This Project Can Do

- Book a new train ticket
- Cancel an existing ticket
- View all booked tickets
- Check train availability
- Store all data in a MySQL database

---

Technologies Used

- Python 3
- MySQL
- mysql-connector-python library
- Git & GitHub for version control

---

Folder Overview

TTBGIT/
│
├── TRAIN_GITHUB.py      - Main script with all booking logic
├── README.md            - This file
└── (You can add database script or .gitignore here)

---

Setup Instructions

1. Clone this repo

   git clone https://github.com/Mahanth6666/TrainBookingSystem.git
   cd TrainBookingSystem

2. Install MySQL connector

   pip install mysql-connector-python

3. Create the database

   Open MySQL and run:

   CREATE DATABASE train;

4. Update database connection

   Make sure your TRAIN_GITHUB.py file has the correct database credentials:

   con = mysql.connect(
       host="localhost",
       user="your_mysql_username",
       password="your_mysql_password",
       database="train"
   )

---

How to Run

Once everything is set up, run:

   python TRAIN_GITHUB.py

Use the terminal interface to book and manage train tickets.

---

To-Do / Improvements

- Add a graphical interface (Tkinter or PyQt)
- Improve error handling
- Add admin login
- Use .env file for secure credentials

---

About Me

Built by Mahanth K  
GitHub: https://github.com/Mahanth6666

---

License

Free to use – MIT License
