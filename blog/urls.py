from django.urls import path
from . import views
app_name = 'blog' #имя приложения

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('', views.PostListView.as_view(), name='post_list'),
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
     #URL страницы отображения всех постов
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'), 
    #формируем URL страницы поста 
    path('<int:post_id>/share/', views.post_share, name='post_share') 
    #формируем URl для поста которым нужно поделиться
]
