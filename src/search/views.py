from django.shortcuts import render
from products.models import Product
from django.views.generic import ListView

# from django.db.models import Q

# Create your views here.
class SearchProductListView(ListView):
    template_name = "search/view.html"

    def get_context_data(self, *args, **kwargs):
        context = super(SearchProductListView,self).get_context_data(*args, **kwargs)
        query = self.request.GET.get('q')
        context['query'] = query
        return context

    def get_queryset(self,*args,**kwargs):
        '''
        __icontains = field contains this
        __iexact = fileds is exactly this
        '''
        print(args)
        print(kwargs)
        request = self.request
        get_dict = request.GET  # will give you the request with url parameter - <QueryDict: {'q': ['shirt']}>
        url_param = get_dict.get('q', None)
        print(url_param)
        if url_param is not None:
            
            # lookups = Q(title__icontains=url_param) | Q(description__icontains=url_param)
            # # if Product.objects.filter(title__icontains=url_param).exists():
            #     # return Product.objects.filter(title__icontains=url_param)
            # if Product.objects.filter(lookups).distinct().exists():
            #     return Product.objects.filter(lookups).distinct()
            # else:
            #     return None  
            # return Product.objects.none()
        
            return Product.objects.search(url_param)
        return Product.objects.featured()

