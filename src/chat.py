import os
from dotenv import load_dotenv

from search import search_prompt
from ingest import search_pdf
from langchain.chat_models import init_chat_model
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import BasePromptTemplate
from langchain_core.documents import Document
from langchain.agents import create_react_agent, AgentExecutor

load_dotenv()   
LLM_API_KEY = os.getenv("LLM_API_KEY")


def database_search(query: str) -> list[Document]:
    return search_pdf(query)

def getLLM() -> BaseChatModel:
    return init_chat_model(google_api_key=LLM_API_KEY,
        model="gemini-2.5-flash-lite", 
        model_provider="google_genai", 
        temperature=0.5)

def main():
    user_question = input("Olá, Faça um pergunta!")
    vetorized_documents = database_search(user_question)
    awnsers = [
        f"{i+1}\n{doc.page_content.strip()}\n" + f"="*50 for i, doc in enumerate(vetorized_documents)
    ]
    
    # Check awnsers from DB
    # print("\n".join(awnsers))
    
    prompt = search_prompt()
    if not prompt:
        print("Não foi possível iniciar o chat. Verifique os erros de inicialização.")
        return
    
    llm = getLLM()
    chain = prompt | llm
    llmawnser = chain.invoke({"pergunta": user_question, "contexto": awnsers})
    print(llmawnser.content)

if __name__ == "__main__":
    main()