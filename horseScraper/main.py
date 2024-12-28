#scapes data

from bs4 import BeautifulSoup
import requests
import pandas as pd

#dictinary of table fields
def getDict():
    dict = {
        'ID':['X'],
        'Name':['x'],
        'Sire':['X'],	
        'Grandsire':['x'],	
        'Dam':['X'],	
        'Damsire':['x'],	
        'Sex':['x'],	
        'Foaled':['x'],	
        'Died':['X'],	
        'Country':['x'],	
        'Colour':['x'],	
        'Breeder':['x'],
        'Owner':['x'],	
        'Trainer':['x'],	
        'Record':['x'],	
        'Earnings':['x'], 
        'Label':['x'],
        'Racing colours':['x'],
        'Jockey':['x'],	
        'Color':['x']}
    return(dict)


def getHorse(search):
    #removes spaces in search
    search = search.replace(" ","_")
    #scape url----------
    pages_to_scrape = requests.get(f"https://en.wikipedia.org/wiki/{search}")
    #sets up parse
    soup = BeautifulSoup(pages_to_scrape.text,"html.parser")
    #pulls labels
    labelCollection = soup.find_all("th",attrs={"class":"infobox-label"})
    #pulls data
    dataCollection = soup.find_all("td",attrs={"class":"infobox-data"})
    #converts dictionary to dataframe
    newEntry = pd.DataFrame(getDict())
    #assins new record id value of 1 and sets horse name
    
    #removes _(horse) prefix for final data presentation
    if (search.find("_(horse)") != -1):
        search = search[0:len(search) -8]
    
    assignedId = {'ID':1,'Name':search}
    #adds assigned value
    newEntry = newEntry._append(assignedId, ignore_index = True)
    #loops labels and data
    for data,label in zip(dataCollection,labelCollection):
        #locates pulled column and updates it
        newEntry.loc[newEntry['ID'] == 1, label.get_text()] = data.get_text()
    return(newEntry.query("ID == 1"))

#sets pull error counter
horsesNotFound = 0
#creates database (dataframe) to hold all horse data
horseDatabase = pd.DataFrame(getDict())

#pulls in csv list of horses
horseList = pd.read_csv('Import/horseList.csv')

#loops horses
for currentHorse in horseList['Horse Name']:
    print(f"Checking {currentHorse}")
    #create new dataframe to hold horse data
    currentRecord = getHorse(currentHorse)
    #checks if return horse data is null
    if(str(currentRecord.query("ID == 1").Sire).find('NaN') != -1):
        #if so searches with prefix _(horse)
        currentRecord = getHorse(f"{currentHorse}_(horse)")
        #checks if that fixed the issue
        if(str(currentRecord.query("ID == 1").Sire).find('NaN') != -1):
            #if still no data 1 is added to error count
            horsesNotFound = horsesNotFound + 1
        else:
            #data was found and is appeneded to dataframe
            horseDatabase = horseDatabase._append(currentRecord, ignore_index = True)
    #data was found and is appeneded to dataframe
    else:
        horseDatabase = horseDatabase._append(currentRecord, ignore_index = True)

#prints horses that could not be pulled
print(f"------Horses Not Found: {horsesNotFound}------")

#---data formatting here----

#removes first formatted row (only x)
horseDatabase = horseDatabase.drop(0)

#Removes ID Column
horseDatabase.drop('ID', axis=1, inplace=True)

#displays final table
#print(horseDatabase)


#exorts to CSV
horseDatabase.to_csv('Export/data.csv', index=False) 