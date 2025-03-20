from config import index, db
from llm import summarize_text
from sentence_transformers import SentenceTransformer
import os



embedding_model  = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')

def query_pinecone(state):
    try:
        user_query = state["messages"][-1]["content"]

        # Convert query to embedding
        query_embedding = embedding_model.encode(user_query).tolist()

        # Perform similarity search
        results = index.query(vector=query_embedding, top_k=5, include_metadata=True)

        # Extract and return relevant documents
        # docs = [
        #     {"role": "system", "content": f"Document: {match['metadata']['text']}"}
        #     for match in results["matches"]
        # ]
        vecids = list(map(lambda x:x['id'],results['matches']))
        dbdocs = db.execute_procedure(vecids)
        print(dbdocs) 
        docs=[]
        for each in dbdocs:
            docs.append(each[0])
        return summarize_text(docs, user_query)
    except Exception as e:
        return f"Failed to fetch content: {e}"
