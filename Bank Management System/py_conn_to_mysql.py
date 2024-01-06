import mysql.connector
from prettytable import PrettyTable


conn = mysql.connector.connect(host='localhost', username='root', password='myfamily@12345')
mycursor = conn.cursor()


mycursor.execute("CREATE DATABASE IF NOT EXISTS bank_management")
mycursor.execute("USE bank_management")
mycursor.execute("CREATE TABLE IF NOT EXISTS signup (username varchar(30), password varchar(30))")
conn.commit()


def signup():
    username = input("Please Enter User Name: ")
    password = input("Please Enter Password: ")
    mycursor.execute("INSERT INTO signup VALUES (%s, %s)", (username, password))
    conn.commit()
    print("\t\t<<<<<<<-------SIGNUP SUCCESSFULLY------->>>>>>>>")


def login():
    username = input("Please Enter User Name: ")
    password = input("Please Enter Password: ")

    mycursor.execute("SELECT username FROM signup")
    user1 = mycursor.fetchall()
    conn.commit()

    user2 = [row[0] for row in user1]

    mycursor.execute("SELECT password FROM signup")
    pass1 = mycursor.fetchall()
    pass2 = [row[0] for row in pass1]
    conn.commit()

    if username not in user2 or password not in pass2:
        print("<<--Wrong Password Or Username-->>!!!!!!")
        f = 1
        while True:
            f = int(input("Press 1 to login again\nPress 2 to exit: "))
            if f == 1:
                login()
            else:
                exit()

    else:
        mycursor.execute("SELECT username FROM signup WHERE username = %s", (username,))
        username = mycursor.fetchone()
        mycursor.execute("SELECT password FROM signup WHERE password = %s", (password,))
        result = mycursor.fetchall()

        print("\t\t<<<<<<<-------LogIn SUCCESSFULLY------->>>>>>>>")
        while True:
            print("[1] Open New Account")
            print("[2] Deposite Amount")
            print("[3] Withdraw Amount")
            print("[4] Balance Enquiry")
            print("[5] Customer Details")
            print("[6] Colse Account")
            print("[7] Show Details")
            print("Press any key for Exit....!")
            a=int(input("Enter the choice You Want to Do : "))
            
            #OPEN NEW ACCOUNT
            if a==1:
                openacc()
            #FOR DEPOSITE AMOUNT
            elif(a==2):
                dep()
            #WITHDRAW AMOUNT
            elif(a==3):
                withdraw()
            #BALANCE ENQUIRY
            elif(a==4):
                bal_enq()
            #CUSTOMER DETAILS
            elif(a==5):
                cust_det()
            #CLOSE ACCOUNT
            elif(a==6):
                close()
            #DISPLAY ALL DETAILS
            elif(a==7):
                show()
                
            else:
                print("<<<<<<------\3THANK YOU SIR\3------>>>>>>>")
                break


def openacc():
    name = input("Please Enter Your Full Name: ")
    acc_no = int(input("Please Enter Account Number: "))
    address = input("Please Enter Your Address: ")
    contact_no = int(input("Please Enter Your Contact Number: "))
    total_balance = int(input("Enter How Much Balance You Want To Deposit: "))

    mycursor.execute(
        "CREATE TABLE IF NOT EXISTS account (name varchar(30), acc_no int, address varchar(30), contact_no int, total_balance int)")
    mycursor.execute(
        "CREATE TABLE IF NOT EXISTS amount (name varchar(30), acc_no int, total_balance int)")

    sql1 = 'INSERT INTO acc VALUES (%s, %s, %s, %s, %s)'
    sql2 = 'INSERT INTO amount VALUES (%s, %s, %s)'
    data1 = (name, acc_no, address, contact_no, total_balance)
    data2 = (name, acc_no, total_balance)

    mycursor.execute(sql1, data1)
    mycursor.execute(sql2, data2)
    conn.commit()
    print("\n<<<<<<<<--------Data Entered Successfully-------->>>>>>>>>\n")


