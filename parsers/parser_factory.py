from parsers.txt_parser import TxtParser
from parsers.pdf_parser import PdfParser
from parsers.docx_parser import DocxParser
from parsers.base_parser import DocumentParser

def get_parser(file_type: str) -> DocumentParser:
    if file_type == "txt":
        return TxtParser()
    elif file_type == "pdf":
        return PdfParser()
    elif file_type == "docx":
        return DocxParser()
    else:
        raise ValueError(f"Unsupported file type: {file_type}")
