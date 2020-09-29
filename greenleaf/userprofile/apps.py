from django.apps import AppConfig


class UserprofileConfig(AppConfig):
    name = 'userprofile'

    def ready(self):
        print(22222)
        import userprofile.signals
        print(22222)
