from django import forms
from django.contrib.auth.models import User
from django import forms
from .models import Event, User, Comment

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'location', 'description', 'category', 'sub_category', 'duration', 'event_date', 'event_time', 'photo',]

    def __init__(self, *args, **kwargs):
        
        user = kwargs.get('user', None)
        super().__init__(*args, **kwargs)
        
        if self.instance and self.instance.user is None:
            self.instance.user = user


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Şifre")
    password_confirmation = forms.CharField(widget=forms.PasswordInput, label="Şifre Tekrarı")

    class Meta:
        model = User
        fields = ['username', 'password', 'email']  

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirmation = cleaned_data.get('password_confirmation')

        
        if password != password_confirmation:
            raise forms.ValidationError("Şifreler uyuşmuyor.")
        
        return cleaned_data

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [ 'username', 'password', 'email', 'location', 'interests', 'first_name', 'last_name',  'birth_date','gender','phone_number','profile_picture']
        exclude=['password','username']


 

    def clean_password_confirm(self):
        password = self.cleaned_data.get("password")
        password_confirm = self.cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Password and confirmation do not match.")
        return password_confirm



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']  
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': 'Yorumunuzu buraya yazın...', 'rows': 4, 'cols': 50}),
        }


