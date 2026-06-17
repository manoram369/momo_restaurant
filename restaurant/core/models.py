from django.db import models

# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=250)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    subject = models.CharField(max_length=250)
    message = models.TextField()
    newsletter = models.BooleanField(default=False)


class Category(models.Model):
    title=models.CharField(max_length=250)
    image=models.ImageField(upload_to="momo_item",null=True)

    def __str__(self):
        return self.title
    
class Momo(models.Model):
    title=models.CharField(max_length=200)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,null=True , related_name="items")
    desc=models.TextField()
    image=models.ImageField(upload_to="momo_image")
    price=models.DecimalField(max_digits=6,decimal_places=2)
    created_at=models.DateTimeField(auto_now=True,null=True)


    def __str__(self):
        return self.title
    