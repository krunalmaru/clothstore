"""myclothstore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from home import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/cart_remove/', views.cart_remove, name='cart_remove'),
    path('cart/item_increase/<int:id>/', views.item_increase, name='item_increase'),
    path('cart/item_decrease/<int:id>/', views.item_decrease, name='item_decrease'),
    path('cart/cart_detail/', views.cart_detail, name='cart_detail'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('contact/', views.contact_us, name='contactus'),
    path('checkout/', views.checkout, name='checkout'),
    path('order/', views.order, name='yourorder'),
    path('product/', views.product, name='product'),
    path('product/<str:id>', views.productdetail, name='productdetail'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
