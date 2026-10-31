from src.BM25 import key_word_search, create_vectorsearch_index
from src.embedding import DataStorage
import os
from src.LLM import assistant

def read_file(dir):
    testdoc_data = []
    file_count = 1
    for i in os.listdir(dir):
        with open(os.path.join(dir,i), 'r') as file:
            file_content = file.read()
        testdoc_data.append({'ID':'doc_'+ str(file_count), 'text':file_content})
        file_count += 1
    print(f"Number of documents detected: {len(testdoc_data)}")
    return testdoc_data, file_count

def read_pdf_files(pdf_paths, file_count):
    import re
    from pypdf import PdfReader

    cleaned_paragraphs = []
    paragraph_vise_data = []
    for pdf_path in os.listdir(pdf_paths):
        reader = PdfReader(os.path.join(pdf_paths,pdf_path))
        full_text = []

        # Extract raw text from each page
        for page in reader.pages:
            text = page.extract_text()
            if text:
                full_text.append(text)
        
        # Combine all page texts into one single string
        combined_text = "\n".join(full_text)
        
        # Split the text into paragraphs using regular expressions.
        # This looks for two or more consecutive newlines or massive spacing.
        paragraphs = re.split(r'\n\s*\n', combined_text)
        
        # Clean up whitespace and filter out empty paragraphs
        # cleaned_paragraphs_temp = [f"""--- Paragraph {index} ---\n {p.strip()}""" for p in paragraphs if p.strip()]
        lcleaned_paragraphs_temp = [f"""--- Paragraph {index} ---\n {p.strip()}""" for index, p in enumerate(paragraphs, 1) if p.strip()]
        for index, paragraph in enumerate(lcleaned_paragraphs_temp, 1):
                print(f"--- Paragraph {index} ---")
                print(paragraph)
                print("\n")
                # paragraph_vise_data.append(f"""--- Paragraph {index} ---\n
                # {paragraph}""")

        cleaned_paragraphs.append({'ID':'doc_'+ str(file_count), 'text':'\n'.join(lcleaned_paragraphs_temp)})
        file_count += 1
    return cleaned_paragraphs

def query_check(user_query):
    query_check_prompt = f"""Instruction: You are query check assistant.
    Rules:
    check query relavance: If the query is related to space or things related to SPACE(example: blackhole, moon, supernova, telescope, stars, dark matter, etc) you SHOULD ONLY say YES.
    Only If the query is irrelevant: check if it is a greeting(ex: Hi, Hello, Good morning, etc) you SHOULD ONLY say Greetings or if the query is gratitude (example: Thanks, etc) then you should say welcome! else ONLY say NO.
    User Query: {user_query}"""
    check_response = ''
    check_response = assistant(query_check_prompt)
    if check_response == 'YES':
        print('Query is space related')
        return True, check_response
    return False, check_response


def RAG_query_analysis(user_query):

    keyword_search_results = key_word_search(user_query)
    print(f'keyword search results: {keyword_search_results}')

    oDataStorage = DataStorage()
    sematic_search_results = oDataStorage.vector_search(user_query)

    data_chunks = f"""Info 1:
    {keyword_search_results[0]}
    Info 2:
    {keyword_search_results[1]}
    Info 3:
    {sematic_search_results["documents"][0][0]}
    Info 4:
    {sematic_search_results["documents"][0][1]}
    Info 5:
    {sematic_search_results["documents"][0][2]}
    """
            
    prompt = f"""Instruction: You are research assistant. You should answer as short as possible (maximum three lines) and politely to the question only with the information given in the Context. If the exact information isn't supported by the retrieved context, explicitly say that the information isn't available. Do not infer an answer from similar terminology.
    Context": {data_chunks}
    "Question": {user_query}
    """
    print(f"Prompt: {prompt}")
    assistant_reply = assistant(prompt)

    return data_chunks, assistant_reply

###############################################################
# Creating index for Simantic/vector and Key word search
###############################################################
def create_index():
    textfile_data, count = oRAG.read_file(r'D:/spacedeck/docs')
    pdf_data = oRAG.read_pdf_files(r'D:/spacedeck/PDF_docs', count)
    data_combined = [*textfile_data, *pdf_data]

    oDataStorage = DataStorage()
    oDataStorage.embedding_docs(data_combined)
    create_vectorsearch_index(data_combined)
    return
