# Desafio MBA Engenharia de Software com IA - Full Cycle

## Instruções para execução do projeto

### Configure o arquivo .env com os seguintes valores

```text
LLM_API_KEY=# Adicione GEMINI KEY HERE
DATABASE_URL=postgresql+psycopg://postgres:postgres@postgres:5432/rag
PG_VECTOR_COLLECTION_NAME=pdf_collection
PDF_PATH=../document.pdf
```

### Como rodar o projeto utilizado devcontainer


1. Abra o vscode
    - Installe a extenção dev containers https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers **se necessário**.

2. Faça o build do devcontainer (Control+P, Dev Containers: Rebuild and Reopen in Container)

3. Incluir arquivo .env no diretório raiz do projeto
    - Necessário utilizar GOOGLE_API_KEY
    - Configure o arquivo conforme exemplos no arquivo .env.example

4. Rode o comando `python ./src/ingest.py` para carregar o documento no banco de dados

5. Rode o comando `python ./src/chat.py` para iniciar o chat e fazer pergunta sobre o documento

### Como rodar o projeto sem utilizar devcontainer

1. Incluir arquivo .env no diretório raiz do projeto
    - Necessário utilizar GOOGLE_API_KEY
    - Configure o arquivo conforme exemplos no arquivo .env.example

2. Rode o comando `make run-start-environment` para preparar subir os containers

3. Rode o comando `make run-ingest-db` para carregar o documento no banco de dados

4. Rode o comando `make run-chat` para iniciar o chat e fazer pergunta sobre o documento 

5. Rode o comando `make run-stop-environment` para remover os containers e os volumes

## Exemplo de execução do script ingest.py

```text
$ make run-ingest-db
docker exec -it cis /bin/bash -c "python ./src/ingest.py"
Ingestion complete.

```
## Exemplos de execução do script chat.py

**Reposta positiva**

```text
$ make run-chat
docker exec -it cis /bin/bash -c "python ./src/chat.py"
Olá, Infome como posso te ajudar ou digite 'sair' para encerrar o programa! 
...........................................................................
Liste 10 empresas
1. Aliança Energia Participações
2. Aliança Esportes Comércio
3. Aliança Esportes ME
4. Aliança Hotelaria Comércio
5. Aliança Hotelaria EPP
6. Aliança Logística ME
7. Aliança Mineração Holding
8. Aliança Mídia LTDA
9. Aliança Publicidade Serviços
10. Aliança Siderurgia ME
...........................................................................
Informe o faturamento e o ano da sétima empresa
Aliança Mineração Holding R$ 148.721,33 1999
...........................................................................
```

**Reposta negativa**

```text
$ make run-chat
docker exec -it cis /bin/bash -c "python ./src/chat.py"
Olá, Infome como posso te ajudar ou digite 'sair' para encerrar o programa! 
...........................................................................
Qual é o faturamento da empresa Alfa Agronegócio Indústria em 2000?
Não tenho informações necessárias para responder sua pergunta.
...........................................................................
```
