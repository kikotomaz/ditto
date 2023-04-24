import openai
from ditto.ai.wrappers import ai_wrapper

class AIChat(ai_wrapper.AI):

    def __init__(self, model):
        super().__init__(model)

    def evaluate(self, prompt):

        prompt = prompt.read()

        response = openai.ChatCompletion.create(model=self.model, messages=prompt, max_tokens=512, temperature=.5)

        return response.choices[0].message.content