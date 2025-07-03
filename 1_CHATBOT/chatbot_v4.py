import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

def load_api_key():
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("A chave de API do Groq não foi encontrada. Certifique-se de ter um arquivo .env com GROQ_API_KEY=SUA_CHAVE")
    return api_key

def create_conversation(api_key):
    llm = ChatGroq(model="meta-llama/llama-4-scout-17b-16e-instruct", temperature=0.7, groq_api_key=api_key)
    memory = ConversationBufferMemory(memory_key="history", return_messages=True)
    return ConversationChain(llm=llm, memory=memory)

def main():
    print("--- Chatbot com Memória (LangChain + Groq) ---")
    print("Inicializando...")
    try:
        api_key = load_api_key()
        conversation = create_conversation(api_key)
        print("Chatbot pronto! Digite 'sair' a qualquer momento para terminar.")
        print("-" * 50)
        while True:
            user_input = input("[VOCÊ]: ")
            if user_input.lower() == 'sair':
                print("\n[IA]: Até logo! Foi um prazer conversar com você.")
                break
            response = conversation.invoke(input=user_input)
            print(f"[IA]: {response['response']}")
    except KeyboardInterrupt:
        print("\n[IA]: Encerrando o chatbot. Até logo!")
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    main()
