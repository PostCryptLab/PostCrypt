from django.db import models
from django.contrib.auth.models import User

def upload_location(instance, filename):
    return 'labs/{}/{}'.format(instance.lab_type, filename)


class Document(models.Model):
    docfile = models.FileField(upload_to=upload_location)
    lab_type = models.CharField(max_length=25)

class LabChoice(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name

class OneTimeCode(models.Model):
    code = models.CharField(max_length=10, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='one_time_codes')
    used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)