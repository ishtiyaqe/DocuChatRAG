from rest_framework import serializers
from .models import Document, QA


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id','original_name','created_at']


class UploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id','file','original_name']
        read_only_fields = ['id']


class QASerializer(serializers.ModelSerializer):
    class Meta:
        model = QA
        fields = ['id', 'document', 'question', 'answer', 'top_chunks', 'created_at']