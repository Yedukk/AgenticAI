import os
from pinecone import Pinecone, ServerlessSpec
from db import DatabaseSingleton

LANGSMITH_TRACING = "true"
LANGSMITH_API_KEY = os.environ.get("LANGSMITH_API_KEY")
LANGSMITH_PROJECT = "TestingLLM"
GROK_API_KEYs = "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"#os.environ.get("GROK_API_KEY")

if not GROK_API_KEYs:
    raise ValueError("Missing 'GROK_API_KEY'. Set it in environment variables.")




PINECONE_API_KEY = "62242428-448b-419f-a958-6e3977670073"#os.environ.get("PINECONE_API_KEY")
PINECONE_ENVIRONMENT ="us-east-1" #os.environ.get("PINECONE_ENVIRONMENT") 

#pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)

pc = Pinecone(api_key=PINECONE_API_KEY)

index_name = "uatindex" #os.environ.get("PINECONE_INDEX")
#if index_name not in pinecone.list_indexes():
    #pinecone.create_index(index_name, dimension=768, metric="cosine")

index = pc.Index(index_name)

# Singleton instance
#db = DatabaseSingleton(os.environ.get("SERVER_NAME"), os.environ.get("DATABASE_NAME"), os.environ.get("USER_NAME"), os.environ.get("PASSWORD"))
db = DatabaseSingleton(host="joevirtualagent.database.windows.net",
    database="JoeDev",
    user="JoeDevUser",
    password="fw@GVg4#WSG@vds")