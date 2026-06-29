from llm_client import LLMClient
from pydantic import BaseModel
import tiktoken

class Msg(BaseModel):
    content: str

_encoder = tiktoken.get_encoding("o200k_base")

def getTokens(msgs: list[Msg]):
    return sum(len(_encoder.encode(m['content'])for m in msgs))