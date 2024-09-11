import os
import json
from django.core.mail import send_mail
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver

from config.settings import BASE_DIR, EMAIL_DEFAULT_SENDER
from customer.models import User
from .models import Product, Category

def pre_save_product(sender, instance, *args, **kwargs):
    print('Before saving product or category')
pre_save.connect(pre_save_product, sender=Product)
pre_save.connect(pre_save_product, sender=Category)

@receiver(post_save, sender=Product)
@receiver(post_save, sender=Category)
def post_save(sender, instance, created, *args, **kwargs):
    if created:
        print('After saving Product or Category')
        subject = 'Update Product or Category'
        message = 'Successfully saved Product or Category'
        from_email = EMAIL_DEFAULT_SENDER
        recipient_list = [user.email for user in User.objects.all()]

        send_mail(subject=subject, message=message, from_email=from_email, recipient_list=recipient_list,
                  fail_silently=False)

@receiver(post_delete, sender=Product)
@receiver(post_delete, sender=Category)
def save_deleted_instance(sender, instance, *args, **kwargs):

    global filename, new_data
    if sender == Product:
        filename = os.path.join(BASE_DIR, 'product/product_data', 'Product.json')
        new_data = {
            'id': instance.id,
            'name': instance.name,
            'price': instance.price,
            'image': str(instance.image),
            'description': instance.description,
            'category': instance.category.title if instance.category else None,
            'quantity': instance.quantity,
        }
    elif sender == Category:
        filename = os.path.join(BASE_DIR, 'product/category_data', 'Category.json')
        new_data = {
            'id': instance.id,
            'title': instance.title,
        }

    if not os.path.exists(filename):
        with open(filename, 'w') as file:
            json.dump([], file)

    with open(filename, 'r+') as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            data = []

        data.append(new_data)
        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()
