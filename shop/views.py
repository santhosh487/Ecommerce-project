import json
import logging
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt  # Will remove usage for add_to_favourite

from .models import Category, Product, Cart, Favourite
from .forms import CustomUserForm

logger = logging.getLogger(__name__)


def home(request):
    products = Product.objects.filter(trending=1)
    return render(request, "shop1/index.html", {"products": products})


@login_required
def remove_favourite(request, fid):
    fav_item = Favourite.objects.filter(id=fid, user=request.user).first()
    if fav_item:
        fav_item.delete()
    else:
        messages.error(request, "Favourite item not found or permission denied.")
    return redirect("favviewpage")


def favviewpage(request):
    if request.user.is_authenticated:
        favourites = Favourite.objects.filter(user=request.user)
        total_price = sum(fav.product.selling_price for fav in favourites)

        context = {
            'favourites': favourites,
            'total_price': total_price
        }
        return render(request, 'shop1/fav.html', context)
    else:
        return redirect('login')


def cart_page(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        total_price = sum(item.total_cost for item in cart)
        context = {
            'cart': cart,
            'total_price': total_price
        }
        return render(request, 'shop1/cart.html', context)
    else:
        return redirect('login')


def remove_cart(request, cid):
    cartitem = Cart.objects.filter(id=cid, user=request.user).first()
    if cartitem:
        cartitem.delete()
    else:
        messages.error(request, "Cart item not found or you don't have permission to delete it.")
    return redirect("/cart")


@login_required
def add_to_favourite(request):
    if request.method == "POST" and request.headers.get('x-requested-with', '').lower() == 'xmlhttprequest':
        try:
            data = json.loads(request.body)
            product_id = data.get('product_id')

            product = Product.objects.get(id=product_id)

            # Create favourite relation if not exists
            fav, created = Favourite.objects.get_or_create(user=request.user, product=product)

            return JsonResponse({'status': 'Product Added To Favourite'}, status=200)

        except Product.DoesNotExist:
            return JsonResponse({'status': 'Product not found'}, status=404)
        except Exception as e:
            logger.error(f"Error adding to favourite: {e}")
            return JsonResponse({'status': f'Error: {str(e)}'}, status=500)
    return JsonResponse({'status': 'Invalid request'}, status=400)


@login_required
@csrf_exempt  # You can keep this for now if you don't want to deal with CSRF tokens on cart (but better to fix CSRF)
def add_to_cart(request):
    if request.method == "POST" and request.headers.get('x-requested-with', '').lower() == 'xmlhttprequest':
        try:
            data = json.loads(request.body)
            product_id = data.get('product_id')
            product_qty = int(data.get('product_qty', 1))

            product = Product.objects.get(id=product_id)

            if product.quantity >= product_qty:
                cart_item, created = Cart.objects.get_or_create(
                    user=request.user,
                    product=product,
                    defaults={'product_qty': product_qty}
                )
                if not created:
                    cart_item.product_qty += product_qty
                    cart_item.save()

                return JsonResponse({'status': 'Product added to cart'})
            else:
                return JsonResponse({'status': 'Insufficient stock'}, status=400)

        except Product.DoesNotExist:
            return JsonResponse({'status': 'Product not found'}, status=404)
        except Exception as e:
            logger.error(f"Error adding to cart: {e}")
            return JsonResponse({'status': f'Error: {str(e)}'}, status=500)
    return JsonResponse({'status': 'Invalid request'}, status=400)


def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Logged Out Successfully")
    return redirect("/")


def login_page(request):
    if request.user.is_authenticated:
        return redirect("/")
    if request.method == 'POST':
        name = request.POST.get('username')
        pwd = request.POST.get('password')
        user = authenticate(request, username=name, password=pwd)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully")
            return redirect("/")
        else:
            messages.error(request, "Invalid User Name or Password")
            return redirect("/login")
    return render(request, "shop1/login.html")


def register(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registered Successfully. You Can Login Now.")
            return redirect('login')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomUserForm()
    return render(request, 'shop1/register.html', {'form': form})


def collections(request):
    categories = Category.objects.filter(status=False)
    return render(request, "shop1/collection.html", {"categories": categories})


def collectionsview(request, name):
    category = Category.objects.filter(name=name, status=False).first()
    if category:
        products = Product.objects.filter(category=category, status=False)
        return render(request, "shop1/products/index.html", {
            "products": products,
            "category": category,
            "category_name": name
        })
    messages.warning(request, "No such category found.")
    return redirect("collections")


def product_details(request, cname, pname):
    category = Category.objects.filter(name=cname, status=False).first()
    if not category:
        messages.warning(request, "No Such Category Found.")
        return redirect("collections")

    product = Product.objects.filter(name=pname, category=category, status=False).first()
    if not product:
        messages.warning(request, "No Such Product Found.")
        return redirect("collections")

    return render(request, "shop1/products/product_details.html", {"product": product})
