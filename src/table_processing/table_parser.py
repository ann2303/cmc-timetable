import camelot
import pandas as pd
from abc import abstractmethod, ABC
import logging


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
        if self.table is not None:
            return self.table
        else:
            try:
                self.table = self.parse()
                return self.table
            except Exception as e:
                logging.error(f"Exception: {e}")
                raise e


class PDFTableParser(TableParser):
    """Parses tables from a PDF file using Camelot.
    
    Extends TableParser to handle PDF files specifically. Uses 
    Camelot to extract tables from a PDF. Returns a list of 
    Pandas DataFrames for each extracted table.
    """
    
    def __init__(self, file):
        super().__init__(file)

    def parse(self):
        table = camelot.read_pdf(self.file)[0]
        result = table.df.loc[1:]
        result.columns = table.df.loc[0]
        return result
    
        
class PickleParser(TableParser):
    """Parse tables from a Pickle file."""
    
    def parse(self):
        return pd.read_pickle(self.file)
    

class ExcelTableParser(TableParser):
    """Parse tables from an Excel file."""
    
    def __init__(self, file, sheet_name=None):
        super().__init__(file)
        self.sheet_name = sheet_name

    def parse(self):
        excel_file = pd.ExcelFile(self.file)
        result = excel_file.parse()
        if type(result) == dict:
            if self.sheet_name is None:
                raise ValueError("Excel file contains multiple sheets. Please specify the sheet name.")
            else:
                return result[self.sheet_name]
        return result
        
    
