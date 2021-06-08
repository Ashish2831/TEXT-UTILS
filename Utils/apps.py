from django.apps import AppConfig

class AnalyserConfig(AppConfig):
    name = 'Utils'

    def ready(self):
        import Utils.signals
        return super().ready()