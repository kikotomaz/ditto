import os
import openai
# import numpy
import npc_dio_mod

openai.api_key = os.getenv("OPENAI_API_KEY")

#===================Params===================
world_directory: str = "./_solarpunk"
enviroment_name: str = "herville"
character_name: str = "gerg"
#============================================

#Create character and populate with content
gerg_char = npc_dio_mod.Character(character_name, enviroment_name, world_directory) 
#This ^^ is all you'd be using in an application

#Run conversation loop
print("converstation simulator initializing...")
running = True

while(running):

    inp = ""
    while(inp == ""):
        inp = input("Player: ")

    #Check for debug commands
    if(inp[0] == "/"):
        match(inp):

            case "/stop":
                running = False
                continue
    
            case "/log":
                print(gerg_char.debug_log)
                continue
            case _:
                print(f"command {inp} not found")
                continue

    print(gerg_char.name + ": " + gerg_char.talk(inp, debug = True))
