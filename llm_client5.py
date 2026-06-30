from dotenv import load_dotenv
from openai import OpenAI, RateLimitError, AuthenticationError, APIError
from pricing import cost_usd

load_dotenv()

class LLMClient:
    def __init__(self, temperature=0, model="gpt-40-mini"):
        self.temperature= temperature
        self.model = model
        self.__client = OpenAI(max_retries=3, timeout=30)
        self.costoTotale = 0
        self.n_chimate = 0
        self.ultimo_uso = (0, 0, 0.0) # in , out cost

    def chat(self, message:str, instructions: str):
        try:
            r = self.__client.responses.create(
                input=message,
                temperature=self.temperature,
                instructions=instructions,
                model= self.model
            )
        except RateLimitError as e:
            return f"RateLimitError: {type(e):__name__}"
        except AuthenticationError :
            return f"AuthenticationError"
        except APIError as e:
            return f"APIError: {type(e):__name__}"
        
        return r.output_text.strip()
        
        u = r.usage
        costoUltimaChiamata += cost_usd(self.model, u.input_tokens, u.output_tokens)
        self.costoTotale += costoUltimaChiamata
        self.n_chiamate += 1
        self.ultimo_uso = (u.input_tokens, u.output_tokens, costoUltimaChiamata)
