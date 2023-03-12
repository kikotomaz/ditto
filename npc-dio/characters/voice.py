from characters import ai_wrapper

class Voice:
    @staticmethod
    def revise_response(response: str, dialect_table: str):
        dialect_table += f"\n{response}: "
        ai = ai_wrapper.AI("text-davinci-003", 0.9, 256, stop="\n")

        return ai.evaluate(dialect_table)