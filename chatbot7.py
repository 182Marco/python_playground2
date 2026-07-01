from llm_client import LLMClient
from pydantic import BaseModel
import tiktoken

class Msg(BaseModel):
    content: str
    role: str


def getTokenNum(msgs: list[Msg]) -> int:
    enc = tiktoken.get_encoding("o200k_base")
    return sum(len(tiktoken.enc(m['content'])) for m in msgs)


class chatBot:
    def __init__(self, name="Aiko", tono="aggraziato", budjetToken=2000):
        self.client = LLMClient()
        self.instructions (
            f"Ti chiami {name}, "
            f"rispondi sempre in Italiano con tono {tono}, "
            "Se non trovi una risposta lo dici invece di rispondere comunque"
        )
        self.history = []
        self.budjet = budjetToken

    def send (self, text: str):
        self.history.append({"role": "user", "content": text})
        self.__tronca()
        resp = self.client.chat(self.history, instructions=self.instructions)
        self.history.append({"role": "assistant", "content": resp})
        return resp
    
    def __tronca(self):
        while len(self.history ) > 1 and getTokenNum(self.history) > self.budjet:
            self.history.pop(0)
        
    def chat(self):
        print("Per bloccare la chat scrivi 'Quit' o 'Exit'\n")
        while True:
            text = input("Tu>\n ").strip()
            if text.lower() in {'exit', 'quit'}:
                break
            if not text:
                continue
        resp = self.send(text)
        print(f"\nBot> {resp}")
        inputT, outputT, cost = self.client.ultimo_uso
        print(
            f"Hai {inputT} inputToken + {outputT} outputToken, {inputT + outputT} in totale.\n"
            f"L'ultima domanda ti è costata: {cost:.5f}$\n"
            f"In totale fin'ora hai speso: {self.client.costo_totale:.5f}$\n"
        )
        
if __name__ == "__main__ ":
    chatBot.chat()
        

