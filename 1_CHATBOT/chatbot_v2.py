import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI as genai
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("Erro: A chave de API do Google não foi encontrada.")
    print("Verifique seu arquivo .env e a variável GOOGLE_API_KEY.")
    exit()

# Configuração do modelo LLM
llm = genai(model="gemini-2.0-flash", api_key=api_key, temperature=0.5, convert_system_message_to_human=True)
print("Modelo de Chat (LLM) inicializado.")

# Criação da memória da conversação
memory = ConversationBufferMemory(memory_key="history", return_messages=True)
print("Memória da conversação inicializada.")

# Criação do encadeamento de conversação
#    - 'verbose=True': Isso fará com que o LangChain imprima no terminal o que está
#      pensando e o prompt completo que ele está enviando para a IA. É ÓTIMO para aprender!
conversation_chain = ConversationChain(llm=llm, memory=memory, verbose=True)


# --- INICIANDO A CONVERSA ---

print("\n--- Início da Conversa ---")

# 5. Primeira interação com a Chain
#    Usamos o método .invoke() para enviar a entrada do usuário.
#    A Chain cuida do resto: adiciona à memória, formata o prompt, envia para o LLM.
primeira_pergunta = "Qual é meu nome?."
resposta1 = conversation_chain.invoke(input=primeira_pergunta)

print("\n[VOCÊ]:", primeira_pergunta)
print("[IA]:", resposta1['response'])

print("\n--- Próxima Interação ---")

# 6. Segunda interação
#    Note que não precisamos lembrar a IA do nosso nome. A memória cuidará disso!
segunda_pergunta = "Qual o meu nome?"
resposta2 = conversation_chain.invoke(input=segunda_pergunta)

print("\n[VOCÊ]:", segunda_pergunta)
print("[IA]:", resposta2['response'])

print("\n--- Fim da Conversa ---")


