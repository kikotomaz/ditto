import re


class Prompt:

    location: str

    variables: dict

    above: str
    below: str

    def __init__(self, location):
        self.location = f"{location}.prompt"
        self.variables = dict()
        self.above = ""
        self.below = ""

    def write(self, variable: str, inp):
        if(variable.upper() == "ABOVE"):
            self.above = inp
            return
        if(variable.upper() == "BELOW"):
            self.below = inp
            return

        self.variables[variable.upper()] = inp
        return

    def read(self):
        prompt = list()
        prompt.append({"role" : "system", "content" : self.flatten()})
        return prompt

    def flatten(self):
        prompt_str = open(self.location).read()

        # remove comments
        prompt_str = re.sub(";;.*", "", prompt_str)


        for v in self.variables:
            prompt_str = prompt_str.replace(f"<<{v}>>", f"{self.variables[v]}")

        prompt_str = self.above + prompt_str + self.below
        return prompt_str

