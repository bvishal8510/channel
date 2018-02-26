from django.apps import AppConfig

class TalkConfig(AppConfig):
    name = 'talk'

    def ready(self):
        import talk.signals