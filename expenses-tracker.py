#!/usr/bin/python3

from datetime import datetime
import os


def main():
    menu()


file_path = os.path.expanduser("~/Lab-3-Personal_Expenses_Tracker_NatnaelAyele/balance.txt")

def menu():
    while True:
        print("="*8, "Welcome to personal expense tracker", "="*8 )
        print("1. Check Remaining Balance")
        print("2. Add New Expense")
        print("3. View Expenses ")
        print("4. Exit")
        choice = input("enter your choise: ").strip()
        print("")

        if choice == '1':
            check_balance()
        elif choice == '2':
            add_expense()
        elif choice == '3':
            view_expense()
        elif choice == '4':
            break
        else:
             print("Invalid choise")

        print("")


def check_balance():
    with open (file_path, 'r') as f:
        contetnt = f.read()
        print("="*8 + "Balance report" + "="*8, contetnt, sep='\n')
    while True:
        choise = input("Want to add money (y/n): ").lower().strip()
        
        if choise == 'y':
            amount = add_balance()
            update_balance(amount)
            break

        elif choise == 'n':
            break
        else:
            print("Invalid option")

def  add_balance():
    while True:
        amount = input("Enter amount: ").strip()
        if amount:
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
    with open(file_path, 'r')as f:
        lines = f.readlines()
    current_balance = float(lines[0].split('=')[1].strip())
    available_balance = float(lines[2].split('=')[1].strip())
    lines[0] = f"balance = {amount + current_balance}\n"
    lines[2] = f"available balance = {amount + available_balance}"
    with open(file_path, 'w') as f:
        f.writelines(lines)

    print("Amount added to balance successfuly!")
    print(f"New balance is {amount + available_balance}")


def add_expense():
    with open(file_path) as f:
        lines = f.readlines()
    current_balance = float(lines[0].split('=')[1].strip())
    current_expense = float(lines[1].split('=')[1].strip())
    print(f"Available balance is {current_balance}")
    date = get_valid_date()
    item_list = get_item_price()
    print ("")
    print("="*9, "this are the inforation entered", "="*9)
    sum = 0
    for key in item_list:
        print(f"{key}: {item_list[key]}")
        sum += item_list[key]
    print ("=" * 50)
    print ("")

    filename = f"expenses_{date}.txt"
    expense_file_path = os.path.expanduser(f"~/Lab-3-Personal_Expenses_Tracker_NatnaelAyele/{filename}")
    
    while True:
        confirmation = input("Is the above information correct (y/n): ").lower().strip()
        if confirmation:
        
                if confirmation == 'y':
                    if sum < current_balance:
                        filename = f"expenses_{date}.txt"

                        if os.path.exists(expense_file_path):
                            with open(expense_file_path, "r") as f:
                                lines = f.readlines()
                                expense_id = len(lines) + 1
                        else:
                            expense_id = 1


                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        
                        with open(expense_file_path, "a") as f:
                            for key in item_list:
                                f.write(f"{expense_id}. {timestamp} | {key} | {item_list[key]}\n")
                                expense_id += 1

                        
                        new_balance = current_balance - sum
                        with open(file_path, 'r') as f:
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
                elif confirmation == 'n':
                    break
        else:
            print("invalid input")



def get_valid_date():
    while True:
        date_input = input("Enter date (YYYY-MM-DD): ").strip()

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
        choice = input("Enter your choice: ").strip()
    
        if choice == '1':
            while True:
                name = input("Enter name: ")
                if name.strip():
                    results = search_by_item(name)
                    print_search_results(results)
                    break
                else:
                    print("Invalid input")

        elif choice == '2':
            while True:
                amount = input("Enter paid amount: ")
                if amount.strip():
                    results = search_by_amount(amount)
                    print_search_results(results)
                    break
                else:
                     print("Invalid input")
        elif choice == '3':
            break
        else:
            print("invalid choice")

expenses_dir = os.path.expanduser("~/Lab-3-Personal_Expenses_Tracker_NatnaelAyele/")

def get_expense_files():
    files = []
    for file in os.listdir(expenses_dir):
        if file.startswith("expenses_") and file.endswith(".txt"):
            files.append(os.path.join(expenses_dir, file))
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
        print("")
        return

    print("\n=== Search Results ===")
    for file, line in results:
        print(f"[{file}] {line}")
        print("")



if __name__ == "__main__":
    main()
