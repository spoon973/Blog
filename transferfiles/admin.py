from django.contrib import admin
from transferfiles.models import Category,FileStore

# Register your models here.

admin.site.register(Category)
admin.site.register(FileStore)
