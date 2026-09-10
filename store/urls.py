from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='home'),

    path('checkout/', views.checkout, name='checkout'),

    path(
    'my-orders/',
    views.my_orders,
    name='my_orders'
),

    path(
    'order-success/<int:order_id>/',
    views.order_success,
    name='order_success'
),

    path(
        'product/<int:product_id>/',
        views.product_detail,
        name='product_detail'
    ),

    path(
        'register/',
        views.register,
        name='register'
    ),

    path(
        'login/',
        views.login_view,
        name='login'
    ),

    path(
        'logout/',
        views.logout_view,
        name='logout'
    ),

    path(
        'cart/',
        views.cart,
        name='cart'
    ),

    path(
        'cart/add/<int:product_id>/',
        views.add_to_cart,
        name='add_to_cart'
    ),
    path(
    'cart/increase/<int:product_id>/',
    views.increase_quantity,
    name='increase_quantity'
),

path(
    'cart/decrease/<int:product_id>/',
    views.decrease_quantity,
    name='decrease_quantity'
),

path(
    'cart/remove/<int:product_id>/',
    views.remove_from_cart,
    name='remove_from_cart'
),
path(
    'order/<int:order_id>/',
    views.order_detail,
    name='order_detail'
),
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)