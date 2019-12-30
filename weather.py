import requests
from bs4 import BeautifulSoup
import pandas as pd

page = requests.get("https://forecast.weather.gov/MapClick.php?lat=42.28210000000007&lon=-83.74846999999994#.XgZ0nBdKiu4")
soup = BeautifulSoup(page.content, "html.parser")
week = soup.find(id="seven-day-forecast-body")
items = week.find_all(class_="tombstone-container")


detailed_forecast = soup.find(id="detailed-forecast-body")
details = detailed_forecast.find_all(class_="col-sm-10 forecast-text")
days = detailed_forecast.find_all(class_="col-sm-2 forecast-label")

period_names = [item.find(class_="period-name").get_text() for item in items]
short_desc = [item.find(class_="short-desc").get_text() for item in items]
temp = [item.find(class_="temp").get_text() for item in items]

detail = [detail.get_text() for detail in details]
day = [day.get_text() for day in days]

weather_data = pd.DataFrame(
    {
    "period" : period_names,
    "short_descriptions" : short_desc,
    "temperature" : temp,
     }
)

detailed_data = pd.DataFrame(
    {
    "period" : day,
    "detailed_descriptions" : detail,
    }
)

print(weather_data)
print(detailed_data)

#weather_data.to_csv("Ann_Arbor_Week.csv")
#detailed_data.to_csv("Ann_Arbor_Detailed.csv")
df3 = pd.merge(weather_data, detailed_data, on="period", how="outer")
df3.to_csv("Ann_Arbor_Weather.csv")
