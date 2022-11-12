from django.shortcuts import render
from django.db.models import Q
from store.models import Product, Order

# Create your views here.
def hello(request):
  # select_related -> many-to-one
  # prefetch_related -> many-to-many
  # products=  Product.objects.select_related('collection').all()
  orders = Order.objects.prefetch_related("orderitem_set").order_by('placed_at')[:5]
  

  context= {
    "orders": list(orders),
    "count": orders.count(),
  }
  return render(request, "index.html", context)
