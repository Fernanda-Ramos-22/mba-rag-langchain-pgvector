import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from search import search_context


PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""


def main():
    load_dotenv()

    google_api_key = os.getenv("GOOGLE_API_KEY")

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",
        google_api_key=google_api_key,
        temperature=0,
    )

    print("Chat iniciado. Digite 'sair' para encerrar.\n")

    while True:
        pergunta = input("PERGUNTA: ")

        if pergunta.lower().strip() in ["sair", "exit", "quit"]:
            print("Encerrando chat.")
            break

        contexto = search_context(pergunta)

        prompt = PROMPT_TEMPLATE.format(
            contexto=contexto,
            pergunta=pergunta
        )

        resposta = llm.invoke(prompt)

        print(f"RESPOSTA: {resposta.content}\n")


if __name__ == "__main__":
    main()