from npc_dio_mod import ai
from npc_dio_mod.action import Action
import os
import re

class Character:
    name: str = "Unnamed NPC"

    # dialect_table: str

    personal_desc: str
    physical_desc: str

    #knowledge
    world: str
    enviroment: str
    personal: str
    considerations: str

    actions: list()

    thoughts: str
    mind: ai.AIChat

    conversation: list
    # memory: str
    debug_log: str

    def __init__(self, character_name: str, enviroment_name: str, world_directory: str, actions = ""):
        self.name = character_name.capitalize()
        
        self.world = open(f"{world_directory}/world.prompt", "r").read()
        self.enviroment = open(f"{world_directory}/enviroments/{enviroment_name}.prompt", "r").read()

        character_dir: str = f"{world_directory}/characters/{character_name}"

        self.physical_desc = open(f"{character_dir}/physical.prompt", "r").read()
        self.personal_desc = open(f"{character_dir}/personal.prompt", "r").read()
        # self.dialect_table = open(f"{character_dir}/dialect_table.txt", "r").read()
        if (os.path.isfile(f"{character_dir}/considerations.prompt")):
            self.considerations = open(f"{character_dir}/considerations.prompt", "r").read()
        else:
            self.considerations = open(f"{world_directory}/considerations.prompt", "r").read()

        if (actions == ""):
            self.actions = list()
        else:
            self.actions = actions

        self.mind = ai.AIChat(model="gpt-3.5-turbo")
        self.thoughts = ""
        self.conversation = list()

        self.debug_log = ""

#Knowledge Compilation
    def self_knowledge(self):
        return f"{self.physical_desc}\n\n{self.personal_desc}"

    def world_knowledge(self):
        return f"{self.world}\n\n{self.enviroment}"

    def format_knowledge(self):
        knowledge = (f"* Knowledge:\n"
                    f"{self.world_knowledge()}\n"
                    f"You are {self.name}.\n"
                    f"{self.self_knowledge()}\n"
                    )
        return knowledge

    def format_actions(self):
        action_list = ""
        for a in self.actions:
            action_list += a.to_string() + "\n"

        return action_list


    # summarize memory into a knowledge
    # def sleep(self):
    
#Prompting
    
    def flatten_convo(self):
        convo = ''
        for i in self.conversation:

            role = "OTHER"
            if(i['role']=="assistant"):
                role = self.name.upper()

            convo += f"{role}: {i['content']}"
        
        return convo.strip()

    def thoughts_prompt(self):

        prompt = ai.Prompt("npc_dio_mod/provoke_thoughts")
        prompt.write("ABOVE", self.format_knowledge())
        prompt.write("CHAT", self.flatten_convo())
        prompt.write("NAME", self.name)
        t = self.thoughts
        if(t == ""):
            t = "no previous thoughts."
        prompt.write("PREV", t)
        prompt.write("ACTIONS", self.format_actions())
        prompt.write("CONSIDERATIONS", self.considerations)

        return prompt.read()

    def response_prompt(self):  

        prompt = ai.Prompt("npc_dio_mod/provoke_response_action")
        prompt.write("NAME", self.name)
        prompt.write("ACTIONS", self.format_actions())
        prompt.write("THOUGHTS", self.thoughts)
        prompt.write("CHAT", self.flatten_convo())

        prompt = prompt.read()
        
        # prompt.extend(self.conversation)
        
        return prompt

    def action_prompt(self, response):

        prompt = ai.Prompt("npc_dio_mod/evaluate_actions")
        # prompt.write("ABOVE", self.self_knowledge())

        prompt.write("ACTIONS", self.format_actions())
        prompt.write("CHAT", self.flatten_convo())
        prompt.write("NAME", self.name)
        prompt.write("THOUGHTS", self.thoughts)
        prompt.write("RESPONSE", response)

        return prompt.read()

    def actions_to_functions(self, response):
        response = response.split()

        taken_actions = filter(lambda a: (a.name in response), self.actions)
        output = list()
        for a in taken_actions:
            output.append(a.do)

        return output
    # prompt character to choose (from a list of feelings and emotions) how it feels in the given situation
    # def query(self, situation):

#Actions
    def talk(self, input, debug: bool = False):

        self.conversation.append({"role" : "user", "content" : f"{input} > [NONE, NONE]"})

        #Prompt for forethought
        prompt = self.thoughts_prompt()
        self.thoughts = self.mind.evaluate(prompt)

        #Prompt for reaction
        prompt = self.response_prompt()
        reaction = self.mind.evaluate(prompt)
        print(reaction)
        self.conversation.append({"role" : "assistant", "content" : reaction})
        reaction = reaction.split(">")
        response = reaction[0]

        action = "NONE"
        if(len(reaction) > 1):
            action = reaction[1]
            # actions_do = re.sub("\[.*","", actions)
            # actions_do = self.actions_to_functions(actions_do)
            # for a in actions_do:
                # a("PARAM")

        # response = voice.Voice.revise_response(response, self.dialect_table)
        # self.conversation.append({"role" : "assistant", "content" : response})
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
        if(debug):
            print(self.debug_log)
    

        return response
    
    # def leave(self)