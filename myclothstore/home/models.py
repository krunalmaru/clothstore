from django.db import models
import uuid
from django.contrib.auth.models import User
import datetime
from django.core.exceptions import ValidationError

# Create your models here.
class Basemodel(models.Model):
    uid = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

class Category(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class SubCategory(models.Model):
    name = models.CharField(max_length=150)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.name

class Product(models.Model):
    Availability = (('In Stock','In stock'),('Out Of Stoke','Out Of Stoke'))
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default='')
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE,default='',related_name='subcategory')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='product/img')
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    availability = models.CharField(choices=Availability, null=True, max_length=100)
    description = models.TextField(null=True)
    date = models.DateField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.name



class Contact_us(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField()

    def __str__(self) -> str:
        return self.email
    
class Order(models.Model):
    image = models.ImageField(upload_to='product/order')
    product = models.CharField(max_length=100, default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.CharField(max_length=5)
    total = models.CharField(max_length=10, default='')
    address = models.TextField()
    mobile = models.CharField(max_length=18)
    pincode = models.CharField(max_length=10)
    date = models.DateField(default=datetime.datetime.today)

    def __str__(self) -> str:
        return self.user.username