# core/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import FileResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.conf import settings
from .models import FileShare, URLShare
import os
import mimetypes


def home(request):
    return render(request, "home.html")


@csrf_exempt
def upload_file(request):
    if request.method == "POST":
        f = request.FILES.get("file")

        MAX_UPLOAD = 25 * 1024 * 1024  # 25 MB
        if not f:
            return render(request, "upload_result.html", {"error": "No file uploaded."})
        if f.size > MAX_UPLOAD:
            return render(request, "upload_result.html", {"error": "File too large (max 25MB)."})
        
        fs = FileShare.objects.create(file=f)
        link = request.build_absolute_uri(f"/f/{fs.token}/")
        return render(request, "upload_result.html", {"link": link})

    return redirect("/")


@csrf_exempt
def submit_url(request):
    if request.method == "POST":
        url = request.POST.get("url")
        if not url:
            return render(request, "url_result.html", {"error": "No URL provided."})
        
        us = URLShare.objects.create(original_url=url)
        link = request.build_absolute_uri(f"/u/{us.token}/")
        return render(request, "url_result.html", {"link": link})

    return redirect("/")


def serve_file(request, token):
    fs = get_object_or_404(FileShare, token=token)

    if fs.is_expired() or not fs.file:
        return render(request, "expired.html")

    file_path = fs.file.path
    if not os.path.exists(file_path):
        return render(request, "expired.html")

    mime_type, _ = mimetypes.guess_type(file_path)

    try:
        # Open file inline (not forced download)
        response = FileResponse(open(file_path, "rb"), content_type=mime_type or "application/octet-stream")
        response["Content-Disposition"] = f'inline; filename="{os.path.basename(file_path)}"'
        return response
    except FileNotFoundError:
        raise Http404("File not found.")


def redirect_url(request, token):
    us = get_object_or_404(URLShare, token=token)
    if us.is_expired():
        return render(request, "expired.html")
    
    # Currently redirects instantly
    return redirect(us.original_url)
