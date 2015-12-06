import requests, os, shutil, time, datetime

allChannels = {'starsports1':401, 'sonymax':303, 'stargold':302, 'starmovies':342, 'starmoviesaction':355, 'Al Jazeera':533, 'Z ETC Bollywood':669, 'Discovery Science':561, 'Star Plus HD':105, 'Star Plus': 106, 'DD National':104}

os.system('rm /Users/minchu/pi/JSON/today/*.json')
os.system('mv /Users/minchu/pi/JSON/tomorrow/*json /Users/minchu/pi/JSON/today')


tomorrowDate = datetime.date.today() + datetime.timedelta(days=1)
print(tomorrowDate)
tomorrowDateStr = str(tomorrowDate).replace('-','')
print(tomorrowDateStr)

#shutil.rmtree('/Users/minchu/pi/JSON/*.json')
#os.system('rm /Users/minchu/pi/JSON/*.json')
print ('JSON folder cleaned\n')
for name, number in allChannels.items():
	print('Downloading ' + name)
	os.system('curl -O http://www.tatasky.com/tvguiderv/readfiles.jsp?fileName='+tomorrowDateStr+'/00'+str(number)+'_event.json')
print('Moving files to the directory')
os.system('mv *.json /Users/minchu/pi/JSON/tomorrow')
print('All files moved')
