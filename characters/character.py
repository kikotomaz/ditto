from characters import ai_wrapper
from characters import voice

class Character:
    name: str = "Unnamed"

    dialect_table: str

    personal_desc: str
    physical_desc: str

    #knowledge
    world: str
    enviroment: str
    personal: str

    mind: ai_wrapper.AI

    def __init__(self, character_name: str, enviroment_name: str, world_directory: str):
        self.name = character_name
        
        self.world = open(f"{world_directory}/world.txt", "r").read()
        self.enviroment = open(f"{world_directory}/enviroments/{enviroment_name}.txt", "r").read()

        character_dir: str = f"{world_directory}/characters/{character_name}"

        self.physical_desc = open(f"{character_dir}/physical.txt", "r").read()
        self.personal_desc = open(f"{character_dir}/personal.txt", "r").read()
        self.dialect_table = open(f"{character_dir}/dialect_table.txt", "r").read()

        self.mind = ai_wrapper.AI("text-davinci-003", 0.6, 256, stop="Player: ")


    def profile(self):
        return f"{self.physical_desc}\n\n{self.personal_desc}"

    def talk(self, context):

        prompt =( f"* Context:\n"
                  f"{self.world}\n"
                  f"{self.enviroment}\n"
                  f"* Instructions:\n"
                  f"You are {self.name}. {self.profile()}\n"
                  f"This is a conversation between {self.name} and Player\n"
                  f"Respond as Gerg would respond. Only respond with what you know, say 'I dont know' if you are unsure.\n"
                  f"{context}\n"
                  f"{self.name}:\n"
                )

        response = self.mind.evaluate(prompt)
        # response = voice.Voice.revise_response(response, self.dialect_table)
        return response
