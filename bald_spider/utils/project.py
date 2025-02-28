from bald_spider.settings.settings_manager import SettingsManager


def get_settings(settings="settings"):
    _settings = SettingsManager()
    _settings.set_settings(settings)
    return _settings