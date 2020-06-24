from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
# Create your models here.

User = settings.AUTH_USER_MODEL

class ObjectViewed(models.Model):
    # user            = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)  # User Instance
    #ip_address
    content_type    = models.ForeignKey(ContentType, on_delete=models.CASCADE)    # Product, Order, Cart
    object_id       = models.PositiveIntegerField() # USer_id, Product_id, Order id
    content_object  = GenericForeignKey('content_type','object_id') # product instance
    product         = models.ForeignKey(Product) # id=1, product_obj.objectviewed_set.all()
    
    