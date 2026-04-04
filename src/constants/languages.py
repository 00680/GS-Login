
from enum import Enum
from typing import Dict

class LanguageKey(Enum):
    ENGLISH = 'en'
    CHINESE_HK = 'zh_HK'

LANGUAGES: Dict[LanguageKey, str] = {
    LanguageKey.ENGLISH.value: 'English',
    LanguageKey.CHINESE_HK.value: '繁體中文',
}

