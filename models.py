from django.db import models

# Create your models here.
class reg(models.Model):
    name=models.CharField(max_length=30)
    address=models.CharField(max_length=100)
    mobile=models.IntegerField()
    email=models.EmailField()
    password=models.CharField(max_length=30)
    conformpassword=models.CharField(max_length=30)

class fishpro(models.Model):
    fname=models.CharField(max_length=30)
    description=models.TextField()
    breed=models.CharField(max_length=30,null='True')
    status=models.CharField(max_length=30)
    price=models.IntegerField()
    image=models.ImageField(upload_to='fish/')

class addcart(models.Model):
    fname=models.CharField(max_length=30)
    description=models.CharField(max_length=30)
    price=models.IntegerField()
    image=models.ImageField(upload_to='fish/')
    name=models.CharField(max_length=30)
    mobile=models.IntegerField()

class pay(models.Model):
    fname=models.CharField(max_length=30)
    price=models.IntegerField()
    name=models.CharField(max_length=30)
    mobile=models.IntegerField()



    


    




    
