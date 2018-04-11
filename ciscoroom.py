#!/usr/bin/env python3
from ciscosparkapi import CiscoSparkAPI

apiKey="<CiscoAPIKEY>"
api = CiscoSparkAPI(access_token=apiKey)

# Create a new demo room
demo_room = api.rooms.create('darkmatter')


# Post a message to the new room, and upload a file
api.messages.create(demo_room.id, text="Embrace The Void...")
