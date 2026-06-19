# Ingestão e Busca Semântica com LangChain e PostgreSQL + pgVector

Projeto desenvolvido para ingestão de um arquivo PDF e busca semântica via CLI, utilizando Python, LangChain, PostgreSQL com pgVector e Gemini.

## Objetivo

O sistema permite:

- Ler um arquivo PDF;
- Dividir o conteúdo em chunks;
- Gerar embeddings;
- Armazenar os vetores no PostgreSQL com pgVector;
- Permitir perguntas via terminal;
- Responder somente com base no conteúdo do PDF.

## Tecnologias

- Python
- LangChain
- PostgreSQL
- pgVector
- Docker e Docker Compose
- Gemini API

## Estrutura do projeto

```txt
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── src/
│   ├── ingest.py
│   ├── search.py
│   └── chat.py
├── document.pdf
└── README.md