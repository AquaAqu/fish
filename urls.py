"""
URL configuration for aquasite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

from django.urls import path
from . import views

urlpatterns = [
    path('index/',views.index,name='index'),   
    


    path('home/',views.home,name='home'),
    path('adhome/',views.adhome,name='adhome'),


    path('shop/',views.shop,name='shop'),
    path('contact/',views.contact,name='contact'),
    path('userreg/',views.userreg,name='userreg'),
    path('userlogin/',views.userlogin,name='userlogin'),
    path('adlogin/',views.adlogin,name='adlogin'),
    path('adproduct/',views.adproduct,name='adproduct'),
    path('listpro/',views.listpro,name='listpro'),
    path('list/',views.list,name='list'),
    path('cart/<int:id>/',views.cart,name='cart'),
    path('add_to_cart/',views.add_to_cart,name='add_to_cart'),
    path('cartlist/',views.cartlist,name='cartlist'),
    path('delete/<int:id>/',views.delete,name='delete'),
    path('delete1/<int:id>/',views.delete1,name='delete1'),


    path('payment/',views.payment,name='payment'),
    path('paymenthandler/', views.paymenthandler, name='paymenthandler'),



   
]
