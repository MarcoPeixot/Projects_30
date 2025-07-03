# Importando as bibliotecas necessárias
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

def main():
    """
    Função principal que executa o chatbot.
    """
    # --- CONFIGURAÇÃO INICIAL ---
    load_dotenv()

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("Erro: A chave de API do Groq não foi encontrada.")
        print("Certifique-se de ter um arquivo .env com GROQ_API_KEY=SUA_CHAVE")
        return # Encerra a função se a chave não for encontrada

    print("--- Chatbot com Memória (LangChain + Groq) ---")
    print("Inicializando...")

    # --- INICIALIZAÇÃO DO MODELO E DA MEMÓRIA ---
    try:
        llm = ChatGroq(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            temperature=0.7,
            groq_api_key=api_key # Passando a chave diretamente
        )
        
        memory = ConversationBufferMemory(memory_key="history", return_messages=True)

        # Usamos verbose=False agora para uma conversa mais limpa.
        # Mude para True se quiser ver os "pensamentos" do LangChain.
        conversation_chain = ConversationChain(llm=llm, memory=memory, verbose=True)
        
        print("Chatbot pronto! Digite 'sair' a qualquer momento para terminar.")
        print("-" * 50)

    except Exception as e:
        print(f"Erro durante a inicialização: {e}")
        return

    # --- LOOP DE CONVERSA INTERATIVO ---
    while True:
        try:
            # 1. Pede a entrada do usuário
            user_input = input("[VOCÊ]: ")

            # 2. Verifica se o usuário quer sair
            if user_input.lower() == 'sair':
                print("\n[IA]: Até logo! Foi um prazer conversar com você.")
                break # Quebra o loop while

            # 3. Envia a entrada para a chain e obtém a resposta
            response = conversation_chain.invoke(input=user_input)
            
            # 4. Imprime a resposta da IA
            print(f"[IA]: {response['response']}")

        except (KeyboardInterrupt, EOFError):
            # Permite sair com Ctrl+C ou Ctrl+D de forma elegante
            print("\n[IA]: Conversa encerrada. Até a próxima!")
            break
        except Exception as e:
            print(f"\nOcorreu um erro: {e}")
            print("Vamos tentar novamente.")


# --- PONTO DE ENTRADA DO SCRIPT ---
# Garante que a função main() só seja executada quando o script for rodado diretamente
if __name__ == "__main__":
    main()