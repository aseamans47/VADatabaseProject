import pymongo
from pymongo import MongoClient
import os
import time
import pprint

#Checks the operating system being used and clears the console. Pretty much just checks if it is Windows.
def clearConsole():
    os.system('cls' if os.name=='nt' else 'clear')

#I made this function to make a cleaner way to print a dictionary.
def printDictionary(dict):

    for i, j in dict.items():
        print(i,j)

#This function is used in almost all the other functions in order to find a record to either show, delete or update.
def findRecord():
    
    #I found myself printing out the selections so much that I just made a dictionary to print. This made it a
    #little easier and made the code a little neater.
    selections = { 1 : "Category", 2 : "Item", 3 : "Station", 4 : "Value", 'q' : "Exit to main menu"}

    clearConsole()

    printDictionary(selections)
    
    keySelection = input('Select a search category : \n')

    if keySelection == 'q':
        return
        
    try:
        keySelection = selections[int(keySelection)]
    except KeyError:
        print('Invalid Choice, please try again')
        time.sleep(5)
        findRecord()
    except ValueError:
        print('Invalid Choice, please try again')
        time.sleep(5)
        findRecord()

    valueSelection = input(f'Enter {keySelection}:\n')    

    query = {keySelection : valueSelection}
    
    return query

#I found that I would have to reconnect to the database in each function if I didnt pass the
# collection to each function. This function creates an entry in the database.
def create(collection):

    keys = ('Category', 'Item', 'Station', 'Value')
   
    document = dict.fromkeys(keys)

    for key in document:
       document[key] = input('enter {}\n'.format(key))

    if '%' in document['Value']:
        document['ValueType'] = 'Percentage'
    else:
        document['ValueType'] = 'Number'

    try:
        collection.insert_one(document)
        print("Record entered successfully")
    except:
        print("Unable to insert document. Please check your submission and try again")


def retrieve(collection):
    
    queries = findRecord()

    numParamQuery = "Would you like to add more values to your search? (This may find more specific results)\n"\
        "Enter y or n\n"

    for i in range(3):

        userChoice = input(numParamQuery)

        if userChoice == 'n':
            break
        else:
            queries.update(findRecord())

    try:
        for record in collection.find_one(queries):
            pprint.pprint(record)
    except AttributeError:
        print("Record not found. Please try again")

#finds and asks for updates to a record.
def update(collection):

    selections = {1: "Category", 2: "Item", 3: "Station", 4: "Value", 'q': "Exit to main menu"}

    print("Search for a record to update. \n")
    recordToUpdate = findRecord()

    sel = int(input("Select record field to update. \n"))

    printDictionary(selections)

    entry = input("Enter {}. \n".format(selections[sel]))

    dictUpdate = { "$set": {selections[sel]:  entry}}

    try:
        collection.update_one(recordToUpdate, dictUpdate)
        print("Record updated.")
    except:
        "Update unsuccessful. Please try again.\n"


    
#Finds and confirms the deletion of a record.
def delete(collection):

    print("Search for a record to delete. \n")
    recordToDelete = findRecord()

    confirm = input("Confirm record deletion.\n")

    if confirm == 'y':
        print("record deleted")
    elif confirm == 'n':
        delete(collection)
    else:
        delete(collection)
        

#This function asks the user to choose an option for the database.
def userChoice(collection):

    choice = 5

    while choice != 0:
        
        print(' Enter 1 to create a new record.\n Enter 2 to retrieve a record.\n Enter 3 to update a record.\n '
              'Enter 4 to delete a record.\n Enter 0 to quit')
        
        choice = int(input())
        
        if choice == 1:
            create(collection)
        if choice == 2:
            retrieve(collection)
        if choice == 3:
            update(collection)
        if choice == 4:
            delete(collection)
        else:
            continue

#Driver Code.
def main():
    try:
        client = MongoClient()
    except:
        print("Server not available")

    db = client.MHDatabase

    collection = db.mhCollection

    userChoice(collection)

main()