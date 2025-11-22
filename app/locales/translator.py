import json
from pathlib import Path


LOCALES_DIR = Path(__file__).parent / "texts"

DEFAULT_LANG = "en"


class I18N:
    def __init__(self):
        self.translations = {}
        self.load_languages()

    def load_languages(self):
        for file in LOCALES_DIR.glob("*.json"):
            lang_code = file.stem
            with open(file, "r", encoding="utf-8") as f:
                self.translations[lang_code] = json.load(f)

    def t(self, lang: str, key: str) -> str:

        lang_data = self.translations.get(lang)

        if not lang_data:
            lang_data = self.translations[DEFAULT_LANG]

        return lang_data.get(key) or self.translations[DEFAULT_LANG].get(key)


i18n = I18N()
