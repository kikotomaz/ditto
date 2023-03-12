import openai
from enum import Enum

class AIMode(Enum):
    COMPLETE = 0,
    EDIT = 2,
    INSERT = 4,

#Wrapper class for OPENAI API
class AI:

    mode: AIMode = AIMode.COMPLETE #Unused
    model: str = "text-davinci-003"
    temperature: float = 0
    max_tokens: int = 256
    stop: str

    def __init__(self, model, temperature, max_tokens, stop: str = ""):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.stop = stop


    def evaluate(self, pr: str):

        response = openai.Completion.create(
        model=self.model,
        prompt=pr,
        temperature=self.temperature,
        max_tokens=self.max_tokens,
        stop = self.stop,
        )

        return response.choices[0].text.strip()