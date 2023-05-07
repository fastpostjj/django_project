from django.http import HttpRequest
from django.shortcuts import render
from products.models import Category, Products

# Create your views here.

def products_views(request):
    text = "Интернет-магазин саженцев и семян"
    return render(request, 'products/products.html', {'text':text, })

def index(request):
    number = 5
    print(type(object))
    objects = Products.objects.all().order_by('-id')[:5]

    return render(request, 'products/index.html', {'objects':objects,})
