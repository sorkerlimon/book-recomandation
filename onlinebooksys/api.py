# import requests

# def search_books(query):
#     base_url = 'http://openlibrary.org/search.json'
#     params = {'q': query}

#     response = requests.get(base_url, params=params)
#     if response.status_code == 200:
#         data = response.json()
#         return data.get('docs', [])
#     else:
#         return []

# def get_book_details(book_id):
#     base_url = f'http://openlibrary.org/works/{book_id}.json'

#     response = requests.get(base_url)
#     if response.status_code == 200:
#         return response.json()
#     else:
#         return None
import requests

def search_books_by_title(title):
    url = f'https://www.googleapis.com/books/v1/volumes?q=intitle:{title}'

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get('items', [])
    else:
        return []
    
def search_books_by_author(author):
    url = f'https://www.googleapis.com/books/v1/volumes?q=inauthor:{author}'

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get('items', [])
    else:
        return []

def search_books_by_genre(genre):
    url = f'https://www.googleapis.com/books/v1/volumes?q=subject:{genre}'

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get('items', [])
    else:
        return []

def get_book_details(book_id):
    url = f'https://www.googleapis.com/books/v1/volumes/{book_id}'

    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None
import requests

def search_books_by_multiple_genre(genres):
    all_books = []

    for genre in genres:
        url = f'https://www.googleapis.com/books/v1/volumes?q=subject:{genre}'
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            books = data.get('items', [])

            # Filter books based on rating
            # filtered_books = [book for book in books if book.get('volumeInfo', {}).get('averageRating', 0) >=  4.2]
            filtered_books = [book for book in books if book.get('volumeInfo', {}).get('averageRating', 0) >= 3.5 and book.get('volumeInfo', {}).get('ratingsCount', 0) >= 10]

            all_books.extend(filtered_books)

    return all_books


