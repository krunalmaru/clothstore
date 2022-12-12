from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


class UsercreateForm(UserCreationForm):

    email = forms.EmailField(required=True, label='Email', error_messages={'exists':'This is Already Exist'})

    class Meta:
        model = User
        fields = ('username', 'email', 'password1','password2')
    
    def __init__(self, *args,**kwargs):
        super(UsercreateForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'


    def save(self, commit=True):
        user =super(UsercreateForm,self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    
    def clean_email(self):
        if User.objects.filter(email = self.cleaned_data['email']).exists():
            raise forms.ValidationError('Email Already Register')
        return self.cleaned_data['email']