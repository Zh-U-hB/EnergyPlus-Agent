from eppy.modeleditor import IDF
from abc import ABC, abstractmethod
from typing import Dict

from src.utils.logging import get_logger

class BaseConverter(ABC):

    def __init__(self, idf: IDF):
        self.idf = idf
        self.logger = get_logger(__name__)
    

    @abstractmethod
    def convert(self) -> IDF:
        pass

    @abstractmethod
    def add_to_idf(self) -> None:
        pass
    
    @abstractmethod
    def validate(self, data:Dict) -> bool:
        pass