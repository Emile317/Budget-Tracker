from datetime import datetime
import tkinter as tk
from tkinter import ttk
import json

with open("main.json", "r") as json_read:
    json_data = json.load(json_read)

print(json_data)

def main():
    summary(json_data["income"], json_data["expenses"])

    functions = [add_income, add_expense, view_history, save_and_quit]
    while True:
        choice = input("""Select what you want to do:
1: Add to your income
2: Add an expense
3: View history
4: Save and quit
""")    
        # checks if choice is int and calls chosen function
        try:
            int(choice)
        except ValueError:
            print("Please input a number")
            continue
        functions[int(choice)-1]() if 0 < int(choice) <= len(functions) else print("Please select one of the options")
        
    
    
# prints summary of income and expenses
def summary(income, expenses):
    print("Your current income per month: ${}".format(income))
    print("Your current total expenses per month: ${}".format(expenses))

# allows user to add to income
def add_income():
    while True:
        added_income = input("Input how much you want to add to your income: ")
        if added_income.isdigit() == True:
            if int(added_income) > 0:   
                json_data["income"] += int(added_income)
                time = datetime.strftime(datetime.now(), "%m/%d/%Y, %H:%M:%S")
                break
            else:
                print("Please add an integer above 0.")
        else:
            print("Please input a number.")
    note = input("Add a note (otherwise leave empty): ")
    transaction = [int(added_income), time, note]
    json_data["income_history"].append(transaction)
    main()

# allows user to add an expense
def add_expense():
    while True:
        added_expense = input("Input how much you want to add to your expenses: ")
        if added_expense.isdigit() == True:
            if int(added_expense) > 0:   
                json_data["expenses"] += int(added_expense)
                time = datetime.strftime(datetime.now(), "%m/%d/%Y, %H:%M:%S")
                break
            else:
                print("Please add an integer above 0.")
        else:
            print("Please input a number.")
    note = input("Add a note (otherwise leave empty): ")
    transaction = [int(added_expense), time, note]
    json_data["expenses_history"].append(transaction)
    main()

def view_history():
    while True:
        choice = input("""Select what you want to do:
1: View history
2: View history of certain time period
""")
        if choice.isdigit() == True:
            if int(choice) > 0 and not int(choice) > 2:
                choice2 = json_data["income_history"] if int(choice) == 1 else json_data["expenses_history"]
                break
            else:
                print("Please select one of the options.")
        else:
            print("Please input a number.")

    for transaction in json_data["income_history"]:
        income_amount = "$" + str(transaction[0])
        income_date_time = transaction[1]
        income_note = transaction[2]
    
    for transaction in json_data["expenses_history"]:
        expenses_amount = "$" + str(transaction[0])
        expenses_date_time = transaction[1]
        expenses_note = transaction[2]
    
    print("Income history\t\t\t\tExpenses history")
    print("{}\t{}\t{}\t\t{}\t{}\t{}".format(income_amount, income_date_time, income_note, expenses_amount, expenses_date_time, expenses_note))
    main()
    
def save_and_quit():
    with open("main.json", "w") as write_file:
        json.dump(json_data, write_file, indent=4)
    quit()

root = tk.Tk()
root.title("Budget Tracker")

mainframe = ttk.Frame(root)
mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))

button = ttk.Button(mainframe, text="quit", command=save_and_quit)
button.grid(column=3, row=3)

main()