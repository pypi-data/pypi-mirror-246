from langchain.document_loaders import Docx2txtLoader
from langchain.document_loaders import UnstructuredPDFLoader
from langchain.document_loaders import UnstructuredPowerPointLoader
from langchain.document_loaders import UnstructuredURLLoader
from langchain.document_loaders.image import UnstructuredImageLoader

def all_loaders(path: str):
    if path.endswith("docx"):
        data=Docx2txtLoader(path)
        return data.load()
    
    if path.endswith("pdf"):
        data=UnstructuredPDFLoader(path)
        return data.load()
    
    if path.endswith("ppt"):
        data=UnstructuredPowerPointLoader(path)
        return data.load()
    
    if "https" in path:
        url = [path]
        data=UnstructuredURLLoader(urls=url)
        return data.load()
    
    if path.endswith("png") or path.endswith("jpg"):
        loader=UnstructuredImageLoader(path)
        data=loader.load()
        return data[0]

