import re

class Memory:

    name: str
    personal: str
    physical: str
    enviromental: str
    world: str
    etc: str

    def __init__(self, name, personal, physical, enviromental, world, etc = list()):
        self.name = name
        self.personal = personal
        self.physical = physical
        self.enviromental = enviromental
        self.world = world
        etc_knowledge = ""
        for e in etc:
            etc_knowledge += f"{e}\n\n"
        self.etc = etc_knowledge

    def general_knowledge(self):
        knowledge = (
            f"-- General Knowledge\n"
            f"- Global Knowledge:\n"
            f"{self.world}\n"
            f"- Current Enviroment: "
            f"{self.enviromental}\n"
            f"- Miscellaneous\n"
            f"{self.etc}\n"
        )
        return knowledge


    def self_knowledge(self):
        knowledge = (
            f"-- Knowledge about SELF: "
            f"You are {self.name}\n"
            f"- Personality\n"
            f"{self.personal}\n"
            f"- Appearance\n"
            f"{self.physical}\n"
 
        )
        return knowledge

    def format_knowledge(self):
        knowledge = (
            f" * Knowledge\n"
            f"{self.general_knowledge()}"
            f"\n"
            f"{self.self_knowledge()}"
       )

        return knowledge