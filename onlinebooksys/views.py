from django.shortcuts import render,HttpResponse
from django.utils.html import strip_tags
from django.shortcuts import render
from .api import *
from django.contrib.auth.decorators import login_required
from .models import *
import random


def mainpage(request):
    return render(request, 'landing.html')

@login_required(login_url='login')
def dashboard(request):
    user = request.user.user_profile
    books = Bookmodel.objects.filter(p_user=user)
    total = Bookmodel.objects.filter(p_user=user).count()
    planning = Bookmodel.objects.filter(p_user=user, bookstatus="Planning To Read").count()
    finished = Bookmodel.objects.filter(p_user=user, bookstatus="Finished Reading").count()
    genre = ""

    for book in books:
        genre = book.bookgenre + ", " + genre
    genre = (genre[:-2])
    unique_genre = genre.split(", ")
    unique_genre = list(set(unique_genre))
    rec_books = search_books_by_multiple_genre(unique_genre)
    random.shuffle(rec_books)

    if len(rec_books) >= 5:
        random_books = random.sample(rec_books, 5)
    else:
        random_books = rec_books
    
    book1 = random_books[0]
    book2 = random_books[1]
    book3 = random_books[2]
    book4 = random_books[3]
    book5 = random_books[4]

    Data = {'books':books, 'total': total, 'planning': planning, 'finished': finished, 
            'book1':book1, 'book2':book2, 'book3':book3, 'book4':book4, 'book5':book5}

    return render(request, 'dashboard.html', Data)

@login_required(login_url='login')
def search_view(request):
    query = None
    if request.method == 'GET':
        query = request.GET.get('q')
        if query is None:
            return render(request, 'search.html')
        else:
            search_type = request.GET.get('customRadioInline1')
            if search_type == 'title':
                search_results = search_books_by_title(query)
            elif search_type == 'author':
                search_results = search_books_by_author(query)
            else:
                search_results = search_books_by_genre(query)
            books = []
            for book in search_results:
                book_id = book['id']
                book_details = get_book_details(book_id)
                title = book_details['volumeInfo'].get('title', 'No Title')
                genre = ', '.join(book_details['volumeInfo'].get('categories', []))
                author = ', '.join(book_details['volumeInfo'].get('authors', ['No Author']))
                publish_date = book_details['volumeInfo'].get('publishedDate', 'Unknown')[:4] if 'publishedDate' in book_details['volumeInfo'] else 'Unknown'
                description = book_details['volumeInfo'].get('description', 'No Description')
                description = strip_tags(description)
                books.append({'title': title, 'author': author, 'description': description, 'book_id': book_id, 'publish_date': publish_date, 'genre': genre})
            # print(query)
            return render(request, 'search.html', {'books': books, 'query': query, 'book_details': book_details})
        
@login_required(login_url='login')
def book_details_view(request, book_id):
    book = get_book_details(book_id)
    user = request.user.user_profile
    if request.method == 'POST':
        rating = request.POST.get('customRadioInline1')
        status = request.POST.get('gridRadios')
        id = book['id']
        title = book['volumeInfo'].get('title')       
        genre = ', '.join(book['volumeInfo'].get('categories', []))
        genre = genre.replace('/', ', ')
        genre = genre.replace('  ', ' ')
        genre = genre.replace(' ,', ',')
        avgrating = book['volumeInfo'].get('averageRating', 0)
        vote_count = book['volumeInfo'].get('ratingsCount', 0)
        existing_book = Bookmodel.objects.filter(p_user=user, bookid=id).first()
        if existing_book:
            # existing_book.bookname = title
            existing_book.bookstatus = status
            existing_book.bookrating = rating
            existing_book.save()
        else:
            obj = Bookmodel(p_user=user, bookname=title, bookid=id, bookstatus=status, bookrating=rating, bookgenre=genre,
                            bookoverallrating=avgrating, bookvote= vote_count)
            obj.save()  
    return render(request, 'book_details.html', {'book': book, 'book_id': book_id})
        


