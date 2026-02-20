import json
from pathlib import Path
from django import template
from django.conf import settings
from django.utils.translation import get_language

register = template.Library()

TRANSLATIONS_PATH = Path(settings.BASE_DIR) / "translations.json"

try:
    DATA = json.loads(TRANSLATIONS_PATH.read_text(encoding="utf-8"))
except Exception as e:
    DATA = {}
    print("❌ Failed to load translations.json:", e)

@register.simple_tag
def t(key):
    lang = (get_language() or "en").split("-")[0]
    return DATA.get(key, {}).get(lang, DATA.get(key, {}).get("en", key))
