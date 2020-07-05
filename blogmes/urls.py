from django.urls import path, re_path, include
from blogmes import views

app_name = 'blogmes'

urlpatterns = [
    re_path('index(?P<pindex>\d*)$', views.index, name='index'),  # 首页视图的url路径
    path('recommend', views.recommend, name='recommend'),  # 类别名称视图

    path('post', views.particulars, name='particulars'),  # 详情页视图
    path('category',views.category, name='category'),  # 类别访问路径
    path('tag', views.tag, name='tag'),  # 标签访问路径

    path('text1', views.text1, name='text'),  # 测试
    path('text2', views.text2, name='text'),  # 测试
]