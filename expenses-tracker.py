#!/usr/bin/python3

from datetime import datetime
import os


def menu():
    while True:
        print("="*8, "Welcome to personal expense tracker", "="*8 )
        print("1. Check Remaining Balance")
        print("2. Add New Expense")
        print("3. View Expenses ")
        print("4. Exit")
        choice = input("enter your choise: ").strip()
        print("")

        match choice:
            case '1':
                check_balance()
            case '2':
                add_expense()
            case '3':
                view_expense()
            case '4':
                break
            case _:
                print("Invalid choise")

        print("")


def check_balance():
    with open ('balance.txt', 'r') as f:
        contetnt = f.read()
        print("="*8 + "Balance report" + "="*8, contetnt, sep='\n')
    while True:
        choise = input("Want to add money (y/n): ").strip()
        
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
        if amount.stip():
            try:
                amount = float(amount)
                if amount <= 0:
                    print("amount must be greater than zero")
                else:
                    return amount
            except ValueError:
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


def add_expense():
    with open('balance.txt') as f:
        lines = f.readlines()
    current_balance = float(lines[0].split('=')[1].strip())
    current_expense = float(lines[1].split('=')[1].strip())
    print(f"Available balance is {current_balance}")
    date = get_valid_date()
    item_list = get_item_price()
    print("="*9, "this are the inforation entered", "="*9)
    sum = 0
    for key in item_list:
        print(f"{key}: {item_list[key]}")
        sum += item_list[key]
    while True:
        confirmation = input("Is the above information correct (y/n): ").lower().stip()
        if confirmation:
            match confirmation:
                case 'y':
                    if sum < current_balance:
                        filename = f"expenses_{date}.txt"

                        if os.path.exists(filename):
                            with open(filename, "r") as f:
                                lines = f.readlines()
                                expense_id = len(lines) + 1
                        else:
                            expense_id = 1


                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        
                        with open(filename, "a") as f:
                            for key in item_list:
                                f.write(f"{expense_id}. {timestamp} | {key} | {item_list[key]}\n")
                                expense_id += 1

                        
                        new_balance = current_balance - sum
                        with open('balance.txt', 'r') as f:
                            lines = f.readlines()
                        lines[0] =f"balance = {new_balance}\n"
                        lines[1] =f"Total expenses to date = {current_expense + sum}\n"
                        lines[2] =f"Available balance = {new_balance}\n"
                        with open('balance.txt', 'w') as f:
                            f.writelines(lines)

                        print("Expenses saved successfully!")
                        print(f"New available balance: {new_balance}")
                        break
                    else:
                        print("insufficient balance! can not save expense")
                        break
                case 'n':
                    break
        else:
            print("invalid input")



def get_valid_date():
    while True:
        date_input = input("Enter date (YYYY-MM-DD): ").stip()

        try:
            valid_date = datetime.strptime(date_input, "%Y-%m-%d")
            return valid_date.date()
        except ValueError:
            print("Invalid input. Please use YYYY-MM-DD and check it's a real date.")


def get_item_price():
    items = {}

    while True:
        i = input("How many items do you want to insert: ")
        if not i.strip():
            print("Invalid input")
            continue

        try:
            i = int(i)
            if i <= 0:
                print("Number must be greater than zero")
                continue
            break
        except:
            print("Must be a number!!!!")


    for _ in range(i):

        while True:
            item = input("Enter the name of the item: ").strip()
            if item:
                break
            print("Invalid item name")


        while True:
            price = input(f"Enter the price for {item}: ").strip()
            if not price:
                print("Invalid price")
                continue
            try:
                price = float(price)
                if price <= 0:
                    print("Price cannot be less than or equal to zero")
                    continue
                break
            except:
                print("Price must be a number")

        items[item] = price

    return items


def view_expense():
    while True:
        print("1. search by item name")
        print("2. search by amount")
        print("3. back to main menu")
        choice = input("Enter your choice: ").stip()
        match choice:
            case '1':
                while True:
                    name = input("Enter name: ")
                    if name.strip():
                        results = search_by_item(name)
                        print_search_results(results)
                        break
                    else:
                        print("Invalid input")

            case '2':
                 while True:
                    amount = input("Enter paid amount: ")
                    if amount.stip():
                        results = search_by_amount(amount)
                        print_search_results(results)
                        break
                    else:
                        print("Invalid input")
            case '3':
                break
            case _:
                print("invalid choice")

def get_expense_files():
    files = []
    for file in os.listdir():
        if file.startswith("expenses_") and file.endswith(".txt"):
            files.append(file)
    return files

def search_by_item(item_name):
    files = get_expense_files()
    item_name = item_name.lower()

    results = []

    for file in files:
        with open(file) as f:
            for line in f:
                try:
                    parts = line.strip().split(" | ")
                    item = parts[1].lower()
                    if item_name in item:
                        results.append((file, line.strip()))
                except:
                    continue

    return results

def search_by_amount(amount):
    files = get_expense_files()

    try:
        amount = float(amount)
    except:
        print("Amount must be a number.")
        return []

    results = []

    for file in files:
        with open(file) as f:
            for line in f:
                try:
                    parts = line.strip().split(" | ")
                    price = float(parts[2])
                    if price == amount:
                        results.append((file, line.strip()))
                except:
                    continue

    return results

def print_search_results(results):
    if not results:
        print("No matches found.")
        return

    print("\n=== Search Results ===")
    for file, line in results:
        print(f"[{file}] {line}")


menu()
