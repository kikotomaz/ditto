import os
import openai
from characters import character
from characters import voice

openai.api_key = os.getenv("OPENAI_API_KEY")

#===================Params===================
world_directory: str = "./_test_world"
enviroment_name: str = "herville"
character_name: str = "gerg"
#============================================

#Create character and populate with content
gerg_char = character.Character(character_name, enviroment_name, world_directory) #This is all you'd be using in an application

#Run conversation loop
print("converstation simulator initializing...")

context = ""
running = True
while(running):

    inp = input("Player: ")

    if(inp == "/stop"):
        running = False
    
    context += "\nPlayer: " + inp
    response = gerg_char.name + ": " + gerg_char.talk(context)
    context += "\n" + response
    print(response)
