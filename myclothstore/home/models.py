from django.db import models
import uuid
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

# Create your models here.
class Basemodel(models.Model):
    uid = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

class Category(Basemodel):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class SubCategory(Basemodel):
    name = models.CharField(max_length=150)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Product(Basemodel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default='')
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE,default='',related_name='subcategory')
    image = models.ImageField(upload_to='product/img')
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.name


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
            raise forms.ValidationError(self.fields['email'].error_message['exists'])
        
        return self.cleaned_data['email']
