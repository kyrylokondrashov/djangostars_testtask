from bookstore.models import Book
from django.db.models.signals import post_save, pre_save, pre_delete
from django.dispatch import receiver
import datetime


@receiver(post_save, sender=Book)
def create_boom(sender, instance, created,  **kwargs):
    if created:
        f = open('file.txt', 'a+')
        f.write(" New book was created. Fields: id — {}, title — {}, "
                "author — {}, ISBN — {}, price — {}, publish date — {} at {}\n\r"
                .format(instance.id, instance.title, instance.author, instance.ISBN, instance.price,
                instance.publish_date, datetime.datetime.now()))
        f.close()


@receiver(pre_save, sender=Book)
def update_book(sender, instance, **kwargs):
    try:
        t = Book.objects.get(pk = instance.pk)
        f = open('file.txt', 'a+')
        f.write("Book was updated at {}. \n\r Fields was: id — {}, title — {}, "
                "author — {}, ISBN — {}, price — {}, publish date — {}\n\r"
                "Fields become: id — {}, title — {}, "
                "author — {}, ISBN — {}, price — {}, publish date — {}\n\r"
                .format(datetime.datetime.now(),t.id, t.title, t.author, t.ISBN, t.price,
                t.publish_date,instance.id, instance.title, instance.author, instance.ISBN, instance.price,
                instance.publish_date))
        f.close()
    except:
        pass


@receiver(pre_delete, sender=Book)
def delete_book(sender,instance,**kwargs):
    f = open('file.txt', 'a+')
    f.write(" Book was deleted. Fields: id — {}, title — {}, "
            "author — {}, ISBN — {}, price — {}, publish date — {} at {}\n\r"
            .format(instance.id, instance.title, instance.author, instance.ISBN, instance.price,
            instance.publish_date, datetime.datetime.now()))
    f.close()