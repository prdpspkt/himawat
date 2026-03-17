from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
import uuid


@require_http_methods(["POST"])
@csrf_exempt
def media_upload(request):
    """
    Handle media file uploads for TinyMCE editor.
    Accepts file uploads and returns the URL to the uploaded file.
    """
    if 'file' not in request.FILES:
        return JsonResponse({'error': 'No file provided'}, status=400)

    file = request.FILES['file']

    # Validate file type (images only)
    allowed_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg'}
    file_ext = os.path.splitext(file.name)[1].lower()

    if file_ext not in allowed_extensions:
        return JsonResponse({'error': 'Invalid file type. Only images are allowed.'}, status=400)

    # Generate unique filename
    filename = f"{uuid.uuid4().hex}{file_ext}"

    # Save file to media uploads directory
    upload_path = os.path.join('uploads', 'editor', filename)

    # Save the file
    saved_path = default_storage.save(upload_path, ContentFile(file.read()))
    file_url = default_storage.url(saved_path)

    return JsonResponse({
        'location': file_url,
        'filename': filename
    })
