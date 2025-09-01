# Desafio MBA Engenharia de Software com IA - Full Cycle

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
Olá, Faça um pergunta! Qual é o faturamento da empresa Alfa Agronegócio Indústria em 1931?
R$ 85.675.568,77
```

**Reposta negativa**

```text
$ make run-chat
docker exec -it cis /bin/bash -c "python ./src/chat.py"
Olá, Faça um pergunta! Qual é o faturamento da empresa Alfa Agronegócio Indústria em 2000?
Não tenho informações necessárias para responder sua pergunta.
```
