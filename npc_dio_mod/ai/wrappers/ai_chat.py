import openai
from npc_dio_mod.ai.wrappers import ai_wrapper

class AIChat(ai_wrapper.AI):

    def __init__(self, model):
        super().__init__(model)

    def evaluate(self, msgs):

        response = openai.ChatCompletion.create(model=self.model, messages=msgs, max_tokens=512, temperature=1)

        return response.choices[0].message.content