import os
import yaml

from constants.languages import LanguageKey

class ConfigLoader:
    DEFAULT_CONFIG = {
        'accounts': {}, 
        'game_folders': [],
        'settings': {
            'language': LanguageKey.CHINESE_HK.value
        }
    }

    cfg :dict

    def __init__(self):
        self.path = os.path.join(os.environ.get("APPDATA"), 'GSLogin', 'config.yml')

        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        
        if not os.path.exists(self.path):
            self.cfg = self.DEFAULT_CONFIG
            self.save()
        else:
            with open(self.path, 'r', encoding='utf-8') as f:
                self.cfg = yaml.safe_load(f) or self.DEFAULT_CONFIG

    def save(self):
        with open(self.path, 'w', encoding='utf-8') as f:
            yaml.safe_dump(self.cfg, f, allow_unicode=True)

    def get(self, key, default=None):
        return self.cfg.get(key, default)

Config = ConfigLoader()