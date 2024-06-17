from django.db import models


def upload_location(instance, filename):
    return 'labs/{}/{}'.format(instance.lab_type, filename)


class Document(models.Model):
    docfile = models.FileField(upload_to=upload_location)
    lab_type = models.CharField(max_length=25)
