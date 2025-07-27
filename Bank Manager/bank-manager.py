# Importing Modules
from time import sleep
import pathlib
import json
from datetime import datetime as d

#Typing Effect
def typing(text,delay = 0.03):
    for word in text:
        print(word,end="")
        sleep(delay)
    print()

#Time Assign
x = d.now()
time = f'{x.strftime('%d %m %Y')}'

#JSON file
p = pathlib.Path(__file__).with_name("data.json")

# Defining the Functions

#Writing And Read Data
def loadData():
        with p.open('r') as f:
            try:
                return json.load(f)
            except Exception:
                return []  
data = loadData()      

def writeData(data):
    with p.open('w') as f:
        json.dump(data,f, indent=2)

#User Design Function
def checkUser(username,accountNo):
    for user in data:
        if user['username'].lower() == username.lower() and user['accountNo'] == accountNo:
            return user
        elif user['accountNo'] == accountNo:
            return None
    return 0

def balanceDeduction(removeAmount,user_exists):
    if removeAmount < user_exists['balance']:
        user_exists['balance'] -= removeAmount
        user_exists['transaction'].append({
            "Type" : "Debited",
            "Amount": removeAmount,
            "Time" : time})
        writeData(data)
        return None
    elif removeAmount > user_exists['balance']:
        typing("Insufficient Balance.. Try Again.")
        return 0

def balanceAdd(amount,user_exists):
    user_exists['balance'] += amount
    user_exists['transaction'].append({
            "Type" : "Credited",
            "Amount": amount,
            "Time" : time})
    writeData(data)

def moneyTransfer(user1,user2,amount):
    if user1['balance'] <= amount:
        user1['balance'] -= amount
        user1['transaction'].append({
            "Type" : "Transfered",
            "Amount": amount,
            "Time" : time})
        user1['balance'] += amount
        user1['transaction'].append({
            "Type" : "Recieved",
            "Amount": amount,
            "Time" : time})
        writeData(data)
        typing(f"Rs.{amount} Transfered to {user2['username']} from {user1['username']}.")
    elif user1['balance'] < amount:
        typing("Insufficient Balance.") 

def checkAccountNo():
    while True:
        accountNo = input("Enter Your Account Number : ")
        if len(accountNo) >= 8 and len(accountNo) <= 10:
            return accountNo
        else:
            print("Enter a Valid Account Number Between 8 to 10.")


