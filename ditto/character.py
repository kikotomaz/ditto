from ditto import ai
from ditto.character_assets.memory import Memory
# from ditto.character_assets.voice import Voice
import os
import re

class Character:
    name: str = "Unnamed NPC"

    actions: list
    memory = Memory
    mind: ai.AIChat
    thoughts: str
    considerations: str

    conversation: list
    # short_memory: str
    debug_log: str

    def __init__(self, name, memory: Memory, actions: list, etc: list, considerations):
        self.name = name
        self.memory = memory
        self.considerations = considerations
        self.mind = ai.AIChat(model="gpt-3.5-turbo")
        self.thoughts = ""
        self.actions = actions
        self.conversation = list()

        self.debug_log = ""

    @staticmethod
    def create(character_name, enviroment_name, world_directory, actions = list(), etc = ""):

        character_dir: str = f"{world_directory}/characters/{character_name}"

        physical = open(f"{character_dir}/physical.prompt", "r").read()
        personal = open(f"{character_dir}/personal.prompt", "r").read()
 
        enviromental = open(f"{world_directory}/enviroments/{enviroment_name}.prompt", "r").read()
        world = open(f"{world_directory}/world.prompt", "r").read()

        if (os.path.isfile(f"{character_dir}/considerations.prompt")):
            considerations = open(f"{character_dir}/considerations.prompt", "r").read()
        else:
            considerations = open(f"{world_directory}/considerations.prompt", "r").read()

        memory = Memory(character_name, personal, physical, enviromental, world, etc)

        return Character(character_name.capitalize(), memory, actions, etc, considerations)
        

    def format_actions(self):
        action_list = ""
        for a in self.actions:
            action_list += a.to_string() + "\n"

        return action_list

    def flatten_convo(self):
        convo = ''
        for i in self.conversation:

            role = "OTHER"
            if(i['role']=="assistant"):
                role = self.name.upper()

            convo += f"{role}: {i['content']}"
        
        return convo.strip()

    def thoughts_prompt(self):
        prompt = ai.Prompt("ditto/prompts/provoke_thoughts")
        prompt.write("NAME", self.name)
        prompt.write("CHAT", self.flatten_convo())
        t = self.thoughts    
        if(t == ""):
            t = "no previous thoughts."
        prompt.write("THOUGHTS", t)
        prompt.write("ACTIONS", self.format_actions())
        prompt.write("CONSIDERATIONS", self.considerations)
        prompt.write("ABOVE", self.memory.format_knowledge())
        return prompt.read()

    def response_prompt(self):  

        prompt = ai.Prompt("ditto/prompts/provoke_response")
        prompt.write("NAME", self.name)
        prompt.write("CHAT", self.flatten_convo())
        prompt.write("THOUGHTS", self.thoughts)
        prompt.write("ACTIONS", self.format_actions())

        prompt.write("ABOVE", self.memory.self_knowledge())
        prompt = prompt.read()
        prompt.extend(self.conversation)
        
        return prompt

    def get_actions(self, r):
        

        if (not isinstance(r, list)):
            r = r.replace("[","")
            r = r.replace("]","")
            r = r.replace(" ","")
            if (r == "NONE"):
                return list()
            r = r.split(",")

        action_name = r.pop(0)
        action_parameter = r.pop(0)

        action = "NONE"

        for a in self.actions:
            if(a.name.upper() == action_name.upper()):
                action = a

        output = list()
        if not (action == "NONE"):
            output.append(lambda : action.do(action_parameter))

        if(len(r) > 0):
            output.extend(self.get_actions(r))

        return output
        
    # prompt character to choose (from a list of feelings and emotions) how it feels in the given situation
    # def query(self, situation):
    
    # summarize memory into a knowledge
    # def sleep(self):

    def talk(self, input):

        self.conversation.append({"role" : "user", "content" : f"{input} > [NONE, NONE]"})

        #Prompt for forethought
        prompt = self.thoughts_prompt()
        self.thoughts = self.mind.evaluate(prompt)

        #Prompt for reaction
        prompt = self.response_prompt()
        reaction = self.mind.evaluate(prompt)
        print(reaction)
        reaction = reaction.split(">")
        response = reaction[0]
        action = "NONE"
        if(len(reaction) > 1):
            action = reaction[1]
            actions_do = self.get_actions(action)
            for a in actions_do:
                a()

        # response = voice.Voice.revise_response(response, self.dialect_table)

        self.debug_log = (
                f"\n========================== DEBUG ====================================\n"
                f"=== STIMULI ===\n"
                f"{input}\n\n"
                f"=== INTERNAL ===\n"
                f"{self.thoughts}\n\n"
                f"=== RESPONSE ===\n"
                f"{response}\n"
                f"=== ACTIONS ===\n"
                f"{self.format_actions()}\n"
                f"{action}\n"
                # f"{actions_do}\n"
                f"========================== END DEBUG =================================\n"
        )
    
        print(self.debug_log)
        self.conversation.append({"role" : "assistant", "content" : f"{response} > {action}"})

        return response