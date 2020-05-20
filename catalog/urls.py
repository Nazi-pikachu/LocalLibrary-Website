from django.urls import path
from .import views
urlpatterns = [
    path('',views.index,name='index'),
    path('books/', views.BookListView.as_view(), name="books"),
    path('authors/',views.AuthorListView.as_view(),name="authors"),
    path('authors/<int:pk>',views.AuthorDetailView.as_view(),name="author-detail"),
    path('books/<int:pk>', views.BookDetailView.as_view(),name="book-detail"),
    path('mybooks/',views.LoanedBooksByUserListView.as_view(), name='my-borrowed'), 
    path('borrowedbooks/',views.BorrowedBooksListView.as_view(),name='borrowedBooks'),
    path('book/<uuid:pk>',views.renew_book_librarian, name='renew-book-librarian'),
    path('authors/create',views.AuthorCreate.as_view(),name='author_create'),
    path('authors/<int:pk>/update',views.AuthorUpdate.as_view(),name='author_update'),
    path('authors/<int:pk>/delete',views.AuthorDelete.as_view(),name='author_delete')
   
]
