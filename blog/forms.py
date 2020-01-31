from django import forms #импортируем класс forms
from .models import Comments





class EmailPostForm(forms.Form): 
    name = forms.CharField(max_length=25) # текстовое поле имя 
    email = forms.EmailField() #поле с мылом отправителя
    to = forms.EmailField() # поле с мылом получателя
    comments = forms.CharField(required=False, widget=forms.Textarea) #поле с комментарием по необходимости (не обязательное поле)


class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('name', 'email', 'body')

