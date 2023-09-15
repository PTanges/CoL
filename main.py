from account import Account
import examples
import settings
from termcolor import colored

def createTextfile():
  f = open("guestbook.txt", "w")
  f.write("==== **** ====\n")
  f.close()

def fillGuestBook(guestbook):
  city, state = validateTextInput()
  Guest = Account(city, state)
  Guest.createIncomeSheet(calculateSalary())
  expenses = {}
  promptExpenses(expenses)
  Guest.createExpenseSheet(expenses["housing"], expenses["utilities"], expenses["transportation"], expenses["livingExpenses"], expenses["loans"], expenses["medical"], expenses["savings"], expenses["misc"])
  Guest.setDescription(Guest.promptDescription())
  guestbook.append(Guest)
  Guest.printAllowance()
  print() # Formatting
  print("Successfully saved to guestbook!\n")

def promptCommand(command):
  commands = "[1] View Entries\n"
  commands += "[2] Create new Entry\n"
  commands += "[3] Calculate Hourly or Yearly Salary\n"
  commands += "[4] Change existing entry's cost of rent\n"
  commands += "[5] Adjust ALL expenses by a percentage (%)\n"
  commands += "[6] Calculate income required for budget\n"
  commands += "[7] Export guests to text file\n"
  commands += "[11] Exit Program\n"
  commands += "Command: "
  while True:
    try:
      command = int(input(">> Enter a valid command\n" + commands))
      if command > 0:
        break
    except ValueError:
      print("Invalid input, try again\n")

  return command

def _promptExpenses(prompts):
  prompts["housing"] = "Enter monthly housing/rent cost: $"
  prompts["utilities"] = "Enter monthly utilities cost, including phone and wifi: $"
  prompts["transportation"] = "Enter monthly transportation costs,\nsuch as auto loan, insurance, maintenance and gasoline: $"
  prompts["livingExpenses"] = "Enter monthly living expenses,\nsuch as food clothes and household supplies: $"
  prompts["loans"] = "Enter monthly loan payments, including credit card: $"
  prompts["medical"] = "Enter monthly medical related expenses such as insurance: $"
  prompts["savings"] = "Enter monthly amount sent to savings and or 401k: $"
  prompts["misc"] = "Enter monthly miscellanous expenditures: $"

def promptExpenses(expenses):
  # Order: housing, utilities, transportation, livingExpenses, loans, medical, savings, misc
  count = 0
  prompts = {}
  _promptExpenses(prompts)
  
  while True:
    try:
      expenses["housing"] = float(input(prompts["housing"]))
      expenses["utilities"] = float(input(prompts["utilities"]))
      expenses["transportation"] = float(input(prompts["transportation"])) 
      expenses["livingExpenses"] = float(input(prompts["livingExpenses"]))
      expenses["loans"] = float(input(prompts["loans"]))
      expenses["medical"] = float(input(prompts["medical"]))
      expenses["savings"] = float(input(prompts["savings"])) 
      expenses["misc"] = float(input(prompts["misc"]))
      
      if all(expenses) > 0:
        break
    except ValueError:
      print("Invalid input, enter a number greater than 0...\n")
  
def calculateSalary():
  while True:
    try:
      salary = float(input("Enter your hourly or yearly salary: $"))
      if salary > 500:
        print(f'Yearly Salary: {round(salary, ndigits=2):,.2f}\nHourly Salary: {round(salary/2080, ndigits=2):,.2f}\n')
        break
      elif salary <= 500 and salary > 0:
        print(f'Yearly Salary: {round(salary * 2080, ndigits=2):,.2f}\nHourly Salary: {round(salary, ndigits=2):,.2f}\n')
        break
    except ValueError:
      print("Invalid input, try again\n")
  
  salary = round(salary, ndigits = 2)
  return salary

def _budgetRentChange(newRent, housingCost):
  while True:
    print(f'${housingCost:,.2f} is the current housing cost...')
    try:
      newRent = float(input("input a new cost: $"))
      if newRent > 0:
        print("Success!\n====\nNew Budget:")
        break
    except ValueError:
      print("Invalid housing cost, try again\n")
  return newRent

