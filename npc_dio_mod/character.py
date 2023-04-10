from npc_dio_mod import wrappers
#from npc_dio_mod.character import voice

class Character:
    name: str = "Unnamed NPC"

    dialect_table: str

    personal_desc: str
    physical_desc: str

    #knowledge
    world: str
    enviroment: str
    personal: str

    thoughts: str
    mind: wrappers.AIChat

    conversation: list
    debug_log: str

    def __init__(self, character_name: str, enviroment_name: str, world_directory: str):
        self.name = character_name.capitalize()
        
        self.world = open(f"{world_directory}/world.txt", "r").read()
        self.enviroment = open(f"{world_directory}/enviroments/{enviroment_name}.txt", "r").read()

        character_dir: str = f"{world_directory}/characters/{character_name}"

        self.physical_desc = open(f"{character_dir}/physical.txt", "r").read()
        self.personal_desc = open(f"{character_dir}/personal.txt", "r").read()
        self.dialect_table = open(f"{character_dir}/dialect_table.txt", "r").read()

        self.mind = wrappers.AIChat(model="gpt-3.5-turbo")
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

    def format_prompt(self):  
        system = (  f"{self.format_knowledge()}"
                    f"* Instructions:\n"
                    f"The following describes a conversation between {self.name} and Player\n"
                    f"Based on what {self.name} is currently thinking\n"
                    # f"Write a verbal response for {self.name} that incorporates the most contextually salient of their thoughts"
                    f"Write a verbal response for {self.name} that summarizes and communicates the most important thought and keeps the conversation going:\n"
                    f"'{self.thoughts}'\n"
                    f"Respond as concisely as possible."
                    )         
        messages = [{"role": "system", "content": system}]      
        messages.extend(self.conversation)
        
        return messages

    def flatten_convo(self):
        convo = ''
        for i in self.conversation:

            role = "OTHER"
            if(i['role']=="assistant"):
                role = self.name.upper()

            convo += '%s: %s\n' % (role, i['content'])
        return convo.strip()

    def talk(self, input, debug: bool = False):

        self.conversation.append({"role" : "user", "content" : input})

        intention_prompt = f"{self.format_knowledge()}"
        intention_prompt += open("./npc_dio_mod/prompt_intention.txt").read()
        intention_prompt = intention_prompt.replace("<<CHAT>>", self.flatten_convo())
        intention_prompt = intention_prompt.replace("<<NAME>>", self.name)
        intention_prompt = intention_prompt.replace("<<PREV>>", self.thoughts)
        
        intention = list()
        intention.append({"role" : "system", "content" : intention_prompt})
        self.thoughts = self.mind.evaluate(intention)

        prompt = self.format_prompt()
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
