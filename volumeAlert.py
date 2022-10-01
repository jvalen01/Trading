import pandas as pd #data manipulation and analysis package
from alpha_vantage.timeseries import TimeSeries #enables data pull from Alpha Vantage
import time
from discordwebhook import Discord
import requests
import collections

#Add stocks you want to scan to watchlist:
watchlist = [] 
watchlist.append("FSLR")
watchlist.append("WOLF")
watchlist.append("SWAV")
watchlist.append("TSLA")
watchlist.append("MNTK")

#Calculate average volume last 15 days/weeks/hours. 
def averageVolumeCalc(vdata):
    count = 0;
    for i in range(7):
        volume = vdata[i]
        count = count + volume
    av = count/7
    return av

#Scanner with alert system:
def volumeScan(watchlist):
    for stock in watchlist: #Loop through every stock in watchlist.

        #Få data fra alpha_vantage:
        ts = TimeSeries(key='RDJBQY68IAAB12LO', output_format='pandas')
        data, meta_data = ts.get_daily(symbol=stock, outputsize='compact')
        vdata = data['5. volume'] #The volume data column.
        last_volume = vdata[0] #Volume last day. 
        averageVolume = averageVolumeCalc(vdata)
        volumeTrigger = 2*averageVolume #High volume trigger.

        #The message we want to send:
        message = "STOCK ALERT!!! The stock " + stock + " is showing high volume " + "%.6f" % averageVolume  
        
        #Check and send discord message:
        if last_volume > volumeTrigger:
            discord = Discord(url="https://discord.com/api/webhooks/1025813472325410917/n3ZVPlIPiOTLaKrCgJXF8a2tRYHIny3eePq6xjO-J1YAySpld_4KnPYXU4ZOIu8W_6Ry")
            discord.post(content=message)

volumeScan(watchlist) #Running the scan with the watchlist:)
