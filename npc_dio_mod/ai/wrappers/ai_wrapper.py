import openai

#Wrapper class for OPENAI API
class AI:

    model: str

    max_tokens: int = 256
    temperature: float = 0.8
    top_p: float
    stop: str
    presence_penalty: float
    frequency_penalty: float
    best_of: int

    logit_bias = None

    def __init__(self, model):
        self.model = model