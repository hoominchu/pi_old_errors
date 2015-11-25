import sys
import time
sys.path.append("/Library/Python/2.7/site-packages")
#import nltk
import speech_recognition as sr
import random
#from nltk import sent_tokenize, word_tokenize
#from nltk.stem import PorterStemmer
import serial

#devices = ["COM1","COM2","COM3","COM4","COM5","COM6","COM7","COM8","COM9","COM10"]
"""for port in devices:
    try:
        arduino = serial.Serial(port,9600)
        print (port)
        break
    except:
        pass
"""
arduino = serial.Serial("COM4",9600)
#ps = PorterStemmer()

allCommands = []

devices = ['tv','light','fan','settopbox']

greetWords = ['hey','hi','hello']

keyWords = ['theatermode','mute','unmute','connect','goto','turnon','turnoff','watch','increasevolumebit','decreasevolumebit','increasevolumeby','decreasevolumeby','play','pause','stop','forward','favorite','change','howdy','goodmorning','afternoon','evening','morning','nextchannel','prevchannel','next','back','entertainment', 'mute' , 'music' , 'news' ,'sports' , 'movie' , 'shuffle' , 'answertolife' , 'joke' , 'anotherjoke']

tvKeyWords = ['theatermode','mute','unmute','connect','goto','watch','increasevolumebit','decreasevolumebit','increasevolumeby','decreasevolumeby','play','pause','stop','forward','favorite','change','howdy','goodmorning','afternoon','evening','morning','nextchannel','prevchannel','next','back','entertainment', 'mute' , 'music' , 'news' ,'sports' , 'movie' , 'shuffle' , 'answertolife' , 'joke' , 'anotherjoke']

endWords = ['bye']

negativeWords = ['dont']

guide = {'wimbledon':'starsports1',  'tennis':'starsports1', 'football':'starsports2', 'hindimovie':'sonymax', 'movie':'stargold', 'englishmovie':'starmovies', 'actionmovie':'starmoviesaction', 'news':'indiatv', 'businessnews':'ET Now','internationalnews':'Al Jazeera', 'music':'MTV', 'bollywoodmusic': 'Z ETC Bollywood', 'indiemusic':'MTV indies', 'science':'Discovery Science','cartoon':'hungama'}
channelsDict = {'channelName':'number', 'starsports1':401, 'starsports2':406, 'sonymax':303, 'stargold':302, 'starmovies':342, 'starmoviesaction':355, 'indiatv':460, 'ET Now':525, 'Al Jazeera':533, 'mtv':655, 'Z ETC Bollywood':669, 'MTV indies':667, 'Discovery Science':561, 'hungama':605, 'discovery':100}

#channelsList = ['starsports','espn','smax','stargold','starmovies','moviesnow']

def text2int(textnum, numwords={}):
    if not numwords:
        units = [
        "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
        "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
        "sixteen", "seventeen", "eighteen", "nineteen",
        ]

        tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

        scales = ["hundred", "thousand", "million", "billion", "trillion"]

        numwords["and"] = (1, 0)
        for idx, word in enumerate(units):  numwords[word] = (1, idx)
        for idx, word in enumerate(tens):       numwords[word] = (1, idx * 10)
        for idx, word in enumerate(scales): numwords[word] = (10 ** (idx * 3 or 2), 0)

    ordinal_words = {'first':1, 'second':2, 'third':3, 'fifth':5, 'eighth':8, 'ninth':9, 'twelfth':12}
    ordinal_endings = [('ieth', 'y'), ('th', '')]

    textnum = textnum.replace('-', ' ')

    current = result = 0
    for word in textnum.split():
        if word in ordinal_words:
            scale, increment = (1, ordinal_words[word])
        else:
            for ending, replacement in ordinal_endings:
                if word.endswith(ending):
                    word = "%s%s" % (word[:-len(ending)], replacement)

            if word not in numwords:
                #raise Exception("Illegal word: " + word)
                continue

            scale, increment = numwords[word]

        current = current * scale + increment
        if scale > 100:
            result += current
            current = 0

    return result + current

def negCheck():
    for commandWord in commandWords:
        for negativeWord in negativeWords:
            if commandWord == negativeWord:
                return True
            else:
                return False

def greetcheck(command):
    global userName
    for word in wordsList:
        for greetWord in greetWords:
            if (word == greetWord):
                print((random.choice(greetWords)).capitalize())
                print('Good to see you!')
                print('Here are the things you can do')
                print('You can turn on/off the TV, Increase/Decrease its volume, Play/Pause, ask your TV to put on a particular genre of channels, And do a lot more!')
                print('You can say things like "switch on TV" or "increase volume"')
                return 1
            
    for word in wordsList:
        #print (word)
        for keyWord in keyWords:
            if (word == keyWord):
                print ('Please wait...\n')
                action(word,command)
                
                return 2
    #print (wordsList)    
    print('I can\'t do that right now. But I will learn soon!\n')        

