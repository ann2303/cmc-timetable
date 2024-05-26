from doit.tools import create_folder
from pathlib import Path

DOIT_CONFIG = {'default_tasks': ['translate_update', 'mo']}
SRCDIR = Path('src')
PODEST = SRCDIR / 'po'

def task_pot():
    """Re-create .pot ."""
    return {
            'actions': [f'pybabel extract -F babel.cfg -o cmc-timetable.pot {str(SRCDIR)}'],
            'file_dep': list(SRCDIR.rglob("*.py")) + list(SRCDIR.rglob("*.html")) + ['babel.cfg'],
            'targets': ['cmc-timetable.pot'],
           }


def task_po():
    """Update translations."""
    return {
            'actions': [f'pybabel update -D cmc-timetable -d {str(PODEST)} -i cmc-timetable.pot'],
            'file_dep': ['cmc-timetable.pot'],
            'targets': [PODEST / "ru_RU.UTF-8" / "LC_MESSAGES" / "cmc-timetable.po"],
           }


def task_mo():
    """Compile translations."""
    return {
            'actions': [
                (create_folder, [PODEST / "ru_RU.UTF-8" / "LC_MESSAGES"]),
                f'pybabel compile -D cmc-timetable -l ru_RU.UTF-8 -i {str(PODEST / "ru_RU.UTF-8" / "LC_MESSAGES" / "cmc-timetable.po")} -d {str(PODEST)}'
                       ],
            'file_dep': [PODEST / "ru_RU.UTF-8" / "LC_MESSAGES" / "cmc-timetable.po"],
            'targets': [PODEST / "ru_RU.UTF-8" / "LC_MESSAGES" / "cmc-timetable.mo"],
           }
    
def task_translate_update():
    return {
            'actions': None,
            'task_dep': ['pot', 'po']
           }