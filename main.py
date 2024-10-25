import text_tools
import llm_tools

url = 'https://www.uscis.gov/book/export/html/68600'

text_splits = text_tools.langchain_text_splitter(url)
