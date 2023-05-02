from ditto import ai
from ditto.character_assets.memory import Memory
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

    def __init__(self, name, memory: Memory, actions: list, considerations):
        self.name = name
        self.memory = memory
        self.considerations = considerations
        self.mind = ai.AIChat(model="gpt-3.5-turbo")
        self.thoughts = ""
        self.actions = actions
        self.conversation = list()

        self.debug_log = ""


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

            convo += f"{role}: {i['content']}\n"

        return convo.strip()

    def thoughts_prompt(self):

        prompt = ai.Prompt("ditto/prompts/provoke_thoughts")
        prompt.write("ABOVE", self.memory.format_knowledge())
        prompt.write("NAME", self.name)
        prompt.write("CHAT", self.flatten_convo())
        t = self.thoughts
        if(t == ""):
            t = "no previous thoughts."
        prompt.write("THOUGHTS", t)
        prompt.write("ACTIONS", self.format_actions())
        prompt.write("CONSIDERATIONS", self.considerations)

        return prompt

    def response_prompt(self):

        prompt = ai.Prompt("ditto/prompts/provoke_response")
        prompt.write("ABOVE", self.memory.format_knowledge())
        prompt.write("NAME", self.name)
        prompt.write("CHAT", self.flatten_convo())
        prompt.write("THOUGHTS", self.thoughts)
        prompt.write("ACTIONS", self.format_actions())

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

    # summarize conversation into a knowledge
    # def sleep(self):

    def talk(self, input):

        self.conversation.append({"role" : "user", "content" : f"{input} > [NONE, NONE]"})

        #Prompt for forethought
        prompt = self.thoughts_prompt()
        self.thoughts = self.mind.evaluate(prompt)
        #Prompt for reaction
        prompt = self.response_prompt()
        reaction = self.mind.evaluate(prompt)

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

        self.conversation.append({"role" : "assistant", "content" : f"{response} > {action}"})

        return response

    def debug_knowledge(self):
        summary = (
            f"{self.memory.format_knowledge()}\n"
        )
        return summary

def create(character_name, enviroment_name, world_directory, actions = list(), etc = list()):

    world_file = f"{world_directory}/world"
    enviroment_file = f"{world_directory}/enviroments/{enviroment_name}"

    character_dir: str = f"{world_directory}/characters/{character_name}"

    physical_file = f"{character_dir}/physical"
    personal_file = f"{character_dir}/personal"
    etc_file = f"{character_dir}/etc"

    dirs = list()
    k = list()

    dirs.append(world_file)
    k.append(get_knowledge(world_file))

    dirs.append(enviroment_file)
    k.append(get_knowledge(enviroment_file))

    dirs.append(physical_file)
    k.append(get_knowledge(physical_file))

    dirs.append(personal_file)
    k.append(get_knowledge(personal_file))

    if(os.path.isfile(etc_file)):
        dirs.append(etc_file)
        k.append(get_knowledge(etc_file))

    for e in etc:
        dirs.append(f"{world_directory}/etc/{e}")
        k.append(get_knowledge(f"{world_directory}/etc/{e}"))

    #better parser
    for i in range(0, len(k)):

        lines = k[i].split("\n")
        knowledge_i = ""
        for l in lines:
            line = l.strip()
            line = re.sub(";;.*", "", line)

            if(line.startswith("%")):
                import_dir = line.split(" ")[1]
                # this conditional makes no sense to me but it works
                if (import_dir in dirs):
                    k.append(open(f"{world_directory}/{import_dir}", "r").read())
                    dirs.append(f"{world_directory}/{import_dir}")
                continue

            if(line.isspace()):
                continue

            knowledge_i += f"{line}\n"

        k[i] = knowledge_i

    world = k.pop(0)
    enviromental = k.pop(0)
    physical = k.pop(0)
    personal = k.pop(0)
    etc_knowledge = k

    memory = Memory(character_name, personal, physical, enviromental, world, etc_knowledge)


    if (os.path.isfile(f"{character_dir}/considerations")):
        considerations = open(f"{character_dir}/considerations", "r").read()
    else:
        considerations = open(f"{world_directory}/considerations", "r").read()

    return Character(character_name.capitalize(), memory, actions, considerations)

def get_knowledge(file):

    if(os.path.isfile(file)):
        return open(file, "r").read()

    if(os.path.isfile(f"{file}.know")):
        return open(f"{file}.know", "r").read()

    # for windows
    if(os.path.isfile(f"{file}.txt")):
        return open(f"{file}.txt", "r").read()

    return ""
