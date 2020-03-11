from django.db import models

# Create your models here.


class UploadedFile(models.Model):

    file = models.FileField(upload_to='uploaded_files/')
    separator = models.CharField(max_length=1, verbose_name='separador')
    token = models.UUIDField()
