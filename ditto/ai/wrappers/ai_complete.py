import openai
from ditto.ai.wrappers import ai_wrapper

class AIComplete(AI):

    def __init__( self, model ):
        super().__init__(model)

    def evaluate(self, pr):

        response = openai.Completion.create(
        model=self.model,
        prompt=pr,
        max_tokens=512
        )

        return response.choices[0].text.strip()