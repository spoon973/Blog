from django.db import models
# Create your models here.

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
        db_table = 'FileCategory'
        # 给模型类起一个更可读的中文名
        verbose_name = '分类'
        # 指定模型的复数形式
        verbose_name_plural = verbose_name

class FileStore(models.Model):
    '''存储文件类'''
    TYPE = (
        ('Z', 'zip'),
        ('T', 'txt'),
        ('PT', 'ppt'),
        ('PF', 'pdf'),
        ('W', 'word'),
        ('H', 'html'),
        ('O', 'other'),
        ('E', 'excel'),
        ('M', 'markdown'),
    )
    # 文件名
    name = models.CharField(verbose_name="文件名", max_length=100)
    # 关联字段(文件内容分类)
    category = models.ForeignKey('Category', verbose_name='内容类别', on_delete=models.CASCADE, null=False, blank=False)
    # 文件主题
    file = models.FileField(verbose_name="文件", upload_to='File')
    # 文件本身分类
    floader_cate = models.CharField(verbose_name="文件类别", max_length=2, choices=TYPE, default='O')

    # 内置可重写函数
    def __str__(self):
        return self.name
    class Meta:
        db_table = "FileStore"
        # 给模型类起一个更可读的中文名
        verbose_name = '文件存储'
        # 指定模型的复数形式
        verbose_name_plural = verbose_name