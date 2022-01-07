from bs4 import BeautifulSoup
import requests
import json

def addHoliday():
    
def removeHoliday():
    
def saveHolidayList():
    print(f"Save Holiday List")
    print(f"====================\n")
    
    while True:
        saveprompt = input("Are you sure you want to save your changes (y/n)? ").lower()
        
        if saveprompt == "y":
            with open('Tournament Tracker Roster.csv') as file:
                for i in range(1, len(participants)+1):
                    try:
                        file.write('{},{}\n').format(i, participants[i])
                    except:
                        continue
                print(f"Tournament has been successfully saved")
                file.close()
                break
        elif saveprompt == "n":
            print(f"Canceled:")
            print(f"\n Holiday list file save canceled")
            break
        else:
            print(f"This is not a valid entry. Please enter 'y' or 'n' in the prompt.")
    
def viewHolidays():
    
def exit():
    print(f"Exit")
    print(f"====================\n")
    print(f"All unsaved changes will be lost")
    
    while True:
        
        exitprompt = str(input("Type 'y' to confirm exit or press any other key to cancel: ")).strip().lower()
        
        if exitprompt == "y":
            print(f"Understood. Have a great day")
            quit()
        else:
            print(f"Returning to menu")
            break