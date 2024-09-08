from django.shortcuts import render
from django.db.models import Min, Max, Avg, Count
from app.models import Author, Book

def book_list(request):
    authors = Author.objects.annotate(
        books_count=Count('books'),
        max_price=Max('books__price'),
        min_price=Min('books__price'),
        avg_min_price=Avg('books__price')
    )

    books = Book.objects.annotate(
        min_price=Min('price')
    ).filter(min_price__gt=5000).order_by('-min_price')

    context = {
        'books': books,
        'authors': authors
    }

    return render(request, 'app/index.html', context)
