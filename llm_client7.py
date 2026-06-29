from openai import OpenAI, RateLimitError, AuthenticationError, APIError
from dotenv import load_dotenv
from pricing import cost_usd

load_dotenv()

class LLMClient:
    def __init__(self, model="gpt-o4-mini", temperature=1):
        self.model = model
        self.temperature = temperature
        self.__client = OpenAI(max_retries=3, timeout=30)
        self.n_chiamate = 0
        self.costoTotale = 0.0
        self.costoUltimoUso = (0, 0, 0.0)

    def chat(self, text: str, instructions="Sei un esperto epistemologo"):
        try:
            r = self.__client.responses.create(
                temperature=self.temperature,
                model=self.model,
                input=text,
                instructions=instructions
            )
        except RuntimeError as e:
            return f"RuntimeError: {type(e):__name__}"
        except AuthenticationError:
            return "AuthenticationError"
        except APIError as e:
            self.costoUltimoUso = (0, 0, 0.0)
            return f"APIError: {type(e):__name__}"
        
        u = r.usage
        costNow =  cost_usd(self.model, u.input_tokens, u.output_tokens)
        self.n_chiamate +=1
        self.costoTotale += costNow
        self.costoUltimoUso = (u.input_tokens, u.output_tokens, costNow)
        return r.output_text