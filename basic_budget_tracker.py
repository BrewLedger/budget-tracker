# Personal Budget Tracker
# My very very first python budget app! 

print("============================")
print("  Welcome to Budget Tracker ")
print("============================") 

# My first step: Asking user for their income 
income = float(input("Enter your monthly income: $"))
print ("Got it! Your income is $" + str(income))

# Second step: Ask user for their expenses
expenses = []

while True:
    expense_name = input ("Enter expense name (or 'done' to stop): ")

    if expense_name =="done":
        break 

    expense_amount = float(input("Enter amount : $"))
    expenses.append((expense_name, expense_amount))

# Third step: Do calculation and show the summary 
total_expense = sum(amount for name, amount in expenses)
balance = income - total_expense

print("\n============================")
print("        YOUR SUMMARY        ")
print("============================")
print("Income:   $" + str(income))
print("Expenses: $" + str(total_expense))
print("----------------------------")
print("Balance:  $" + str(balance))
print("============================")

# Step 4 - Show each expense
print("\nExpense Breakdown:")
for name, amount in expenses:
    print("  - " + name + ": $" + str(amount)) 