def checkNextWord(keyWord, listName):
    #print (listName)
    index = listName.index(keyWord)
    #indexNext = index + 1
    if len(listName) > index+1:
        return listName[index+1]
    else:
        return len(listName)

def gotoNumber(channelNumber):
    channelNumberString = str(channelNumber)
    for digit in channelNumberString:
        print(digit)
        arduino.write(('DIG_'+digit).encode())
        time.sleep(2.0)

def commandNotClear(errorMessage):
    #response = input(errorMessage)
    response = getVoiceCommand(errorMessage)
    print(response)
    return response

def isDeviceClear():
    global devices, command, tvKeyWords, theDevice
    commandWords = command.split()
    #print(commandWords)
    for i in commandWords:
        for h in tvKeyWords:
            if (i == h):
                #print (i)
                return 'tv'
               
    for word in devices:
        for k in commandWords:
            if (word == k):
                #print('K')
                theDevice = word
                return word
                break

    #whichDevice = input('Please tell me which device (type)\n')
    whichDevice = getVoiceCommand('Please tell me which device\n')

    whichDevice = whichDevice.lower()

    whichDevice = whichDevice.replace('tata sky','settopbox')
    whichDevice = whichDevice.replace('tatasky','settopbox')
    whichDevice = whichDevice.replace('set top box','settopbox')
    
    whichDeviceWords = whichDevice.split()
    for x in whichDeviceWords:
        for y in devices:
            if (x == y):
                print (x)
                return x
    print (whichDevice)

    
def getChannelNumber(channelNameInput):
    global guide, commandWords, channelsDict
    #print (commandWords)
    
    if channelNameInput in list(guide.keys()):
        channelsName= guide.get(channelNameInput, channelNameInput)
        print ('Channel name : ' + channelsName)
        channelNumber = channelsDict.get(channelsName)
        print ("Channel Number: " + str(channelNumber))
        gotoNumber(channelNumber)

    else:
        channelNumber = channelsDict.get(channelNameInput,"Can't find channel")
        print ("Channel Number: " + str(channelNumber))
        gotoNumber(channelNumber)

def doIt():

    global keyWords, greetWords, wordsList, commandWords, command, theDevice, devices
    command = getVoiceCommand('I am listening')
    #command = input('Tell me\n')

    #weKnowCommand = doWeKnowThisCommand(f)

    command = command.lower()

    command = command.replace('tata sky','settopbox')
    command = command.replace('tatasky','settopbox')
    command = command.replace('set top box','settopbox')

    

##    if weKnowCommand == False:
##        f.write(command)
    
##    if (command in allCommands == False):
##        allCommands.append(command)

    command = command.replace(' the ',' ')
    command = command.replace(' a ',' ')
    command = command.replace(' an ',' ')
    command = command.replace(' some ',' ')
    command = command.replace(' any ',' ')
    command = command.replace(' with ',' ')

    #Replacements

    #command = command.replace(' tv ',' ')

    command = command.replace('raise','increasevolumebit')
    command = command.replace('lower','increasevolumebit')
    
    command = command.replace('go to','goto')
    command = command.replace('put on','goto')
    #command = command.replace('let\'s watch','goto')
    #command = command.replace('let us watch','goto')
    command = command.replace('play','goto')
    command = command.replace('show','goto')
    command = command.replace('show any','goto')
    #command = command.replace('i want to watch','goto')
    command = command.replace('catch up','goto')
    command = command.replace('watch','goto')
    
    command = command.replace('switch on','turnon')
    command = command.replace('turn on','turnon')
    command = command.replace('start tv','turnon')

    command = command.replace('switch off','turnoff')
    command = command.replace('turn off','turnoff')

    command = command.replace('volume up','increasevolumebit')
    command = command.replace('volume down','decreasevolumebit')

    command = command.replace('increase volume bit','increasevolumebit')
    command = command.replace('decrease volume bit','increasevolumebit')

    command = command.replace('increase volume little','increasevolumebit')
    command = command.replace('decrease volume little','decreasevolumebit')

    command = command.replace('increase volume by','increasevolumeby')
    command = command.replace('decrease volume by','decreasevolumeby')

    command = command.replace('next channel','nextchannel')
    command = command.replace('previous channel','prevchannel')

    command = command.replace('next program','nextchannel')
    command = command.replace('previous program','prevchannel')

    command = command.replace('channel up','nextchannel')
    command = command.replace('channel down','prevchannel')

