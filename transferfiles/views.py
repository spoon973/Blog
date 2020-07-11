import re
from django.shortcuts import render
from django.utils.encoding import escape_uri_path

from transferfiles.models import FileStore, Category
from django.http import FileResponse

# Create your views here.

def show(request, file_category):
    category = Category.objects.get(name=file_category)
    files = category.filestore_set.all()
    return render(request, 'transferfiles/files_show.html', {'files': files})

def download(request):
    file_url = request.GET.get('file_url')
    print('--------->', file_url)
    file_name = re.match("[^/]+(/[^ ]*)", file_url).group(1)[1:].encode('utf-8')
    file_name = file_name.decode('utf-8')

    file = open("uploads/" + file_url, 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{}"'.format(escape_uri_path(file_name))
    return response