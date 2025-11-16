#!/usr/bin/python3

def menu():
    while True:
        print("="*8, "Welcome to personal expense tracker", "="*8 )
        print("1. Check Remaining Balance")
        print("2. Add New Expense")
        print("3. View Expenses ")
        choice = input("enter your choise: ")
        print("")

        match choice:
            case '1':
                check_balance()
            case '2':
                ...
            case '3':
               ...
            case _:
                print("Invalid choise")

        print("")


def check_balance():
    with open ('balance.txt', 'r') as f:
        contetnt = f.read()
        print("="*8 + "Balance report" + "="*8, contetnt, sep='\n')
    while True:
        choise = input("Want to add money (y/n): ")
        
        match choise:
            case 'y' | 'Y':
                amount = add_balance()
                update_balance(amount)
                break

            case 'n' | 'N':
                break

def  add_balance():
    while True:
        amount = input("Enter amount: ")
        if amount:
            try:
                amount = float(amount)
                if amount <= 0:
                    print("amount must be greater than zero")
                else:
                    return amount
            except:
                print("Amount must be a number")
        else:
            print("Amount can't be empty")


def update_balance(amount):
    with open('balance.txt', 'r')as f:
        lines = f.readlines()
    current_balance = float(lines[0].split('=')[1].strip())
    available_balance = float(lines[2].split('=')[1].strip())
    lines[0] = f"balance = {amount + current_balance}\n"
    lines[2] = f"available balance = {amount + available_balance}"
    with open('balance.txt', 'w') as f:
        f.writelines(lines)

    print("Amount added to balance successfuly!")
    print(f"New balance is {amount + available_balance}")

menu()
