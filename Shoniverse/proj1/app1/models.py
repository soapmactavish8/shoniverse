from pyexpat import model
from statistics import mode
from unittest.util import _MAX_LENGTH
from django.db import models
from adminservices.models import Product
from django.utils import timezone
# from django.utils import datetime
# Create your models here.
class User(models.Model):
    fname = models.CharField(max_length=30)
    lname = models.CharField(max_length=30)
    email = models.EmailField()
    password = models.CharField(max_length=300)
    phone = models.CharField(max_length=12, null=True)

    def __str__(self):
        return self.fname

class Address(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    address1 = models.CharField(max_length=300)
    address2 = models.CharField(max_length=300)
    city = models.CharField(max_length=50)
    postalcode = models.CharField(max_length=10)
    phoneno = models.CharField(max_length=12)
    userId = models.ForeignKey(User,on_delete=models.CASCADE)

class Cart(models.Model):
    prodid = models.ForeignKey(Product, on_delete=models.CASCADE)
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/')
    price = models.FloatField()
    quantity = models.BigIntegerField()

    def add(self, product):
        pass

    def remove(self, product):
        pass

    def decrement(self, product):
        pass

    def clear(self):
        pass

STATUS_CHOICES = (
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On The Way','On The Way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel')
)

class Order(models.Model):
    orderid = models.CharField(unique=True, max_length=100, null=True, blank=True, default=None)
    address = models.ForeignKey(Address, on_delete=models.CASCADE,null=True )
    userid = models.ForeignKey(User, on_delete=models.CASCADE,null=True )
    prodid = models.ForeignKey(Product, on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/')
    price = models.FloatField()
    quantity = models.BigIntegerField()
    Datetime_of_payment = models.DateTimeField(default=timezone.now)
    Invoice_No = models.BigIntegerField(default=0)
    Razorpay_order_id = models.CharField(max_length=500, null=True, blank=True)
    Razorpay_payment_id = models.CharField(max_length=500, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=500, null=True, blank=True)
    status = models.CharField(max_length=50,choices=STATUS_CHOICES,default='Pending')

    
class Contacts(models.Model):
    subject = models.CharField(max_length=100)
    message = models.TextField()
    userid = models.ForeignKey(User, on_delete=models.CASCADE,null=True)

    
class Reviews(models.Model):
    title = models.CharField(max_length=100)
    reviewMsg = models.TextField()
    userid = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    date =  models.DateField(null=True)
    prodid = models.ForeignKey(Product, on_delete=models.CASCADE,null=True)
   
