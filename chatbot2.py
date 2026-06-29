from llm_client import LLMClient
import tiktoken

_encoder = tiktoken.get_encoding("o200k_base")

def getNumToken(texts):
    return  sum(len(_encoder.encode(t["content"])for t in texts))