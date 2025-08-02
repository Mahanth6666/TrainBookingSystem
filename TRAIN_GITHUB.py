import mysql.connector as mysql
from getpass import getpass
import re

# Establish connection to MySQL
try:
    con = mysql.connect(
        host="localhost",
        user="root",
        password="Mahanth2004",
        database="train"
    )
    if con.is_connected():
        print("Connected to the database")
except mysql.Error as e:
    print(f"Error connecting to the database: {e}")
    exit(1)

def authenticate_user():
    attempts = 3
    while attempts > 0:
        username = input("Enter username: ")
        password = input("Enter password: ")
        
        # Dummy check for illustration purposes
        if username == "a" and password == "p":
            print("Authentication successful")
            return True
        else:
            print("Invalid credentials, try again")
            attempts -= 1
    
    print("Too many failed attempts, exiting")
    exit(1)

def made_by():
    msg = '''
        Train Ticket Booking System              :
        Roll No                                  : 86
        School Name                              : PSG TECH
        Session                                  : 2024
        
        Thanks for evaluating my Project.
        \n\n\n
    '''
    for x in msg:
        print(x, end='')

def menu():
    print('   M A I N   M E N U')
    print(" 1. Ticket booking ")
    print(" 2. Show passenger details ")
    print(" 3. Add new passenger ")
    print(" 4. Modify passenger details ")
    print(" 5. Show class coach details ")
    print(" 6. Remove passenger ")
    print(" 7. Show all passengers ")  # Option for showing all passengers
    print(" 8. Show made by ")
    print(" 9. show train details")
    print(" 10. Exit")  # Adjusted exit option
