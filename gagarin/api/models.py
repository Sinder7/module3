from django.db import models

class Missions(models.Model):
    name = models.CharField(max_length=255)
    launch_details = models.JSONField()
    landing_details = models.JSONField()
    spacecraft = models.JSONField()