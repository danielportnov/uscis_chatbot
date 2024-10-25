import hashlib

def create_document_hash(document):
    page_content = document.page_content
    return hashlib.sha256(page_content.encode('utf-8')).hexdigest()

def hash_all_documents(text_splits):
    document_hashes = {}

    for document in text_splits:
        document_hash = create_document_hash(document)
        document_hashes[document_hash] = document
    return document_hashes