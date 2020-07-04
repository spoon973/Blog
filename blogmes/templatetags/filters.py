# 自定义过滤器

# 导入Library类
from django.template import Library
from blogmes.models import *
# 创建一个Library类对象
register = Library()

# 使用装饰器进行注册
@register.filter
def title_last(id):
    '''当前id的上一条数据信息'''
    post = Post.objects.get(id=id-1)
    return post.title

@register.filter
def title_next(id):
    '''当前id的下一条数据信息'''
    post = Post.objects.get(id=id+1)
    return post.title

