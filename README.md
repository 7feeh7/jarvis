# Sistema RAG com FastAPI e MongoDB

Este projeto implementa um **sistema RAG (Retrieval-Augmented Generation)** usando **FastAPI** como backend, **MongoDB Atlas com Vector Search** para armazenamento vetorial e um pipeline de ingestão e busca otimizado.

## Tecnologias

- [Python 3+](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [MongoDB Atlas Vector Search](https://www.mongodb.com/products/platform/atlas-vector-search)
- [OpenAI API](https://platform.openai.com/)
- [Apache Kafka](https://kafka.apache.org/)
- [Uvicorn](https://www.uvicorn.org/)

## Arquitetura

Abaixo, um diagrama simplificado mostrando o uso do projeto:

<img width="1863" height="2363" alt="rag" src="https://github.com/user-attachments/assets/c3a2d7f5-2d1f-4c21-8cf3-13147f975bec" />


## Features

- [x] Ingestão de conhecimento e embeddings.
- [x] Armazenamento em base vetorial com **MongoDB Vector Search**.
- [x] Recuperação semântica usando embeddings e filtros
- [x] Suporte a múltiplos **namespaces** para separar domínios de conhecimento.
- [x] Memória de conversas para contexto contínuo.
- [x] Geração de respostas via modelo LLM.
- [x] Filtro por **score mínimo** para relevância.
- [x] Retorno apenas do documento mais relevante (modo Best Match).

## Pré-requisitos

Antes de começar, configure:

- Python 3+ instalado.
- Conta no MongoDB Atlas com Vector Search habilitado
- Chave de API de um provedor de LLM (ex.: OpenAI)

## Instalação
> OBS: E NECESSARIO CONFIGURAR O ARQUIVO .ENV

1. Clonar o repositório:

   ```bash
   git clone https://github.com/7feeh7/jarvis.git
   ```

2. Crie e acesse o ambiente virtual do python:

   ```bash
   python -m venv venv
   ```
   ```bash
   source venv/Scripts/activate
   ```

3. Instale as dependencias:

   ```bash
   pip install -r requirements.txt
   ```

4. Rodando a aplicação:

   ```bash
   uvicorn app.main:app --reload
   ```
5. Agora deve estar em execução:
- API: http://localhost:8080
- Swagger: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Documentação

A documentação da API deve esta indisponível no link local: http://127.0.0.1:8000/docs.

## Contribuindo

Contribuições para o projeto são bem vindas! Pra contribuir com o projeto, siga estas etapas:

1. De um fork no repositorio.
2. Crie uma nova branch para sua feature ou bug fix.
3. Faça suas alterações, confirmando e pressionando conforme necessário.
4. Envie uma solicitação pull com uma descrição detalhada de suas alterações.

## Contato

Para qualquer dúvida ou consulta, entre em contato com [Felipe](mailto:felipe.pires.soaresti@gmail.com).

Sinta-se à vontade para entrar em contato conosco se tiver algum comentário, sugestão ou se encontrar algum problema ao usar o projeto. Sua opinião é valiosa para nós e nos ajuda a melhorar a aplicação.
