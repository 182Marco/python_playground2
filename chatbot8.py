from llm_client import LLMClient
from typing import TypedDict, Literal
import tiktoken

class Message(TypedDict):
    role: Literal["user", "assistant"]
    content: str

def getNumTokens(messages: list[Message]):
    encoder = tiktoken.get_encoding("o200k_base")
    return sum(len(encoder.encode(m['content'])) for m in messages)


class ChatBox():
    def __init__(self, name="Aiko", tono="perentorio", budjet_token=2000):
        self.__client = LLMClient()
        self.name = name
        self.instuzioni = (
            f"Sei {name}, un grande chef vegano. \n"
            f"In ogni ricetta di risposta scrivi in modo {tono} che se vogliono cambiare ingredienti non devono comunque sfruttare animali"
        )
        self.budjet = budjet_token
        self.history = []
        
    def send(self, text:str):
        self.history.append({"role": "user", "content": text})
        self.__tronca()
        resp = self.__client.chat(text, instructions=self.instuzioni)
        self.history.append({"role": "assistant", "content": resp})
        return resp
    
    def __tronca(self):
        while len(self.history) > 1 and getNumTokens(self.history) > self.budjet:
            self.history.pop(0)
    
    def chat(self):
        print('Per chiudere la chat scrivi "Quit" o "Exit"')
        while True:
            text = input("Tu> ").strip()
            if text.lower() in {"quit", "exit"}:
                break
            if not text:
                continue
            resp = self.send(text)
            inp, out, tot = self.__client.ultimo_uso
            print(f"\nBot> {resp}")
            print(f"Con questa domanda hai usato: {inp} token in input, {out} in output, {inp + out} token totali\n" 
                  f"Con questa domanda hai speso ${tot:.5f}.\n"
                  f"In totale hai speso ${self.__client.costo_totale:.5f}.\n"
            )

if __name__ == "__main__":
    ChatBox().chat()

