import camelot
import pandas as pd
from abc import abstractmethod, ABC
import re


class TableParser(ABC):
    """Parses tables from a file.
    
    Attributes:
        file (str): The path to the file to parse. 

    Methods:
        parse(): Parses all tables from the file.
        get_table(): Gets tables from the file.
    """
    def __init__(self, file):
        self.file = file
        self.table = None
        
    @abstractmethod
    def parse(self):
        pass
    
    def get_table(self):
        if self.table:
            return self.table
        else:
            self.table = self.parse()
            return self.table


class PDFTableParser(TableParser):
    """Parses tables from a PDF file using Camelot.
    
    Extends TableParser to handle PDF files specifically. Uses 
    Camelot to extract tables from a PDF. Returns a list of 
    Pandas DataFrames for each extracted table.
    """

    def parse(self):
        table = camelot.read_pdf(self.file)[0]
        return table.df


    
        
class PickleParser(TableParser):
    """Parse tables from a Pickle file."""
    
    def parse(self):
        return pd.read_pickle(self.file)
        
    
