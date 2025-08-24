from rest_framework import status, views, generics, permissions
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.core.files.storage import default_storage
from django.http import FileResponse
from .models import Document, QA
from .serializers import DocumentSerializer, UploadSerializer, QASerializer
from .utils.parse_docs import extract_text_from_file
from .utils.chunking import chunk_text
from .utils.vectordb import VectorIndex
from .utils.model_client import ModelClient
from .permissions import IsOwner
import os

class UploadView(views.APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({'error': 'No file provided'}, status=400)

        original_name = file.name
        path = default_storage.save(f"uploads/{original_name}", file)
        full_path = os.path.join(settings.MEDIA_ROOT, path)

        # Extract full text
        full_text = extract_text_from_file(full_path)
        if not full_text.strip():
            return Response({'error': 'Could not extract text from file'}, status=400)

        # Save document with full text
        doc = Document.objects.create(
            owner=request.user,
            file=path,
            original_name=original_name,
            text=full_text
        )

        # Build vector index (still may need chunks for FAISS)
        idx_dir = os.path.join(settings.MEDIA_ROOT, 'indices', str(doc.id))
        os.makedirs(idx_dir, exist_ok=True)
        faiss_path = os.path.join(idx_dir, 'index.faiss')
        meta_path = os.path.join(idx_dir, 'meta.json')

        vi = VectorIndex(faiss_path, meta_path)
        # Use chunks only for vector indexing, but you still have full_text stored in Document
        chunks = chunk_text(full_text)
        vi.build(chunks)

        doc.faiss_path, doc.meta_path = faiss_path, meta_path
        doc.save()

        return Response(DocumentSerializer(doc).data, status=201)



class ListDocsView(generics.ListAPIView):
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Document.objects.filter(owner=self.request.user).order_by('-created_at')


class AskView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, doc_id: int):
        question = request.data.get('question', '').strip()
        if not question:
            return Response({'error': 'Empty question'}, status=400)
        
        doc = get_object_or_404(Document, id=doc_id)
        if doc.owner_id != request.user.id:
            return Response({'detail': 'Not found.'}, status=404)

        # Load vector index
        vi = VectorIndex(doc.faiss_path, doc.meta_path).load()
        hits = vi.search(question, k=5)  # list of dicts

        # Ensure hits are in expected format
        if not hits:
            # fallback: wrap full doc text in a single chunk dict
            hits = [{'chunk': doc.text}]

        mc = ModelClient()
        answer = mc.answer(hits, question)

        # Ensure non-empty
        if not answer.strip():
            answer = "Cannot find answer."


        # Save QA
        qa = QA.objects.create(document=doc, question=question, answer=answer, top_chunks=hits)

        return Response(QASerializer(qa).data)


class DocFileView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, doc_id: int):
        doc = get_object_or_404(Document, id=doc_id)
        if doc.owner_id != request.user.id:
            return Response({'detail': 'Not found.'}, status=404)
        return FileResponse(open(os.path.join(settings.MEDIA_ROOT, str(doc.file)), 'rb'))
