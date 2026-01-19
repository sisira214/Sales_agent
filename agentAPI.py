# main.py
from fastapi import FastAPI, Query
from Sales_langchain import run_agent

app = FastAPI(title="E-Commerce Assistant API", version="1.0")

@app.get("/")
def home():
    return {"message": "Welcome to the E-Commerce Assistant API!"}

@app.post("/query")
def query_agent(user_query: str = Query(..., description="User query for e-commerce assistant"), reset_memory: bool = False):
    """
    Send a query to the LangGraph-powered e-commerce assistant.
    """
    try:
        response = run_agent(user_query)
        return {"status": "success", "query": user_query, "response": response}
    except Exception as e:
        return {"status": "error", "error": str(e)}
