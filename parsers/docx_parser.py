import docx
from parsers.base_parser import DocumentParser
import io

class DocxParser(DocumentParser):
    def parse(self, file) -> str:
        doc = docx.Document(io.BytesIO(file.read()))
        return "\n".join([p.text for p in doc.paragraphs])