def dep():
    name = input("Please Enter Your Full Name: ")
    acc_no = int(input("Please Enter Account Number: "))
    dep_am = input("Please Enter The Amount: ")

    mycursor.execute("UPDATE acc SET total_balance = total_balance + " + dep_am + " WHERE acc_no = " + str(acc_no))
    conn.commit()

    mycursor.execute("SELECT total_balance FROM acc WHERE acc_no = " + str(acc_no))
    myresult = mycursor.fetchall()
    t = PrettyTable(['total_balance'])
    for total_balance in myresult:
        t.add_row([total_balance])
    print("\n<<<<<<<<------After Deposit, This is Your Available Balance------>>>>>>>>")
    print(t)


# WITHDRAW AMOUNT
def withdraw():
    name = input("Please Enter Your Full Name: ")
    acc_no = int(input("Please Enter Account Number: "))
    withdraw_am = input("Please Enter The Amount: ")

    mycursor.execute("SELECT total_balance FROM acc WHERE acc_no = " + str(acc_no))
    myresult = mycursor.fetchall()
    t = PrettyTable(['total_balance'])
    for total_balance in myresult:
        t.add_row([total_balance])
    print("\n<<<<<<<<--------After Withdraw, This is Your Available Balance-------->>>>>>>>")
    print(t)


# BALANCE ENQUIRY
def bal_enq():
    acc_no = int(input("Enter Your Account Number: "))

    mycursor.execute("SELECT total_balance FROM acc WHERE acc_no = " + str(acc_no))
    myresult = mycursor.fetchall()
    t = PrettyTable(['total_balance'])
    for total_balance in myresult:
        t.add_row([total_balance])
    print("\n<<<<<<<<--------This Is Your Balance Enquiry-------->>>>>>>>")
    print(t)


# CUSTOMER DETAILS
def cust_det():
    acc_no = int(input("Please Enter Account Number: "))

    mycursor.execute("SELECT * FROM acc WHERE acc_no = " + str(acc_no))
    myresult = mycursor.fetchall()
    t = PrettyTable(['name', 'acc_no', 'address', 'contact_no', 'total_balance'])
    for name, acc_no, address, contact_no, total_balance in myresult:
        t.add_row([name, acc_no, address, contact_no, total_balance])
    print("\n<<<<<<<<--------CUSTOMER DETAILS-------->>>>>>>>>")
    print(t)


# CLOSE ACCOUNT
def close():
    name = input("Please Enter Your Full Name: ")
    acc_no = int(input("Please Enter Account Number: "))

    mycursor.execute('DELETE FROM acc WHERE acc_no = ' + str(acc_no))
    conn.commit()
    print("\n<<<<<<<<--------Your Account Is Closed-------->>>>>>>>")


# DISPLAY ALL INFORMATION
def show():
    mycursor.execute("SELECT * FROM acc")
    myresult = mycursor.fetchall()
    t = PrettyTable(['name', 'acc_no', 'address', 'contact_no', 'total_balance'])
    for name, acc_no, address, contact_no, total_balance in myresult:
        t.add_row([name, acc_no, address, contact_no, total_balance])
    print("\n<<<<<<<<<--------This is All Information-------->>>>>>>>")
    print(t)
    conn.close()


print("*****************************************************************************************")
print("<<<<<<<<<<---------- BANK MANAGEMENT SYSTEM ---------->>>>>>>>>>>")
print("1.SIGNUP\n2.LOGIN")

ch = int(input("\nSIGNUP/LOGIN (1, 2): "))
if ch == 1:
    signup()
elif ch == 2:
    login()
else:
    print("Invalid Information....!!")
# from prettytable import PrettyTable
# import mysql.connector

# conn=mysql.connector.connect(host='localhost',username='root',password='myfamily@12345',database='bank_management')
# mycursor=conn.cursor()


# mycursor.execute("create database if not exists bank_management")  #Execute an SQL statement
# mycursor.execute("use bank_management")
# mycursor.execute("create table if not exists signup(username varchar(30),password varchar(30))")
# conn.commit()

# # # Signup Function
# # def signup():
# #     username=input("Please Enter User Name : ")
# #     password=input("Please Enter Password : ")
# #     mycursor.execute("insert into signup values("+username+","+password+")")
# #     conn.commit()  #commit() is used for change/update the database after insert or update query
# # #print("\t\t<<<<<<<<-------SIGNUP SUCCESSFULLY------->>>>>>>>")
# # print("Now Please Login to continue")
# # # login()

