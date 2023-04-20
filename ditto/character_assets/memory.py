
class Memory:

    name: str
    personal: str
    physical: str
    enviromental: str
    world: str
    etc: list()
    
    def __init__(self, name, personal, physical, enviromental, world, etc = ""):
        self.name = name
        self.personal = personal
        self.physical = physical
        self.enviromental = enviromental
        self.world = world
        self.etc = etc

    def self_knowledge(self):
        return f"{self.physical}\n\n{self.personal}"

    def world_knowledge(self):
        return f"{self.world}\n\n{self.enviromental}"

    def format_knowledge(self):
        knowledge = (f" * Knowledge:\n"
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

