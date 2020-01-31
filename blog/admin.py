from django.contrib import admin
from .models import *
# Register your models here.




@admin.register(Post) #декоратор для регистрации модели 
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status') #отображение полей модели в админке
    list_filter = ('status', 'created', 'publish', 'author') #фильтрация полей модели
    search_fields = ('title', 'body') #поля по которым можно выполнять поиск
    prepopulated_fields = {'slug': ('title', )} #формирование слага из названия поста
    raw_id_fields = ('author', ) #содержит список полей
    date_hierarchy = 'publish' # фильтр по дате публикации
    ordering = ('status', 'publish') #сортировка по статусу и публикации
    




@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('name', 'post', 'email', 'created',)
    list_filter = ('active', 'created', 'updated')
    search_fields = ('body', 'name', 'post')
    

