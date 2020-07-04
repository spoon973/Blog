from django.contrib import admin
from blogmes.models import *
# Register your models here.

admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Category)