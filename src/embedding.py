from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.utils import embedding_functions
from src.read_files import read_file
from src.LLM import assistant

class DataStorage():
    def __init__(self):
        ##Emmbedding model
        model_name = 'sentence-transformers/all-MiniLM-L6-v2'
        # model = SentenceTransformer(model_name)

        ##Converting and storing data into ChromaDB using embedding_functons and model
        embed_function = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=model_name)

        ##Initialise client-> a dir which acts as DB
        self.client = chromadb.PersistentClient(path='./vector_search_db')

        ##Create a collection with a name to store it in the client -> 'chrom_db' dir
        self.collection = self.client.get_or_create_collection(name='space', embedding_function=embed_function)

    ## Add data to the collection 'space'
    ## documents = read_file('./docs') ## Example output: [{'ID': 'doc_1', 'text': 'the doc content'}, {'id': 'doc_1', 'content': }..]
    ##################################################################################################################
    def embedding_docs(self, documents):
                self.collection.add(documents=[doc['text'] for doc in documents], ids=[doc['ID'] for doc in documents])

        # ##Retrive data from conformation
        # result = collection.get(ids=['doc_1'], include=["embeddings"])
        # print(result)

    def vector_search(self, user_query):
        answer = self.collection.query(query_texts=user_query, n_results=3)   ## n_results is no of search outputs
        for i, doc in enumerate(answer["documents"][0]):
            print(f"Result {i+1}: {doc} (Score: {answer['distances'][0][i]})")

        
        return answer
            
#         results = f"""Info 1: 
# {answer["documents"][0][0]}
# Info 2:
# {answer["documents"][0][1]}
# Info 3:
# {answer["documents"][0][2]}
# """
#         prompt = f"""Context": {results}
# "Question": {user_query}
# """
#         print(f"Prompt: {prompt}")
#         assistant_reply = assistant(prompt)
#         # with open(r"D:\RAG\results\result.txt", 'a') as file:
#         #         reply = f'{user_query}\n{assistant_reply}\n\n'
#         #         file.write(reply)
#         print(f"Intelligent asistant answer: {assistant_reply}")

# oDataStorage = DataStorage()
# for l in ['How many planets are there in solar system']:
#     oDataStorage.embaedding_query(l)