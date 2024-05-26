"""Module with table parsers."""

import logging
from abc import ABC, abstractmethod

import camelot
import pandas as pd

from gettext_translate import _


class TableParser(ABC):
    """Parses tables from a file.

    Attributes:
        file (str): The path to the file to parse.

    Methods:
        parse(): Parses all tables from the file.
        get_table(): Gets tables from the file.
    """

    def __init__(self, file):
        """
        Initialize the TableParser class by setting the file attribute.

        Args:
            file (str): The path to the file to parse.
        """
        self.file = file
        self.table = None

    @abstractmethod
    def parse(self):
        """Parse all tables from the file."""
        pass

    def get_table(self):
        """
        Return the parsed table, or attempts to parse the table if it has not been parsed yet.

        Returns:
            The parsed table, or raises an exception if the table cannot be parsed.
        """
        if self.table is not None:
            return self.table
        else:
            try:
                self.table = self.parse()
                return self.table
            except Exception as e:
                logging.error(_("Exception: {}").format(e))
                raise e


class PDFTableParser(TableParser):
    """Parse tables from a PDF file using Camelot.

    Extend TableParser to handle PDF files specifically. Uses
    Camelot to extract tables from a PDF. Returns a list of
    Pandas DataFrames for each extracted table.
    """

    def __init__(self, file):
        """Initialize the TableParser class by calling the superclass constructor with the provided file."""
        super().__init__(file)

    def parse(self):
        """
        Parse a PDF table using the Camelot library and returns the table data as a pandas DataFrame.

        Args:
            self (TableParser): The TableParser instance.

        Returns:
            pandas.DataFrame: The parsed table data, with the first row as the column names.
        """
        table = camelot.read_pdf(self.file)[0]
        result = table.df.loc[1:]
        result.columns = table.df.iloc[0].tolist()
        result.group = result.group.map(int)
        return result


class PickleParser(TableParser):
    """Parse tables from a Pickle file."""

    def parse(self):
        """
        Parse the table data from a pickle file.

        Returns:
            pandas.DataFrame: The parsed table data.
        """
        result = pd.read_pickle(self.file)
        result.group = result.group.map(int)
        return result


class ExcelTableParser(TableParser):
    """Parse tables from an Excel file."""

    def __init__(self, file, sheet_name=None):
        """
        Initialize a TableParser instance with the given file and optional sheet name.

        Args:
            file (str): The file to parse.
            sheet_name (str, optional): The name of the sheet to parse, if the file contains multiple sheets.
        """
        super().__init__(file)
        self.sheet_name = sheet_name

    def parse(self):
        """
        Parse an Excel file and returns the contents as a pandas DataFrame.

        Args:
            self (TableParser): The TableParser instance.

        Returns:
            pandas.DataFrame: The contents of the Excel file as a DataFrame.

        Raises:
            ValueError: If the Excel file contains multiple sheets and the sheet name is not specified.
        """
        excel_file = pd.ExcelFile(self.file)
        result = excel_file.parse()
        if isinstance(result, dict):
            if self.sheet_name is None:
                raise ValueError(_("Excel file contains multiple sheets. Please specify the sheet name."))
            else:
                return result[self.sheet_name]
        result.group = result.group.map(int)
        return result
