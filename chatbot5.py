from llm_client import LLMClient
from pydantic import BaseModel
import tiktoken

_encoder = tiktoken.get_encoding("o200k_base")

class Text(BaseModel):
    content: str

def getTokens(messages: list[Text]):
    return sum(len(_encoder.encode(m['content']) for m in messages))


class chatBot():
    def __init__(self, nome="aiko", tono="codiale", budjet_token=2000):
        self.client= LLMClient()
        self.istruzioni= (
            f"Sei {nome} rispondi sempre con tono {tono} "
            "usa sempre l'italiano "
            "se non sai la risposta non inventare"
        )
        self.budjet = budjet_token
        self.storia = []
        