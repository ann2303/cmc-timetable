import pandas as pd
from auth.models import User
import logging
    

class Timetable:
    """Class for getting timetable and it's processing"""
    
    columns = ['day of week', 'start', 'finish', 'room', 'subject', 'teacher', 'group']
    
    timetable: pd.DataFrame = pd.DataFrame(columns=columns)
    
    @staticmethod
    def load_timetable(df: pd.DataFrame) -> str:
        """Load timetable from given dataframe"""
        df_columns = set(df.columns)
        if not df_columns == set(Timetable.columns):
            logging.error(f"Provided DataFrame must have columns: {', '.join(Timetable.columns)}")
            logging.error(f"Provided DataFrame: \n{len(df_columns)}")
            for i in df_columns:
                logging.error(f"{i}")
        
        Timetable.timetable = df.sort_values(['day of week', 'start'])
        return Timetable.timetable.to_html()
         
    @staticmethod    
    def get_timetable_for_student(student_group) -> str:
        """
        Get timetable for a specific student by group.

        Args:
            student_group (int): The group of student to get the timetable for.
            
        Returns:
            str: The timetable for the specified student in html format.
        """
    
        return Timetable.timetable[Timetable.timetable['group'] == student_group].to_html()
    
    
    @staticmethod
    def get_timetable_for_teacher(teacher_name: str) -> str:
        """
        Get timetable for a specific teacher.

        Args:
            teacher_name: The teacher name.
            
        Returns:
            str: The timetable for the specified student in html format.
        """
        
        return Timetable.timetable[Timetable.timetable['teacher'] == teacher_name].to_html()
    
    @staticmethod
    def get_timetable_for_admin(teacher: User):
        """
        Get timetable for a specific teacher.

        Args:
            teacher (User): The teacher to get the timetable for.
            
        Returns:
            pd.DataFrame: The timetable for the specified teacher.
        """
        
        return Timetable.timetable.to_html()
    
    
    def update(new_timetable: pd.DataFrame):
        """
        Update the timetable with a new DataFrame.

        Args:
            new_timetable (pd.DataFrame): The new timetable to replace the existing one.
        """
        new_timetable.set_index(['group', 'start_time', 'day_of_week'], inplace=True)
        
        for index, row in new_timetable.iterrows():
            if index in Timetable.timetable.index:
                Timetable.timetable.loc[index] = row
            else:
                Timetable.timetable = Timetable.timetable.append(row)
                  
        
        