from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Max, Min
from django.core.paginator import Paginator
import markdown

from blogmes.models import Specific_Post, Tag, Category

# Create your views here.
# 创建全局变量,记录当前博客页面的页数
index_page = None

def index(request, pindex):
    '''首页视图'''
    # 使用全局变量
    global index_page
    # 判断是否存在get请求cg(category - 推荐)变量参数
    if request.GET.get('cg'):
        # 获取参数中推荐类别的id
        category_id = int(request.GET.get('cg'))
        # 如果id值为0,展示默认首席推荐
        if category_id == 0:
            recommend_posts = Specific_Post.objects.order_by('-read')
        else:
            # 从数据库中查询该条件的文章内容
            category = Category.objects.get(id = category_id)
            recommend_posts = category.specific_post_set.all()
        # 还是用当前页面的也说,不重新加载页数(默认为 1)
        pindex = index_page
    # 为正常请求index页面
    else:
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
        # 正常查询推荐文章
        recommend_posts = Specific_Post.objects.order_by('-read')
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
    mes = {'page': page, 'Ranking_posts': Ranking_posts,'recommend_posts': recommend_posts, 'categorys': categorys}
    return render(request, 'index.html', mes)

def particulars(request):
    '''详情页视图'''
    # 判断请求是否为get请求
    if request.method == "GET":
        # 查询要访问的详情id
        id = request.GET.get('id')
        # 根据id查询数据库数据
        post = Specific_Post.objects.get(id=id)
        post.content = markdown.markdown(post.content,
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc',
                                  ])
        # 查询数据库该模型类的最大值
        max_id = Specific_Post.objects.aggregate(Max('id'))
        # 查询数据库该模型类的最小值
        min_id = Specific_Post.objects.aggregate(Min('id'))
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
        return render(request, 'tag_list.html', mes)

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
        return render(request, 'category_list.html', mes)


def text1(request):
    category = Category.objects.get(name="科技")
    posts = category.post_set.all()
    print('----->', posts)
    return render(request,'text.html', {'mes': '000'})

def text2(request):
    mes = request.GET.get('mes') + 'lalala'
    return JsonResponse({'mes': mes})

