from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name="book_list"),
    path('book_detail/<int:pk>/', views.book_detail, name="book_detail"),
    path('add_book', views.add_book, name="add_book"),
    path('book_edit/<int:pk>/', views.edit_book, name="edit_book"),
    path('book_delete/<int:pk>/', views.delete_book, name="delete_book"),

    path('members/', views.member_list, name="member_list"),
    path('members/create', views.create_member, name="create_member"),
    path('members/<int:pk>/update/', views.update_member, name="update_member"),
    path('members/<int:pk>/delete/', views.delete_member, name="delete_member"),

    path('issue_book_to_member/', views.issue_book_to_member, name="issue_book_to_member"),
    path('issued_books/', views.issued_books, name="issued_books"),
    path('return_book/<int:issuance_id>/', views.return_book, name="return_book"),

    path('search/', views.search_books, name="search_books"),

]