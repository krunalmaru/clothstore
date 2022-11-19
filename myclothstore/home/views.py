from django.shortcuts import render
from home.models import Category,SubCategory,Product
# Create your views here.
def home(request):
    category = Category.objects.all()
    categoryId = request.GET.get('category')
    if categoryId:
        product = Product.objects.filter(subcategory=categoryId).order_by('-uid')
    else:
        product = Product.objects.all()
    context = {'category':category,'product':product}
    return render(request, 'home/index.html', context)