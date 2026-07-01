class AppSettings:
    def __init__(self, prefix):
        self.prefix = prefix

    def _settings(self, name, dflt):
        from django.conf import settings

        return getattr(settings, self.prefix + name, dflt)
    
    @property
    def PATH_LENGTH(self):
        return self._settings("PATH_LENGTH", 200)
    

app_settings = AppSettings(('DRF_TRACKING_'))