# Importing Modules
from time import sleep
import pathlib
import json
from datetime import datetime as d

# Typing Effect
def typing(text, delay=0.01):
    for word in text:
        print(word, end="")
        sleep(delay)
    print()

# JSON file path
p = pathlib.Path(__file__).with_name("data.json")

# Data Management Functions
def loadData():
    if p.exists():
        with p.open('r') as f:
            try:
                return json.load(f)
            except Exception:
                return []
    return []

def writeData(data):
    with p.open('w') as f:
        json.dump(data, f, indent=2)

# User Utility Functions
def checkUser(username, accountNo):
    for user in data:
        if user['username'] == username and user['accountNo'] == accountNo:
            return user
    return None

def balanceDeduction(removeAmount, user_exists):
    if removeAmount <= user_exists['balance']:
        user_exists['balance'] -= removeAmount
        user_exists.setdefault('transaction', []).append({
            "Type": "Debited",
            "Amount": removeAmount,
            "Time": time
        })
        writeData(data)
        typing("Amount Deducted.")
    else:
        typing("Insufficient Balance.. Try Again.")

def balanceAdd(amount, user_exists):
    user_exists['balance'] += amount
    user_exists.setdefault('transaction', []).append({
        "Type": "Credited",
        "Amount": amount,
        "Time": time
    })
    writeData(data)

def checkAccountNo():
    while True:
        accountNo = input("Enter Your Account Number : ")
        if 8 <= len(accountNo) <= 10:
            return accountNo
        else:
            print("Enter a Valid Account Number Between 8 to 10 digits.")

# Main Loop
while True:
    x = d.now()
    time = x.strftime('%d-%m-%Y')

    typing('''
           Banking Manager
    \t -- MENU --
        1. Register New User
        2. Check Balance
        3. Add Money
        4. Withdraw Money
        5. Transfer Money
        6. Mini Statement
        7. Exit
        8. Correction Panel
    ''')

    choice = int(input("Enter Your Choice : "))
    data = loadData()

    if choice == 1:
        try:
            typing("\nEnter User Details to Check If the User Already Exists -")
            newUser = {
                'username': input("Enter Your Name : "),
                'accountNo': int(checkAccountNo())
            }

            user_exists = checkUser(newUser["username"], newUser["accountNo"])

            if user_exists:
                typing("User Already Exists, Cannot Add Again.")
            else:
                newUser['balance'] = int(input("Enter Your Current Balance : "))
                newUser['transaction'] = []
                data.append(newUser)
                writeData(data)
                typing("New User Added.")

        except Exception:
            typing("Unexpected Error Occurred.... Try Again.")
        sleep(2)

    elif choice == 2:
        try:
            username = input("Enter Your Name : ")
            accountNo = int(checkAccountNo())

            user_exists = checkUser(username, accountNo)

            if user_exists:
                typing(f"Your Current Balance : Rs.{user_exists['balance']}")
            else:
                typing("User Not Found.")
        except Exception as e:
            typing(str(e))
        sleep(2)

    elif choice == 3:
        try:
            username = input("Enter Your Name : ")
            accountNo = int(checkAccountNo())

            user_exists = checkUser(username, accountNo)

            if user_exists:
                typing("User Found!!")
                amount = int(input("Enter the Amount You Want to Add : "))
                balanceAdd(amount, user_exists)
                typing("Amount Added.")
            else:
                typing("User Not Found.")
        except Exception as e:
            typing(str(e))
        sleep(2)

    elif choice == 4:
        try:
            username = input("Enter Your Name : ")
            accountNo = int(checkAccountNo())

            user_exists = checkUser(username, accountNo)

            if user_exists:
                typing("User Found!!")
                removeAmount = int(input("Enter the Amount to Withdraw : "))
                balanceDeduction(removeAmount, user_exists)
            else:
                typing("User Not Found.")
        except Exception as e:
            typing(str(e))
        sleep(2)

    elif choice == 5:
        try:
            typing("\nEnter Your Details -")
            sender_name = input("Enter Your Name : ")
            sender_acc = int(checkAccountNo())
            sender = checkUser(sender_name, sender_acc)

            if sender:
                typing("\nEnter Receiver's Details -")
                receiver_name = input("Enter Receiver's Name : ")
                receiver_acc = int(checkAccountNo())
                receiver = checkUser(receiver_name, receiver_acc)

                if receiver:
                    amount = int(input("Enter Amount to Transfer : "))
                    if amount <= sender['balance']:
                        balanceDeduction(amount, sender)
                        balanceAdd(amount, receiver)
                        typing("Transfer Successful.")
                    else:
                        typing("Insufficient Funds.")
                else:
                    typing("Receiver Not Found.")
            else:
                typing("Sender Not Found.")
        except Exception as e:
            typing(str(e))
        sleep(2)

    elif choice == 6:
        try:
            typing("\nEnter Your Details -")
            username = input("Enter Your Name : ")
            accountNo = int(checkAccountNo())

            user_exists = checkUser(username, accountNo)

            if user_exists:
                typing(f"\nMini Statement for Account No. - {accountNo}")
                transactions = user_exists.get("transaction", [])
                last_5 = transactions[-5:]
                for i, txn in enumerate(reversed(last_5), 1):
                    typing(f"{i}. {txn['Time']} - {txn['Type']} - Rs.{txn['Amount']}")
            else:
                typing("User Not Found.")
        except Exception as e:
            typing(str(e))
        sleep(2)

    elif choice == 7:
        print("Exiting", end="")
        for _ in range(3):
            sleep(0.5)
            print(".", end="")
        break

    elif choice == 8:
        try:
            typing("\nEnter Your Details -")
            username = input("Enter Your Name : ")
            accountNo = int(checkAccountNo())

            user_exists = checkUser(username, accountNo)

            if user_exists:
                while True:
                    option = input("Enter What You Want to Change (Username/AccountNo) : ").lower()
                    if option == "username":
                        newUsername = input("Enter New Username : ")
                        user_exists['username'] = newUsername
                        writeData(data)
                        break
                    elif option == "accountno":
                        newAccountNo = int(input("Enter New Account Number : "))
                        user_exists['accountNo'] = newAccountNo
                        writeData(data)
                        break
                    else:
                        print("Invalid Option.")
                print("Changes Saved.")
            else:
                typing("User Not Found.")
        except Exception as e:
            typing(str(e))
        sleep(2)

    else:
        typing("Invalid Choice. Try Again.")
        sleep(1)
