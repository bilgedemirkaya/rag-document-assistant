from abc import ABC, abstractmethod

class DocumentParser(ABC):
    @abstractmethod
    def parse(self, file) -> str:
        """Parse the uploaded file and return text"""
        pass