def ticketbooking():
    try:
        xo = con.cursor()

        # Display available class coaches
        s = "SELECT * FROM class_coach"
        xo.execute(s)
        cs = xo.fetchall()

        # Print class coach table header
        print(f"{'SNo':<5} {'Class':<16} {'Price':<10}")
        print("-" * 40)

        # Print each class coach's details
        for x in cs:
            print(f"{x[0]:<5} {x[1]:<16} {x[2]:<10}")

        tot = 0
        tickets = 0

        # Select class coach and number of tickets
        while True:
            try:
                tic = int(input("Enter serial number of the class coach: "))
                if tic not in [1, 2, 3]:
                    print("Invalid choice, please select a valid class")
                    continue
                tickets = int(input("Enter number of tickets: "))
                break
            except ValueError:
                print("Please enter valid numbers")

        # Calculate total cost based on class coach selected
        if tic == 1:
            print("You have selected second seater")
            tot = 2000 * tickets
        elif tic == 2:
            print("You have selected sleeper class")
            tot = 4000 * tickets
        elif tic == 3:
            print("You have selected first class AC")
            tot = 6000 * tickets

        # Display available destinations
        s = "SELECT * FROM desti"
        xo.execute(s)
        destinations = xo.fetchall()

        # Print destination table header
        print(f"\n{'DNo':<5} {'Destination':<15} {'Cost':<10}")
        print("-" * 40)

        # Print each destination's details
        for destination in destinations:
            print(f"{destination[0]:<5} {destination[1]:<15} {destination[2]:<10}")

        # Select destination
        while True:
            try:
                ddd = int(input("Enter destination number of your destination: "))
                if ddd not in [d[0] for d in destinations]:
                    print("Invalid choice, please select a valid destination")
                    continue
                break
            except ValueError:
                print("Please enter valid numbers")

        selected_destination = next(d for d in destinations if d[0] == ddd)[1]
        destination_cost = next(d for d in destinations if d[0] == ddd)[2]

        # Calculate total cost based on selected destination
        tot += tickets * destination_cost

        print("Total bill: Rs", tot, "\n")

        # Adding passenger details after booking
        x = []
        name = input("Enter the passenger's name: ")
        x.append(name)

        while True:
            age = input("Enter passenger's age: ")
            if not age.isdigit():
                print("Invalid age, please enter a numeric value")
                continue
            break
        x.append(int(age))

        while True:
            phonenum = input("Enter phone number (digits only): ")
            if not re.match("^\d+$", phonenum):
                print("Invalid phone number, please enter digits only.")
                continue
            break
        x.append(int(phonenum))

        # Set the starting point to a default value
        startingpoint = "Coimbatore"  # Default value
        x.append(startingpoint)

        # Append total cost and number of tickets to the passenger's data
        x.append(tot)
        x.append(tickets)

        # Display available trains
        print("\nAvailable Trains:")
        s = "SELECT * FROM traind"
        xo.execute(s)
        trains = xo.fetchall()

        # Print train table header
        print(f"{'Train ID (tid)':<10} {'Train Name':<20} {'Destination 1':<20} {'Destination 2':<20} {'Destination 3':<20}")
        print("-" * 100)

        # Print each train's details
        for train in trains:
            print(f"{train[0]:<10} {train[1]:<20} {train[2]:<20} {train[3]:<20} {train[4]:<20}")

        # Ask for train ID after displaying trains
        while True:
            tid = input("Enter train ID (tid): ")
            if not tid.isdigit():
                print("Invalid Train ID, please enter a numeric value.")
                continue
            break
        x.append(int(tid))

        # Append the selected destination to passenger's data
        x.append(selected_destination)

        # Prepare the SQL insert statement
        sql = """
            INSERT INTO passenger (name, age, phonenum, reg_date, startingpoint, totalcost, tickets, tid, destination)
            VALUES (%s, %s, %s, CURRENT_DATE, %s, %s, %s, %s, %s)
        """
        xo.execute(sql, tuple(x))
        con.commit()

        # Fetch and print the added passenger details
        sql_fetch = "SELECT * FROM passenger WHERE phonenum = %s"
        xo.execute(sql_fetch, (int(phonenum),))
        passenger_details = xo.fetchone()

        if passenger_details:
            print("\nTicket booked and passenger added successfully")
            print("\nPassenger Details:")
            print(f"{'PNo':<5} {'Name':<20} {'Age':<5} {'Phone':<15} {'Train ID':<10} {'Tickets':<7} {'Total cost':<10} {'Starting Point':<15} {'Destination':<15} {'Registration Date':<15}")
            print("-" * 120)

            # Use a conditional check to replace None with an empty string for each field
            formatted_details = [
                passenger_details[0] if passenger_details[0] is not None else '',
                passenger_details[1] if passenger_details[1] is not None else '',
                passenger_details[2] if passenger_details[2] is not None else '',
                passenger_details[4] if passenger_details[4] is not None else '',
                passenger_details[7] if passenger_details[7] is not None else '',
                passenger_details[6] if passenger_details[6] is not None else '',
                passenger_details[5] if passenger_details[5] is not None else '',
                passenger_details[8] if passenger_details[8] is not None else '',
                passenger_details[9] if passenger_details[9] is not None else '',
                passenger_details[3] if passenger_details[3] is not None else '',
            ]
            
            print(f"{formatted_details[0]:<5} {formatted_details[1]:<20} {formatted_details[2]:<5} {formatted_details[3]:<15} {formatted_details[4]:<10} {formatted_details[5]:<7} {formatted_details[6]:<10} {formatted_details[7]:<15} {formatted_details[8]:<15} {formatted_details[9]:<15}")

    except mysql.Error as e:
        print(f"Error in ticket booking: {e}")

def showall():
    try:
        xo = con.cursor()
        s = "SELECT * FROM passenger"
        xo.execute(s)
        result = xo.fetchall()
        
        if result:
            print("\nPassenger Details:")
            print("-" * 100)
            print(f"{'PNo':<5} {'Name':<20} {'Age':<5} {'Phone':<15} {'COST':<12} {'Total Tickets':<15} {'Train ID':<15} {'Starting':<10} {'Destination':<10}")
            print("-" * 100)
            for row in result:
                # Replace None with "N/A" for display purposes
                row = [x if x is not None else "N/A" for x in row]
                print(f"{row[0]:<5} {row[1]:<20} {row[2]:<5} {row[4]:<15} {row[3]:<15} {row[5]:<15} {row[6]:<15} {row[7]:<10} {row[8]:<7}  {row[9]:<12}")
        else:
            print("No passenger details available.")
    except mysql.Error as e:
        print(f"Error fetching passenger details: {e}")


