from typing import Union, List

from langchain_core.documents import Document

from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def get_documents(config, 
                  content: str) -> Union[List[Document], None]: 
    try: 
        loader = TextLoader(content)
        text_documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=config['chunk_size'], 
                                                    chunk_overlap=config['chunk_overlap'])
        documents = text_splitter.split_documents(text_documents)
        return documents
    except: 
        return None