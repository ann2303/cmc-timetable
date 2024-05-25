import gettext
import locale

LOCALES = {
    ("ru_RU", "UTF-8"): gettext.translation('cmc-timetable', "po", ["ru"]),
    ("en_US", "UTF-8"): gettext.NullTranslations(),
}

def _(text):
    return LOCALES[locale.getlocale()].gettext(text)
