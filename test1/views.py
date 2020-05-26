from django.shortcuts import render, redirect
from .models import Sliders, CATEGORY_CHOICES, Item, Cart, Transaction
from django.http import HttpResponse
from django.db.models import Q
from .paytm import generate_checksum, verify_checksum
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
# Create your views here.


def index(request):
    slides = Sliders.objects.filter(published='True')
    return render(request, 'index.html', {'slides': slides})


def category(request):
    context = {}
    category_ty = request.GET.get('category')
    context['c_choices'] = CATEGORY_CHOICES
    filter_items = Item.objects.all()
    if category_ty:
        filter_items = Item.objects.filter(category=category_ty)
    context['products'] = filter_items
    return render(request, 'category.html', context)


def contact(request):
    return render(request, 'contact.html')


def cart(request):
    context = {}
    cart = Cart.objects.filter(user_id=request.user.id).order_by('created')
    context['cart_objs'] = cart
    total = sum(pro.product.discount_price * pro.quantity for pro in cart)
    context['total'] = total
    if request.is_ajax():
        del_id = request.GET.get('del_id', '')
        p_id = request.GET.get('id')
        quantity = request.GET.get('quantity')
        if request.user.is_authenticated:
            cart_u = Cart.objects.filter(Q(id=p_id) & Q(user=request.user))
            if del_id:
                cart_u = Cart.objects.filter(
                    Q(id=del_id) & Q(user=request.user))
                cart_u.delete()
            if cart_u:
                cart_u.update(quantity=quantity)
            return HttpResponse("success")
        else:
            cart = request.session.get('cart', {})
            id = p_id
            if int(quantity) > 1:
                cart[id] = quantity
            else:
                cart[id] = quantity
            request.session['cart'] = cart
    return render(request, 'cart.html', context)


# @login_required(login_url='login/')
def add_to_cart(request):
    quantity = request.GET.get('quantity')
    product_id = request.GET.get('product_id')
    if request.user.is_authenticated:
        cart = Cart.objects.create(product_id=product_id, user=request.user)
        if quantity:
            cart.quantity = quantity
            cart.save()
        return HttpResponse("success")
    else:
        print(type(quantity))
        print("ok")
        cart = request.session.get('cart', {})
        id = product_id
        cart[id] = cart.get(id, quantity)
        request.session['cart'] = cart
        # request.session.set_expiry(5)
        return redirect('/')


def product_details(request, slug=None, pk=None):
    context = {}
    product = Item.objects.filter(slug=slug).first()
    context['product'] = product
    return render(request, 'product.html', context)


@login_required(login_url='/login')
def initiate_payment(request):
    amount = request.POST.get('amount')
    print(amount)
    transaction = Transaction.objects.create(
        made_by=request.user, amount=amount)
    transaction.save()
    # merchant_key = settings.PAYTM_SECRET_KEY
    params = (
        ('MID', settings.PAYTM_MERCHANT_ID),
        ('ORDER_ID', str(transaction.id)),
        ('CUST_ID', str(transaction.made_by)),
        ('TXN_AMOUNT', str(transaction.amount)),
        ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
        ('WEBSITE', settings.PAYTM_WEBSITE),
        # ('EMAIL', request.user.email),
        # ('MOBILE_N0', '9911223388'),
        ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
        ('CALLBACK_URL', 'http://127.0.0.1:8000/callback/'),
        # ('PAYMENT_MODE_ONLY', 'NO'),
    )
    merchant_key = settings.MERCHANT_KEY
    print(settings.PAYTM_MERCHANT_ID)
    print(merchant_key)
    paytm_params = dict(params)
    checksum = generate_checksum(paytm_params, merchant_key)

    transaction.checksum = checksum
    transaction.save()

    paytm_params['CHECKSUMHASH'] = checksum
    print('SENT: ', checksum)
    return render(request, 'redirect.html', context=paytm_params)


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        paytm_checksum = ''
        print(request.body)
        print(request.POST)
        received_data = dict(request.POST)
        print(received_data)
        paytm_params = {}
        merchant_key = 'peOVLtqme@zR5#Rq'
        paytm_checksum = received_data['CHECKSUMHASH'][0]
        for key, value in received_data.items():
            if key == 'CHECKSUMHASH':
                paytm_checksum = value[0]
            else:
                paytm_params[key] = str(value[0])
        # Verify checksum
        is_valid_checksum = verify_checksum(
            paytm_params, merchant_key, str(paytm_checksum))
        if is_valid_checksum:
            print("Checksum Matched")
            received_data['message'] = "Checksum Matched"
        else:
            print("Checksum Mismatched")
            received_data['message'] = "Checksum Mismatched"

        return render(request, 'callback.html', context=received_data)


@csrf_exempt
def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(
            username=username, password=password)
        if user is not None or '':
            auth.login(request, user)
            return HttpResponse('success')
        else:
            return HttpResponse('failure')
    return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('/')
