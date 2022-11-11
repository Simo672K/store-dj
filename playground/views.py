from django.shortcuts import render
from store.models import Product

# Create your views here.
def hello(request):
  products = Product.objects.filter(title__icontains= 'beef')

  context= {
    "products": list(products),
    "count": products.count(),
  }
  return render(request, "index.html", context)
