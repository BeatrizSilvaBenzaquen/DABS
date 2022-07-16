# -*- coding: utf-8 -*-
"""

@author: Beatriz Silva
"""

#%% Libraries

import pandas as pd
import json
from pathlib import Path

#%% Load file

FilePath = input("Please enter the File path:\n")

#Variables
Data = []
deb=1 # Flag for verbose mode

# To open and save all the files in the path
with open(FilePath,encoding="utf8") as file:
    contents = file.readlines()
    
#To separarte all the log information (assuming that in all the files the diferents columns are separated by a space)
for line in contents:
    Data.append(line.split())
 
if (deb==1): print("Success loading the file")

#Saving the data in data frames in order to work in the information
dfData = pd.DataFrame(Data)
#Prepocresing of the data (Clean all the None from the dataframe and Fiels in the right type)
dfData.dropna()
dfData[0]=pd.to_numeric(dfData[0])
dfData[1]=pd.to_numeric(dfData[1])
dfData[4]=pd.to_numeric(dfData[4])


#%% Functions with the different operations
# Assuming the order of the information in the columns is always the same (IP in the field 3, size in bytes field 5 ...)

def Operation1():
    '''
    1. Most frequent IP

    Returns
    -------
    op1 :
        The most common CLIENT IP address

    '''
    op1=dfData[2].value_counts().idxmax()
    return op1

def Operation2():
    '''
    2. Least frequent
    This will be all the IP used one time
    Returns
    -------
    op2 : 
        The lest common CLIENT IP address

    '''
    #op2=dfData[2].value_counts().idxmin()
    op2=[ip[0] for ip in zip(dfData[2].value_counts().index,dfData[2].value_counts()) if ip[1]==1]
    return op2

def Operation3():
    '''
    3.  Events per second

    Returns
    -------
    op3 : 
        Events per second

    '''
    min_TS=dfData[0].min()
    max_TS=dfData[0].max()
    num_Events=dfData[0].count()
    op3=(max_TS-min_TS)/num_Events
    return op3

def Operation4():
    '''
    4. Total amount of bytes exchanged

    Returns
    -------
    op4 : TYPE
        Total amount of bytes exchanged
        (Taking into account both the response header size and the response size in bytes)

    '''
    op4=dfData[4].sum()+dfData[1].sum()
    return op4

def all():
    op1=Operation1()
    op2=Operation2()
    op3=Operation3()
    op4=Operation4()
    return [op1,op2,op3,op4]

#%% Option Menu and taking action
operations = {
'1': ('Most Frequent IP ', Operation1()),
'2': ('Least Frequent IP ', Operation2()),
'3': ('Events per second3 ', Operation3()),
'4': ('Total amount of bytes exchanged ', Operation4()),
'5': ('All operations ', all())
}

# Show Menu (Taking in consideration the possibility of adding more operation to the dicionary, jus need to add the funcion for the operation and the operation to the dictionary)
for o in sorted(operations):
        print(f' {o}) {operations[o][0]}')

operation=input("Select an Operation (index): ")

# Asking for an operation number until we have a valid one
while (int(operation)>len(operations)):
    print("Invalid input")
    operation=input("Select an Operation (index): ")
    
# Call the respective function after a valid index have been introduced
result=operations[operation][1]
print(f' Operation {operation} done !')

#%% Saving the results in plain text JSON format
if(int(operation)==len(operations)):
    operations.pop(operation)
    Results = operations
else:
    Results = {operations[operation][0]:result}

#Transform results to JSON
JString = json.dumps(Results)

# Save JSON file
NameResultFile="Results/Result_operation"+operation+".json"
JFile = open(NameResultFile, "w")
JFile.write(JString)
JFile.close()

print("Results saved in file "+NameResultFile)
print("File path: ", str(Path().absolute())+NameResultFile)