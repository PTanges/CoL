import settings
from termcolor import colored

class Account:
  def __init__(self, city, state):
    self._city = city
    self._state = state
    self._isIncomeAdjust = False

  @property
  def city(self):
    return self._city

  @property
  def state(self):
    return self._state

  @property
  def annualSalary(self):
    return self._annualSalary

  @property
  def hourlySalary(self):
    return self._hourlySalary
    
  @property
  def housing(self):
    return self._housing
    
  @property
  def utilities(self):
    return self._utilities
    
  @property
  def essentials(self):
    return self._essentials
    
  @property
  def transportation(self):
    return self._transportation

  @property
  def livingExpenses(self):
    return self._livingExpenses
    
  @property
  def loans(self):
    return self._loans
    
  @property
  def medical(self):
    return self._medical
    
  @property
  def savings(self):
    return self._savings
    
  @property
  def misc(self):
    return self._misc
        
  @property
  def allowance(self):
    return self._allowance

  @property
  def description(self):
    return self._description

  @property
  def isIncomeAdjust(self):
    return self._isIncomeAdjust

  def setDescription(self, incomingText):
    self._description = incomingText

  def setHousing(self, housing):
    self._housing = housing;
  
  def createIncomeSheet(self, income):
    # Assumption that any number > 500 is the annual and not hourly
    if (income > 500):
      self._annualSalary = income
      self._hourlySalary = round(income / 2080, ndigits = 2)
    elif (income <= 500):
      self._hourlySalary = income
      self._annualSalary = income * 2080
    else:
      raise ValueError("Programmer has messed up")
  
  def createExpenseSheet(self, housing, utilities, transportation, livingExpenses, loans, medical, savings, misc):
    self._housing = housing
    self._utilities = utilities
    self._transportation = transportation
    self._livingExpenses = livingExpenses
    self._loans = loans
    self._medical = medical
    self._savings = savings
    self._misc = misc
    self._allowance = round(self._annualSalary/12, ndigits=2) - self._housing - self._utilities - self._transportation - self._livingExpenses - self._loans - self._medical - self._savings - self._misc

  def adjustExpenses(self, percentage):
    self._housing = round(self._housing * percentage, ndigits = 2)
    self._utilities = round(self._utilities * percentage, ndigits = 2)
    self._transportation = round(self._transportation * percentage, ndigits = 2)
    self._livingExpenses = round(self._livingExpenses * percentage, ndigits = 2)
    self._loans = round(self._loans * percentage, ndigits = 2)
    self._medical = round(self._medical * percentage, ndigits = 2)
    self._savings = round(self._savings * percentage, ndigits = 2)
    self._misc = round(self._misc * percentage, ndigits = 2)
    self.updateAllowance()
    
  def updateAllowance(self):
    self._allowance = round(self._annualSalary/12, ndigits=2) - self._housing - self._utilities - self._transportation - self._livingExpenses - self._loans - self._medical - self._savings - self._misc

  def adjustIncome(self):
    while (round(self._allowance - round((self.annualSalary * (1-settings.taxRate)/12), ndigits=2), ndigits=2)) < 0:
      self._hourlySalary += 0.25
      self._annualSalary = round(self._hourlySalary * 2080, ndigits=2)
      self.updateAllowance()
    self._isIncomeAdjust = True
  
  def resetAccount(self):
    # Set all values to 0
    pass

  def promptDescription(self):
    while True:
      description = input("Enter a short description of your status,\nie single Urban renter with diabetes, etc: ")
      if len(description) > 5:
        break
    return description
  
  def __str__(self):
    return f'Person lives in {self._city}, {self._state}'

  def printAccountSummary(self):
    # All values
    print(f'Person lives in {self._city}, {self._state}\n')
    print(f'>> Income:')

    if self._isIncomeAdjust == True:
      print(colored(f'Annual Salary:\t{self._annualSalary:,.2f} / Hourly: {self._hourlySalary}', "green"))
      print(colored(f'Monthly Salary:\t{round((self._annualSalary/12), ndigits=2):,.2f}\n', "green"))
    else:
      print(f'Annual Salary:\t{self._annualSalary:,.2f} / Hourly: {self._hourlySalary}')
      print(f'Monthly Salary:\t{round((self._annualSalary/12), ndigits=2):,.2f}\n')

    print(f'>> Housing & Utilities:')
    print(f'Housing:\t{self._housing:,}\nUtilities:\t{self._utilities:,}\n')
    print(f'>> Transportation:')
    print(f'Transportation:\t{self._transportation:,}\n')
    print(f'>> Living Expenses, such as food and clothes:')
    print(f'Living Expenses:\t{self._livingExpenses:,}\n')
    print(f'>> Loans, including credit card payments:')
    print(f'Loans:\t{self._loans:,}\n')
    print(f'>> Medical Related Expenditures:')
    print(f'Medical:\t{self._medical:,}\n')
    print(f'>> Miscellaneous Spending')
    print(f'Misc:\t{self._misc:,}\n')
    print(f'>> Savings:')
    print(f'Savings:\t{self._savings:,}\n')
    print(f'>> Approx monthly owed tax {round(((1 - settings.taxRate) * 100)):,.2f}%:')
    print(f'Tax owed:\t{round((self.annualSalary * (1-settings.taxRate)/12), ndigits=2):,.2f}')
    print(f'Allowance:\t{self._allowance:,.2f}\n')
    print(f'>> Remaining Allowance:')
    if (round(self._allowance - round((self.annualSalary * (1-settings.taxRate)/12), ndigits=2), ndigits=2)) <= 0:
      print(colored((f'Allowance:\t{round(self._allowance - round((self.annualSalary * (1-settings.taxRate)/12), ndigits=2), ndigits=2):,.2f}\n'), "red"))
    else:
      print(f'Allowance:\t{round(self._allowance - round((self.annualSalary * (1-settings.taxRate)/12), ndigits=2), ndigits=2):,.2f}\n')
    
    print(f'>> Description:')
    print(f'{self._description}\n')

  def printAllowance(self):
    if (round(self._allowance - round((self.annualSalary * (1-settings.taxRate)/12), ndigits=2), ndigits=2)) <= 0:
      print(colored((f'Allowance:\t{round(self._allowance - round((self.annualSalary * (1-settings.taxRate)/12), ndigits=2), ndigits=2):,.2f}\n'), "red"))

      # Prompt to get input for Y/N, adjusting Income
      _command = "foobar"
      while True:
        try:
          _command = input("\nExpenditure exceeds monthly income, would you like to increase the hourly wage to breakeven? [Y/N]: ")
          if _command == ("Y"):

            _priorAnnual = self._annualSalary
            _priorHourlySalary = self.hourlySalary
            print("Old Wage:")
            print(colored(f'Annual Salary:\t{_priorAnnual:,.2f} / Hourly: {_priorHourlySalary}', "red"))
            print(colored(f'Monthly Salary:\t{round((_priorAnnual/12), ndigits=2):,.2f}', "red"))
            print(colored((f'Monthly Debt:\t{round(self._allowance - round((self.annualSalary * (1-settings.taxRate)/12), ndigits=2), ndigits=2):,.2f}\n'), "red"))
            
            self.adjustIncome()
            print("New Wage:")
            print(colored(f'Annual Salary:\t{self._annualSalary:,.2f} / Hourly: {self._hourlySalary}', "green"))
            print(colored(f'Monthly Salary:\t{round((self._annualSalary/12), ndigits=2):,.2f}\n', "green"))
            print("New Allowance:")
            print(colored((f'Allowance:\t{round(self._allowance - round((self.annualSalary * (1-settings.taxRate)/12), ndigits=2), ndigits=2):,.2f}\n'), "green"))
            print("")
            break
          if _command == ("N"):
            break
        except ValueError:
          print("Invalid text, must be 'Y' or 'N' \n")
    else:
      print(f'Allowance:\t{round(self._allowance - round((self.annualSalary * (1-settings.taxRate)/12), ndigits=2), ndigits=2):,.2f}\n')
  
  def writeAccountSummary(self):
    f = open("guestbook.txt", "a")
    f.write(f'Person lives in {self._city}, {self._state}\n')
    f.write(f'>> Income:\n')
    f.write(f'Annual Salary:\t{self._annualSalary:,.2f} / Hourly: {self._hourlySalary}\n')
    f.write(f'Monthly Salary:\t{round((self._annualSalary/12), ndigits=2):,.2f}\n')
    f.write(f'>> Housing & Utilities:\n')
    f.write(f'Housing:\t{self._housing:,}\nUtilities:\t{self._utilities:,}\n')
    f.write(f'>> Transportation:\n')
    f.write(f'Transportation:\t{self._transportation:,}\n')
    f.write(f'>> Living Expenses, such as food and clothes:\n')
    f.write(f'Living Expenses:\t{self._livingExpenses:,}\n')
    f.write(f'>> Loans, including credit card payments:\n')
    f.write(f'Loans:\t{self._loans:,}\n')
    f.write(f'>> Medical Related Expenditures:\n')
    f.write(f'Medical:\t{self._medical:,}\n')
    f.write(f'>> Miscellaneous Spending\n')
    f.write(f'Misc:\t{self._misc:,}\n')
    f.write(f'>> Savings:\n')
    f.write(f'Savings:\t{self._savings:,}\n')
    f.write(f'>> Approx monthly owed tax {round(((1 - settings.taxRate) * 100)):,.2f}%:\n')
    f.write(f'Tax owed:\t{round((self.annualSalary * (1-settings.taxRate)/12), ndigits=2):,.2f}\n')
    f.write(f'Allowance:\t{self._allowance:,.2f}\n')
    f.write(f'>> Remaining Allowance:\n')
    f.write(f'Allowance:\t{round(self._allowance - round((self.annualSalary * (1-settings.taxRate)/12), ndigits=2), ndigits=2):,.2f}\n')
    f.write(f'>> Description:\n{self._description}\n')
    f.write("==== **** ====\n\n")
    f.close()