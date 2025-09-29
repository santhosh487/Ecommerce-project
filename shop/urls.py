from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('cart/', views.cart_page, name='cart'),
    path('fav/', views.favviewpage, name='fav'),
    path('favviewpage/', views.favviewpage, name='favviewpage'),
    path('fav/remove/<int:fid>/', views.remove_favourite, name='remove_favourite'),
    path('remove_cart/<str:cid>', views.remove_cart, name='remove_cart'),
    path('collections/', views.collections, name='collections'),
    path('collections/<str:name>/', views.collectionsview, name='collection'),
    path('collections/<str:cname>/<str:pname>/', views.product_details, name='product_details'),
    path('addtocart/', views.add_to_cart, name='addtocart'),
    path('add-to-favourite/', views.add_to_favourite, name='add_to_favourite'),  # <--- add this
]
