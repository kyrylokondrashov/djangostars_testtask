from django.db import models
import datetime
from django.urls import reverse
from django.contrib.auth.models import User


# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey('Author',on_delete=models.CASCADE)
    ISBN = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    publish_date = models.DateField(default=datetime.datetime.today().strftime('%Y-%m-%d'))

    def __str__(self):
        return "{}".format(self.title)

    def get_absolute_url(self):
        return reverse('bookstore-bookinfo', kwargs={'pk': self.pk})


class Author(models.Model):
    name = models.CharField(max_length=25)
    surname = models.CharField(max_length=25)

    def __str__(self):
        return "{}.{}".format(self.name[0],self.surname)

    def get_absolute_url(self):
        return reverse('bookstore-authorinfo', kwargs={'pk': self.pk})


class Requests(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    path = models.CharField(max_length=1000)
    method = models.CharField(max_length=50)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    post = models.TextField(blank=True, null=True)