def budgetRentChange(guestbook, guidebook):
  city, state = validateTextInput()
  guideFound = False
  
  for guide in guidebook:
    if guide.city == city and guide.state == state:
      newRent = "0.0"
      newRent = _budgetRentChange(newRent, guide.housing)
      
      guide.setHousing(newRent)
      guide.updateAllowance()
      guide.printAccountSummary()
      guideFound = True
      break

  guestFound = False
  if len(guestbook) > 0 and guideFound == False:
    for guest in guestbook:
      if guest.city == city and guest.state == state:
        newRent = "0.0"
        newRent = _budgetRentChange(newRent, guest.housing)
        
        guest.setHousing(newRent)
        guest.updateAllowance()
        guest.printAccountSummary()
        guestFound = True
        break
  
  if guideFound == False and len(guestbook) == 0:
    print("No such entry exists... try again\n")
  elif len(guestbook) > 0 and guestFound == False:
    print("No such entry exists... try again\n")

def _adjustBudgetByPercent(percentage):
  increaseOrDecrease = ""
  while True:
    try:
      percentage = float(input("Adjust by a set %, writen as an integer (20% would be written as 20): %"))
      if percentage <= 150 and percentage > 0:
        break
      else:
        print("Number must be a positive integer between 1 and 150, try again\n")
    except ValueError:
      print("Invalid input, try again\n")

  while True:
    try:
      increaseOrDecrease = input("Increase or Decrease? ").upper()
      if increaseOrDecrease.startswith("I"):
        percentage = 1 + (percentage/100)
        break
      elif increaseOrDecrease.startswith("D"):
        percentage = 1 - (percentage/100)
        break
      else:
        print("Command not supported... must be 'Increase' or 'Decrease'")
    except ValueError:
      print("Invalid text, must be 'Increase' or 'Decrease' \n")
  
  print("Success!\n====\nNew Budget:")
  return percentage

def adjustBudgetByPercent(guidebook, guestbook):
  city, state = validateTextInput()
  guideFound = False
  
  for guide in guidebook:
    if guide.city == city and guide.state == state:
      percentage = "0.0"
      percentage = _adjustBudgetByPercent(percentage)

      guide.adjustExpenses(percentage)
      guide.printAccountSummary()
      guideFound = True
      break

  guestFound = False
  if len(guestbook) > 0 and guideFound == False:
    for guest in guestbook:
      if guest.city == city and guest.state == state:
        percentage = "0"
        percentage = _adjustBudgetByPercent(percentage)
        
        guest.adjustExpenses(percentage)
        guest.printAccountSummary()
        guestFound = True
        break
  
  if guideFound == False and len(guestbook) == 0:
    print("No such entry exists... try again\n")
  elif len(guestbook) > 0 and guestFound == False:
    print("No such entry exists... try again\n")

def validateTextInput():
  while True:
    city = input("Enter the city name: ").upper()
    state = input("Enter the state: ").upper()
    if all(char.isalpha() or char.isspace() for char in city):
      if all(char.isalpha() or char.isspace() for char in state):
        break
    else:
      print("Invalid city or state name, try again\n")
  return city, state

def promptSubEntryCommand(guestbook, guidebook):
  commands = "[1] View guide examples\n"
  if len(guestbook) > 0:
    commands += "[2] View user entries\n"
    commands += "[3] Back to main menu\nCommand: "
  else:
    commands += "[2] Back to main menu\nCommand: "
  while True:
    try:
      command = int(input(">> Enter a valid command\n" + commands))
      if command == 1:
        for guide in guidebook:
          print("==== **** ==== **** ====")
          guide.printAccountSummary()
      elif command == 2:
        if len(guestbook) > 0:
          for guest in guestbook:
            print("==== **** ==== **** ====")
            guest.printAccountSummary()
        else:
          break
      elif command == 3:
        break
    except ValueError:
      print("Invalid input, try again\n")

def _calculateIncomeByRent(guestbook, guidebook):
  city, state = validateTextInput()
  guideFound = False
  
  for guide in guidebook:
    if guide.city == city and guide.state == state:
      newRent = "0.0"
      newRent = _budgetRentChange(newRent, guide.housing)
      
      guide.setHousing(newRent)
      guide.updateAllowance()
      guide.adjustIncome()
      guide.printAccountSummary()
      guideFound = True
      break

  guestFound = False
  if len(guestbook) > 0 and guideFound == False:
    for guest in guestbook:
      if guest.city == city and guest.state == state:
        newRent = "0.0"
        newRent = _budgetRentChange(newRent, guest.housing)
        
        guest.setHousing(newRent)
        guest.updateAllowance()
        guide.adjustIncome()
        guest.printAccountSummary()
        guestFound = True
        break
  
  if guideFound == False and len(guestbook) == 0:
    print("No such entry exists... try again\n")
  elif len(guestbook) > 0 and guestFound == False:
    print("No such entry exists... try again\n")

