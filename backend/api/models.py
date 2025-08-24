from django.db import models
from django.contrib.auth.models import User

class Document(models.Model):
    owner = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    file = models.FileField(upload_to='uploads/')
    original_name = models.CharField(max_length=255)
    text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # paths to vector index + metadata
    faiss_path = models.CharField(max_length=255, blank=True)
    meta_path = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.id}:{self.original_name}"

class QA(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='qas')
    question = models.TextField()
    answer = models.TextField()
    top_chunks = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Q{self.id} on Doc{self.document_id}"