from django.db import models
from django.utils import timezone #импортируем модуль для отображения времени прямо сейчас
from django.contrib.auth.models import User #импортируем модель для определения автора(зарегистрировавшихся пользователей)
from django.urls import reverse #импортируем функцию формирования URL постов
# Create your models here.


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

    class Meta: #класс для отображения статей с фильтром (сначала новые)
        ordering = ('-publish',)

    def __str__(self):
        return self.title #Корректное отображение названия модели

    def get_absolute_url(self): #формирование URL для страницы поста
        return reverse('blog:post_detail', args=[self.publish.year, #формируем через функцию reverse
            self.publish.month, self.publish.day, self.slug]) #аргументами являются название приложения : вьюха отображения args=[обращаемся через поле publish к необходимым полям для формирования URl]
    
    

