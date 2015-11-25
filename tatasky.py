import requests, json
import datetime

channelsDict = {}
channelsDictRev = {}
showTimeDict = {}
showTimeDictRev = {}
allChannels = {'starsports1':401, 'starsports2':406, 'sonymax':303, 'stargold':302, 'starmovies':342, 'starmoviesaction':355, 'indiatv':460, 'ET Now':525, 'Al Jazeera':533, 'mtv':655, 'Z ETC Bollywood':669, 'MTV indies':667, 'Discovery Science':561, 'hungama':605}
allChannelsRev = {v: k for k, v in allChannels.items()}
timeList = []

nowTime = datetime.datetime.now()
nowTime = nowTime.replace(hour = 18, minute = 0)
cNum = 107

for key in allChannels.values():

    print(key)
    
    r = requests.get('http://www.tatasky.com/tvguiderv/readfiles.jsp?fileName=20151121/00'+str(key)+'_event.json')
    j = r.json()
    timeObject = datetime.datetime.now()


    num = (len(j["eventList"]))

    cid = j["cid"]
    cid = int(cid)



    for i in range(0,num):

        showTitle = (j["eventList"][i]["et"])
        showTime = (j["eventList"][i]["st"])
        
        channelsDict[showTitle] = cid
        channelsDictRev[cid] = showTitle
        showTimeDict[showTime] = showTitle
        showTimeDictRev[showTitle] = showTime

        timeList.append(showTime)

        #print (curC + ' ' + str(showTime) + '\n')

#print(channelsDict)
#print('\n')
#print(showTimeDict)
#print(showTimeDict)
what = input('What do you want to watch?\n')


for item in showTimeDictRev.keys():
    if what in item:
        print (showTimeDictRev[item])
        print (channelsDict[item])
        print (channelsDictRev[(channelsDict[item])])
        print (allChannelsRev[channelsDict[item]])
print(showTimeDict)

for obj in timeList:
    #print(obj)
    hourShowTime = obj[0:2]
    minuteShowTime = obj[3:5]
    showTimeX = timeObject.replace(hour = int(hourShowTime),minute = int(minuteShowTime), second = 0)
    #print('Show starts at : ' + str(showTimeX))
    #print('Now : ' + str(nowTime))
    if (showTimeX <= nowTime):
        #print('checking')
        continue
    else:
        #print('done')
        #print(obj)
        ind = (timeList.index(obj))
        if (ind>0):
            useInd = ind-1
        else:
            useInd = 0
        #print(showTimeDict[timeList[useInd]])
        break
#print(channelsDict)

##for time, title in showTimeDict.items():
##    if (title == what):
##        print (time)
##        break
    

