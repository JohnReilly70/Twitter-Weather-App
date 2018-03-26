import json
import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as md
import datetime
from TwitterAPI import TwitterAPI

glasgow = requests.get("http://api.openweathermap.org/data/2.5/forecast?id=2648579&units=metric&APPID=25041c56770cfc0cdb9edbf6371bc2d4")
glasgow.raise_for_status()
glasgow_json = json.loads(glasgow.text)

df = pd.DataFrame(glasgow_json['list'])
df = df[['main','dt']]
df = df.rename(columns={'main': 'Temp', 'dt': 'UNIX Time'})
df['Temp'] = [df['Temp'][index]['temp'] for index, line in enumerate(df['Temp'])]
df['Time'] = [datetime.datetime.fromtimestamp(value) for value in df['UNIX Time']]


today = datetime.datetime.today().date()
delta1 = datetime.timedelta(days=1)
delta5 = datetime.timedelta(days=5)
delta_1_day = today + delta1
delta_5_day = today + delta5
mask = (df['Time'] >= delta_1_day) & (df['Time'] <= delta_5_day)
df = df.loc[mask]

ax=plt.gca()
xfmt = md.DateFormatter('%d/%m/%y %p')
ax.xaxis.set_major_formatter(xfmt)
plt.plot(df['Time'],df['Temp'], 'k--^')
plt.xticks(rotation=10)
plt.grid(axis='both',color='r')
plt.ylabel("Temp (DegC)")
delta_hour = datetime.timedelta(hours=1)
plt.xlim(min(df['Time']),max(df['Time']))
plt.ylim(min(df['Temp'])-1,max(df['Temp'])+1)
plt.title("Forecast Temperature Glasgow")
plt.savefig('five_day_forecast_glasgow.png',dpi=300)


CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_TOKEN_KEY = '-'
ACCESS_TOKEN_SECRET = ''



api = TwitterAPI(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)
file = open('five_day_forecast_glasgow.png', 'rb')
data = file.read()
r = api.request('statuses/update_with_media', {'status':'4 Day Forecast for Glasgow from {} to {} #Glasgow'.format(df.iloc[0]['Time'],df.iloc[-1]['Time'])}, {'media[]':data})
print(r.status_code)