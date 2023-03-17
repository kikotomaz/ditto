import os
import openai
import numpy
import npc_dio_mod

openai.api_key = os.getenv("OPENAI_API_KEY")

#===================Params===================
world_directory: str = "./_test_world"
enviroment_name: str = "herville"
character_name: str = "gerg"
#============================================

#Create character and populate with content
gerg_char = npc_dio_mod.Character(character_name, enviroment_name, world_directory) #This is all you'd be using in an application

#Run conversation loop
print("converstation simulator initializing...")

convo = list()
running = True
while(running):

    inp = input("Player: ")

    if(inp == "/stop"):
        running = False
        continue
    
    
    convo.append({"role" : "user", "content" : inp})
    response = gerg_char.talk(convo)

    convo.append({"role" : "assistant", "content" : response})
    print(gerg_char.name + ": " + response)
