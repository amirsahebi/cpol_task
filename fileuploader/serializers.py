from dataclasses import fields
from email import message
from rest_framework import serializers
from .models import *

class UploadedFileCreateSerializer(serializers.ModelSerializer):

    class Meta : 
        model = UploadedFile
        fields = ['file']

