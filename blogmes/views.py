from django.http import JsonResponse, HttpResponse
from django.shortcuts import render,redirect
from django.db.models import Max, Min
from django.core.paginator import Paginator
from transferfiles.models import Category as TransferFileCategory
import markdown

from blogmes.models import Specific_Post, Tag, Category, Banner_Post

# Create your views here.
# 创建全局变量,记录当前博客页面的页数
index_page = None
cookie_count = 0

def index(request, pindex=None):
    '''首页视图'''
    # 使用全局变量
    global index_page
    global session_count
    # 获取请求中的pindex信息
    try:  # 如果pindex为触发异常,except捕获异常
        # 获取index页面的内容
        pindex = int(pindex)
        # 将当前页面的值赋值给全局变量,以备推荐路径使用
        index_page = pindex
    except:
        # 默认pindex为首页
        pindex = 1
        index_page = pindex

    category_name = request.session.get('category_name', "首席推荐")

    print('------>', category_name)

    if category_name == "首席推荐":
        # 正常查询推荐文章
        recommend_posts = Specific_Post.objects.order_by('-read')
    else:
        try:
            category = Category.objects.get(name=category_name)
            recommend_posts = category.specific_post_set.order_by('-read')
        except:
            recommend_posts = Specific_Post.objects.order_by('-read')
            print("----->" + "数据库查询报错!!!")
    # 查询出轮播图的文章前3篇
    ban_posts = Banner_Post.objects.order_by('-create_time')[:3]
    # 查询出后台所有文章信息
    new_posts = Specific_Post.objects.order_by('-create_time')
    # 获取所有分类
    categorys = Category.objects.all()
    # 获取排行榜文章
    Ranking_posts = Specific_Post.objects.order_by('-read')
    # 分页，每页显示7条信息
    paginator = Paginator(new_posts, 7)
    # 获取当前页面的对象
    page =paginator.page(pindex)
    # 创建变量，保存返回页面的数据
    mes = {'page': page,  # 分页
           'Ranking_posts': Ranking_posts,  # 排行
           'recommend_posts': recommend_posts,  # 分类展示文章
           'categorys': categorys,  # 所有分类对象
           'ban_posts': ban_posts}  # 轮播图文章
    return render(request, 'blogmes/index.html', mes)

def index_category(request):
    global cookie_count
    # 声明全局变量
    # 获取ajax中category_name参数的内容
    category_name = request.GET.get('category_name')
    category_name = "".join(category_name.split())
    try:
        # 清除seesion信息
        request.session.clear()
    except:
        pass
    response = redirect('/index')
    response.set_cookie('cookie_count', cookie_count)
    cookie_count += 1
    # 设置session信息
    request.session['category_name'] = category_name
    # 设置session关闭窗口及删除
    # request.session.set_expiry(0)
    return response

def banner(request, bindex):
    '''轮播图视图处理'''
    # 根据获取的轮播图id,向后台数据库查询数据
    ban_post = Banner_Post.objects.get(id=bindex)
    ban_post.content = markdown.markdown(ban_post.content.replace("\r\n", '  \n'),
                                     extensions=[
                                         'markdown.extensions.extra',
                                         'markdown.extensions.codehilite',
                                         'markdown.extensions.toc',
                                     ], safe_mode=True, enable_attributes=False)
    return render(request, 'blogmes/banner_post.html', {'ban_post': ban_post})

def particulars(request):
    '''详情页视图'''
    # 判断请求是否为get请求
    if request.method == "GET":
        # 查询要访问的详情id
        id = request.GET.get('id')
        # 根据id查询数据库数据
        post = Specific_Post.objects.get(id=id)
        post.content = markdown.markdown(post.content.replace("\r\n", '  \n'),
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc',
                                  ],safe_mode=True,enable_attributes=False)
        # 查询数据库该模型类的最大值
        max_id = Specific_Post.objects.aggregate(Max('id'))
        # 查询数据库该模型类的最小值
        min_id = Specific_Post.objects.aggregate(Min('id'))
        # 创建变量保存返给页面的数据
        mes = {'post': post, 'max_id': max_id, 'min_id': min_id}
        return render(request, 'blogmes/post_info.html', mes)

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
        posts = tag.specific_post_set.all()
        # 创建mes字典，存放返回html的数据
        mes = {}
        # 判断category类别是否为空
        if category != None:
            mes['category'] = category
        # 向mes字典增添数据
        mes['posts'] = posts
        mes['tag'] = tag
        # 返回页面
        return render(request, 'blogmes/tag_list.html', mes)

def category(request):
    '''分类视图'''
    # 获取get请求中的id参数
    if request.method == "GET":
        # 获取get请求中参数的值
        category_id = request.GET.get('id')
        # 通过传过来的标签id值查询到标签模型中的对象
        category = Category.objects.get(id=category_id)
        # 查询对应的标签
        tags = category.tag_set.all()
        # 查询对应的文章
        posts = category.specific_post_set.all()
        mes = {'category': category, 'tags': tags, 'posts': posts}
        return render(request, 'blogmes/category_list.html', mes)


