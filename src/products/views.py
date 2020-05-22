from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.views.generic import ListView, DetailView
from products.models import Product
# Create your views here.

class ProductListView(ListView):
    queryset = Product.objects.all()
    template_name = "products/list.html"

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

    #Detail View
class ProductDetailView(DetailView):
    queryset = Product.objects.all()
    template_name = "products/detail.html"

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
    print(instance)
    qs = Product.objects.filter(pk=pk)
    print(qs.exists())
    if qs.exists() and qs.count() == 1:
        instance = qs.first()
    else:
        raise Http404("Product doesn't exist")
    
    context = {
        'object': instance
    }
    return render(request,"products/detail.html", context)