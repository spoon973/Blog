from django.urls import path,re_path
from transferfiles import views

app_name = "transferfiles"

urlpatterns = [
    re_path('(?P<file_category>[a-z]+)', views.show, name="show"),  # 资料文件列表页视图
    path('7', views.download, name='Download'),  # 资料下载视图
]