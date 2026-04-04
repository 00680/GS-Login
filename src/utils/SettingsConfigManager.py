from config.ConfigLoader import Config, ConfigLoader
from constants.languages import LanguageKey

class SettingsConfigManager:
    @staticmethod
    def getLanguage():
        return Config.get('settings', ConfigLoader.DEFAULT_CONFIG['settings']) \
            .get('language', LanguageKey.CHINESE_HK.value)

    @staticmethod
    def setLanguage(language):
        if 'settings' not in Config.cfg:
            Config.cfg['settings'] = {}
        Config.cfg['settings']['language'] = language
        Config.save()

    @staticmethod
    def getCapSolverApiKey():
        return Config.get('settings', ConfigLoader.DEFAULT_CONFIG['settings']) \
            .get('capSolverApiKey', '')
    
    @staticmethod
    def setCapSolverApiKey(apiKey):
        if 'settings' not in Config.cfg:
            Config.cfg['settings'] = {}
        Config.cfg['settings']['capSolverApiKey'] = apiKey
        Config.save()