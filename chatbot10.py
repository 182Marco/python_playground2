from llm_client import LLMClient
from typing import TypedDict, Literal
import tiktoken 

class Msg(TypedDict):
    role: Literal['user', 'assistant']
    content: str


def getNumToken(msgs):
    encoder = tiktoken.get_encoding('o200k_base')
    return sum(len(encoder.encode(m['content'])) for m in msgs)

class Chatbot():
    def __init__(self, name="Aiko", tone="simpatico", tokenBudjet=2000):
        self.__client = LLMClient()
        self.istruzioni = (
            f"Ti chiami {name}.\n"
            f"Rispondi sempre in Italiano con tono {tone}.\n"
            "Quando non sai qualcosa lo dici e non inventi"
        )
        self.budjet= tokenBudjet
        self.history: list[Msg]=[]

    def send(self, text: str):
        self.history.append({"role": "user", "content": text})
        self.__tronca()
        r = self.__client.chat(self.history, self.istruzioni)
        self.history.append({"role": "assistant", "content": r})
        return r
    
    def __tronca(self):
        while len(self.history) > 1 and getNumToken(self.history) > self.budjet:
            self.history.pop(0)
    
    def chat(self):
        print("Per chiudere la chat scrivi 'Exit' o 'Quit'\n")
        while True:
            text = input("Tu> ").strip()
            if text.lower() in {'quit', 'exit'}:
                break
            if not text:
                continue
            resp = self.send(text)
            print(f"\n Bot> {resp}")
            inp , out, cost = self.__client.ultimo_uso
            print(
                f"In questa domanda hai usato {inp} token in input e {out} in output, spendendo ${cost:.5f}.\n"
                f"In totale hai speso ${self.__client.costo_totale:.5f}"
            )

if __name__ == "__main__":
    Chatbot().chat()

        
