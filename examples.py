from account import Account

def createExamples(guidebook):
  Single = Account("SAN FERNANDO", "CALIFORNIA")
  Single.createIncomeSheet(62400)
  Single.createExpenseSheet(1300, 400, 1000, 460, 0, 110, 220, 0)
  Single.setDescription("Renting a studio, some student debt, a car loan, and under parents medical insurance")
  guidebook.append(Single)

  Couple = Account("NASHVILLE", "TENNESSEE")
  Couple.createIncomeSheet(28)
  Couple.createExpenseSheet(1224, 270, 325, 800, 0, 160, 0, 447)
  Couple.setDescription("Homeowner couple. Company offers cheap Health, Dental, and Medical Care (paid into monthly). No student, phone, or automobile debt. Urban residence")
  guidebook.append(Couple)