def _calculateIncomeByPercent(guestbook, guidebook):
  city, state = validateTextInput()
  
  for guide in guidebook:
    if guide.city == city and guide.state == state:
      percentage = "0.0"
      percentage = _adjustBudgetByPercent(percentage)

      guide.adjustExpenses(percentage)
      guide.adjustIncome()
      guide.printAccountSummary()
      guideFound = True
      break

  guestFound = False
  if len(guestbook) > 0 and guideFound == False:
    for guest in guestbook:
      if guest.city == city and guest.state == state:
        percentage = "0"
        percentage = _adjustBudgetByPercent(percentage)
        
        guest.adjustExpenses(percentage)
        guide.adjustIncome()
        guest.printAccountSummary()
        guestFound = True
        break
  
  if guideFound == False and len(guestbook) == 0:
    print("No such entry exists... try again\n")
  elif len(guestbook) > 0 and guestFound == False:
    print("No such entry exists... try again\n")

def _promptSubIncomeCommandExisting(guestbook, guidebook):
  commands = "[1] Adjust ALL existing expenses for entry by a percentage (%)\n"
  commands += "[2] Adjust ONLY existing Housing cost for an entry\n"
  commands += "[3] Back to main menu\nCommand: "
  while True:
    try:
      command = int(input(">> Enter a valid command\n" + commands))
      if command == 1:
        _calculateIncomeByPercent(guestbook, guidebook)
        break
      elif command == 2:
        _calculateIncomeByRent(guestbook, guidebook)
        break
      elif command == 3:
        break
    except ValueError:
      print("Invalid command, try again\n")

def _promptSubIncomeCommandNew(guestbook):
  city, state = validateTextInput()
  Guest = Account(city, state)
  Guest.createIncomeSheet(0.0)
  expenses = {}
  promptExpenses(expenses)
  Guest.createExpenseSheet(expenses["housing"], expenses["utilities"], expenses["transportation"], expenses["livingExpenses"], expenses["loans"], expenses["medical"], expenses["savings"], expenses["misc"])
  Guest.setDescription(Guest.promptDescription())
  Guest.adjustIncome()
  Guest.printAccountSummary()
  guestbook.append(Guest)

def promptSubIncomeCommand(guestbook, guidebook):
  commands = "[1] Calculate income based on existing entry\n"
  commands += "[2] Calculate income based on NEW entry\n"
  commands += "[3] Back to main menu\nCommand: "
  while True:
    try:
      command = int(input(">> Enter a valid command\n" + commands))
      if command == 1:
        _promptSubIncomeCommandExisting(guestbook, guidebook)
        break
      elif command == 2:
        _promptSubIncomeCommandNew(guestbook)
        break
      elif command == 3:
        break
    except ValueError:
      print("Invalid command, try again\n")

def exportGuests(guestbook):
  createTextfile()
  if len(guestbook) == 0:
    print("Guestbook is empty!\n")
    return

  for guest in guestbook:
    guest.writeAccountSummary()
  print("Successfully written to guestbook.txt!")
  print("Open the files tab on the top left in order to acces the text file")
  print("Note! This file resets upon the program booting up again...\n")

  # Formatting
  input("\nPlease click enter to continue...\n")
  
def main():
  guestbook = []
  guidebook = []
  examples.createExamples(guidebook)
  
  command = ""
  while True:
    command = promptCommand(command)

    # View Entries
    if command == 1:
      promptSubEntryCommand(guestbook, guidebook)
    # Create Entry
    elif command == 2:
      fillGuestBook(guestbook)
    # Calculate Hourly or Yearly Salary
    elif command == 3:
      calculateSalary()
    # Budget adjustment based on rent change
    elif command == 4:
      budgetRentChange(guestbook, guidebook)
    # % CoL increase or decrease
    elif command == 5:
      adjustBudgetByPercent(guestbook, guidebook)
    # Calulate Required Income from input budget
    elif command == 6:
      promptSubIncomeCommand(guestbook, guidebook)
    elif command == 7:
      exportGuests(guestbook)
    # Quit
    elif command == 11:
      print("Saving data to guestbook.txt ...")
      try:
        exportGuests(guestbook)
        print("Success!")
      except:
        print("Error!")
      print("Program terminated")
      break

if __name__ == "__main__":
  main()