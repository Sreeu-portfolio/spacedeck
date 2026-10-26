from src.graph import invoke_langgraph
import time
import pandas as pd
from deepeval_test import test_relevancy

def write_to_excel(excel_name, RAG_response):
    df = pd.read_excel(excel_name, sheet_name='Sheet1')
    for column in ["RAG_Answer", "Response_Time in sec ", "Error_log"]:
        if column in df.columns:
            print(f"Column exists: {column}")
        else:
            df[column] = ''
    
    while len(RAG_response) != 0:
        for question in df['Questions']:
            if RAG_response[0]["Question"] == question:
                print(question)
                df.loc[df['Questions'] == question, "RAG_Answer"] = RAG_response[0]["RAG answer"]
                df.loc[df['Questions'] == question, "Response_Time in sec"] = RAG_response[0]["Response time"]
                df.loc[df['Questions'] == question, "Error_log"] = RAG_response[0]["Error log"]
                df.to_excel(excel_name, sheet_name='Sheet1', index=False)
                break

        RAG_response.pop(0)
        print(f"Updated Score for {question}")

if __name__ == "__main__":
    RAG_response = []
    for user_query in ["What are the main stages in a star's life cycle?",
    "What causes a core-collapse supernova?",
    "What is the Chandrasekhar limit?",
    "How do white dwarfs differ from neutron stars?",
    "How can astronomers detect black holes without seeing them directly?",
    "What is the Hayashi track in stellar evolution?",
    "Why can very massive stars form despite radiation pressure?",
    "What role do neutrinos play in a core-collapse supernova?",
    "What is the asymptotic giant branch (AGB)?",
    "How does the Milky Way's structure reveal its history?",
    "What is dark energy, and how is it connected to cosmic expansion?",
    "What are the main scientific objectives of the James Webb Space Telescope?",
    "What is the purpose of India's Chandrayaan-2 mission?",
    "What was the main objective of India's Mars Orbiter Mission?",
    "Why does a spacecraft need a thermal protection system during atmospheric entry?",
    "What does the entry flight-path angle (EFPA) affect during spacecraft landing?",
    "What is PICA, and why is it used in spacecraft?",
    "What is the role of CHACE-2 in Chandrayaan-2?",
    "How does microgravity affect animals and humans in space?"]:
        start_time = time.perf_counter()  
        data_chunck, RAG_answer, error_log = invoke_langgraph(user_query)
        end_time = time.perf_counter()
        response_time = end_time - start_time 
        RAG_response.append({"Question":user_query, 
                                "Response time": response_time, 
                                "RAG answer": RAG_answer, 
                                "Search chuncks": data_chunck,
                                "Error log": error_log})

    write_to_excel('RAG_evaluation.xlsx', RAG_response)

    ## Deepeval
    test_relevancy()
    print("Execution and Evaluation is done")