from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.views.generic import ListView, DetailView
from products.models import Product

from carts.models import Cart
# Create your views here.


class ProductFeaturedListView(ListView):
    template_name = "products/list.html"

    def get_queryset(self,*args,**kwargs):
        request = self.request
        return Product.objects.featured()  

class ProductFeaturedDetailView(DetailView):
    template_name = "products/featured-detail.html"

    def get_queryset(self,*args,**kwargs):
        request = self.request
        return Product.objects.featured() 

class ProductListView(ListView):
    #queryset = Product.objects.all()
    template_name = "products/list.html"

    def get_context_data(self, *args, **kwargs):
        context =  super(ProductListView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request) 
        context['cart'] = cart_obj
        return context
         
    def get_queryset(self,*args,**kwargs):
        request = self.request
        return Product.objects.all()
    '''
    # How do you understand what context is coming
    def get_context_data(self,*args,**kwargs):
        context = super(ProductListView,self).get_context_data(*args,**kwargs)
        print(context)
        return context

        {'paginator': None, 'page_obj': None, 'is_paginated': False, 'object_list': <QuerySet [<Product: T-Shirt>, <Product: Hat>]>, 'product_list': <QuerySet [<Product: T-Shirt>, <Product: Hat>]>, 'view': <products.views.ProductListView object at 0x000002BF92F68F70>}
        '''

def product_list_view(request):
    queryset = Product.objects.all()
    context = {
        'object_list':queryset
    }
    return render(request,"products/list.html",context)

    #Slug View
class ProductSlugDetailView(DetailView):
    queryset = Product.objects.all()
    template_name = "products/detail.html"

    def get_context_data(self, *args, **kwargs):
        context =  super(ProductSlugDetailView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request) 
        context['cart'] = cart_obj
        return context

    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')
        try :
            instance = Product.objects.get(slug = slug,active = True)
            print(instance)
            #print (instance.image.url) - This will be None for products doesn't have image
        except Product.DoesNotExist:
            raise Http404("Not Found")
        except Product.MultipleObjectsReturned:
            qs = Product.objects.filter(slug=slug,active=True)
            instance = qs.first()
        except:
            raise Http404("Uhhmmm")
        return instance

    #Detail View
class ProductDetailView(DetailView):
    #queryset = Product.objects.all()
    template_name = "products/detail.html"
    def get_context_data(self,*args,**kwargs):
        context  =  super(ProductDetailView, self).get_context_data(*args,**kwargs)
        print(context)
        return context

    def get_object(self,*args,**kwargs):
        request = self.request
        pk = self.kwargs.get('pk')
        instance = Product.objects.get_by_id(pk)
        if instance is None:
            raise Http404("Class Detail View - Product not found")
        return instance
    
    # def get_queryset(self,*args,**kwargs):
    #     request = self.request
    #     pk = self.kwargs.get('pk')
    #     return Product.objects.filter(id=pk)

def product_detail_view(request,pk,*args,**kwargs):
    #instance = Product.objects.get(pk=pk) #id
    # instance = get_object_or_404(Product, pk=pk)
    # try:
    #     instance = Product.objects.filter(id=pk)
    # except Product.DoesNotExist:
    #     print('no products here')
    #     raise Http404("Product doesn't exist")
    # except:
    #     print("huh?")
    
    instance = Product.objects.get_by_id(pk)
    if instance is None :
        raise Http404("From Manager - Product doesn't exist")
    # print(instance)
    # qs = Product.objects.filter(pk=pk)
    # print(qs.exists())
    # if qs.exists() and qs.count() == 1:
    #     instance = qs.first()
    # else:
    #     raise Http404("Product doesn't exist")
    
    context = {
        'object': instance
    }
    return render(request,"products/detail.html", context)