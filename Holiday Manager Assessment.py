from bs4 import BeautifulSoup
from dataclasses import dataclass
from datetime import date, datetime as dt
from itertools import groupby
import requests
import json

@dataclass
class Holiday:
    name: str
    date: dt.date
    
    def __str__(self):
        return self.name + " (" + self.date.strftime("%Y-%m-%d") + ")"

@dataclass
class HolidayList:
    innerHolidays = list
        
    def scrapeHolidays(self):
        for i in range(2020, 2025):
            try:
                url = f"https://www.timeanddate.com/holidays/us/{str(i)}?hol=9565233"
                response = requests.get(url).text
                soup = BeautifulSoup(response, "html.parser")
            
                holidays = soup.find_all("tr", class_="showrow")
                
                for row in holidays:
                    
                    name = row.find("a").text
                    date = dt.strptime(row.find("th").text + " " + str(i), "%b %d %Y")
                    
                    self.innerHolidays.append(Holiday(name, date.date()))
                    
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
                date = dt.strptime(date,"%b %d %Y")
                break
            except:
                print("Error: invaild date format")
                continue
            
        tempHolidayValue = Holiday(name, date)
        
        if isinstance(tempHolidayValue, Holiday):
            if tempHolidayValue not in self.innerHolidays:
                print(f"{tempHolidayValue} has been successfully added to the list")
                self.innerHolidays.append(tempHolidayValue)
            else:
                print(f"{tempHolidayValue} is already in")
        else:
            print(f"Not a holiday object")
        
        return self.innerHolidays
    
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
                with open(filename + ".json", "w") as jsonFile:    
                    holidays = {"holidays": []}
                    for holiday in self.innerHolidays:
                        holidays["holidays"].append(holiday.__dict__)
                    jsonFile.write(json.dumps(holidays, indent = 4, default = str))
                    
                print(f"Your changes have been saved to {filename}.json")
                
            elif saveprompt == "n":
                print(f"Canceled:")
                print(f"Holiday list file save canceled")
                break
            else:
                print(f"This is not a valid entry. Please enter 'y' or 'n' in the prompt.")
                
    def readHolidayJSON(self, filelocation):
        try:
            with open(filelocation, "r") as jsonFile:
                load = json.load(jsonFile)
            
                for x in load["innerHolidays"]:
                    self.innerHolidays.append(Holiday(x["name"], (dt.strptime(x["date"], "%b %d %Y")).date()))
        except:
            print("Error in reading JSON.")
    
    def viewHolidays(self):
        
        currentDate = date.today()
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
                weekPrompt = input("Which week? Enter '1-52' or leave blank for the current week: ")
                
                if int(weekPrompt) not in weeks and weekPrompt != "":
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
    
    def getWeather(self):
        currentDate = date.today()
        
        weatherPrompt = input("Would you like to see this week's weather (y/n)? ").lower()
        
        if weatherPrompt == "y":
            
            weatherResponse = self.viewCurrentWeek(currentDate.year, currentDate.isocalendar()[1] + 1)
            weatherResponse = list(filter(lambda x: x.date.day >= currentDate.day , weatherResponse))
            
            for i in weatherResponse:
                print(i)
        
        elif weatherPrompt == "n":
            nonWeatherResponse = self.viewCurrentWeek(currentDate.year, currentDate.isocalendar()[1] + 1)
            
            for i in nonWeatherResponse:
                print(i)
                
        else:
            print(f"Invalid Entry.")
    
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
    holidayList.readHolidayJSON('holidays.json')
    print(holidayList.innerHolidays)
    
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
            holidayList.removeHoliday()
        elif menuSelection == "3":
            holidayList.viewHolidays()
        elif menuSelection == "4":
            filename = input("Please enter the name for the JSON file: ")
            holidayList.saveHolidayJSON(filename)
        elif menuSelection == "5":
            HolidayList.exit()
        else:
            print(f"This is not a valid entry. Try again")

mainMenu()

weatherURL = ""