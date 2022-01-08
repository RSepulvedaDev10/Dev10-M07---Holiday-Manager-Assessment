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
                date = dt.datetime.strptime(date, "%b %d, %Y")
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
    
    def saveHolidayJSON(self, filename):
        print(f"Save Holiday List")
        print(f"====================\n")
    
        while True:
            saveprompt = input("Are you sure you want to save your changes (y/n)? ").lower()
        
            if saveprompt == "y":
                tempJSONList = []
                
                for x in self.innerHolidays:
                    with open(filename + ".json", "w") as jsonFile:
                        tempJSONList.append(x.__dict__)
                        
                tempJSONList = {"holidays": tempJSONList}
                
                json.dump(tempJSONList, jsonFile)
                
            elif saveprompt == "n":
                print(f"Canceled:")
                print(f"\n Holiday list file save canceled")
                break
            else:
                print(f"This is not a valid entry. Please enter 'y' or 'n' in the prompt.")
                
    def readHolidayJSON(self, filelocation):
        try:
            with open(filelocation, "r") as jsonFile:
                load = json.load(jsonFile)
            
                for x in load["innerHolidays"]:
                    self.innerHolidays.append(Holiday(x["name"], (dt.datetime.strptime(x["date"], "%b %d %Y")).date()))
        except:
            print("Error in reading JSON.")
    
    def viewHolidays(self):
        
        currentDate = dt.date.today()
        yearValue = currentDate.year
        
        years = [str(yearValue - 2), str(yearValue - 1), str(yearValue), str(yearValue + 1), str(yearValue + 1)]
        weeks = [x for x in range(1,53)]

        
        
        print(f"View Holidays")
        print(f"====================\n")
        
        while(True):
            try:
                yearPrompt = input("Which year between 2020 and 2024 would you like to choose: ")
            
                if yearPrompt not in years:
                    raise
                else: 
                    break
            
            except:
                print(f"Invalid input. Please input a year between 2020 and 2024")
                continue
            
        while(True):
            
            try:
                weekPrompt = input("Which week? Enter '1-52' or press 'Enter' for the current week")
                
                if int(weekPrompt) not in weeks or weekPrompt != "":
                    raise
                else:
                    break
                
            except:
                print("Invalid input. Please input a number between 1 and 52 or press 'Enter' while prompt is blank.")
                continue
            
        if weekPrompt == "":
            self.getWeather()
        else:
            print(self.viewCurrentWeek(int(yearPrompt), int(weekPrompt)))
    
    def viewCurrentWeek(self, yearPrompt, weekPrompt):
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
            filename = input("Please enter the name for the JSON file: ")
            HolidayList.saveHolidayJSON(filename)
        elif menuSelection == "5":
            HolidayList.exit()
        else:
            print(f"This is not a valid entry. Try again")

mainMenu()