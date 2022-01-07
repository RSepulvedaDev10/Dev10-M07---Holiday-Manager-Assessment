from bs4 import BeautifulSoup
import datetime as dt
import requests
import json

def addHoliday():
    print(f"Add a Holiday")
    print(f"====================\n")
    
    holidayprompt = input("Holiday Name: ")
    dateprompt = input("Date: ")
    
def removeHoliday():
    
def saveHolidayList():
    print(f"Save Holiday List")
    print(f"====================\n")
    
    while True:
        saveprompt = input("Are you sure you want to save your changes (y/n)? ").lower()
        
        if saveprompt == "y":
            pass
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