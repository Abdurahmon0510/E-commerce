from django.db import models
from social_core.utils import slugify


# Create your models here.




class Author(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True,blank=True,null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Author, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Book(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    published_at = models.DateTimeField(auto_now_add=True)
    price = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f'{self.name} by {self.author}'