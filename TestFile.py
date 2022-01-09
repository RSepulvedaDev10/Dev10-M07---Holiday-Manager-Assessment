import requests

url = "https://community-open-weather-map.p.rapidapi.com/forecast/daily"

querystring = {"q":"Milwaukee, WI","lat":"43.0389","lon":"-87.9065","cnt":"7","units":"imperial"}

headers = {
    'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com",
    'x-rapidapi-key': "09a0e25236msh6ada605176faf8bp1b2d9fjsn3c2e43a1e536"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)