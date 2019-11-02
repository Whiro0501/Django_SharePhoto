from django.forms import ModelForm
from .models import Photo, Contact
from django import forms
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User

class PhotoForm(ModelForm):
    class Meta:
        model = Photo
        fields = ['title', 'comment', 'image', 'category']


class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = ['title', 'name', 'email', 'content']

class UserUpdateForm(forms.ModelForm):
    """ユーザー情報更新フォーム"""

    class Meta:
        model = User
        fields = ('username', 'last_name', 'first_name', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class MyPasswordChangeForm(PasswordChangeForm):
    """パスワード変更フォーム"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


    # name = forms.CharField() # 名前
    # message = forms.CharField(widget=forms.Textarea) #問い合わせ内容
    #
    # # メール送信処理
    # def send_email(self):
    #     # send email using the self.cleaned_data dictionary
    #     subject = self.cleaned_data['name']
    #     message = self.cleaned_data['message']
    #     from_email = settings.EMAIL_BACKEND
    #     #to = [settings.EMAIL_BACKEND
    #
    #     send_mail(subject, message, from_email, to )