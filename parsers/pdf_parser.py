import fitz
from parsers.base_parser import DocumentParser

class PdfParser(DocumentParser):
    def parse(self, file) -> str:
        text = ""
        with fitz.open(stream=file.read(), filetype="pdf") as doc:
            for page in doc:
                text += page.get_text()
        return text
