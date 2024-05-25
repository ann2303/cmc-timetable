import logging

import pandas as pd
from pretty_html_table import build_table

from gettext_translate import _


class Timetable:
    """Class for getting timetable and it's processing"""

    columns = ["day of week", "start", "finish", "room", "subject", "teacher", "group"]

    timetable: pd.DataFrame = pd.DataFrame(columns=columns)

    @staticmethod
    def show_timetable(df: pd.DataFrame) -> str:
        """Show timetable"""
        df.columns = [_("day of week"), _("start"), _("finish"), _("room"), _("subject"), _("teacher"), _("group")]
        return build_table(df, "blue_light", index=False)

    @staticmethod
    def load_timetable(df: pd.DataFrame) -> str:
        """Load timetable from given dataframe"""
        df_columns = set(df.columns)
        if not df_columns == set(Timetable.columns):
            logging.error(_("Provided DataFrame must have columns: {}").format(", ".join(Timetable.columns)))
            logging.error(_("Provided DataFrame: \n{}").format(len(df_columns)))
            for i in df_columns:
                logging.error(f"{i}")

        Timetable.timetable = df.sort_values(["day of week", "start"]).reset_index(drop=True)
        return Timetable.show_timetable(Timetable.timetable)

    @staticmethod
    def get_timetable_for_student(student_group) -> str:
        """
        Get timetable for a specific student by group.

        Args:
            student_group (int): The group of student to get the timetable for.

        Returns:
            str: The timetable for the specified student in html format.
        """

        return Timetable.show_timetable(Timetable.timetable[Timetable.timetable["group"] == student_group])

    @staticmethod
    def get_timetable_for_teacher(teacher_name: str) -> str:
        """
        Get timetable for a specific teacher.

        Args:
            teacher_name: The teacher name.

        Returns:
            str: The timetable for the specified student in html format.
        """

        return Timetable.show_timetable(Timetable.timetable[Timetable.timetable[_("teacher")] == teacher_name])

    @staticmethod
    def get_timetable_for_admin():
        """
        Get timetable for a specific teacher.

        Args:
            teacher (User): The teacher to get the timetable for.

        Returns:
            pd.DataFrame: The timetable for the specified teacher.
        """

        return Timetable.show_timetable(Timetable.timetable)
