import re
from django.shortcuts import render
from transferfiles.models import FileStore
from django.http import FileResponse

# Create your views here.

def index(request):
    return render(request, 'transferfiles/index.html')

def show(request):
    files = FileStore.objects.all()
    return render(request, 'transferfiles/files_show.html', {'files': files})

def download(request):
    file_url = request.GET.get('file_url')
    print(file_url)
    file_name = re.match("[^/]+(/[^ ]*)",file_url).group(1)[1:]
    file = open("uploads/" + file_url, 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{}"'.format(file_name)
    return response