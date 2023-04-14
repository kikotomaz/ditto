from npc_dio_mod import ai
import os

class Character:
    name: str = "Unnamed NPC"

    dialect_table: str

    personal_desc: str
    physical_desc: str

    #knowledge
    world: str
    enviroment: str
    personal: str
    considerations: str

    thoughts: str
    mind: ai.AIChat

    conversation: list
    debug_log: str

    def __init__(self, character_name: str, enviroment_name: str, world_directory: str):
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

        self.mind = ai.AIChat(model="gpt-3.5-turbo")
        self.thoughts = ""
        self.conversation = list()

        self.debug_log = ""

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

    def response_prompt(self):  

        prompt = ai.Prompt("npc_dio_mod/provoke_response")
        prompt.write("ABOVE", self.format_knowledge())
        prompt.write("NAME", self.name)
        prompt.write("THOUGHTS", self.thoughts)
        prompt = prompt.read()
        
        prompt.extend(self.conversation)
        
        return prompt

    def thoughts_prompt(self):

        prompt = ai.Prompt("npc_dio_mod/provoke_thoughts")
        prompt.write("ABOVE", self.format_knowledge())
        prompt.write("CHAT", self.flatten_convo())
        prompt.write("NAME", self.name)
        prompt.write("PREV", self.thoughts)
        prompt.write("CONSIDERATIONS", self.considerations)

        return prompt.read()

    def flatten_convo(self):
        convo = ''
        for i in self.conversation:

            role = "OTHER"
            if(i['role']=="assistant"):
                role = self.name.upper()

            convo += f"{role}: {i['content']}"
        
        return convo.strip()

    def talk(self, input, debug: bool = False):

        self.conversation.append({"role" : "user", "content" : input})

        prompt = self.thoughts_prompt()
        self.thoughts = self.mind.evaluate(prompt)

        prompt = self.response_prompt()
        response = self.mind.evaluate(prompt)

        self.conversation.append({"role" : "assistant", "content" : response})
        # response = voice.Voice.revise_response(response, self.dialect_table)

        self.debug_log = (
                f"\n========================== DEBUG ====================================\n"
                f"=== INTERNAL ===\n"
                f"{self.thoughts}\n\n"
                f"=== RESPONSE ===\n"
                f"{response}\n"
                f"========================== END DEBUG =================================\n"
        )
        if(debug):
            print(self.debug_log)
        return response

    # prompt character to choose (from a list of feelings and emotions) how it feels in the given situation
    # def query(self, situation):