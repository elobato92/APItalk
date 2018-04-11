#!/usr/bin/env python3
import subprocess
from ciscosparkapi import CiscoSparkAPI
import time
from datetime import datetime
import requests
import json

#read API key
config= configparser.ConfigParser()
#Eric's API key 
apiKey="<Cisco-API-key-Here>"

api = CiscoSparkAPI(access_token=apiKey)
roomName="darkmatter"

def getRoomID(api, roomName):
        rawRooms=api.rooms.list()
        rooms=[room for room in rawRooms if room.title == roomName]
        if len(rooms) == 0:
                print("No roomID found.")
                quit()
        else:
                for room in rooms:
                        roomID=(room.id)
        if len(rooms) > 1:
                print("Found multiple rooms with name {} , using newest room.\n -You may want to delete some of the rooms".format(roomName))
        return roomID

roomID=getRoomID(api, roomName)
lastMessageID=''
lastMessageTime=datetime.now()
while True:
        try:
                messages = api.messages.list(roomID)
        except:
                messages()
        for message in messages:
                if message.text[:3] == "run":
                        messageTime=(message.created.split(".")[0])
                        messageTime=datetime.strptime(messageTime, '%Y-%m-%dT%H:%M:%S')
                        if message.id != lastMessageID and messageTime > lastMessageTime:
                                command=message.text[3:]
                                oledMsg="Command: " + command
                                oledMsg="oled-exp -i -c write \"{}\"".format(oledMsg)
                                sendMsg=(subprocess.Popen(oledMsg, shell=True, stdout=subprocess.PIPE).stdout.read()).strip()
                                commandOutput=subprocess.getoutput(command)
                                api.messages.create(roomID,text="Output: \n" + commandOutput)

                                lastMessageID=message.id
                                lastMessageTime=messageTime
                                break
                if message.text[:3] == "url":
                        messageTime=(message.created.split(".")[0])
                        messageTime=datetime.strptime(messageTime, '%Y-%m-%dT%H:%M:%S')
                        if message.id != lastMessageID and messageTime > lastMessageTime:
                                command=message.text[3:]
                                #virtustotal stuff:
                                vtparams = {'apikey': '<VT-key-here>', 'url':command}
                                response = requests.post('https://www.virustotal.com/vtapi/v2/url/scan', data=vtparams)
                                json_response = response.json()
                                commandOutput=str(json_response)
                                api.messages.create(roomID,text="Output: \n" + commandOutput)
                                lastMessageID=message.id
                                lastMessageTime=messageTime
                                break
                if message.text[:6] == "report":
                        messageTime=(message.created.split(".")[0])
                        messageTime=datetime.strptime(messageTime, '%Y-%m-%dT%H:%M:%S')
                        if message.id != lastMessageID and messageTime > lastMessageTime:
                                command=message.text[6:]
                                #virtustotal stuff:
                                headers = {
                                "Accept-Encoding": "gzip, deflate",
                                "User-Agent" : "gzip,  My Python requests library example client or username"
                                }
                                vtparams = {'apikey': '<VT-key-here>', 'resource':command}
                                response = requests.post('https://www.virustotal.com/vtapi/v2/url/report', params=vtparams, headers=headers)
                                json_response = response.json()
                                commandOutput=json.dumps(json_response, indent=2, sort_keys=True)
                                api.messages.create(roomID,text="Output: \n" + commandOutput)
                                lastMessageID=message.id
                                lastMessageTime=messageTime
                                break                                                                
        #time.sleep(30)
