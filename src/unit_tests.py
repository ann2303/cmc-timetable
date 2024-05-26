import unittest
from table_processing.table_parser import (PDFTableParser, PickleParser, ExcelTableParser)
from table_processing.timetable import Timetable
from pathlib import Path



class Test(unittest.TestCase):
    def test_parse_pdf(self):
        parser = PDFTableParser(str(Path(__file__).parent.parent / 'examples' / 'timetable_example.pdf'))
        df = parser.get_table()
        assert df is not None
        
    def test_parse_pkl(self):
        parser = PickleParser(str(Path(__file__).parent.parent / 'examples' / 'timetable_example.pkl'))
        df = parser.get_table()
        assert df is not None
    
    def test_parse_excel(self):
        parser = ExcelTableParser(str(Path(__file__).parent.parent / 'examples' / 'timetable_example.xlsx'))
        df = parser.get_table()
        assert df is not None
    
    def test_load_timetable(self):
        parser = PickleParser(str(Path(__file__).parent.parent / 'examples' / 'timetable_example.pkl'))
        df = parser.get_table()
        Timetable.load_timetable(df)
        assert Timetable.timetable is not None
    
    def test_show_for_student(self):
        parser = PickleParser(str(Path(__file__).parent.parent / 'examples' / 'timetable_example.pkl'))
        df = parser.get_table()
        Timetable.load_timetable(df)
        result = Timetable.get_timetable_for_student(527)
        assert "Ivanov" in result
        assert "Stepanov" not in result
        
if __name__ == '__main__':
    unittest.main()
        
