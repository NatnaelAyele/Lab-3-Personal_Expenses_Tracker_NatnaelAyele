#!/usr/bin/python3

from datetime import datetime
import os


def main():
    menu()

# store the location of 'balance.txt' in avariable
file_path = os.path.expanduser("~/Lab-3-Personal_Expenses_Tracker_NatnaelAyele/balance.txt")


# displays the main menu of the program
def menu():

    # an infinite loop that presents a menu and calls appropriate functions to perform the selected task until the user presses 4 to exit.
    while True:
        print("="*8, "Welcome to personal expense tracker", "="*8 )
        print("1. Check Remaining Balance")
        print("2. View Expenses ")
        print("3. Add New Expense")
        print("4. Exit")
        choice = input("enter your choise: ").strip()
        print("")

        if choice == '1':
            check_balance()
        elif choice == '2':
            view_expense()
        elif choice == '3':
            add_expense()
        elif choice == '4':
            print("exiting program......")
            break
        else:
             print("Invalid choise")

        print("")


"""
reads and displays the current balance, then asks the user.
if they want to add money. If yes, it collects the amount and updates the file. if no, returns to main menu
"""

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


# asks the user for an amount to add and ensures it is a valid positive number.
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


# updates the balance and available balance values in the 'balance.txt' file.
def update_balance(amount):
    with open(file_path, 'r')as f:
        lines = f.readlines()

     # Extract existing balance values from the file by spliting contents of the lines
    current_balance = float(lines[0].split('=')[1].strip())
    available_balance = float(lines[2].split('=')[1].strip())

    # update the balance and available balance amounts
    lines[0] = f"balance = {amount + current_balance}\n"
    lines[2] = f"available balance = {amount + available_balance}"

    # write the updated lines
    with open(file_path, 'w') as f:
        f.writelines(lines)

    print("Amount added to balance successfuly!")
    print(f"New balance is {amount + available_balance}")


# Reads the current balance, collects expense items with their price, and saves them to a dated expense file.
def add_expense():

    # Read and store balance information from balance.txt
    with open(file_path) as f:
        lines = f.readlines()
    current_balance = float(lines[0].split('=')[1].strip())
    current_expense = float(lines[1].split('=')[1].strip())
    print(f"Available balance is {current_balance}")

    # calls get_valid_date() to get a valid date from the user
    date = get_valid_date()

    #calls get_item_price to get a dictionary of name-price pair value for items
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
    

    # an infinite loop that asks if the information for the expense is correct or not until pressed y for yes or n for no.
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

                            
                        # append each item with its id, time stamp, name and price to 'expense-YYYY-MM-DD.txt'

                        with open(expense_file_path, "a") as f:
                            for key in item_list:
                                f.write(f"{expense_id}. {timestamp} | {key} | {item_list[key]}\n")
                                expense_id += 1

                        
                        new_balance = current_balance - sum
                        
                        # update the infromation inside balance.txt
                        with open(file_path, 'r') as f:
                            lines = f.readlines()
                        lines[0] =f"balance = {new_balance}\n"
                        lines[1] =f"Total expenses to date = {current_expense + sum}\n"
                        lines[2] =f"Available balance = {new_balance}\n"
                        with open(file_path, 'w') as f:
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



# Prompts the user for a date and ensures it follows YYYY-MM-DD format.
def get_valid_date():

    # an infinite loop that asks for date until a correct formated date is inserted
    while True:
        date_input = input("Enter the date the items were bought (format: YYYY-MM-DD): ").strip()

        try:
            valid_date = datetime.strptime(date_input, "%Y-%m-%d")
            return valid_date.date()
        except ValueError:
            print("Invalid input. Please use YYYY-MM-DD and check it's a real date.")


# Asks the user for the number of items, then collects item names and prices.
def get_item_price():
    items = {}
    
    # an infinite loop that asks how many items you want to insert until an integer number is pressed
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

    
    # iterate for the number of times the user inserted, asking the name and price in each iteration
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
        
        # store the name and the price for an item as a key-value pair in a dictionary
        items[item] = price

    return items



# Displays the expense search menu and handles search actions.
def view_expense():

    # an infinite loop that presents a menu and calls appropriate functions to perform the selected task until the user presses 3 to exit.
    while True:
        print("1. search by item name")
        print("2. search by amount")
        print("3. back to main menu")
        choice = input("Enter your choice: ").strip()
        
        # Search by item name
        if choice == '1':
            while True:
                name = input("Enter name: ")
                if name.strip():
                    results = search_by_item(name)
                    print_search_results(results)
                    break
                else:
                    print("Invalid input")
        

        # Search by amount
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


# Returns a list of 'expenses-YYYY-MM-DD.txt' files found in the directory.
def get_expense_files():
    files = []
    for file in os.listdir(expenses_dir):
        if file.startswith("expenses_") and file.endswith(".txt"):
            files.append(os.path.join(expenses_dir, file))
    return files


# Searches all 'expenses-YYYY-MM-DD.txt' files for items that match the given name.
def search_by_item(item_name):

    # Get list of all expense files in the directory
    files = get_expense_files()
    item_name = item_name.lower()

    results = []

    for file in files:
        with open(file) as f:
            for line in f:
                try:
                    
                    # split each line to into part separated by '|' and store the item name
                    parts = line.strip().split(" | ")
                    item = parts[1].lower()
                    
                     # check if name entered matches any name from the file and append it to a list
                    if item_name in item:
                        results.append((file, line.strip()))
                except:
                    continue

    return results


# Searches all 'expenses-YYYY-MM-DD.txt' files for items that match the given amount.
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

                    # split each line to into part separated by '|' and store the amount
                    parts = line.strip().split(" | ")
                    price = float(parts[2])

                    # check if amount entered matches any amount from the file and append it to a list
                    if price == amount:
                        results.append((file, line.strip()))
                except:
                    continue

    return results   

# Prints the search results in a readable format.
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
