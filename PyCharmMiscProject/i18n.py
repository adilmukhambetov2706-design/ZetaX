import json
from pathlib import Path

_DIR = Path(__file__).parent
_TRANSLATIONS_FILE = _DIR / "translations.json"
_SETTINGS_FILE = _DIR / "settings.json"

_LANG_MAP = {"English": "en", "Russian": "ru", "Kyrgyz": "kg"}
_LANG_MAP_INV = {v: k for k, v in _LANG_MAP.items()}

_translations: dict = {}
_current_lang: str = "en"


def _load():
    global _translations, _current_lang
    try:
        with open(_TRANSLATIONS_FILE, encoding="utf-8") as f:
            _translations = json.load(f)
    except Exception:
        _translations = {}
    try:
        with open(_SETTINGS_FILE, encoding="utf-8") as f:
            _current_lang = json.load(f).get("language", "en")
    except Exception:
        _current_lang = "en"


_load()


def t(key: str) -> str:
    val = _translations.get(_current_lang, {}).get(key)
    if val is None:
        val = _translations.get("en", {}).get(key)
    return val if val is not None else key


def get_language_name() -> str:
    return _LANG_MAP_INV.get(_current_lang, "English")


def set_language(name: str):
    global _current_lang
    _current_lang = _LANG_MAP.get(name, "en")
    try:
        data = {}
        if _SETTINGS_FILE.exists():
            with open(_SETTINGS_FILE, encoding="utf-8") as f:
                data = json.load(f)
        data["language"] = _current_lang
        with open(_SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception:
        pass
