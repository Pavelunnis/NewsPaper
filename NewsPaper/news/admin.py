from django.contrib import admin
from .models import Category, Post
# Register your models here.



# создаём новый класс для представления товаров в админке
class PostAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    list_display = ('heading', 'timeCreate')
    # полей для более красивого отображения
    list_filter = ('heading','timeCreate')
    search_fields = ('heading', 'timeCreate')

admin.site.register(Category)
admin.site.register(Post, PostAdmin)