##    command = command.replace('next','nextchannel')
##    command = command.replace('back','prevchannel')

    command = command.replace('increase volume','increasevolumebit')
    command = command.replace('decrease volume','decreasevolumebit')

    command = command.replace('hindi movie','hindimovie')
    command = command.replace('action movie','actionmovie')

    command = command.replace('international news','internationalnews')
    command = command.replace('business news','businessnews')
    command = command.replace('bollywood music','bollywoodmusic')
    command = command.replace('indie music','indiemusic')
    

    ## Change/Next
    
##    command = command.replace('mute' , 'mute')
##    command = command.replace('play music' , 'music')
##    command = command.replace('show me news' , 'news')                        Avoid replacing a word with the same word. 
##    command = command.replace('sport' , 'sports' )
##    command = command.replace(' entertainment' , 'entertainment' )
##    command = command.replace('favorite this' , 'favorite' )
##    command = command.replace('shuffle' , 'shuffle')
##    command = command.replace('movie' , 'movie')
     
#wisecracks
    command = command.replace('answer to life', 'answertolife')
    command = command.replace('another joke' , 'anotherjoke')

    ##repeat commands
    command = command.replace('show me something' , 'turnon')
    command = command.replace('volume up','increasevolumebit')
    command = command.replace('decrease volume bit','decreasevolumebit')
    command = command.replace('volume high','increasevolumebit')
    command = command.replace('volume low' , 'decreasevolumebit')
    command = command.replace('change to' , 'goto')
    command = command.replace('shut up' , 'mute')
    command = command.replace('play song' , 'music')
    command = command.replace('change' , 'goto')
    command = command.replace('picture', 'movie')
    #command = command.replace('next', 'nextchannel')
    command = command.replace('up', 'increasevolumebit')
    command = command.replace('down' , 'decreasevolumebit')

    command = command.replace('good morning','goodmorning')
    ## repeat for similar commands
    
    
    #print (wordsList)
    theDevice = isDeviceClear()
    #command = command.replace(theDevice,'')

    for word in devices:
        command = command.replace(' ' + word,'')

    command = command.replace('switch on','turnon')
    command = command.replace('turn on','turnon')
    command = command.replace('start tv','turnon')

    command = command.replace('switch off','turnoff')
    command = command.replace('turn off','turnoff')
    command = command.replace ('let there be', 'turnon')

    command = command.replace('theater mode', 'theatermode')

    commandWords = command.split()

    wordsList = commandWords
    
    wordsList.append('endOfCommand')
    state = greetcheck(command)

def getChannelName():
    global guide,commandWords
    print (guide.keys())
    for word in commandWords:
        if word in list(guide.keys()):
            print (word)
            print('here')
            return word
        else:
            return ('notInDict')

        
