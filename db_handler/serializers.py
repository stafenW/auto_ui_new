from rest_framework import serializers
from .models import Process, Image


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'process', 'image', 'thumbnail']


class ProcessSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Process
        fields = ['id', 'title', 'describe', 'create_time', 'images']
