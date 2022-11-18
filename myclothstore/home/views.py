from django.shortcuts import render
from home.models import Category,SubCategory
# Create your views here.
def home(request):
    category = Category.objects.all()
    context = {'category':category}
    return render(request, 'home/index.html', context)