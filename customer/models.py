from django.db import models
from django.utils.text import slugify

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Customer(BaseModel):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='customer/', blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def joined(self):
        return self.created_at.strftime('%d/%m/%Y')

    @property
    def get_initials(self):
        words = self.full_name.split()
        initials = ''.join([word[0].upper() for word in words])
        return initials

    @property
    def image_url(self):
        if self.image:
            return self.image.url

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.full_name)
        super(Customer, self).save(*args, **kwargs)

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = 'customer_customer'
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'
        unique_together = (('first_name', 'last_name'),)
        ordering = ('first_name', 'last_name', 'phone')
