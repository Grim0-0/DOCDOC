from django.apps import AppConfig
import os
import signal

class DcappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dcapp'
    def ready(self):
        from django.contrib.sessions.models import Session
        def clear_sessions_and_exit(signal, frame):
            print("Server is stopping, clearing sessions...")
            Session.objects.all().delete()
            os._exit(0)

        signal.signal(signal.SIGINT, clear_sessions_and_exit)