from django.db import models
from django.utils import timezone #импортируем модуль для отображения времени прямо сейчас
from django.contrib.auth.models import User #импортируем модель для определения автора(зарегистрировавшихся пользователей)
from django.urls import reverse #импортируем функцию формирования URL постов
# Create your models here.
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')


class Post(models.Model):
    STATUS_CHOICES =( #tuple с вариантами, Опубликован пост или Не опубликован
        ('draft', 'Draft'),
        ('published', 'Published')
    )
    title = models.CharField(max_length=250, verbose_name='Заголовок')
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts') #поле определя автора из зарегистрированных пользователей
    publish = models.DateTimeField(default=timezone.now) #
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    objects = models.Manager()
    published = PublishedManager()
    tags = TaggableManager()

    class Meta: #класс для отображения статей с фильтром (сначала новые)
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ('-publish',)

    def __str__(self):
        return self.title #Корректное отображение названия модели

    def get_absolute_url(self): #формирование URL для страницы поста
        return reverse('blog:post_detail', args=[self.publish.year, #формируем через функцию reverse
            self.publish.month, self.publish.day, self.slug]) #аргументами являются название приложения : вьюха отображения args=[обращаемся через поле publish к необходимым полям для формирования URl]
    
    

class Comments(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=50)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Комментарии'
        verbose_name_plural = 'Комментарии'
        ordering = ('created', )

    def __str__(self):
        return 'Comment by {} on '.format(self.name, self.post)
    


    