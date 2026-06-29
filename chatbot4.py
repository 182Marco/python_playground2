from llm_client import LLMClient
from pydantic import BaseModel
import tiktoken

_encoder = tiktoken.get_encoding("o200k_base")

class Msg(BaseModel):
    content: str

def getTokenNum(msgs: list[Msg]):
    return sum(len(_encoder.encode(m['content'])) for m in msgs)