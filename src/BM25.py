import bm25s

## Index for key word search
## corpus = [
#         "a cat is a feline and likes to purr",
#         "a dog is the human's best friend and loves to play",
#         "a bird is a beautiful animal that can fly",
#         "a fish is a creature that lives in water and swims"]
###################################################################
def create_vectorsearch_index(corpus):
        retriever = bm25s.BM25(corpus=corpus)
        ## Extract only the text field for tokenization
        text_only = [doc["text"] for doc in corpus]
        retriever.index(bm25s.tokenize(text_only))
        retriever.save('key_word_search_db')

def key_word_search(query):
    final_result = []
    results = []
    retriever = bm25s.BM25.load('./key_word_search_db', load_corpus=True)
    results, scores = retriever.retrieve(bm25s.tokenize(query), k=2)

    for i in range(results.shape[1]):
        doc, score = results[0, i], scores[0, i]
        print(f"Rank {i+1} (score: {score:.2f}): {doc}")
        final_result.append(f"{doc}")

    return final_result

# key_word_search('How many planets are there in solar system')