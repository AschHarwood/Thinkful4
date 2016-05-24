import numpy as np 
import pandas as pd 
import statsmodels.api as sm 

loansData = pd.read_csv('https://github.com/Thinkful-Ed/curric-data-001-data-sets/raw/master/loans/loansData.csv')

#loansData.to_csv('loansData_clean.csv', header=True, index=False)

"""Cleaning Interest.Rate Column"""

cleanInterestRate = loansData['Interest.Rate'].map(lambda x: round((float(x.rstrip('%'))/100),4))
	
"""Cleaning Loan.Length Column"""

cleanLoanlength = loansData['Loan.Length'].map(lambda x: (float(x.rstrip('months'))))

"""Clean Fico Range"""


cleanFicorange = loansData['FICO.Range'].map(lambda x: x.split('-'))
cleanFicorange = cleanFicorange.map(lambda x: [int(n) for n in x])
cleanFicorange = cleanFicorange.map(lambda x: x[0])

"""rename Fico Range Column"""
loansData.rename(columns={'FICO.Range':'FICO.Score'}, inplace=True)

"""Convert columns in open file"""
loansData['FICO.Score'] = cleanFicorange

loansData['Interest.Rate'] = cleanInterestRate
loansData['Loan.Length'] = cleanLoanlength	

""""""

intrate = loansData['Interest.Rate'] #series is the datatype
loanamt = loansData['Amount.Requested']
fico = loansData['FICO.Score']

"""add a new column"""

#print intrate.values[0]

loansData['IR_TF'] = loansData['Interest.Rate'].map(lambda x: 1 if x > .12 else 0)
loansData['intercept'] = loansData['Interest.Rate'].map(lambda x: 1.0)

#print loansData[['Interest.Rate','IR_TF', 'intercept']][0:20]

ind_vars = ['FICO.Score', 'Amount.Funded.By.Investors', 'intercept']




loansData.to_csv('loansData_clean.csv', header=True, index=False)

"""logit model"""

logit = sm.Logit(loansData['IR_TF'], loansData[ind_vars]) #this is the logit model
result = logit.fit()
coeff = result.params
print(coeff)