def search():
    try:
        xo = con.cursor()
        pno = input("Enter the passenger number: ")
        s = "SELECT * FROM passenger WHERE pno=%s"
        xo.execute(s, (pno,))
        result = xo.fetchall()
        
        for ab in result:
            print("Details: ", ab)
    except mysql.Error as e:
        print(f"Error in search: {e}")

def add_passenger():
    try:
        xo = con.cursor()
        x = []
        name = input("Enter the name: ")
        x.append(name)
        
        while True:
            age = input("Enter age: ")
            if not age.isdigit():
                print("Invalid age, please enter a numeric value")
                continue
            break
        x.append(age)
        
        while True:
            phonenum = input("Enter phone number: ")
            
            break
        x.append(phonenum)
        
        reg_date = input("Enter the registration date (YYYY-MM-DD): ")
        x.append(reg_date)
        
        startingpoint = input("Enter the starting point: ")
        x.append(startingpoint)
        
        endpoint = input("Enter the endpoint: ")
        x.append(endpoint)
        
        pas = tuple(x)
        sql = "INSERT INTO passenger (name, age, phonenum, reg_date, startingpoint, endpoint) VALUES ( %s, %s, %s, %s, %s, %s)"
        xo.execute(sql, pas)
        con.commit()
        print("Passenger added successfully")
    except mysql.Error as e:
        print(f"Error in adding passenger: {e}")

def modify_passenger():
    def modify_detail(field):
        try:
            xo = con.cursor()
            pno = input("Enter PNO of passenger: ")
            new_value = input(f"Enter the new {field}: ")
            s = f"UPDATE passenger SET {field}=%s WHERE pno=%s"
            xo.execute(s, (new_value, pno))
            con.commit()
            print(f"{field.capitalize()} updated successfully")
        except mysql.Error as e:
            print(f"Error in modifying {field}: {e}")

    print("1. Modify name ")
    print("2. Modify phone number ")
    print("3. Modify age ")
    print("4. Modify endpoint")
    
    options = {"1": "name", "2": "phonenum", "3": "age", "4": "endpoint"}
    
    o = input("Your choice: ")
    if o in options:
        modify_detail(options[o])
    else:
        print("Please enter a number between 1 and 4")
        modify_passenger()

def show_classcoach():
    try:
        xo = con.cursor()
        s = "SELECT * FROM class_coach"
        xo.execute(s)
        show = xo.fetchall()
        
        for e in show:
            print(e)
    except mysql.Error as e:
        print(f"Error in showing class coach details: {e}")
def show_traind():
    try:
        xo = con.cursor()
        s = "SELECT * FROM traind"
        xo.execute(s)
        show = xo.fetchall()
        
        for e in show:
            print(e)
    except mysql.Error as e:
        print(f"Error in showing class coach details: {e}")



def remove_passenger():
    try:
        xo = con.cursor()
        pno = input("Enter the passenger number to remove: ")
        s = "DELETE FROM passenger WHERE pno=%s"
        xo.execute(s, (pno,))
        con.commit()
        print("Passenger removed successfully")
        print("Your ammount will be credited within 30 mins")
    except mysql.Error as e:
        print(f"Error in removing passenger: {e}")

# Main loop
authenticate_user()
while True:
    menu()
    try:
        choice = int(input('\nEnter your choice (1..10): '))  # Adjusted for 8 options
        
        if choice == 1:
            ticketbooking()
        elif choice == 2:
            search()
        elif choice == 3:
            add_passenger()
        elif choice == 4:
            modify_passenger()
        elif choice == 5:
            show_classcoach()
        elif choice == 6:
            remove_passenger()
        elif choice == 7:
            showall()

        elif choice == 8:
            made_by()
        elif choice == 9:
            show_traind()
        elif choice == 10:
            print("Exiting the program. Goodbye!")
            break  # Exit the loop and program
        else:
            print("Please enter a number between 1 and 8")
    except ValueError:
        print("Invalid input, please enter a number between 1 and 8")

    print('-' * 100)

# Ensure connection is closed when the program exits
if con.is_connected():
    con.close()
    print("Connection closed")
