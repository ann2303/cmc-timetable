from pathlib import Path

from doit.tools import create_folder

DOIT_CONFIG = {"default_tasks": ["translate_update", "mo"]}
SRCDIR = Path("src")
PODEST = SRCDIR / "po"


def task_gitclean():
    """Clean all generated files not tracked by GIT."""
    return {
        "actions": ["git clean -xdf"],
    }


def task_style():
    """Check style against flake8."""
    return {"actions": ["flake8 src"]}


def task_black():
    """Check style against black."""
    return {"actions": ["black src"]}


def task_isort():
    """Check style against isort."""
    return {"actions": ["isort src"]}


def task_docstyle():
    """Check docstrings against pydocstyle."""
    return {
        "actions": ["pydocstyle src"],
    }


def task_check_linters():
    """Check style against flake8 and black."""
    return {
        "actions": None,
        "task_dep": ["isort", "black", "style", "docstyle"],
    }


def task_pot():
    """Re-create .pot ."""
    return {
        "actions": [f"pybabel extract -F babel.cfg -o cmc-timetable.pot {str(SRCDIR)}"],
        "file_dep": list(SRCDIR.rglob("*.py")) + list(SRCDIR.rglob("*.html")) + ["babel.cfg"],
        "targets": ["cmc-timetable.pot"],
    }


def task_po():
    """Update translations."""
    return {
        "actions": [f"pybabel update -D cmc-timetable -d {str(PODEST)} -i cmc-timetable.pot"],
        "file_dep": ["cmc-timetable.pot"],
        "targets": [PODEST / "ru_RU.UTF-8" / "LC_MESSAGES" / "cmc-timetable.po"],
    }


def task_mo():
    """Compile translations."""
    return {
        "actions": [
            (create_folder, [PODEST / "ru_RU.UTF-8" / "LC_MESSAGES"]),
            f'pybabel compile -D cmc-timetable -l ru_RU.UTF-8 -i {str(PODEST / "ru_RU.UTF-8" / "LC_MESSAGES" / "cmc-timetable.po")} -d {str(PODEST)}',
        ],
        "file_dep": [PODEST / "ru_RU.UTF-8" / "LC_MESSAGES" / "cmc-timetable.po"],
        "targets": [PODEST / "ru_RU.UTF-8" / "LC_MESSAGES" / "cmc-timetable.mo"],
    }


def task_translate_update():
    return {"actions": None, "task_dep": ["pot", "po"]}


def task_create_deployment():
    return {"actions": ["docker compose down", "docker compose up --build -d"], "task_dep": ["mo"]}


def task_delete_deployment():
    return {"actions": ["docker compose down"]}
