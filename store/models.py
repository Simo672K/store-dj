from django.db import models

# Promotion ORM Model
class Promotion(models.Model):
  # the reverse many-to-many relationship field name is product_set by default 
  description= models.CharField(max_length= 255)
  discount = models.FloatField()

# Collection ORM Model
class Collection(models.Model):
  title= models.CharField(max_length= 255) 
  # circular dependencie implimentation, 
  # related_name= '+' -> do not create a reverse relationship in the related class
  featured_product= models.ForeignKey('Product', on_delete= models.SET_NULL, null=True, related_name='+')

# Product ORM Model
class Product(models.Model):
  title = models.CharField(max_length=255)
  slug = models.SlugField(default= '-')
  description = models.TextField()
  unit_price = models.DecimalField(max_digits= 6, decimal_places=2)
  inventory = models.IntegerField()
  last_update = models.DateTimeField(auto_now= True)

  # many-to-one association with Collection model
  collection = models.ForeignKey(Collection,  on_delete= models.PROTECT)

  # (many-to-many) association with Promotion model, 
  # realated_name= 'field_name' is used for naming the related field on the other model of the relationship
  promotions = models.ManyToManyField(Promotion)

# Customer ORM Model
class Customer(models.Model):
  MEMBERSHIP_BRONZE = 'B'
  MEMBERSHIP_SLIVER = 'S'
  MEMBERSHIP_GOLD = 'G'

  # Membership types 
  MEMBERSHIP_CHOICES= [
    (MEMBERSHIP_BRONZE, 'Bronze'),
    (MEMBERSHIP_SLIVER, 'Bronze'),
    (MEMBERSHIP_GOLD, 'Bronze'),
  ]
  first_name = models.CharField(max_length = 255)
  last_name = models.CharField(max_length = 255)
  email = models.EmailField(unique= True)
  phone = models.CharField(max_length= 255)
  birth_date = models.DateTimeField(null= True)
  membership = models.CharField(max_length= 1, choices= MEMBERSHIP_CHOICES, default= MEMBERSHIP_BRONZE)


# Order ORM Model
class Order(models.Model):
  PAYMENT_STATUS_PENDING = 'P'
  PAYMENT_STATUS_COMPLETED = 'C'
  PAYMENT_STATUS_FAILED = 'F'

  PAYMENT_STATUS_CHOICES= [
    (PAYMENT_STATUS_PENDING, 'Pending'),
    (PAYMENT_STATUS_COMPLETED, 'Complete'),
    (PAYMENT_STATUS_FAILED, 'Failed'),
  ]
  placed_at = models.DateTimeField(auto_now_add= True)
  payment_status = models.CharField(max_length= 1, choices= PAYMENT_STATUS_CHOICES, default= PAYMENT_STATUS_PENDING)
  # many-to-one association with Customer model
  customer = models.ForeignKey(Customer, on_delete= models.CASCADE)

class OrderItem(models.Model):
  # many-to-one association with Order model
  order = models.ForeignKey(Order, on_delete= models.PROTECT)
  # many-to-one association with Product model
  product = models.ForeignKey(Product, on_delete= models.PROTECT) 
  quantity = models.PositiveSmallIntegerField()
  unit_price = models.DecimalField(max_digits= 6, decimal_places= 2)


# Address ORM Model
class Address(models.Model):
  street = models.CharField(max_length= 255)
  city= models.CharField(max_length= 255)

  # one-to-one association with Customer model
  # customer = models.OneToOneField(Customer, on_delete= models.CASCADE)

  # many-to-one association with Customer model
  customer = models.ForeignKey(Customer, on_delete= models.CASCADE)

# Cart ORM Model 
class Cart(models.Model):
  created_at= models.DateTimeField(auto_now_add= True)

# CartItem ORM Model
class CartItem(models.Model):
  # many-to-one association with Cart model
  cart= models.ForeignKey(Cart, on_delete= models.CASCADE)
  # many-to-one association with product model
  product= models.ForeignKey(Product, on_delete= models.CASCADE)
  quantity= models.PositiveSmallIntegerField()
  customer= models.OneToOneField(Customer, on_delete= models.CASCADE, primary_key= True) 