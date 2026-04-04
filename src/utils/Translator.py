

from constants.translations import TRANSLATIONS
from utils.SettingsConfigManager import SettingsConfigManager

class Translator:
    @staticmethod
    def translate(key):
        print(TRANSLATIONS.get(key, {}))
        print(SettingsConfigManager.getLanguage())
        return TRANSLATIONS.get(key, {}) \
            .get(SettingsConfigManager.getLanguage(), key)
