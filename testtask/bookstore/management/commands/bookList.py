from django.core.management.base import BaseCommand
from django.utils import timezone
from bookstore.models import Book


class Command(BaseCommand):
    help = 'Displays books list from database'

    def add_arguments(self, parser):
        parser.add_argument('-asc', '--ascendant',action='store_true', default = False,
                            help='Display book list ordered by publish date ascendant')

        parser.add_argument('-desc', '--descendant', action='store_true', default=False,
                            help='Display book list ordered by publish date descendant')


    def handle(self, *args, **kwargs):
        bookList = Book.objects.all()
        if kwargs['ascendant']:
            bookList = bookList.order_by('publish_date')

        if kwargs['descendant']:
            bookList = bookList.order_by('-publish_date')

        for book in bookList:
            self.stdout.write("Book title — {}, Book author - {}, Book ISBN - {}, Book price - {}, Book publish date - {},"
                              .format(book.title,book.author,book.ISBN, book.price,book.publish_date))