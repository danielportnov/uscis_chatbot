# import tools
# from pinecone import Pinecone
# import os
# from langchain_ollama.llms import OllamaLLM
# import warnings

# # # split text into documents based on heading tags (document properties: page_content, metadata)
# text_splits = tools.langchain_text_splitter(url)

# # load embeddings into pinecone index
# index_name = "uscis-embeddings"
# namespace = "uscis-policy-manual"

# tools.create_pinecone_index(index_name)
# tools.load_embeddings_into_pinecone(text_splits, index_name, namespace)
# vector_store = tools.get_vector_store(index_name, namespace)

# query = "What is the purpose of the USCIS policy manual?"
# ids = tools.get_document_ids_from_query(index_name, namespace, query)
# context = tools.get_context_from_document_ids(ids)

# context_str = ''

# for c in context:
#     context_str += c[1]
#     context_str += " " + "METADATA: " + str(c[2]) + "\n\n"

# prompt = f"Context: {context_str}\nQuery: {query}"

# answer = llm.invoke(prompt)


# warnings.filterwarnings("ignore")

# url = 'https://www.uscis.gov/book/export/html/68600'
# index_name = "uscis-embeddings"
# namespace = "uscis-policy-manual"

# llm = OllamaLLM(model="llama3.1:8b")
# text_splits = tools.langchain_text_splitter(url)


# import sqlite3

# def search_sql_table_for_id(db_name, id):
#     # Connect to SQLite database
#     conn = sqlite3.connect(db_name)
#     cursor = conn.cursor()

#     # Query the table for the given id
#     cursor.execute('''
#     SELECT * FROM hashed_text_splits WHERE hash = ?
#     ''', (id,))

#     # Fetch the result
#     result = cursor.fetchone()

#     # Close the connection
#     conn.close()

#     return result

# db_name = 'hashed_text_splits.db'
# result = search_sql_table_for_id(db_name, id)

# if result:
#     print(result)



# retrieval_chain = tools.get_retrieval_chain(vector_store)
# query = "What is the purpose of the USCIS policy manual?"
# answer_with_context = retrieval_chain.invoke({"input": query})