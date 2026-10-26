from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END, START
from langgraph.types import RetryPolicy, Command
from src.main import query_check, RAG_query_analysis
from datetime import datetime
import pandas as pd


class AgentState(TypedDict):
    query: str
    query_validy: str
    RAG_reply: str
    data_chunks: str
    error_handler: str
    error_log: str

## Node 1
def validate_query_node(state: AgentState) -> Command:
    try:
        validity = False
        validity_response = ''
        validity, validity_response = query_check(state['query'])
        print(f"Analaysing if the query is relavant: {validity_response}")
        if validity:
            return Command(update={"query_validy": validity}, goto="RAG_node")
        else:
            return Command(update={"query_validy": validity, "error_log": validity_response}, goto="Error_handler")
    except Exception as e:
        return Command(update={"error_log": str(e)}, goto="Error_handler")

## Node 2
def RAG_node(state: AgentState) -> Command:
    try:
        RAG_result = ''
        data_chunks = ''
        data_chunks, RAG_result = RAG_query_analysis(state['query'])
        print(f"RAG Analysis on the universe: {RAG_result}")
        return Command(update={"data_chunks": data_chunks, "RAG_reply": RAG_result}, goto=END)
    except Exception as e:
        return Command(update={"RAG_reply": "Failed", "error_log": str(e)}, goto="Error_handler")

# Node 3
def Error_handler(state: AgentState) -> Command:
    print(f"Query is out of universe")
    if "Greetings" in state["error_log"]:
        fall_back_message = "Greetings Eathling, ready for a cosmic adventure?"
    elif "welcome" in state["error_log"]:
        fall_back_message = "Well, thanks for exploring the universe with me!"
    elif state["error_log"] == 'NO':
        fall_back_message = "Oops! That question is out of my universe! Ask me something about space/cosmos instead."
    else:
        fall_back_message = "I encountered a technical issue processing your request. Please try again shortly."
    return Command(update={"error_handler": fall_back_message}, goto=END)

def build_graph():
    print("Building The Graph")
    graph = StateGraph(AgentState)

    ## Adding nodes
    graph.add_node("validate_query_node", validate_query_node, retry_policy=RetryPolicy(max_attempts=3), destinations=[END])
    graph.add_node("RAG_node", RAG_node, retry_policy=RetryPolicy(max_attempts=3))
    graph.add_node("Error_handler", Error_handler)

    ## Adding edges
    graph.add_edge(START, "validate_query_node")

    return graph.compile()

def invoke_langgraph(user_query):
    print(f"start time: {datetime.now()}")

    app = build_graph()
    print(f"Users's Query: {user_query}")

    app_result = app.invoke({
        "query": user_query,
        "query_validy": '',
        "RAG_reply": '',
        "data_chunks": '',
        "error_handler": '',
        "error_log": ''
    })

    print(f"query: {user_query}\n"
        f"query validity: {app_result['query_validy']}\n"
        f"RAG reply: {app_result['RAG_reply']}\n"
        f"error handler: {app_result['error_handler']}\n"
        f"error log: {app_result['error_log']}\n")

    print(f"end time: {datetime.now()}")

    if app_result['error_handler']:
        return app_result["data_chunks"], app_result['error_handler'], app_result['error_log']
    else:
        return app_result["data_chunks"], app_result['RAG_reply'], ''


# if __name__ == "__main__":
#     for user_query in :
#         response_time = []
#         start_time = time.perf_counter()
#         user_query = 'What is the Chandrasekhar limit?'      
#         invoke_langgraph(user_query)
#         end_time = time.perf_counter()
#         response_time.append(end_time - start_time)
#     write_to_excel('RAG_evaluation.xlsx', 'Actual name')