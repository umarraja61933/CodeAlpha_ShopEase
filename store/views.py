from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required

from .models import Product, Order, OrderItem



# ==========================================
# HOME
# ==========================================

def home(request):

    search = request.GET.get('search', '')

    category = request.GET.get('category', '')


    products = Product.objects.all()


    if search:

        products = products.filter(
            name__icontains=search
        )


    if category:

        products = products.filter(
            category__iexact=category
        )


    categories = Product.objects.values_list(
        'category',
        flat=True
    ).distinct()


    return render(
        request,
        'home.html',
        {
            'products': products,

            'categories': categories,

            'search': search,

            'selected_category': category,
        }
    )



# ==========================================
# PRODUCT DETAILS
# ==========================================

def product_detail(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )


    return render(
        request,
        'product_detail.html',
        {
            'product': product
        }
    )



# ==========================================
# REGISTER
# ==========================================

def register(request):

    if request.method == 'POST':

        username = request.POST['username']

        email = request.POST['email']

        password = request.POST['password']


        if User.objects.filter(
            username=username
        ).exists():

            return render(
                request,
                'register.html',
                {
                    'error':
                    'Username already exists.'
                }
            )


        User.objects.create_user(

            username=username,

            email=email,

            password=password
        )


        return redirect('login')


    return render(
        request,
        'register.html'
    )



# ==========================================
# LOGIN
# ==========================================

def login_view(request):

    # Get the page user originally wanted to visit

    next_url = request.GET.get(
        'next',
        ''
    )


    if request.method == 'POST':

        username = request.POST['username']

        password = request.POST['password']


        user = authenticate(

            request,

            username=username,

            password=password
        )


        if user is not None:

            login(
                request,
                user
            )


            # Keep user on the page
            # they originally requested

            next_url = request.POST.get(
                'next',
                ''
            )


            if next_url:

                return redirect(next_url)


            return redirect('home')


        return render(

            request,

            'login.html',

            {
                'error':
                'Invalid username or password.',

                'next':
                next_url,
            }
        )


    return render(

        request,

        'login.html',

        {
            'next':
            next_url,
        }
    )



# ==========================================
# LOGOUT
# ==========================================

def logout_view(request):

    logout(request)

    return redirect('home')



# ==========================================
# ADD TO CART
# ==========================================

def add_to_cart(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )


    cart = request.session.get(
        'cart',
        {}
    )


    product_id = str(product_id)


    if product_id in cart:

        if cart[product_id] < product.stock:

            cart[product_id] += 1


    else:

        if product.stock > 0:

            cart[product_id] = 1


    request.session['cart'] = cart


    return redirect('cart')



# ==========================================
# CART
# ==========================================

def cart(request):

    cart_data = request.session.get(
        'cart',
        {}
    )


    products = []

    total = 0


    for product_id, quantity in cart_data.items():

        product = get_object_or_404(
            Product,
            id=product_id
        )


        subtotal = (
            product.price * quantity
        )


        total += subtotal


        products.append({

            'product': product,

            'quantity': quantity,

            'subtotal': subtotal,
        })


    return render(

        request,

        'cart.html',

        {
            'products': products,

            'total': total,
        }
    )



# ==========================================
# INCREASE QUANTITY
# ==========================================

def increase_quantity(
    request,
    product_id
):

    product = get_object_or_404(

        Product,

        id=product_id
    )


    cart = request.session.get(

        'cart',

        {}
    )


    product_id = str(product_id)


    if product_id in cart:

        if cart[product_id] < product.stock:

            cart[product_id] += 1


    request.session['cart'] = cart


    return redirect('cart')



# ==========================================
# DECREASE QUANTITY
# ==========================================

def decrease_quantity(

    request,

    product_id
):

    cart = request.session.get(

        'cart',

        {}
    )


    product_id = str(product_id)


    if product_id in cart:

        if cart[product_id] > 1:

            cart[product_id] -= 1

        else:

            del cart[product_id]


    request.session['cart'] = cart


    return redirect('cart')



# ==========================================
# REMOVE FROM CART
# ==========================================

def remove_from_cart(

    request,

    product_id
):

    cart = request.session.get(

        'cart',

        {}
    )


    product_id = str(product_id)


    if product_id in cart:

        del cart[product_id]


    request.session['cart'] = cart


    return redirect('cart')



# ==========================================
# CHECKOUT
# LOGIN REQUIRED
# ==========================================

@login_required
def checkout(request):

    cart_data = request.session.get(

        'cart',

        {}
    )


    if not cart_data:

        return redirect('cart')


    products = []

    total = 0


    for product_id, quantity in cart_data.items():

        product = get_object_or_404(

            Product,

            id=product_id
        )


        # Check available stock

        if quantity > product.stock:

            return redirect('cart')


        subtotal = (

            product.price * quantity
        )


        total += subtotal


        products.append({

            'product': product,

            'quantity': quantity,

            'subtotal': subtotal,
        })


    # ======================================
    # PLACE ORDER
    # ======================================

    if request.method == 'POST':

        full_name = request.POST[
            'full_name'
        ]

        phone = request.POST[
            'phone'
        ]

        address = request.POST[
            'address'
        ]


        # Create Order

        order = Order.objects.create(

            user=request.user,

            total_amount=total,

            full_name=full_name,

            phone=phone,

            address=address,

            status='Pending'
        )


        # Create Order Items
        # and reduce stock

        for item in products:

            product = item[
                'product'
            ]

            quantity = item[
                'quantity'
            ]


            OrderItem.objects.create(

                order=order,

                product=product,

                quantity=quantity,

                price=product.price
            )


            product.stock -= quantity

            product.save()


        # Clear cart

        request.session['cart'] = {}


        return redirect(

            'order_success',

            order_id=order.id
        )


    return render(

        request,

        'checkout.html',

        {
            'products': products,

            'total': total,
        }
    )



# ==========================================
# ORDER SUCCESS
# ==========================================

def order_success(

    request,

    order_id
):

    order = get_object_or_404(

        Order,

        id=order_id
    )


    return render(

        request,

        'order_success.html',

        {
            'order': order,
        }
    )



# ==========================================
# MY ORDERS
# ==========================================

@login_required
def my_orders(request):

    orders = Order.objects.filter(

        user=request.user

    ).order_by(

        '-created_at'
    )


    return render(

        request,

        'my_orders.html',

        {
            'orders': orders,
        }
    )



# ==========================================
# ORDER DETAILS
# ==========================================

@login_required
def order_detail(

    request,

    order_id
):

    order = get_object_or_404(

        Order,

        id=order_id,

        user=request.user
    )


    return render(

        request,

        'order_detail.html',

        {
            'order': order,
        }
    )