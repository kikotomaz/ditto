

class Action:

    name: str
    desc: str
    
    options: list()

    def __init__(self, name, desc, func, options = ""):
        self.name = name
        self.desc = desc
        self.func = func

        if(options == ""):
            self.options = list()
        else:
            self.options = options
        

    def do(self, parameter):
        self.func(parameter)
    
    def to_string(self):
       
        r = f"{self.name} : {self.desc}\n"

        for o in self.options:
            r += f" - {o[0]} : {o[1]}\n"
        
        return r