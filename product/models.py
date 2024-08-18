from django.db import models

from customer.models import User


# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True
class Category(BaseModel):
    title = models.CharField(max_length=100,unique=True)
    def __str__(self):
        return self.title
    class Meta:
        verbose_name_plural = 'Categories'
        db_table = 'category'
        ordering = ['-id']
class Product(BaseModel):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    quantity = models.PositiveIntegerField(default=0, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,null=True, blank=True)
    description = models.TextField()
    discount = models.FloatField(default=0, blank=True, null=True)

    def __str__(self):
        return self.name

class Image(BaseModel):
     image = models.ImageField(upload_to='products/', null=True, blank=True)
     product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='images')
     is_primary = models.BooleanField(default=False)

class Comment(BaseModel):
    class RatingChoices(models.IntegerChoices):
        zero = 0
        one = 1
        two = 2
        three = 3
        four = 4
        five = 5
    message = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to='comments/', null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='comments')

class Attribute(BaseModel):
     name = models.CharField(max_length=100,null=True,blank=True)
     def __str__(self):
         return self.name
class AttributeValue(BaseModel):
     value = models.CharField(max_length=100,null=True,blank=True)
     def __str__(self):
         return self.value
class ProductAttribute(BaseModel):
      attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE,related_name='attributes')
      value = models.ForeignKey(AttributeValue, on_delete=models.CASCADE,related_name='values')
      product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='attributes')

