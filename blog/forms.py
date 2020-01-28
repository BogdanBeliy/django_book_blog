from django import forms #импортируем класс forms


class EmailPostForm(forms.Form): 
    name = forms.CharField(max_length=25) # текстовое поле имя 
    email = forms.EmailField() #поле с мылом отправителя
    to = forms.EmailField() # поле с мылом получателя
    comments = forms.CharField(required=False, widget=forms.Textarea) #поле с комментарием по необходимости (не обязательное поле)