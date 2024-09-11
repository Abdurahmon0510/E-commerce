import json
import os
from django.core.mail import send_mail
from django.db.models.signals import post_save, pre_save, pre_delete, post_delete
from django.dispatch import receiver



from config.settings import EMAIL_DEFAULT_SENDER, BASE_DIR
from customer.models import User

from .models import Author, Book


def pre_save_author(sender, instance, *args, **kwargs):
    print('Before saving author')
pre_save.connect(pre_save_author, sender=Author)


@receiver(post_save, sender=Author)
def post_save_author(sender, instance, created, *args, **kwargs):
    if created:
        print('After saving author')
        subject = 'Update Author'
        message = 'successfully saved author'
        from_email = EMAIL_DEFAULT_SENDER
        recipient_list = [user.email for user in User.objects.all()]

        send_mail(subject=subject, message=message, from_email=from_email, recipient_list=recipient_list,
                  fail_silently=False)



# AWS =>  Amazon Web Services
# Nginx => Gunicorn
@receiver(pre_delete, sender=Author)
def pre_delete_author(sender, instance, *args, **kwargs):
    print('Before deleting author')


@receiver(post_delete, sender=Author)
@receiver(post_delete, sender=Book)
def save_deleted_instance(sender, instance, *args, **kwargs):
    global new_data, filename
    if sender == Author:
        filename = os.path.join(BASE_DIR, 'app/Author_data', 'Author.json')
        new_data = {
            'id': instance.id,
            'name': instance.name,
        }
    elif sender == Book:
        filename = os.path.join(BASE_DIR, 'app/Book_data', 'Book.json')
        new_data = {
            'id': instance.id,
            'title': instance.name,
            'author': instance.author.name,
            'description': instance.description,
            'price': instance.price,
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