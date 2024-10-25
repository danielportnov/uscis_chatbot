import text_tools
import llm_tools

url = 'https://www.uscis.gov/book/export/html/68600'

text = text_tools.get_text_from_url(url)
# TODO: finish project with 3 batches... to know it works
batched_text = text_tools.batch_text(text)
embeddings = llm_tools.generate_embeddings(batched_text)