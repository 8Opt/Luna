"""
Objects in this file is in charge of two things: 

    1. Embedding data with relevant model. 
    2. Store data with relevant vector database. 
        1. For textual data: Luna stores it in ChromaDB. 
        2. For image data: Luna stores it in FAISS (working great with .bin file)

"""

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