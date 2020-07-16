import markdown
from django.db import models
from django.utils import timezone
from mdeditor.fields import MDTextField
from django.utils.html import strip_tags
from django.contrib.auth.models import User

class Post(models.Model):
    '''抽象文章类'''
    #  标题
    title = models.CharField(verbose_name='标题', max_length=200)
    # 创建时间
    create_time = models.DateTimeField(verbose_name='创建时间', default=timezone.now)
    # 内容,使用富文本编辑器
    content = MDTextField(verbose_name="内容")
    # 文章作者
    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)

    class Meta:
        # 创建抽象基类
        abstract =True

class Specific_Post(Post):
    '''具体文章信息表'''
    # 浏览的次数
    read = models.IntegerField(verbose_name='浏览次数', default=0)
    # 喜欢的人数
    like = models.IntegerField(verbose_name='点赞次数', default=0)
    # 文章摘要
    excerpt = models.CharField(verbose_name='摘要', max_length=200, null=True, blank=True)
    # 创建外键关系
    # 类别类和文章类的关系是 一对多
    # 创建级联删除，当删除主表的时候从表也随着一起删除
    category = models.ForeignKey('Category', verbose_name='类别', on_delete=models.CASCADE)
    # 标签类和文章类的关系是 多对多
    tags = models.ManyToManyField('Tag', verbose_name='标签', blank=True)
    # 文章图片
    pic = models.ImageField(verbose_name='文章图片', db_column="post_pic", upload_to='blogmes')

    # 重写save方法
    def save(self, *args, **kwargs):
        # 首先实例化一个 Markdown 类，用于渲染 body 的文本。
        # 由于摘要并不需要生成文章目录，所以去掉了目录拓展。
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])

        # 先将 Markdown 文本渲染成 HTML 文本
        # strip_tags 去掉 HTML 文本的全部 HTML 标签
        # 从文本摘取前 77 个字符赋给 excerpt
        self.excerpt = strip_tags(md.convert(self.content))[:100]
        super().save(*args, **kwargs)

    # 内置可重写函数
    def __str__(self):
        return self.title
    # 创建元类
    class Meta:
        # 指定自定义数据库表名
        db_table = 'Specific_Post'
        # 给模型类起一个更可读的中文名
        verbose_name = '文章'
        # 指定模型的复数形式
        verbose_name_plural = verbose_name

class Banner_Post(Post):
    '''bannner轮播图文章'''
    # bannner轮播文章图片
    pic = models.ImageField(verbose_name='轮播图片', db_column="bannner_pic", upload_to='banner_mes')

    # 内置可重写函数
    def __str__(self):
        return self.title

    # 创建元类
    class Meta:
        # 指定自定义数据库表名
        db_table = 'Banner_Post'
        # 给模型类起一个更可读的中文名
        verbose_name = '轮播图文章'
        # 指定模型的复数形式
        verbose_name_plural = verbose_name

class Tag(models.Model):
    '''文章标签类'''
    # 标签名
    name = models.CharField(max_length=100, verbose_name="标签名", default="其他")
    # 关联字段
    category = models.ForeignKey('Category', verbose_name='分类',
                                 on_delete=models.CASCADE, null=True, blank=True)
    # 内置可重写函数
    def __str__(self):
        return self.name
    # 设置元类
    class Meta:
        # 指定自定义数据库表名
        db_table = 'Tag'
        # 给模型类起一个更可读的中文名
        verbose_name = "标签"
        # 指定模型的复数形式
        verbose_name_plural = verbose_name

class Category(models.Model):
    '''文章分类'''
    # 分类名
    name = models.CharField(max_length=200, verbose_name="类名", default="其他")
    # 内置可重写函数
    def __str__(self):
        return self.name
    # 创建元类
    class Meta:
        # 指定自定义数据库表名
        db_table = 'PostCategory'
        # 给模型类起一个更可读的中文名
        verbose_name = '分类'
        # 指定模型的复数形式
        verbose_name_plural = verbose_name

