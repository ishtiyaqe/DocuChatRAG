from django.contrib import admin
from .models import Document, QA

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    # Display fields in list view
    list_display = (
        'id',
        'original_name',
        'owner',        # ForeignKey, will show username
        'file',
        'created_at',
        'faiss_path',
        'meta_path',
    )
    list_filter = ('created_at', 'owner')  # Optional: filters in admin sidebar
    search_fields = ('original_name', 'text', 'owner__username')  # Optional: search box

@admin.register(QA)
class QAAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'document',   # Shows the related document's __str__
        'question',
        'created_at',
    )
    list_filter = ('created_at', 'document')  # Optional
    search_fields = ('question', 'answer', 'document__original_name')  # Optional