def action(keyWord,command):
    global theDevice,commandWords
    #print (command)
    if (theDevice == 'tv'):
        number = text2int (command, numwords={})
        if (keyWord == 'nextchannel'):
                print('OK')
                arduino.write('SKY_CH_UP'.encode())
        if (keyWord == 'prevchannel'):
                print('OK')

        if (keyWord == 'nextnextchannel'):
                print('OK')
                arduino.write('SKY_CH_UP'.encode())
        if (keyWord == 'prevprevchannel'):
                print('OK')
                
                arduino.write('SKY_CH_DOWN'.encode())
        if (keyWord == 'goto'):
            #print(number)
            if (number == 0):
                channelNameInput = checkNextWord(keyWord,command.split())
                getChannelNumber(channelNameInput)
                #print (channelName)
                channelName = channelNameInput
                if (channelName != 'notInDict'):
                    print('Putting on ' + str(channelName))
                    return
                else:
                    response = commandNotClear('Please tell a number or the name of a channel\n')
                    number = text2int (response, numwords={})
                    if (number == 0):
                        print('Go to channel ' + response)
                    else:
                        print('Go to channel ' + str(number))
            #Add action for commands with channel names. Right now this works only for numbers.

        if (keyWord == 'turnon'):
            print('Turning the tv on')
            arduino.write('TV_ON'.encode())

        if (keyWord == 'turnoff'):
            print('Turning the tv off')
            arduino.write('TV_ON'.encode())

        if (keyWord == 'increasevolumebit'):
            print('Increase the volume by 5')
            for x in range(0,5):
                arduino.write('VOL_UP'.encode())
                time.sleep(2.0)

        if (keyWord == 'decreasevolumebit'):
            print('Decrease the volume by 5')
            for i in range(0,5):
                arduino.write('VOL_DOWN'.encode())
                time.sleep(2.0)

        if (keyWord == 'increasevolumeby'):
            if (number == 0):
                response = commandNotClear('Please tell me how much')
                number = text2int (response, numwords={})
            print('Increase the volume by ' + str(number))
            for i in range(0,number):
                arduino.write('VOL_UP'.encode())
                print('+1')
                time.sleep(2.0)
                
        if (keyWord == 'decreasevolumeby'):
            if (number == 0):
                response = commandNotClear('Please tell me how much')
                number = text2int (response, numwords={})
            print('Decrease the volume by ' + str(number))
            for i in range(0,number):
                arduino.write('VOL_DOWN'.encode())
                time.sleep(2.0)

        if (keyWord == 'goodmorning'):
            print('Good morning ' + userName)

        # Add all the other possible greet commands like Good night, afternoon etc.

        if (keyWord == 'mute'):
            print('Mute')
            arduino.write('MUTE'.encode())

        if (keyWord == 'unmute'):
            print('Unmute')
            arduino.write('MUTE'.encode())

        if (keyWord == 'music'):
            print('Playing a Music Channel')

        if (keyWord == 'news'):
            print('Showing you today\'s News')

        if (keyWord == 'sports'):
                print('Sports channel for you')

        if (keyWord == 'movie'):
                print('Grab some popcorn!')

        if (keyWord == 'entertainment'):
                print('I love to entertain you!')
                
        if (keyWord == 'shuffle'):
                print('Shuffle channels for you, Let me know when to stop.')
                
        if (keyWord == 'favorite'):
                print('Got it, added this channel to your favorites!')

        if (keyWord == 'answertolife'):
                print('Mr. Adams suggests that the answer to everything in life is 42')

        if (keyWord == 'joke'):
                print('I met my soulmate. She didn\'t.')

        if (keyWord == 'anotherjoke'):
                print('Comedy Nights with Kapil airs on Saturdays every week at 10:30 pm.')

        if (keyWord == 'theatermode'):
            print('Theatre mode on')
            arduino.write('LIGHT_ON'.encode())
            movieNumber = 342
            gotoNumber(movieNumber)

    if (theDevice == 'light'):
        if (keyWord == 'turnon'):
            print('Turning the light on')
            arduino.write('LIGHT_ON'.encode())

        if (keyWord == 'turnoff'):
            print('Turning the light off')
            arduino.write('LIGHT_ON'.encode())

    if (theDevice == 'fan'):
        if (keyWord == 'turnon'):
            print('Turning fan on')
            arduino.write('FAN_ON'.encode())

        if (keyWord == 'turnoff'):
            print('Turning the light off')
            arduino.write('FAN_ON'.encode())

    if (theDevice == 'settopbox'):
        if (keyWord == 'turnon'):
            print('Turning the set top box on')
            arduino.write('SKY_ON'.encode())

        if (keyWord == 'turnoff'):
            print('Turning the set top box off')
            arduino.write('SKY_ON'.encode())

def doWeKnowThisCommand(f):
    for line in f:
        if (line == command):
            return True
            break
        else:
            continue

             
def getVoiceCommand(whatToPrint):
    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print(whatToPrint)
        audio = r.listen(source)

    # recognize speech using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        #print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
        return r.recognize_google(audio)

    except sr.UnknownValueError:
        #print("Google Speech Recognition could not understand audio")
        getVoiceCommand(whatToPrint)

flag = 0

wordsList=[]

#theDevice = 'dontknow'    

currentChannel = 10

myName = 'pi'

#userName = input('What is your name?\n')
#userName = getVoiceCommand('What is your name?')

userName = 'Minchu'

f = open('commandList.txt','w')
f.write('Commands\n')
f.close()

f = open('commandList.txt','r')

while (flag == 0):
    doIt()
##    activateWord = getVoiceCommand('Hi I am Pi. And my nickname is Adam. Say Pi or Adam to activate me. ')
##    #activateWord = input('Hi, I am Pi. Say pi to activate me\n')
##    activateWord = activateWord.lower()
##    print(activateWord)
##    if (activateWord == 'pi' or activateWord == 'pi ' or activateWord == 'Pi' or activateWord == 'Pi ' or activateWord == 'pie' or activateWord == 'hey pi' or activateWord == 'siri' or activateWord == 'ok google' or activateWord == 'buy' or activateWord == 'hi adam' or activateWord == 'hi eve' or activateWord == 'adam' or activateWord == 'Adam'):
##        doIt()
##        #flag = 1
##    else:
##        continue



f.close()
    
