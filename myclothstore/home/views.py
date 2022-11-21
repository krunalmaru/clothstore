from django.shortcuts import render, redirect
from home.models import Category,SubCategory,Product
from django.contrib.auth import authenticate,login,logout
from home.models import UsercreateForm


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

def signup(request):
    if request.method == 'POST':
        form = UsercreateForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user= authenticate(
                username = form.cleaned_data['username'],
                password = form.cleaned_data['password1'], 
            )
            login(request, new_user)
            return redirect('home')
    else:
        form = UsercreateForm()

    context = {
        'form':form,
    }
    return render(request, 'registration/signup.html',context)


def login_view(request):
    return render(request,'home/login.html')

