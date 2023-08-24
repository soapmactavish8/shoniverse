from ast import mod
from distutils.command.upload import upload
from pyexpat import model
from django.db import models

# Create your models here.
class admin(models.Model):
    adminEmail = models.CharField(max_length=30)
    adminpass = models.CharField(max_length=300)

class Category(models.Model):
    c_name = models.CharField(max_length=30)


class SubCategory(models.Model):
    s_name = models.CharField(max_length=30)
    catid = models.ForeignKey(Category,on_delete=models.CASCADE, null=True)

selectsize = (
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
    )

class Product(models.Model):
    catid = models.ForeignKey(Category,on_delete=models.CASCADE, null=True)
    subcatid = models.ForeignKey(SubCategory,on_delete=models.CASCADE, null=True)
    prodName = models.CharField(max_length=100)
    prodDescription = models.TextField(max_length=500)
    prod_img = models.ImageField(upload_to='images/', null=True)
    stock = models.CharField(max_length=20,default=None)
    prodPrice = models.DecimalField(decimal_places=2,max_digits=20,default=0.00)
    prodQuantity = models.BigIntegerField()
    brand = models.CharField(max_length=50, null=True)
    prodColor = models.CharField(max_length=50, null=True)
    prodSize = models.CharField(max_length=50, choices=selectsize)
    prodDescription1 = models.TextField(max_length=500 , null=True)
    prodDisccountPrice = models.DecimalField(decimal_places=2, max_digits=20, default=0.00)
  
 
    
