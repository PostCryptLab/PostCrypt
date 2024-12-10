from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password

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
    code = models.CharField(max_length=128)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='one_time_codes')
    used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def set_code(self, raw_code):
        """
        Hash the code before saving
        :param raw_code: Original unhashed code
        """
        self.code = make_password(raw_code)

    def check_code(self, raw_code):
        """
        Verify if the provided code matches the stored hashed code
        :param raw_code: Code to check
        :return: Boolean indicating if code is correct
        """
        return check_password(raw_code, self.code)
    
    def save(self, *args, **kwargs):
        if not self.code.startswith('pbkdf2_sha256$'):
            self.set_code(self.code)
        super().save(*args, **kwargs)