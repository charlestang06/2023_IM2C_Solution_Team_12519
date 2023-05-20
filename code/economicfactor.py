# Import required modules
import numpy as np
import os
import csv

# Define a class called EconomicFactor
class EconomicFactor:
    # Constructor method that initializes instance variables
    def __init__(self, symbol, ebitda_margin, pe_ratio, sales_growth, gross_profit_growth, std, rsi, ocf, competitors=[]):
        self.symbol = symbol
        self.ebitda_margin = ebitda_margin
        self.pe_ratio = pe_ratio
        self.sales_growth = sales_growth
        self.gross_profit_growth = gross_profit_growth
        self.std = std
        self.rsi = rsi
        self.ocf = ocf
        self.competitors = competitors #[[name, distance], [name, distance]]
    
    # Method that calculates the profit index for an EconomicFactor instance
    def profit_index(self):
        return self.ebitda_margin + 10 / self.pe_ratio

    # Method that calculates the growth index for an EconomicFactor instance
    def growth_index(self):
        return 0.01 * (0.3 * self.sales_growth + 0.7 * self.gross_profit_growth)
    
    # Method that calculates the risk index for an EconomicFactor instance
    def risk_index(self):
        return self.std / 100 + 1 / 80 * self.rsi - 1.1 / self.ocf
    
    # Method that calculates the competitor index for an EconomicFactor instance
    def competitor_index(self):
        total = 0
        for i in range(len(self.competitors)):
            total += 1 / np.sqrt(self.competitors[1])
        return total
    
    # Method that calculates the economic index for an EconomicFactor instance
    def economic_index(self):
        return self.profit_index() + self.growth_index() - self.risk_index() - self.competitor_index()

# Set the working directory to a specific location
os.chdir('C:\\Users\\charl\\MathModeling\\IM2C')

# Create an empty list called table to store EconomicFactor instances
table = []

# Open a CSV file called financialdata.csv in read mode
with open('financialdata.csv', 'r') as f:
    csvReader = csv.reader(f)
    # Read the header row of the CSV file
    fields = next(csvReader)

    # Iterate over each row in the CSV file
    for line in csvReader:
        # Extract the values from the row and convert them to floats
        temp = line[1:]
        temp[1:] = list(map(float, temp[1:]))
        # Create an EconomicFactor instance with the extracted values and append it to the table list
        table.append(EconomicFactor(*temp))

# Print the economic index for each EconomicFactor instance in the table list
for x in table:
    print(x.economic_index())
