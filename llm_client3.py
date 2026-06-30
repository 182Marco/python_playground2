from openai import OpenAI, APIError, RateLimitError, AuthenticationError
from dotenv import load_dotenv
from pricing import cost_usd

load_dotenv()


class LLMClient():
    def __init__(self, model="chatgpt-4o-mini", temperature=0):
        self.model=model
        self.temperature = temperature
        self._client = OpenAI(max_retries=3, timeout=30)
        self.costoTotale = 0.0
        self.n_chiamate = 0
        self.ultimoUso = (0, 0, 0.0)  # (in, out, cost)

    
    def chat(self, messages, instructions=None):
        try:
            r = self._client.responses.create(
                    model= self.model,
                    input= messages,
                    instructions=instructions,
                    temperature=self.temperature
            )
        
        except RateLimitError as e:
            return f"RuntimeError: {type(e):__name__}"
        except AuthenticationError:
            return f"AuthenticationError"
        except APIError as e:
            self.ultimoUso = (0, 0, 0.0)
            return f"APIError: {type(e):__name__} riprova più tardi"
        
        u = r.usage
        costoUltimaChiamata = cost_usd(self.model, u.input_tokens, u.output_tokens)
        self.costoTotale +=  costoUltimaChiamata
        self.n_chiamate += 1
        self.ultimoUso = (u.input_token, u.output_tokens, costoUltimaChiamata)

        return r.output_text.strip()