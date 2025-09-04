import os
from dotenv import load_dotenv

from search import search_prompt
from ingest import search_pdf
from langchain.chat_models import init_chat_model
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.documents import Document
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import trim_messages
from langchain_core.runnables import RunnableLambda

load_dotenv()

LLM_API_KEY = os.getenv("LLM_API_KEY")

def database_search(query: str) -> list[Document]:
    return search_pdf(query)

def getLLM() -> BaseChatModel:
    return init_chat_model(google_api_key=LLM_API_KEY,
        model="gemini-2.5-flash-lite", 
        model_provider="google_genai", 
        temperature=0.5)
    
def getAwnserFromDB(query: str) -> str:
    documents = database_search(query)
    awnsers = [
        f"{i+1}\n{doc.page_content.strip()}\n" + f"="*50 for i, doc in enumerate(documents)
    ]
    # Check awnsers from DB
    # print("\n".join(awnsers))
    return awnsers

def prepare_inputs(payload: dict) -> dict:
    raw_history = payload.get("historico_nao_tratado", [])
    # Assuming `messages` is a list of HumanMessage and AIMessage objects
    trimmed = trim_messages(
        raw_history,
        token_counter=len,
        max_tokens=4,
        strategy="last",
        start_on="human",
        include_system=True,
        allow_partial=False,
    )
    
    # For debugging purposes, you can uncomment the following lines to see the trimmed history
    def debug_history():
        print("=== Raw History Messages ===")
        for msg in raw_history:
            print(f"{msg.type}: {msg.content}")
        print("============================")
    # debug_history()
    
    return {"pergunta": payload.get("pergunta",""), "contexto":payload.get("contexto",""), "historico": trimmed}

# In-memory session store
session_store: dict[str, InMemoryChatMessageHistory] = {}
def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    if session_id not in session_store:
        session_store[session_id] = InMemoryChatMessageHistory()
    return session_store[session_id]

def main():
    prompt = search_prompt()
    if not prompt:
        print("Não foi possível iniciar o chat. Verifique os erros de inicialização.")
        return
    llm = getLLM()
    
    prepare = RunnableLambda(prepare_inputs)
    chain = prepare | prompt | llm
    conversational_chain = RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="pergunta",
        history_messages_key="historico_nao_tratado"
    )

    user_question = input("Olá, Faça um pergunta ou digite 'sair' para encerrar o programa! \n")
    while True:    
        awnsers = getAwnserFromDB(user_question)
        config = {"configurable": {"session_id": "demo-session"}}
        
        llmawnser = conversational_chain.invoke({"pergunta": user_question, "contexto": awnsers}, config=config)
        print(llmawnser.content), 
        
        user_question = input()
        if user_question.lower() in ["sair", "exit", "quit"]:
            break

if __name__ == "__main__":
    main()