while True:

    # Option Showcase
    typing('''
           Banking Manager
            -- MENU --
        1. Register New User
        2. Check Balance
        3. Add Money
        4. Withdrawn Money
        5. Transfer Money
        6. Mini Statement
        7. Exit
        8. Correction Panel
    ''')

    # Option Choosing
    choice = int(input("Enter Your Choice : "))

    # Choices Defining
    if choice == 1:
        try:
            typing("\nEnter User Details to if the User is Present or Not -")
            newUser = {
                    'username' : input("Enter Your Name : "),
                    'accountNo' : int(checkAccountNo())
                }
            
            user_exists = checkUser(newUser["username"],newUser["accountNo"])
            
            if user_exists == None:
                typing("Another User Already Exists With Same Account Number, Cann't Add Again.")
            elif user_exists:
                typing("Another User Already Exists With Same Name and Account Number in Our Server. Can't Add Again.")
            else:
                newUser = {
                    'username' : newUser["username"],
                    'accountNo' : newUser["accountNo"],
                    'balance' : int(input("Enter Your Current Balance : ")),
                    'transcation' : []
                }
                data.append(newUser)
                writeData(data)
                typing("New User Add.")
 
        except Exception as e:
            typing("Unexpected Error.")
        sleep(2)

    elif choice == 2:
        try:
            username = input("Enter Your Name : ")
            accountNo = int(checkAccountNo())
                    
            user_exists = checkUser(username,accountNo)
        
            if user_exists:
                typing(f"Your Current Balance : Rs.{user_exists['balance']}")
            else:
                typing("User Not Found.")

        except Exception as e:
            typing("Unexpected Error.")
        sleep(2)
        
    elif choice == 3:
        try:
            username = input("Enter Your Name : ")
            accountNo = int(checkAccountNo())
                    
            user_exists = checkUser(username,accountNo)
        
            if user_exists:
                amount = int(input("Enter the Amount You Want to Add : "))
                balanceAdd(amount,user_exists)
                print(f"Rs.{amount} Amount Added. Current Balance is Rs.{user_exists['balance']}.")
            else:
                typing("User Not Found.")

        except Exception as e:
            typing("Unexpected Error.")
        sleep(2)

    elif choice == 4:
        try:
            username = input("Enter Your Name : ")
            accountNo = int(checkAccountNo())
                    
            user_exists = checkUser(username,accountNo)
        
            if user_exists:
                removeAmount = int(input("Enter the Amount to Withdraw : "))
                a = balanceDeduction(removeAmount,user_exists)
                if a == None:
                    print(f"Rs.{removeAmount} Amount Deduced. Current Balance is Rs.{user_exists['balance']}.")
                elif a == 0:
                    print(f"Current Balance is Rs.{user_exists['balance']}.")
            else:
                typing("User Not Found.")

        except Exception as e:
            typing("Unexpected Error.")
        sleep(2)

    elif choice == 5:
        try:
            typing("\nEnter Sender's Details -")
            username = input("Enter Sender's Name : ")
            accountNo = int(checkAccountNo())
                    
            user_exists1 = checkUser(username,accountNo)
        
            if user_exists1:
                typing("\nEnter the Reciever's Details -")
                username = input("Enter Reciever's Name : ")
                accountNo = int(checkAccountNo())
                user_exists = checkUser(username,accountNo)

                if user_exists:
                    amountTransfer = int(input("Enter the Amount to Transfer : "))
                    moneyTransfer(user_exists,user_exists1,amountTransfer)
                else:
                    typing("Reciever's Account Not Found.")
            else:
                typing("Sender's Account Not Found.")
            
        except Exception as e:
            typing("Unexpected Error.")
        sleep(2)

    elif choice == 6:
        try:
            typing("\nEnter Your Details -")
            username = input("Enter Your Name : ")
            accountNo = int(checkAccountNo())
                    
            user_exists = checkUser(username,accountNo)
            if user_exists:
                typing(f'For Account No. - {accountNo}')
                count = 0
                for sate in user_exists['transaction']:
                    if count == 5:
                        break
                    print(f"{count+1}. Type : {sate['Type']}, Amount : {sate['Amount']}, Date : {sate["Time"]}.")
                    count+=1
                    print("--End--")

            else:
                print("User Not Found.")

        except Exception as e:
            print(e)
        sleep(2)

    elif choice == 7:
        print("Exiting",end="")
        for _ in range(3):
            sleep(0.5)
            print(".",end="")
        break

    elif choice == 8:
        try:
            typing("\nEnter Your Details -")
            username = input("Enter Your Name : ")
            accountNo = int(checkAccountNo())
                    
            user_exists = checkUser(username,accountNo)

            if user_exists:
                while True:
                    option = input("Enter What You Wanted to Change (Username/AccountNo) : ").lower()
                    
                    if option == "username":
                        newUsername = input("Enter the Correct Username : ")
                        user_exists['username'] = newUsername
                        writeData(data)
                        break
                    elif option == "accountno":
                        newAccountNo = int(input("Enter the Correct Account Number : "))
                        user_exists['accountNo'] = newAccountNo
                        writeData(data)
                        break
                    else:
                        print("Invaild!!")
                print("Changes Done.")     
            else:
                print("User Not Found.")

        except Exception as e:
            print(e)
        sleep(2)

    else:
        typing("Invalid Choice. Try Again.")
        sleep(1)

#Type of Accounts