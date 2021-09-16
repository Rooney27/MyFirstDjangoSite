from django.db import models

# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=100)
    def __str__(self):
        return self.title
class Item(models.Model):
    title = models.CharField(max_length=100)
    discription = models.CharField(max_length=3000)
    price = models.IntegerField()
    photo = models.ImageField(upload_to='static/items/foto', default='static/items/foto/no_foto.jpg')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    discount = models.PositiveIntegerField(default=0)
    def __str__(self):
        return '#'+ str(self.id)+' '+self.title

class Order(models.Model):
    first_name = models.CharField(max_length=50)
    second_name = models.CharField(max_length=50)
    address = models.CharField(max_length=500)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    is_paid = models.BooleanField(default=False)
    def __str__(self):
        return self.first_name + " "+ self.second_name
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,null=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    count = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    def __str__(self):
        return self.item.title
class Promotion(models.Model):
    title = models.CharField(max_length=100)
    discription = models.CharField(max_length=1000)
    start_date = models.DateField()
    end_date = models.DateField()
class PromotionItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    discount = models.PositiveIntegerField()
    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE,null=True)
    smallImage = models.ImageField(upload_to='static/items/Promofoto', default='static/items/foto/no_foto.jpg')
    largeImage = models.ImageField(upload_to='static/items/Promofoto', default='static/items/foto/no_foto.jpg')
    