# #LOGIN FUNCTION
# def login():
#     username=input("Please Enter User Name : ")
#     password=input("Please Enter Password : ")
    
#     mycursor=conn.cursor()
#     mycursor.execute("use bank_management")
#     mycursor.execute("select username from signup")
#     user1=mycursor.fetchall()   #fetches all remaining row in from of tuple
#     conn.commit()
    
#     user2=[]
#     for i in range (len(user1)):
#         user2.append(user1[i][0])
        
#     mycursor=conn.cursor()
#     mycursor.execute("select password from signup")
#     pass1=mycursor.fetchall()
#     pass2=[]
#     for i in range(len(pass1)):
#         pass2.append(pass1[i][0])
#     conn.commit()
    
#     if (username not in user2)or(password not in pass2):
#         print("<<--Wrong Password Or Username-->>!!!!!!")
#         f=1
#         while True:
#             f=int(input("Press 1 login Again\nPress 2 for Exit : "))
#             if f==1:
#                 login()
#             else:
#                 exit()
                
#     else:
#         mycursor=conn.cursor()
#         #mycursor.execute("select username from signup where username="+username+"")
#         mycursor.execute("SELECT username FROM signup WHERE username = %s", (username,))
#         username=mycursor.fetchone()
#         #mycursor.execute("select password from signup where password="+password+"")
#         # mycursor.execute("SELECT password FROM signup WHERE password = %s", (password,))
#         # password=mycursor.fetchone()    #fetches one row in the from of tuple
#         mycursor.execute("SELECT password FROM signup WHERE password = %s", (password,))
#         result = mycursor.fetchall()
        
        
#         print("\t\t<<<<<<<<-------LogIn SUCCESSFULLY------->>>>>>>>")
#         conn.commit()
#         while True:
#             print("[1] Open New Account")
#             print("[2] Deposite Amount")
#             print("[3] Withdraw Amount")
#             print("[4] Balance Enquiry")
#             print("[5] Customer Details")
#             print("[6] Colse Account")
#             print("[7] Show Details")
#             print("Press any key for Exit....!")
#             a=int(input("Enter the choice You Want to Do : "))
            
#             #OPEN NEW ACCOUNT
#             if a==1:
#                 openacc()
#             #FOR DEPOSITE AMOUNT
#             elif(a==2):
#                 dep()
#             #WITHDRAW AMOUNT
#             elif(a==3):
#                 withdraw()
#             #BALANCE ENQUIRY
#             elif(a==4):
#                 bal_enq()
#             #CUSTOMER DETAILS
#             elif(a==5):
#                 cust_det()
#             #CLOSE ACCOUNT
#             elif(a==6):
#                 close()
#             #DISPLAY ALL DETAILS
#             elif(a==7):
#                 show()
                
#             else:
#                 print("<<<<<<------\3THANK YOU SIR\3------>>>>>>>")
#                 break
# #Signup Function
# def signup():
#     username=input("Please Enter User Name : ")
#     password=input("Please Enter Password : ")
#     mycursor.execute("use bank_management")
#     # mycursor.execute(f"insert into username,password values {username},{password}")
#     str = "INSERT INTO signup VALUES (%s,%s)"
#     val = (username,password)
#     mycursor.execute(str,val)
#     conn.commit()  #commit() is used for change/update the database after insert or update query
#     print("\t\t<<<<<<<<-------SIGNUP SUCCESSFULLY------->>>>>>>>")
# signup()
# print("Now Please Login to continue")
# login()


# def openacc():
#     name=input("Please Enter Your Full Name : ")
#     acc_no=int(input("Please Enter Account Number : "))
#     address=input("Please Enter Your Address : ")
#     contact_no=int(input("Please Enter Your Contact Number : "))
#     total_balnace=int(input("Enter How Much Balance You Want To Deposite : "))
#     data1=(name,acc_no,address,contact_no,total_balnace)
#     data2=(name,acc_no,total_balnace)
#     mycursor.execute("create table if not exitsacc(name varchar(30),acc_no int,address varchar(30),contact_no int,total_balance int")
#     mycursor.execute("create table if not exists amount(name varchar(30),acc_no int,total_balance int)")
    
