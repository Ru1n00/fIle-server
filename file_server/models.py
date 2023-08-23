from django.db import models
from django.contrib.auth.models import User

# Create your models here.

def upload_path(instance, filename):
    return f'files/{instance.user.id}/{filename}'

class File(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)
    file = models.FileField(upload_to=upload_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name
    

    def save(self, *args, **kwargs):
        if self.file:
            self.name = self.file.name
        super().save(*args, **kwargs)