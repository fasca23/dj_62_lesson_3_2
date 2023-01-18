from django.shortcuts import render, redirect
from books.models import Book
from books.converters import DateConverter

def index(request):
    return redirect('books')

def books_view(request):
    books = Book.objects.all().order_by('-pub_date')
    books_new = []
    for book in books:
        books_new.append({'name': book.name, 'author': book.author, 'pub_date': DateConverter().to_url(book.pub_date)})

    template = 'books/books_list.html'
    context = {
        'books': books_new
    }
    return render(request, template, context)

def books_date(request, date):
    
    date_str = DateConverter().to_only_date(date)
    
    books = Book.objects.filter(pub_date=date_str)
    
    min_date = Book.objects.all().order_by('pub_date')[0].pub_date
    max_date = Book.objects.all().order_by('-pub_date')[0].pub_date
    
    if date_str == str(min_date):
        prev_date = None
    else: prev_date = DateConverter().to_url(Book.objects.filter(pub_date__lt=date).order_by('-pub_date').first().pub_date)
        
    if date_str == str(max_date):
        next_date = None
    else: next_date = DateConverter().to_url(Book.objects.filter(pub_date__gt=date).order_by('pub_date').first().pub_date)
       
    print(f'Предыдущая дата ----- {prev_date}')

    print(f'Следующая дата ----- {next_date}')
    
    books_new = []
    for book in books:
        books_new.append({'name': book.name, 'author': book.author, 'pub_date': DateConverter().to_url(book.pub_date)})

    template = 'books/books_date.html'
    context = {
        'books': books_new,
        'next_date': next_date,
        'prev_date': prev_date
    }
    return render(request, template, context)
