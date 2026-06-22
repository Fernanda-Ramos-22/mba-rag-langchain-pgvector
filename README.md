# Ingestão e Busca Semântica com LangChain e PostgreSQL + pgVector

Projeto desenvolvido para a disciplina de Engenharia de Software com IA (Full Cycle).

O sistema implementa uma solução RAG (Retrieval Augmented Generation) utilizando Python, LangChain, PostgreSQL com extensão pgVector e Gemini.

## Objetivo

O sistema permite:

* Ler um arquivo PDF;
* Dividir o conteúdo em chunks;
* Gerar embeddings;
* Armazenar os vetores no PostgreSQL com pgVector;
* Recuperar os trechos semanticamente mais relevantes;
* Responder perguntas via terminal utilizando exclusivamente o conteúdo do PDF.

---

# Arquitetura

```text
PDF
↓
PyPDFLoader
↓
RecursiveCharacterTextSplitter
↓
Embeddings (Gemini)
↓
PGVector (PostgreSQL)
↓
Similarity Search
↓
Gemini
↓
Resposta ao usuário
```

---

# Tecnologias utilizadas

* Python 3.12
* LangChain
* PostgreSQL
* pgVector
* Docker
* Docker Compose
* Google Gemini

---

# Estrutura do projeto

```text
mba-rag-langchain-pgvector/
│
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── src/
│   ├── ingest.py
│   ├── search.py
│   └── chat.py
├── document.pdf
└── README.md
```

---

# Componentes da aplicação

## ingest.py

Responsável por:

* carregar o PDF;
* dividir o documento em chunks;
* gerar embeddings;
* armazenar os vetores no PostgreSQL através do PGVector.

## search.py

Responsável por:

* conectar ao PGVector;
* recuperar os documentos semanticamente mais relevantes utilizando Similarity Search.

## chat.py

Responsável por:

* receber perguntas do usuário;
* recuperar o contexto através do search.py;
* enviar o contexto para o Gemini;
* retornar a resposta final.

---

# Pré-requisitos

* Python 3.12+
* Docker
* Docker Compose

---

# Criando ambiente virtual

```bash
python3 -m venv .venv
```

Ativando o ambiente:

```bash
source .venv/bin/activate
```

---

# Instalando dependências

```bash
pip install -r requirements.txt
```

---

# Configuração das variáveis

Criar um arquivo `.env` baseado no `.env.example`.

Exemplo:

```env
GOOGLE_API_KEY=sua_chave
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5433/vectordb
PGVECTOR_COLLECTION=pdf_chunks
```

---

# Subindo PostgreSQL + pgVector

```bash
docker compose up -d
```

Verificar se o container está em execução:

```bash
docker ps
```

---

# Executando a ingestão

```bash
python src/ingest.py
```

Saída esperada:

```text
📄 Carregando PDF...
✂️ Dividindo em chunks...
📦 Total de chunks gerados: XX
🧠 Criando embeddings...
🗄️ Conectando ao PGVector...
🧹 Limpando coleção anterior...
💾 Salvando documentos...
✅ Ingestão concluída com sucesso!
```

Todos os chunks do documento são processados e armazenados no PostgreSQL.

---

# Executando o chat

```bash
python src/chat.py
```

Exemplo:

Pergunta:

```text
Qual o valor do orçamento?
```

Resposta:

```text
R$497,00/mês
```

Pergunta fora do contexto:

```text
Qual é a capital da França?
```

Resposta:

```text
Não tenho informações necessárias para responder sua pergunta.
```

Dessa forma, o sistema responde somente com base nas informações armazenadas no banco vetorial.

---

# Fluxo de execução

1. Subir PostgreSQL:

```bash
docker compose up -d
```

2. Executar a ingestão:

```bash
python src/ingest.py
```

3. Executar o chat:

```bash
python src/chat.py
```

---

# Evidências de persistência no PostgreSQL

Entrar no container:

```bash
docker exec -it langchain_pgvector psql -U postgres -d vectordb
```

Listar tabelas:

```sql
\dt
```

Resultado esperado:

```text
langchain_pg_collection
langchain_pg_embedding
```

Consultar coleções:

```sql
select * from langchain_pg_collection;
```

Resultado esperado:

```text
pdf_chunks
```

---

# Considerações

Durante os testes iniciais foi utilizada uma limitação temporária na quantidade de chunks devido às restrições da cota gratuita da API utilizada.

Para a versão final submetida, essa limitação foi removida, garantindo que todo o documento seja indexado e armazenado no PostgreSQL através do PGVector.

---

# Autor

Fernanda Ramos

MBA em Engenharia de Software com IA – Full Cycle