from openai import OpenAI, RateLimitError, APIError, AuthenticationError
from dotenv import load_dotenv
from pricing import cost_usd

load_dotenv()

class LLMClient():
    def __init__(self, model="chatgpt-4o-mini", temperature=0):
        self.model = model
        self.temperature = temperature
        self.__client = OpenAI(max_retries=3, timeout=30)
        self.costoTotale = 0.0
        self.n_chimate = 0
        self.costo_ultimoUso = (0, 0, 0.0)
    

    def chat(self, messaggio: str, instructions: str):
        try:
            r = self.__client.responses.create(
                input=messaggio,
                model=self.model,
                instructions=instructions
            )

        except RateLimitError as e:
            return f"RateLimitError: {type(e):__name__}"
        except AuthenticationError as e:
            return "AuthenticationError"
        except APIError as e:
            return f"APIError: {type(e):__name__}"
        
    
        u = r.usage
        costo_ultimaChimata = cost_usd(self.model, u.input_tokens, u.output_tokens)
        self.n_chimate += 1
        self.costoTotale += costo_ultimaChimata
        self.costo_ultimoUso = u.input_tokens, u.output_tokens, costo_ultimaChimata

        return r.output_text.strip()