#     sql1='insert into acc_value(%s,%s,%s,%s,%s)'
#     sql2='insert into amount valuse(%s,%s,%s)'
#     c=conn.cursor()
#     mycursor.execute(sql1,data1)
#     mycursor.execute(sql2,data2)
#     conn.commit()
#     print("")
#     print("<<<<<<<<--------Data Entered Successfully-------->>>>>>>>>")
#     print("")
    
# def dep():
#     name=input("Please Enter Your Full Name : ")
#     acc_no=int(input("Please Enter Account Number : "))
#     dep_am=input("Please Enter The Anount : ")
#     address=int(input("Please Enter How Much Amount You Deposited : "))
#     c=conn.cursor()
#     mycursor.execute("update acc set total_balance=total_balance+"+dep_am+'where acc_no='+acc_no+';')           
#     conn.commit()
#     mycursor.execute("select total_balance from acc where acc_no="+str(acc_no))
#     myresult=mycursor.fetchall()
#     t=PrettyTable(['total_balance'])
#     for total_balance in myresult:
#         t.add_row([total_balance])
#     print("<<<<<<<<------After Deposite This is Your Available Balance------>>>>>>>>")
#     print(t)
    
# #WITHDRAW AMOUNT 
# def withdraw():
#     name=input("Please Enter Your Full Name : ")
#     acc_no=int(input("Please Enter Account Number : "))
#     dep_am=input("Please Enter The Anount : ")
#     c=conn.cursor()
#     mycursor.execute("select total_balance from acc where acc_no="+str(acc_no))
#     myresult=mycursor.fetchall()
#     t=PrettyTable(['total_balance'])
#     for total_balance in myresult:
#         t.add_row([total_balance])   
#     print("<<<<<<<<--------After Withdraw This Your Available Balance-------->>>>>>>>")
#     print(t)
    
#     #BALANCE ENQUIRY 
# def bal_enq():
#         acc_no=int(input("Enter Your Account Number : "))
#         c=conn.cursor()
#         mycursor.execute("select total_balance from acc where acc_no="+str(acc_no))
#         myresult=mycursor.fetchall()
#         t=PrettyTable(['total_balance'])
#         for total_balance in myresult:
#             t.add_row([total_balance])
#         print("<<<<<<<<--------This Is Your Balance Enquiry-------->>>>>>>>")
#         print(t) 
        
# #CUSTOMER DETAILS
# def cust_det():
#     acc_no=int(input("Please Enter Account Number : "))
#     c=conn.cursor()
#     mycursor.execute("select *from acc where acc_no="+str(acc_no))
#     myresult=mycursor.fetchall()
#     t=PrettyTable(['name','acc_no','address','contact_no','total_balance'])
#     for name,acc_no,address,contact_no,total_balance in myresult:
#         t.add_row([name,acc_no,address,contact_no,total_balance])
#     print("<<<<<<<<--------CUSTOMER DETAILS-------->>>>>>>>>")
#     print(t)
    
# #CLOSE ACCOUNT 
# def close():
#     name=input("Please Enter Your Full Name : ")
#     acc_no=int(input("Please Enter Account Number : "))
#     c=conn.cursor()
#     mycursor.execute('delete from acc where acc_no='+str(acc_no))
#     conn.commit()
#     print("<<<<<<<<--------Your Account Is Closed-------->>>>>>>>")
    
# #DISPLAY ALL INFORMATION 
# def show():
#     mycursor=conn.cursor()
#     mycursor.execute("select * from acc")
#     myresult=mycursor.fetchall()
#     t=PrettyTable(['name','acc_no','address','contact_no','total_balance'])
#     for name,acc_no,address,contact_no,total_balance in myresult:
#         t.add_row([name,acc_no,address,contact_no,total_balance])
#     print("<<<<<<<<<--------This is All Information-------->>>>>>>>")
#     print(t)
#     conn.close()
    
#     #MAIN START
#     print("*****************************************************************************************")
#     print("<<<<<<<<<<---------- BANK MANAGEMENT SYSTEM ---------->>>>>>>>>>>")
#     print(("1.SIGNUP\n2.LOGIN"))
    
#     ch=int(input("\nSIGNUP/LOGIN(1,2):"))
#     if ch==1:
#         signup()
#     elif ch==2:
#         login()
#     else:
#         print("Invalid Information....!!")
    
    