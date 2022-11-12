from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html, urlencode
from django.urls import reverse
from . import models
# Register your models here.

@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
  list_display = ['title', 'products_count']

  @admin.display(ordering='products_count')
  def products_count(self, collection):
    url = (
      reverse("admin:store_product_changelist")
      + '?'
      + urlencode({
        'collection__id': str(collection.id)
      })
      )
    return format_html("<a href='{}'>{}</a>", url, collection.products_count)
  
  def get_queryset(self, request) :
    return super().get_queryset(request).annotate(
      products_count= Count('product')
    )
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
  prepopulated_fields= {
    'slug': ('title',)
  }
  list_display= ['title', 'unit_price', 'inventory_status', 'collection']
  list_editable= ['unit_price']
  list_select_related= ['collection']
  list_per_page= 50
  search_fields= ['title']

  @admin.display(ordering='inventory')
  def inventory_status(self, product):
    if product.inventory < 10:
      return 'Low'
    return 'Ok'

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
  list_display= ['first_name', 'last_name', 'membership', 'orders_count']
  search_fields = ['first_name__istartswith', 'last_name__istartswith']
  list_editable= ['membership']
  ordering= ['first_name', 'last_name']
  list_per_page= 10

  def orders_count(self, customer):
    url = (reverse("admin:store_order_changelist")
      +'?'
      +urlencode({
        'customer__id': str(customer.id)
      }))
    return format_html("<a href='{}'>{}</a>", url, customer.orders_count)
  
  def get_queryset(self, request) :
    return super().get_queryset(request).annotate(
      orders_count= Count('order')
    )

class OrderItemInline(admin.TabularInline):
  autocomplete_fields= ["product"]
  model= models.OrderItem
@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
  autocomplete_fields= ['customer']
  inlines= [OrderItemInline]
  list_display= ['id', 'placed_at', 'customer_name']
  list_select_related= ['customer']
  ordering= ['placed_at', 'id']

  def customer_name(self, order):
    return order.customer.first_name+' '+ order.customer.last_name