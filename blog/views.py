from django.shortcuts import render, get_object_or_404
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView #импорт класса для отображения списка объектов (постов) со встроенным пагинатором
from .forms import EmailPostForm, CommentsForm #импортируем форму из файла forms.py 
from django.core.mail import send_mail #импортируем функцию отправки сообщения на почту
from taggit.models import Tag
from django.db.models import Count






def post_detail(request, year, month, day, post): #вьюха отображения страницы поста
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year, publish__month=month, publish__day=day) #обозначаем переменную получающую опубликованный пост из модели Post, атрибуты прнимают значения года месяца и дня для фильтрации и формирования URL поста
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentsForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
        return render(request, 'blog/post/post_detail.html', {'post' : post, 'new_comment' : new_comment, 'comments' : comments, 'comment_form' :  comment_form})
    else:
        comment_form = CommentsForm()
    
    post_tag_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tag_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
    context = {
        'post' : post,
        'new_comment' : new_comment,
        'comments' : comments,
        'comment_form' :  comment_form,
        'similar_posts' : similar_posts
        }
    return render(request, 'blog/post/post_detail.html', context) #возвращает данные определенного поста и отображает в шаблоне html




def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/post_list.html', {'page': page, 'posts': posts, 'tag' : tag})




class PostListView(ListView): #класс для вывода всех опубликованных постов из модели Post  
    queryset = Post.published.all() #получаем все посты через queryset запрос
    context_object_name = 'posts' #обозначаем контекст для последующей итерации в шаблоне
    paginate_by = 1 # устанавливаем колличество постов на 1 странице для реализации пагинации
    template_name = 'blog/post/post_list.html' #называем шаблон в который будем выводить полученные данные




def post_share(request, post_id): #функция отправки поста на почту

    post = get_object_or_404(Post, id=post_id,status='published')# Получение статьи по идентификатору.
    sent = False #переменная с исходным значением False для последующей реализации отображения в шаблоне успешной отправки
    if request.method == 'POST': #проверка метода запроса

        form = EmailPostForm(request.POST) # инициализируем экземпляр класса EmailPostForm() 
        if form.is_valid():
            # Если Все поля формы прошли валидацию выполняем отправку.
            cd = form.cleaned_data #метод clean_data возвращает словарь с данными из формы
            # Отправка электронной почты.
            post_url = request.build_absolute_uri(post.get_absolute_url()) # формируем полный URL адрес поста
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title) # Тема сообщения
            message = 'Read "{}" at {}\n\n{}\'s comments:{}'.format(post.title, post_url, cd['name'], cd['comments']) # Тело сообщения
            send_mail(subject, message, 'uxui.des@gmail.com', [cd['to']]) #отправка сообщения обязательные аргумент : тема, тело, мыло отправителя , кому отправляется 
            sent = True #перезаписываем переменную при успешной отправке
            return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent}) #выводим сообщение об успешно отправке Email
    else:
        form = EmailPostForm() 
        return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})#выводим форму с указанием ошибок для исправления