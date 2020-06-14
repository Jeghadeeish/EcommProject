from django.conf import settings
from django.db import models

from products.models import Product
from django.contrib.auth.models import User

from django.db.models.signals import pre_save, post_save, m2m_changed

# Create your models here.
User = settings.AUTH_USER_MODEL

class CartManager(models.Manager):
    def new_or_get(self, request):
        cart_id = request.session.get("cart_id", None)
        qs = self.get_queryset().filter(id=cart_id)
        if qs.count() == 1:
            new_obj = False
            cart_obj = qs.first()
            if request.user.is_authenticated and cart_obj.user is None:
                user_cart = self.model.objects.filter(user=request.user).first()
                if user_cart is not None:
                    cart_obj.products.add(*user_cart.products.all())
                    cart_obj.user = request.user
                    cart_obj.save()
                    user_cart.delete()
                else:
                    cart_obj.user = request.user
                    cart_obj.save()
        else:
            cart_obj = Cart.objects.new(user=request.user)
            new_obj = True
            request.session['cart_id'] = cart_obj.id
        return cart_obj, new_obj
 
    def new(self, user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                cart_obj = self.model.objects.filter(user=user).first()
                if cart_obj is not None:
                    return cart_obj
                user_obj = user
        return self.model.objects.create(user=user_obj)

class Cart(models.Model):
    user        =   models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    products    =   models.ManyToManyField(Product, blank=True)
    subtotal    =   models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    total       =   models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    updated     =   models.DateTimeField(auto_now=True)
    timestamp   =   models.DateTimeField(auto_now_add=True)

    objects = CartManager()

    def __str__(self):  
        return str(self.id)
        # if self.user:
        #     return str(self.id) + ',' + self.user.username + ',' + str(self.total)
        # else:
        #     return str(self.id) + ',' + str(self.total)

def m2m_changed_cart_receiver(sender, instance, action, *args, **kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        products = instance.products.all()
        total = 0
        for x in products: 
            # print(x)   
            total += x.price
        # print("Total",total)
        instance.total = total  # Cart total display
        if instance.subtotal != instance.total:     # This will reduce DB hits
            instance.subtotal = total
            instance.save()
m2m_changed.connect(m2m_changed_cart_receiver,sender=Cart.products.through)

def pre_save_cart_receiver(sender, instance, *args, **kwargs):
    # print(instance.subtotal)
    if instance.subtotal > 0 :
        instance.total = float(instance.subtotal) * float(1.08)     # + 15 
    else:
        instance.total = 0.00
pre_save.connect(pre_save_cart_receiver,sender=Cart)