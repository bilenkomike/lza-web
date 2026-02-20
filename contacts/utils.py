import json
from django.conf import settings
from django.utils.translation import get_language
from pathlib import Path

TRANSLATIONS_PATH = Path(settings.BASE_DIR) / "translations.json"

def t(key: str, default: str = "") -> str:
    try:
        data = json.loads(TRANSLATIONS_PATH.read_text(encoding="utf-8"))
    except Exception:
        return default or key

    lang = (get_language() or "en").split("-")[0]
    return data.get(key, {}).get(lang, data.get(key, {}).get("en", default or key))
