from django.urls import path, re_path, include
from blogmes import views

app_name = 'blogmes'

urlpatterns = [
    path('', views.index, name='index'),
    path('index_category', views.index_category),
    re_path('banner/(?P<bindex>\d*)$',views.banner, name='banner'),
    path('post', views.particulars, name='particulars'),  # 详情页视图
    path('category',views.category, name='category'),  # 类别访问路径
    path('tag', views.tag, name='tag'),  # 标签访问路径
    path('knowledge', views.knowledge, name='text')

]

