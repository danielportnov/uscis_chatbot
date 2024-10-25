from pinecone import Pinecone, ServerlessSpec
import os
import llm_tools

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

index_name = "embedding-test"

# pc.create_index(
#     name=index_name,
#     dimension=4096,
#     metric="cosine",
#     spec=ServerlessSpec(
#         cloud="aws",
#         region="us-east-1"
#     ) 
# )

text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Integer euismod, orci ut placerat ultricies, odio nulla tincidunt odio, a viverra lorem magna eget erat. Nulla facilisi. Ut fringilla magna nec justo convallis, ut feugiat nunc ullamcorper. Suspendisse potenti. In scelerisque orci sit amet ligula dignissim, vel lacinia mauris efficitur."
text, vector = llm_tools.generate_embedding(text)

index = pc.Index(index_name)
index.upsert([(text, vector)])