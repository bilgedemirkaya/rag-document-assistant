from parsers.base_parser import DocumentParser

class TxtParser(DocumentParser):
    def parse(self, file) -> str:
        return file.read().decode("utf-8")
