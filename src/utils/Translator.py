from constants.translations import TRANSLATIONS
from utils.SettingsConfigManager import SettingsConfigManager

class Translator:
    @staticmethod
    def translate(key):
        return TRANSLATIONS.get(key, {}) \
            .get(SettingsConfigManager.getLanguage(), key)
