# core/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, FileResponse
from django.utils import timezone
from django.conf import settings
from .models import FileShare, URLShare
from django.views.decorators.csrf import csrf_exempt
import os


def home(request):
    # return render(request, "home.html")
    return render(request, "frontend/home.html")


@csrf_exempt
def upload_file(request):
    if request.method == "POST":
        f = request.FILES.get("file")
        # simple max size enforcement (25 MB)
        MAX_UPLOAD = 25 * 1024 * 1024
        if not f:
            return render(request,
                          "frontend/upload_result.html",
                          {"error": "No file uploaded."})
        if f.size > MAX_UPLOAD:
            return render(request, "frontend/upload_result.html",
                          {"error": "File too large (max 25MB)."})
        fs = FileShare.objects.create(file=f)
        link = request.build_absolute_uri(f"/f/{fs.token}/")
        return render(request, "frontend/upload_result.html", {"link": link})
    return redirect("/")


@csrf_exempt
def submit_url(request):
    if request.method == "POST":
        url = request.POST.get("url")
        if not url:
            return render(request,
                          "frontend/url_result.html",
                          {"error": "No URL provided."})
        us = URLShare.objects.create(original_url=url)
        link = request.build_absolute_uri(f"/u/{us.token}/")
        return render(request, "frontend/url_result.html", {"link": link})
    return redirect("/")


def serve_file(request, token):
    fs = get_object_or_404(FileShare, token=token)
    if fs.is_expired() or not fs.file:
        return render(request, "frontend/expired.html")
    # Serve via FileResponse (efficient)
    file_path = fs.file.path
    if not os.path.exists(file_path):
        # file missing; treat as expired
        return render(request, "frontend/expired.html")
    response = FileResponse(
        open(
            file_path,
            "rb"),
        as_attachment=True,
        filename=os.path.basename(file_path))
    return response


def redirect_url(request, token):
    us = get_object_or_404(URLShare, token=token)
    if us.is_expired():
        return render(request, "frontend/expired.html")
    return redirect(us.original_url)
