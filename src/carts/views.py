from django.shortcuts import render, redirect
from accounts.forms import LoginForm, GuestForm
from accounts.models import GuestEmail
from orders.models import Order
from carts.models import Cart
from products.models import Product
from billing.models import BillingProfile

from addresses.forms import AddressForm
from addresses.models import Address
from django.http import JsonResponse
# Create your views here.

def cart_detail_api_view(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    products = [{
        "id": x.id,
        "url": x.get_absolute_url(),
        "name": x.name, 
        "price": x.price
        } 
        for x in cart_obj.products.all()]  #[<object>,<object><object>]
    return JsonResponse({"products":products, "subtotal": cart_obj.subtotal, "total":cart_obj.total})

def cart_home(request):
    print("Entering into cart_home")
    print(request)
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    # print(cart_obj)
    # print(cart_obj.products.all())
    # products = cart_obj.products.all()
    # total = 0
    # for x in products:
    #     print(x)    
    #     total += x.price
    # # print(total)
    # cart_obj.total = total
    # cart_obj.save()
    return render(request,"carts/home.html",{"cart":cart_obj})

def cart_update(request):
    print("from cart_update - request",request.POST)
    product_id = request.POST.get('product_id')
    
    if product_id is not None:
        try:
            product_obj = Product.objects.get(id=product_id)
        except Product.DoesNotExists:
            print("Show message to user, product is gone?")
            return redirect("cart:home")
        cart_obj, new_obj = Cart.objects.new_or_get(request) 
        if product_obj in cart_obj.products.all():
            cart_obj.products.remove(product_obj)
            added = False
        else:
            cart_obj.products.add(product_obj)  # cart_obj.products.add(product_id)
            added = True
        request.session['cart_items'] = cart_obj.products.count()
    #cart_obj.products.remove(product_obj)
    # return redirect(product_obj.get_absolute_url()) 
    # here we are redirecting to product page
        if request.is_ajax():       # Asynchronous JavaScript or XML
            print("Ajax Request")   
            json_data = {
                "added": added,
                "removed": not added,
                "cartItemCount": cart_obj.products.count(),
            }
            return JsonResponse(json_data)
    return redirect("cart:home")

def checkout_home(request):
    print("request : ",request.user)
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj = None
    if cart_created or cart_obj.products.count() == 0:
        return redirect("cart:home")
    # else:
    #     print(Order.objects.get_or_create(cart=cart_obj))
    #     order_obj, new_order_obj = Order.objects.get_or_create(cart=cart_obj)
    # user = request.user
    # billing_profile = None
    login_form = LoginForm()
    guest_form = GuestForm()
    address_form = AddressForm()
    billing_address_id = request.session.get("billing_address_id", None)
    shipping_address_id = request.session.get("shipping_address_id", None)
    print("checkout_home_request")
    print(request.session.get("billing_address_id"))
    print(request.session.get("shipping_address_id"))
    # billing_address_form = AddressForm()
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    # guest_email_id = request.session.get('guest_email_id')
    # if user.is_authenticated:
    #     # logged in user checkout; remember payment stuff
    #     billing_profile, billing_profile_created = BillingProfile.objects.get_or_create(user=user, email=user.email)
        
    # elif guest_email_id is not None:
    #     # guest user checkout; auto reloads payment stuff 
    #     guest_email_obj = GuestEmail.objects.get(id=guest_email_id)
    #     billing_profile, billing_guest_profile_created = BillingProfile.objects.get_or_create(email=guest_email_obj.email)
    # else:
    #     pass
    address_qs = None 
    if billing_profile is not None:
        if request.user.is_authenticated:
            address_qs = Address.objects.filter(billing_profile=billing_profile)
        # shipping_address_qs = address_qs.filter(address_type='shipping')
        # billing_address_qs = address_qs.filter(address_type='billing')

        order_obj, order_obj_created = Order.objects.new_or_get(billing_profile,cart_obj)
        if shipping_address_id:
            order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
            del request.session["shipping_address_id"]
        if billing_address_id:
            order_obj.billing_address = Address.objects.get(id=billing_address_id)
            del request.session["billing_address_id"]
        if billing_address_id or shipping_address_id:
            order_obj.save()
        # order_qs = Order.objects.filter(billing_profile=billing_profile,cart=cart_obj,active=True)
        # if order_qs.count() == 1:
        #     order_obj = order_qs.first()
        # else:
        #     # old_order_qs = Order.objects.exclude(billing_profile=billing_profile).filter(cart=cart_obj,active=True)
        #     # if old_order_qs.exists():
        #     #     old_order_qs.update(active=False)
        #     order_obj = Order.objects.create(billing_profile=billing_profile, cart=cart_obj)
    
    if request.method == 'POST':
        is_done = order_obj.check_done()
        if is_done:
            order_obj.mark_as_paid()
            request.session['cart_items']=0
            print("cart_id : ",request.session['cart_id'])
            # del request.session['cart_id']
            query = Cart.objects.get(id=request.session['cart_id'])
            query.delete()
            return redirect("cart:success")

    context = {
        "object":order_obj,
        "billing_profile":billing_profile,
        "login_form": login_form,
        "guest_form": guest_form,
        "address_form": address_form,
        "address_qs":address_qs,
        # "billing_address_form": billing_address_form,
    }

    return render(request, "carts/checkout.html",context)

def checkout_done_view(request):
    context = {}
    return render(request, "carts/checkout-done.html", context)