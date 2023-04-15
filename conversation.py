import os
import openai
import npc_dio_mod

openai.api_key = os.getenv("OPENAI_API_KEY")

#===================Params===================
world_directory: str = "./_solarpunk"
enviroment_name: str = "herville"
character_name: str = "dedrick"
#============================================

#Create character and populate with content
gerg_char = npc_dio_mod.Character(character_name, enviroment_name, world_directory) 
#dedrick_char = npc_dio_mod.Character("Dedrick", enviroment_name, world_directory) 


#Run conversation loop
print("converstation simulator initializing...")
running = True

def leave():
    print("conversation ended by " + character_name)
    running = False

#Actions
leave_convo = ("Leave", "Leave the conversation immediately", leave)
show_item = ("Show_Item", "Show an item to the player. This gives them the item temporarily.", lambda: print("[Showing item]"))

actions = list()
actions.append(leave_convo)
actions.append(show_item)

gerg_char = npc_dio_mod.Character(character_name, enviroment_name, world_directory, actions = actions) 

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

    print(gerg_char.name + ": " + gerg_char.talk(inp, debug = False))
