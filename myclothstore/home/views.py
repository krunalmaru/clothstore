from django.shortcuts import render, redirect
from home.models import Category,SubCategory,Product
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from home.models import UsercreateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from cart.cart import Cart

# Create your views here.
def home(request):
    category = Category.objects.all()
    categoryId = request.GET.get('category')
    if categoryId:
        product = Product.objects.filter(subcategory=categoryId).order_by('-id')
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
            messages.error(request,'invalid')
            return redirect('home')
    else:
        form = UsercreateForm()

    context = {
        'form':form,
    }
    return render(request, 'registration/signup.html',context)

@login_required(login_url='/accounts/login/')
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id = id)
    cart.add(product=product)
    return redirect('home')

@login_required(login_url='/accounts/login/')
def cart_remove(request):
    cart = Cart(request)
    cart.clear()
    return redirect('cart_detail')

@login_required(login_url='/accounts/login/')
def item_increase(request, id):
    cart = Cart(request)
    product = Product.objects.get(id = id)
    cart.add(product=product)
    return redirect('cart_detail')

@login_required(login_url='/accounts/login/')
def item_decrease(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect('cart_detail')


@login_required(login_url='/accounts/login/')
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect('cart_detail')

@login_required(login_url='/accounts/login/')
def cart_detail(request):
    return render(request,'cart/cart_detail.html')