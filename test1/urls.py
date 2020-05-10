from django.urls import path
from .views import (index, cart, category, contact, login, logout,
                    add_to_cart, product_details, initiate_payment, callback)

urlpatterns = [
    path('', index, name='index'),
    path('cart', cart, name='cart'),
    path('contact', contact, name='contact'),
    path('category', category, name='category'),
    path('add_to_cart', add_to_cart, name='add_to_cart'),
    path('product/<str:slug>-<int:pk>', product_details, name='details'),
    path('pay/', initiate_payment, name='pay'),
    path('callback/', callback, name='callback'),
    path('login/', login, name="login"),
    path('logout', logout, name='logout')
]
