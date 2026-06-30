from openai import OpenAI, RateLimitError, AuthenticationError, APIError
from dotenv import load_dotenv
from pricing import cost_usd

load_dotenv()


class ClientLLM():
    def __init__(self, model="gpt-4o-mini", temperature=0):
        self.model = model
        self.temperature = temperature
        self.__client = OpenAI(max_retries=3, timeout=30)
        self.n_chimate = 0
        self.costoToale = 0.0
        self.costoUltimoUso = 0, 0, 0.0

    def chat(self, text: str, instructions="Sei un esperto di js"):
        try:
            r = self.__client.responses.create(
                temperature=self.temperature,
                model=self.model,
                input=text,
                instructions=instructions
                )
        except RateLimitError as e:
            return f"RateLimitError: {type(e):__name__}"
        except AuthenticationError as e:
            return "AuthenticationError"
        except APIError as e:
            self.costoUltimoUso = (0, 0, 0.0)
            return f"APIError: {type(e):__name__}"
        
        u = r.usage
        costThisCall = cost_usd(self.model, u.input_tokens, u.output_tokens)
        self.n_chimate += 1
        self.costoToale += costThisCall
        self.costoUltimoUso = u.input_tokens, u.output_tokens, costThisCall

        return r.output_text
