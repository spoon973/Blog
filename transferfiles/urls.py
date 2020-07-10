from django.urls import path,re_path
from transferfiles import views

app_name = "transferfiles"

urlpatterns = [
    path('', views.index, name='index'),  # 框架页视图
    path('show', views.show, name="show"),  # 资料文件列表页视图
    path('download',views.download, name='download'),  # 资料下载视图

    path('text', views.text, name='text'),
    path('text1', views.text1, name='text1'),
]