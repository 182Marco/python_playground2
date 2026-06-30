from openai import OpenAI, APIError, AuthenticationError, RateLimitError
from dotenv import load_dotenv

load_dotenv()

class LLMClient():
    def __init__(self, model="gpt-4.1-mini", temperature=0.7):
        self.model = model
        self.temperature = temperature
        self._client = OpenAI(max_retries=3, timeout=30)
        self.costoTotale = 0.0
        self.n_chimate = 0
        self.ultimo_uso = (0, 0, 0.0)