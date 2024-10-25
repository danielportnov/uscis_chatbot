import text_tools
import llm_tools
import chunk_tools

url = 'https://www.uscis.gov/book/export/html/68600'

text = text_tools.get_text_from_url(url)

