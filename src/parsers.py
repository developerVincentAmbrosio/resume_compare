import os
import docx2txt
from typing import Final, List
from langchain_core.documents import Document
from langchain_core.document_loaders import Blob
from langchain_core.document_loaders.base import BaseBlobParser
from langchain_community.document_loaders.parsers import PyPDFParser

class NativeDocx2txtParser:
    def parse(self, blob: Blob) -> List[Document]:
        with blob.as_bytes_io() as bytes_io:
            text = docx2txt.process(bytes_io)
        return [Document(page_content=text, metadata={"source": blob.path})]

class NativeTextParser(BaseBlobParser):
    def lazy_parse(self, blob: Blob) -> List[Document]:
        text = blob.as_string()
        return [Document(page_content=text, metadata={"source": blob.path})]

PARSER_MAPPING: Final = {
    # dict of all possible file uploads
    ".pdf": PyPDFParser,
    ".docx": NativeDocx2txtParser,
    ".txt": NativeTextParser
}

def resume_text_extraction(file_name: str, file_bytes: bytes) -> str:
    
    ext = os.path.splitext(file_name.lower())[1]
    
    parser_class = PARSER_MAPPING.get(ext)

    if not parser_class:
        return f"[Unsupported file format: {ext}]"
    
    try:
        parser = parser_class()
        blob = Blob.from_data(data=file_bytes, path=file_name)
        documents = parser.parse(blob)

        extracted_text = "".join([doc.page_content for doc in documents])
        
        if not extracted_text.strip():
            return "[Error: Extracted text is empty. File might be an un-scannable image/PDF]"

        return extracted_text
        

    except Exception as e:
        return f"[Error parsing file with LangChain: {str(e)}]"
