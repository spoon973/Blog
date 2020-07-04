from django.urls import path,include
from blogmes import views

app_name = 'blogmes'

urlpatterns = [
    path('index', views.index, name='index'),  # 首页视图的url路径
    path('post', views.particulars, name="particulars"),  # 详情页视图
    path('category',views.category, name='category'),  # 类别访问路径
    path('tag', views.tag, name="tag"),  # 标签访问路径
    path('about', views.about, name="about") # 测试
]