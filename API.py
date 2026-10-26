from fastapi import FastAPI, HTTPException
from src.graph import invoke_langgraph

app = FastAPI()

@app.get('/')
async def root():
    return {"messgae": "Ask anything about Space :)"}

@app.get('/{question}')
async def RAG_query(question: str) -> dict[str, str]:
    print(f"Query: {question}")
    if len(question) > 100:
        raise  HTTPException(status_code=413, detail='Query length is beyound expectation')
    try:
        search_data_chunck, RAG_reply = invoke_langgraph(question)
        if 'technical issue' in RAG_reply:
            raise  HTTPException(status_code=400, detail=RAG_reply)
        
        return {"messgae": RAG_reply}
    except Exception as e:
        print(f"Exception {e} occured while RAG search")
        raise  HTTPException(status_code=400, detail=str(e))