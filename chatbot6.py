from llm_client import LLMClient
from pydantic import BaseModel
import tiktoken

_encoder = tiktoken.get_encoding("o200k_base")

class Msg(BaseModel):
    content: str

def getTokenNum(msgs: list[Msg]):
    return sum(len(_encoder.encode(m['content'])) for m in msgs)

class ChatBox:
    def __init__(self, name="Aiko", tono="garbato", budjetToken=2000):
        self.client = LLMClient()
        self.instructions = (
            f"Ti chiami {name}.\n"
            f"Rispondi sempre con tono {tono}"
            "Quando non lo sai lo ametti e non rispondi sbagliato"
        )
        self.budjet = budjetToken
        self.history = []

    def send(self, text: str):
        self.history.append({"role": "user", "content": text})
        resp = self.client.chat(self.history, instructions=instructions)
        self.history.append({"role": "assistant", "content": resp})
        return resp
    
    def chat(self):
        print("Premi 'exit' o 'quit' per terminare la chat.\n")
        text = input("Tu> ").strip()
        while True:
            if text.lower() in {'exit', 'quit'}:
                break
            if not text:
                continue
        risp = self.send(text)
        inp, out, costo = self.client.ultimo_uso
        print(f"\nBot> {risp}")
        print(f"[{inp} + {out} token - costoUltimaDomanda: ${costo:.5f}]\ncosto totale: ${self.client.costo_totale:.5f}\n")
      