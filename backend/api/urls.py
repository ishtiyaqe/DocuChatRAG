from django.urls import path
from .views import UploadView, ListDocsView, AskView, DocFileView

urlpatterns = [
    path('upload/', UploadView.as_view()),
    path('documents/', ListDocsView.as_view()),
    path('ask/<int:doc_id>/', AskView.as_view()),
    path('file/<int:doc_id>/', DocFileView.as_view()),
]
