import os

def read_file(dir):
    file_id = 1
    sematic_search_dcollection = []
    keyword_search_dcollection = []
    for i in os.listdir(dir):
        with open(os.path.join(dir,i), 'r') as file:
            file_content = file.read()
        sematic_search_dcollection.append({"id":'_'.join(['doc',str(file_id)]), 'content':file_content})
        keyword_search_dcollection.append(file_content)
        file_id += 1
    print(f"Number of documents detected: {len(sematic_search_dcollection)}")
    return sematic_search_dcollection, keyword_search_dcollection



# data = read_file(r"D:/RAG/docs")
# print(data)