from django.shortcuts import render, get_object_or_404
from .models import *
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView #импорт класса для отображения списка объектов (постов) со встроенным пагинатором
from .forms import EmailPostForm #импортируем форму из файла forms.py 
from django.core.mail import send_mail #импортируем функцию отправки сообщения на почту


# def post_list(request):
#     object_list = Post.published.all()
#     paginator = Paginator(object_list, 1)
#     page = request.GET.get('page')
#     try:
#         posts = paginator.page(page)
#     except PageNotAnInteger:
#         posts = paginator.page(1)
#     except EmptyPage:
#         posts = paginator.page(paginator.num_pages)
#     return render(request, 'blog/post/post_list.html', {'page': page, 'posts': posts})




def post_detail(request, year, month, day, post): #вьюха отображения страницы поста
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year, publish__month=month, publish__day=day) #обозначаем переменную получающую опубликованный пост из модели Post, атрибуты прнимают значения года месяца и дня для фильтрации и формирования URL поста
    return render(request, 'blog/post/post_detail.html', {'post': post}) #возвращает данные определенного поста и отображает в шаблоне html


class PostListView(ListView): #класс для вывода всех опубликованных постов из модели Post  
    queryset = Post.published.all() #получаем все посты через queryset запрос
    context_object_name = 'posts' #обозначаем контекст для последующей итерации в шаблоне
    paginate_by = 1 # устанавливаем колличество постов на 1 странице для реализации пагинации
    template_name = 'blog/post/post_list.html' #называем шаблон в который будем выводить полученные данные



# def post_share(request, post_id):
#     post = get_object_or_404(Post, id=post_id, status='published')
#     sent = False
#     if request.method == 'POST':
#         form = EmailPostForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             post_url = request.build_absolute_uri(request.get_absolute_url())
#             subject = '{} ({}) рекомендую прочитать "{}"'.format(cd['name'], cd['email'], post.title)
#             message = 'Read "{}" at {} \n\n {}\, {}'.format(post.title, post_url, cd['name'], cd['comments'])
#             send_mail(subject, message, 'uxui.des@gmail.com', [cd['to']])
#             sent = True
#         else:
#             form = EmailPostForm()
#             return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})



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
            send_mail(subject, message, 'admin@myblog.com', [cd['to']]) #отправка сообщения обязательные аргумент : тема, тело, мыло отправителя , кому отправляется 
            sent = True #перезаписываем переменную при успешной отправке
            return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent}) #выводим сообщение об успешно отправке Email

    else:
        form = EmailPostForm() 
        return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})#выводим форму с указанием ошибок для исправления