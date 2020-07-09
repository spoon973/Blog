from django.db import models
from blogmes.models import Category
# Create your models here.

class FileStore(models.Model):
    '''存储文件类'''
    # 文件名
    name = models.CharField(verbose_name="文件名", max_length=100)
    # 关联字段
    category = models.ForeignKey(to=Category, verbose_name='类别', on_delete=models.CASCADE, null=True, blank=True)
    # 文件主题
    file = models.FileField(verbose_name="文件", upload_to='File')

    # 内置可重写函数
    def __str__(self):
        return self.name
    class Meta:
        db_table = "FileStore"
        # 给模型类起一个更可读的中文名
        verbose_name = '文件存储'
        # 指定模型的复数形式
        verbose_name_plural = verbose_name