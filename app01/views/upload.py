import os

from django.conf import settings
from django.shortcuts import render, redirect


def upload_list(request):
    if request.method == "GET":
        return render(request, 'upload.html')
    else:
        file_obj = request.FILES.get("avatar")
        media_path = os.path.join('media', file_obj.name)
        f = open(media_path, mode='wb')
        for chunk in file_obj.chunks():
            f.write(chunk)
        f.close()
        return redirect('/upload/list/')
