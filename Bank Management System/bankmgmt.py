import mysql.connector
from prettytable import PrettyTable
import random
import re #re.match----> Match at beginning of string

# Establish database connection
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='myfamily@12345',
    database='bankmgmt'
)
cursor = conn.cursor()

# Create tables if they don't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS banks (
        bank_id INT AUTO_INCREMENT PRIMARY KEY,
        bank_name VARCHAR(100),
        bank_email VARCHAR(100)
    )
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        account_number VARCHAR(20),
        balance DECIMAL(10, 2),
        bank_id INT,
        FOREIGN KEY (bank_id) REFERENCES banks(bank_id)
    )
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS signup (
        username VARCHAR(30) PRIMARY KEY,
        password VARCHAR(30)
    )
""")

conn.commit()


# Function to handle user login
def login():
    print("\t<<<<<<------ Login Wizard ------>>>>>> ")
    username = input("Please Enter User Name: ")
    password = input("Please Enter Password: ")

    cursor.execute("SELECT username FROM signup WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()

    if user:
        print("\n<<--Login Successful-->>")
        return True
    else:
        print("\n<<--Wrong Password or Username-->>")
        return False


# Function to handle user signup
def signup():
    print("\n<<<<<<------ SignUp Wizard ------>>>>>>")
    
    # Validate username
    while True:
        username = input("Please Enter User Name: ")
        if len(username) <= 10:
            break
        else:
            print("Username should be exactly 10 characters long.")

    # Validate password
    #re.match----> Match at beginning of string
    while True:
        password = input("Please Enter Password: ")
        if len(password) <= 8 and re.match("^\d+$", password):
            break
        else:
            print("Password should be exactly 8 digits long.")

    
    bank_name = input("Enter Bank Name: ")
    bank_email = input("Enter Bank Email: ")

    # Insert bank data into the banks table
    cursor.execute("""
        INSERT INTO banks (bank_name, bank_email)
        VALUES (%s, %s)
    """, (bank_name, bank_email))
    conn.commit()

    # Insert user signup data into the signup table
    cursor.execute("INSERT INTO signup (username, password) VALUES (%s, %s)", (username, password))
    conn.commit()

    print("\n<<--Signup Successful-->>")


# Function to create a new customer account
def create_account():
    name = input("Enter customer name: ")
    
    # Validate name
    while True:
        if len(name) <= 30:
            break
        else:
            print("Name should be at most 30 characters long.")
            name = input("Enter customer name: ")
    
    account_number = ''.join(random.choices('0123456789', k=12))
    
    balance = float(input("Enter initial balance: "))
    
    # Insert customer data into the database
    cursor.execute("""
        INSERT INTO customers (name, account_number, balance)
        VALUES (%s, %s, %s)
    """, (name, account_number, balance))
    conn.commit()

    print("\n<<--Account created successfully-->>")
    print("Your account number is: ", account_number)


# Function to update customer data
def update():
    cus_id = int(input("Please enter the customer ID: "))
    up_name = input("Enter customer name you want to change: ")
   # up_account_number = input("Enter account number you want to change: ")

    cursor.execute("""
        UPDATE customers
        SET name = %s
        WHERE customer_id = %s
    """, (up_name,cus_id))
    conn.commit()

    print("<<<<<<------Updation Successful------>>>>>>")


# Function to deposit amount into a customer's account
def deposit():
    account_number = input("Enter account number: ")
    amount = float(input("Enter amount to deposit: "))

    # Update the customer's balance in the database
    cursor.execute("""
        UPDATE customers
        SET balance = balance + %s
        WHERE account_number = %s
    """, (amount, account_number))
    conn.commit()

    print("\n<<--Amount deposited successfully-->>")


# Function to withdraw amount from a customer's account
def withdraw():
    account_number = input("Enter account number: ")
    amount = float(input("Enter amount to withdraw: "))

    # Check if the customer has sufficient balance
    cursor.execute("""
        SELECT balance
        FROM customers
        WHERE account_number = %s
    """, (account_number,))
    balance = cursor.fetchone()

    if balance:
        if balance[0] >= amount:
            # Update the customer's balance in the database
            cursor.execute("""
                UPDATE customers
                SET balance = balance - %s
                WHERE account_number = %s
            """, (amount, account_number))
            conn.commit()

            print("\n<<--Amount withdrawn successfully-->>")
        else:
            print("\n<<--Insufficient balance-->>")
    else:
        print("\n<<--Customer not found-->>")


# Function to display customer details
def display_details():
    account_number = input("Enter account number: ")

    # Retrieve customer details from the database
    cursor.execute("""
        SELECT name, account_number, balance
        FROM customers
        WHERE account_number = %s
    """, (account_number,))
    customer = cursor.fetchone()

    if customer:
        table = PrettyTable(["Name", "Account Number", "Balance"])
        table.add_row(customer)
        print("\n" + str(table))
    else:
        print("\n<<--Customer not found-->>")


# Function to close a customer's account
def close():
    account_number = input("Enter account number: ")

    # Check if the customer exists
    cursor.execute("""
        SELECT name
        FROM customers
        WHERE account_number = %s
    """, (account_number,))
    customer = cursor.fetchone()

    if customer:
        # Delete the customer's account from the database
        cursor.execute("""
            DELETE FROM customers
            WHERE account_number = %s
        """, (account_number,))
        conn.commit()

        print("\n<<--Account closed successfully-->>")
    else:
        print("\n<<--Customer not found-->>")


# Function to display bank details
def display_bank_details():
    cursor.execute("""
        SELECT bank_id, bank_name, bank_email
        FROM banks
    """)
    banks = cursor.fetchall()

    if banks:
        table = PrettyTable(["Bank ID", "Bank Name", "Bank Email"])
        for bank in banks:
            table.add_row(bank)
        print("\n" + str(table))
    else:
        print("\n<<--No banks found-->>")


# Bank management system menu
print("\t*****************************************************************************************\n")
print("\t\t<<<<<<<<<<---------- BANK MANAGEMENT SYSTEM ---------->>>>>>>>>>>\n")
print("\t*****************************************************************************************\n\n\n")

print("********************************")
print("1. SIGNUP")
print("2. LOGIN")
print("********************************")

choice = input("\n<> If You Want To Signup Press 1\n\t\tOr\n<> If You Want To login Press 2\n\nPlease Enter Your Choice (1 or 2): ")

if choice == "1":
    signup()
elif choice == "2":
    logged_in = login()
    if logged_in:
        while True:
            print("\nBank Management System")
            print("1. Create Account")
            print("2. Deposit Amount")
            print("3. Withdraw Amount")
            print("4. Display Customer Details")
            print("5. Update Data")
            print("6. Close Account")
            print("7. Display Bank Details")
            print("8. Exit")
            print("*****************************************************************************************")

            choice = input("Enter your choice: ")

            if choice == "1":
                create_account()
            elif choice == "2":
                deposit()
            elif choice == "3":
                withdraw()
            elif choice == "4":
                display_details()
            elif choice == "5":
                update()
            elif choice == "6":
                close()
            elif choice == "7":
                display_bank_details()
            elif choice == "8":
                break
            else:
                print("\nInvalid choice!")
    else:
        exit()
else:
    print("\nInvalid choice!")
    exit()

# Close database connection
conn.close()
