from datetime import datetime

income = 0
expenses = 0
income_history = []
expenses_history = []

def main():
    summary(income, expenses)

    functions = [add_income, add_expense, view_history]
    while True:
        choice = input("""Select what you want to do:
1: Add to your income
2: Add an expense
3: View history
""")
        if choice.isdigit() == True:
            if int(choice) > 0 and not int(choice) > len(functions):
                selection = functions[int(choice)-1]
                selection()
                break
            else:
                print("Please select one of the options.")
        else:
            print("Please input a number.")
    
    
# prints summary of income and expenses
def summary(income, expenses):
    print("Your current income per month: ${}".format(income))
    print("Your current total expenses per month: ${}".format(expenses))

# allows user to add to income
def add_income():
    global income, expenses, income_history
    while True:
        added_income = input("Input how much you want to add to your income: ")
        if added_income.isdigit() == True:
            if int(added_income) > 0:   
                income += int(added_income)
                time = datetime.now()
                break
            else:
                print("Please add an integer above 0.")
        else:
            print("Please input a number.")
    note = input("Add a note (otherwise leave empty): ")
    transaction = [int(added_income), time, note]
    income_history.append(transaction)
    main()

# allows user to add an expense
def add_expense():
    global income, expenses, expenses_history
    while True:
        added_expense = input("Input how much you want to add to your expenses: ")
        if added_expense.isdigit() == True:
            if int(added_expense) > 0:   
                expenses += int(added_expense)
                time = datetime.now()
                break
            else:
                print("Please add an integer above 0.")
        else:
            print("Please input a number.")
    note = input("Add a note (otherwise leave empty): ")
    transaction = [int(added_expense), time, note]
    expenses_history.append(transaction)
    main()

def view_history():
    while True:
        choice = input("""Select what you want to do:
1: View income history
2: View expenses history
""")
        if choice.isdigit() == True:
            if int(choice) > 0 and not int(choice) > 2:
                choice2 = income_history if int(choice) == 1 else expenses_history
                break
            else:
                print("Please select one of the options.")
        else:
            print("Please input a number.")

    for transaction in choice2:
        amount = "$" + str(transaction[0])
        date_time = datetime.strftime(transaction[1], "%m/%d/%Y, %H:%M:%S")
        note = transaction[2]
        print("{}\t{}\t{}".format(amount, date_time, note))
    

main()