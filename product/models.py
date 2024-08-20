from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from customer.models import User

# Bazaviy model
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

# Kategoriya modeli
class Category(BaseModel):
    title = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Categories'
        db_table = 'category'
        ordering = ['-id']

# Mahsulot modeli
class Product(BaseModel):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    image = models.ImageField(upload_to='products', blank=True, null=True)
    quantity = models.PositiveIntegerField(default=0, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField()
    discount = models.FloatField(default=0, blank=True, null=True)
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def discounted_price(self):
        return self.price * (1 - (self.discount / 100))

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})
    def shipping_cost(self):
        return self.price * 0.15

    def __str__(self):
        return self.name

# Rasm modeli
class Image(BaseModel):
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    is_primary = models.BooleanField(default=False)

# Izoh modeli
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
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')

# Attribute modeli
class Attribute(BaseModel):
    name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name

# AttributeValue modeli
class AttributeValue(BaseModel):
    value = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.value

# ProductAttribute modeli
class ProductAttribute(BaseModel):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, related_name='attributes')
    value = models.ForeignKey(AttributeValue, on_delete=models.CASCADE, related_name='values')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='attributes')
