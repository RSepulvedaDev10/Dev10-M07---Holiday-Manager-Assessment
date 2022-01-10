from bs4 import BeautifulSoup
from dataclasses import dataclass
from datetime import date, datetime as dt
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
    innerHolidays: list
        
    def scrapeHolidays(self):
        try:
            for i in range(2020, 2025):
                url = f"https://www.timeanddate.com/holidays/us/{str(i)}?hol=9565233"
                response = requests.get(url).text
                soup = BeautifulSoup(response, 'html.parser')
            
                holidays = soup.find_all("tr", class_="showrow")
                
                for row in holidays:
                    
                    name = row.find("a").text
                    date = dt.strptime(row.find("th").text + " " + str(i), "%b %d %Y")
                    
                    self.innerHolidays.append(Holiday(name, date.date()))
        except:
            print(f"Website cannot be reached.")
            
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
    
    def readHolidayJSON(self, filelocation):
        try:
            with open(filelocation, "r") as jsonfile:
                data = json.load(jsonfile)
                for i in data["holidays"]:
                    dateString = i["date"]
                    formattedDate = dt.strptime(dateString, "%Y-%m-%d")
                    holiday = Holiday(i["name"], formattedDate)
                    self.innerHolidays.append(holiday)
        except:
            print(f"Error in reading JSON")
    
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
                break
                
            elif saveprompt == "n":
                print(f"Canceled:")
                print(f"Holiday list file save canceled")
                break
            else:
                print(f"This is not a valid entry. Please enter 'y' or 'n' in the prompt.")
                continue
                
    
    def viewHolidays(self):
        
        currentWeek = (dt.today().isocalendar()[1]) + 1
        currentYear = (dt.today().isocalendar()[0])
        
        years = [int(currentYear - 2), int(currentYear - 1), int(currentYear), int(currentYear + 1), int(currentYear + 2)]
        weeks = [x for x in range(1,53)]

        
        
        print(f"View Holidays")
        print(f"====================\n")
        
        while(True):
            try:
                yearPrompt = int(input("Which year between 2020 and 2024 would you like to choose: "))
            
                if yearPrompt not in years:
                    raise
                else: 
                    break
            
            except:
                print(f"Invalid input. Please input a year between 2020 and 2024")
                continue
            
        while(True):
            
            try:
                weekPrompt = int(input("Which week? Enter '1-52' or enter '0' for the current week: "))
                
                if int(weekPrompt) not in weeks and weekPrompt != 0:
                    raise
                else:
                    break
                
            except:
                print("Invalid input. Please input a number between 1 and 52 or press 'Enter' while prompt is blank.")
                continue
            
        if weekPrompt == 0:
            weatherPrompt = input("Would you like to see this week's weather (y/n)? ").lower()
            if weatherPrompt == "y":
                print(f"Pulling weather. Here are all the holidays for the week, and weather for the rest of the week:")
                self.viewCurrentWeek()
            elif weatherPrompt == "n":
                print(f"Here are all the holidays for week {currentWeek} in {currentYear}:")
                self.displayHolidaysinWeek(currentYear,currentWeek)
            else:
                print(f"Invalid Entry.")
        else:
            print(type(weekPrompt))
            print(type(yearPrompt))
            print(f"Here are all the holidays for week {weekPrompt} in {yearPrompt}:")
            self.displayHolidaysinWeek(yearPrompt, weekPrompt)
    
    def displayHolidaysinWeek(self, year, week):
        tempList = self.filterHolidaysbyWeek(year, week)
        for holiday in tempList:
            print(holiday)
    
    def viewCurrentWeek(self):
        week = (dt.today().isocalendar()[1]) + 1
        year = (dt.today().isocalendar()[0])
        tempList = self.filterHolidaysbyWeek(year, week)
        weather = self.getWeather()
        for holiday in tempList:
            print(str(holiday) + " - " + weather)
        
          
    def numberofHolidays(self):
        return len(self.innerHolidays)
    
    def filterHolidaysbyWeek(self, year, week):
        results = filter(lambda x: x.date.year == year, filter(lambda x: x.date.isocalendar()[1] == week, self.innerHolidays))
        return results
    
    def getWeather(self):
        weatherDict = {}
        currentDate = dt.today().isocalendar()
        week = []
        for i in range(1,8):
            day = dt.fromisocalendar(currentDate[0], currentDate[1] + 1, i)
            week.append(day)
        
            
        url = "https://community-open-weather-map.p.rapidapi.com/forecast/daily"

        querystring = {"q":"milwaukee, us","lat":"43.0389","lon":"-87.9065","cnt":"7","units":"imperial"}

        headers = {
        'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com",
        'x-rapidapi-key': "09a0e25236msh6ada605176faf8bp1b2d9fjsn3c2e43a1e536"
        }

        response = requests.request("GET", url, headers=headers, params=querystring).json()
        response = response.get("list")
        print(response)
            
        for day in response:
            universalDate = day.get('dt')
            convertedDate = int(universalDate)
            utcDate = dt.utcfromtimestamp(convertedDate)
            utcDate = utcDate.replace(hour=0)
            if utcDate in week:
                weather = ((day.get("weather"))[0]).get("main")
                weatherDict[utcDate] = weather
                    
        return(weather)
    
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
    
    holidayList = HolidayList([])
    holidayList.scrapeHolidays()
    holidayList.readHolidayJSON('holidays.json')
    print(f"There are currently {len(holidayList.innerHolidays)} holidays stored in the system")
    
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