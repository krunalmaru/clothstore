from django.shortcuts import render, redirect, HttpResponse
from home.models import Category,SubCategory,Product,Contact_us, Order,Brand
from django.contrib.auth import authenticate,login,logout
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
# from home.models import UsercreateForm
from .forms import UsercreateForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from cart.cart import Cart

# Create your views here.
def home(request):
    category = Category.objects.all()
    categoryId = request.GET.get('category')
    brands = Brand.objects.all()
    brandId =  request.GET.get('brand')
    if categoryId:
        product = Product.objects.filter(subcategory=categoryId).order_by('-id')
    elif brandId:
        product = Product.objects.filter(brand=brandId).order_by('-id')
    else:
        product = Product.objects.all()

    paginator = Paginator(product,6 )
    page_no = request.GET.get('page')
    pageshow = paginator.get_page(page_no)
    context = {'category':category,'product':pageshow,'brands':brands}
    return render(request, 'home/index.html', context)


def signup(request):    
    if request.method == 'POST':
        form = UsercreateForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            messages.success(request, "Registration successful." )
            return redirect('login')        
        messages.error(request, 'Invalid Information')

    else:

        form = UsercreateForm()
    context = {
        'form':form,
    }
    return render(request, 'registration/signup.html',context)

    
def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        # form = UsercreateForm()
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                # messages.info(request, f"You are now logged in as {username}.")
                return redirect('home')
        else:
            messages.error(request,"Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html',{'form':form} )    
def product(request):
    brand = Brand.objects.all()
    brandId = request.GET.get('brand')
    category = Category.objects.all()
    categoryid = request.GET.get('category')
    if brandId:
        products = Product.objects.filter(brand=brandId).order_by('-id')
    elif categoryid:
        products = Product.objects.filter(subcategory=categoryid).order_by('-id')
    else:
        products = Product.objects.all()
    
    paginator = Paginator(products,3 )
    page_no = request.GET.get('page')
    pageshow = paginator.get_page(page_no)
    
    context = {'product':pageshow,'brand':brand,'category':category,'products':products}

    return render(request, 'home/product.html',context)

def productdetail(request, id):
    product = Product.objects.filter(id=id).first()
    context = {'product':product}
    return render(request, 'home/productdetail.html', context)

def search(request):
    query = request.GET['query']
    product = Product.objects.filter(name__icontains = query)
    context = {'product':product}
    return render(request, 'home/search.html', context)

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

def contact_us(request):
    if request.method == "POST":
        contact = Contact_us(
            name = request.POST.get('name'),
            email = request.POST.get('email'),
            subject = request.POST.get('subject'),
            message = request.POST.get('message')
        )
        contact.save()
    return render(request, 'home/contact.html')

def checkout(request):
    if request.method == 'POST':
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')
        pincode = request.POST.get('pincode')
        cart = request.session.get('cart')
        uid = request.session.get('_auth_user_id')
        user = User.objects.get(pk=uid)
        # print(mobile, address, pincode, cart, user)

        for i in cart:
            # print(i)
            a = int(cart[i]['price'])
            b = cart[i]['quantity']
            total = (a * b)
            order= Order(
                user = user,
                product = cart[i]['name'],
                price = cart[i]['price'],
                quantity = cart[i]['quantity'],
                image = cart[i]['image'],
                address = address,
                mobile = mobile,
                total = total,
                pincode = pincode

            )
            order.save()
            request.session['cart'] = {}
        return redirect('yourorder')
    return HttpResponse('this is checkout ')


@login_required(login_url='/accounts/login/')
def order(request):
    uid = request.session.get('_auth_user_id')
    user = User.objects.get(pk=uid)
    order = Order.objects.filter(user=user)
    context = {'order':order}
    return render(request, 'home/order.html', context)

def paymentdone(request):
    user = request.user
    uid = request.session.get('_auth_user_id')
    user = User.objects.get(pk=uid)
    cart = Order.objects.filter(user=user)
    for i in cart:
        Order(user=user, product=i.product,quantity=i.quantity).save()
    return redirect('yourorder')

