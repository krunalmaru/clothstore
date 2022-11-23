from django.contrib import admin
from .models import Category, SubCategory,Product, Order,Contact_us
# Register your models here.
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Contact_us)
