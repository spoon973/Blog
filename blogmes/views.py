from django.http import HttpResponse,JsonResponse
from django.shortcuts import render
from django.db.models import Max,Min
from django.core import serializers
from django.core.paginator import Paginator
from blogmes.models import Post, Tag, Category

# Create your views here.

def index(request, pindex, category_recommend=None):
    '''首页视图'''
    # 按阅读量做排行,查询出由多到少的文章,作为推荐文章
    recommend_posts = Post.objects.order_by('-read')
    # 查询出后台所有文章信息
    new_posts = Post.objects.order_by('-create_time')
    # 获取所有分类
    categorys = Category.objects.all()
    # 分页，每页显示7条信息
    paginator = Paginator(new_posts, 7)
    # 获取请求中的pindex信息
    try:  # 如果pindex为触发异常,except捕获异常
        # 获取index页面的内容
        pindex = int(pindex)
    except:
        # 默认pindex为首页
        pindex = 1
    page =paginator.page(pindex)
    # 创建变量，保存返回页面的数据
    mes = {'page': page, 'recommend_posts': recommend_posts, 'categorys': categorys}

    return render(request, 'index.html', mes)

def recommend(request):
    '''推荐类别视图'''
    recommend_name = request.GET.get('recommend_name')
    recommend_name = "".join(recommend_name.split())
    # print(len(recommend_name))
    category = Category.objects.get(name=recommend_name)
    posts = category.post_set.all()

    # index(category_recommend=posts)

    posts = serializers.serialize("json",category.post_set.all())
    return JsonResponse({'posts': posts})

def particulars(request):
    '''详情页视图'''
    # 判断请求是否为get请求
    if request.method == "GET":
        # 查询要访问的详情id
        id = request.GET.get('id')
        # 根据id查询数据库数据
        post = Post.objects.get(id=id)
        # 查询数据库该模型类的最大值
        max_id = Post.objects.aggregate(Max('id'))
        # 查询数据库该模型类的最小值
        min_id = Post.objects.aggregate(Min('id'))
        # 创建变量保存返给页面的数据
        mes = {'post': post, 'max_id': max_id, 'min_id': min_id}
        return render(request, 'info.html', mes)

def tag(request):
    '''标签视图'''
    # 获取get请求中的id参数
    if request.method == "GET":
        # 获取get请求中参数的值
        tag_id = request.GET.get('id')
        # 通过传过来的标签id值查询到标签模型中的对象
        tag = Tag.objects.get(id=tag_id)
        # 查询对应的类别
        category = tag.category
        # 查询对应的文章
        posts = tag.post_set.all()
        # 创建mes字典，存放返回html的数据
        mes = {}
        # 判断category类别是否为空
        if category != None:
            mes['category'] = category
        # 向mes字典增添数据
        mes['posts'] = posts
        mes['tag'] = tag
        # 返回页面
        print('---------->', mes)
        return render(request, 'tag_list.html', mes)

def category(request):
    '''标签视图'''
    # 获取get请求中的id参数
    if request.method == "GET":
        # 获取get请求中参数的值
        category_id = request.GET.get('id')
        # 通过传过来的标签id值查询到标签模型中的对象
        category = Category.objects.get(id=category_id)
        # 查询对应的标签
        tags = category.tag_set.all()
        # 查询对应的文章
        posts = category.post_set.all()
        mes = {'category': category, 'tags': tags, 'posts': posts}
        return render(request, 'category_list.html', mes)

def text1(request):
    category = Category.objects.get(name="科技")
    posts = category.post_set.all()
    print('----->', posts)
    return render(request,'text.html')

def text2(request):
    mes = request.GET.get('mes') + 'lalala'
    return JsonResponse({'mes': mes})

