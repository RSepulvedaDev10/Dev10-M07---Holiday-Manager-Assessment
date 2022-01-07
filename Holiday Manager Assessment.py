from bs4 import BeautifulSoup
from dataclasses import dataclass
import datetime as dt
import requests
import json

@dataclass
class Holiday:
    name: str
    date: dt.date

@dataclass
class HolidayList:
    innerHolidays = list
        
    def scrapeHolidays(self):
        for i in range(2020, 2025):
            try:
                url = f"https://www.timeanddate.com/calendar/print.html?year={i}&country=1&cols=3&hol=33554809&df=1"
                response = requests.get(url).text
                soup = BeautifulSoup(response, 'html.parser')
            
                holidays = soup.find('table', attrs={'class': 'cht lpad'})
                for row in holidays.find_all_next('tr'):
                
                    cells = row.find_all_next('td')
                    holiday = {}
                
                    holiday['Name'] = cells[1].string()
                    holiday['Date'] = cells[0].string()
                    self.innerHolidays.append(holiday)
                    
            except:
                print(f"Website cannot be reached")
                
        return self.innerHolidays
    
    def addHoliday(self):
        print(f"Add a Holiday")
        print(f"====================\n")

        name = input("Holiday Name: ")
        
        while(True):
            date = input("Date (Ex: Jan 1 2022): ")
            
            try:
                date = dt.strptime(date, "%b %d, %Y")
                break
            except:
                print("Invalid date format")
                continue
                
        tempHolidayValue = Holiday(name, date)
        
        print(f"{tempHolidayValue} has been successfully added to the list")
    
        self.innerHolidays.append(tempHolidayValue)
    
    
    def removeHoliday(self):
        print(f"Remove a Holiday")
        print(f"====================\n")
        
        while(True):
            
            name = input("Holiday Name: ")
            
            
            holidayCheck = self.numberofHolidays()
            
            self.innerHolidays = [x for x in self.innerHolidays if x.name != name]
            
            if holidayCheck > self.numberofHolidays():
                print(f"{name} has been successfully removed from the holiday list")
                break
            else:
                print(f"{name} was not found on the holiday list")
                continue
    
    def saveHolidayList(self):
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
                
    def readHolidayJSON(self):
        pass
    
    def viewHolidays():
        pass
        
    def numberofHolidays(self):
        return len(self.innerHolidays)
    
    def getWeather():
        pass
    
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
    

def mainMenu():
    
    holidayList = HolidayList()
    holidayList.scrapeHolidays()
    
    while(True):
        
        menuSelection = 0
        
        print(f"Holiday Menu")
        print(f"==================")
        print(f"1. Add a Holiday")
        print(f"2. Remove a Holiday")
        print(f"3. View Holiday List")
        print(f"4. Save Holiday List")
        print(f"5. Exit Holiday Menu")
        
        menuSelection = input("Please input a number corresponding with the option you would like to choose: ")
        
        if menuSelection == "1":
            holidayList.addHoliday()
        elif menuSelection == "2":
            HolidayList.removeHoliday()
        elif menuSelection == "3":
            HolidayList.viewHolidays()
        elif menuSelection == "4":
            HolidayList.saveHolidayList()
        elif menuSelection == "5":
            HolidayList.exit()
        else:
            print(f"This is not a valid entry. Try again")

mainMenu()