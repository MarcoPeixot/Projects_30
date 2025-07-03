import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

try:
    api_key = os.getenv("GOOGLE_API_KEY")
    genai.configure(api_key=api_key)
    print("Google Generative AI API configured successfully.")
except Exception as e:
    print(f"Error configuring Google Generative AI API: {e}")
    exit()

model = genai.GenerativeModel("gemini-2.0-flash")
print("Model loaded successfully.")

print("\nEnviando sua pergunta para o Gemini...")
prompt = "Qual a diferença fundamental entre Inteligência Artificial e Inteligência Artificial Generativa? Responda em português de forma simples."
response = model.generate_content(prompt)

print("\n--- Resposta do Gemini ---")
try:
    print(response.text)
except Exception as e:
    print(f"Não foi possível extrair o texto da resposta: {e}")
    print("\nResposta completa (para depuração):")
    print(response) # Imprime o objeto de resposta inteiro se .text falhar

print("--------------------------\n")