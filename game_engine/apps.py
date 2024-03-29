from django.apps import AppConfig


class GameEngineConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'game_engine'

    def ready(self):
        import game_engine.signals
