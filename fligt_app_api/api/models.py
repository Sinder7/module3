from django.db import models


class LunarMission(models.Model):
    name = models.CharField(max_length=255)
    launch_details = models.JSONField()  # Для SQLite можно использовать TextField, если у тебя старая версия Django
    landing_details = models.JSONField()
    spacecraft = models.JSONField()

    def __str__(self):
        return self.name
