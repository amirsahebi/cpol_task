from http import client
from django.db import models
from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User
import os
from minio import Minio
import mimetypes


# Create your models here.

class UploadedFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    file = models.FileField()

    @property
    def type(self):
        extension = mimetypes.guess_type(self.file.url)[0]
        return extension

    @property 
    def size(self):
        return self.file.size



@receiver(models.signals.post_delete, sender=UploadedFile)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `UploadedFile` object is deleted.
    """
    client = Minio("minio:9000","access-key","secret-key",secure= False)
    if instance.file:
        client.remove_object("my-local-bucket",instance.file.name)
        


