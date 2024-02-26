from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.http import HttpResponse

from datetime import datetime

from .models import Book, Member, BookIssuance
from .forms import BookForm, MemberForm

from .utils import calculate_fee

# Create your views here.

def book_list(request):
    books = Book.objects.all()
    return render(request, 'book_list.html', {'books': books })

def book_detail(request, pk):
    book = Book.objects.get(pk=pk)
    return render(request, 'book_detail.html', {'book': book })

def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("book_list")
    else:
        form = BookForm()
    
    return render(request, 'book_add.html', {'form': form })

def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'book_edit.html', { 'form': form, 'pk': pk })

def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'book_delete.html', {'book': book})


def member_list(request):
    members = Member.objects.all()
    return render(request, 'member_list.html', {'members': members})

def members_and_borrowed_books(request):
    members = Member.objects.all()
    return render(request, 'members_and_books.html', {'members': members})

def create_member(request):
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('member_list')
    else:
        form = MemberForm()
    return render(request, 'create_member.html', { 'form': form})

def update_member(request, pk):
    member = get_object_or_404(Member, pk=pk)
    if request.method == 'POST':
        form = MemberForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            return redirect('member_list')
    else:
        form = MemberForm(instance=member)
    return render(request, 'update_member.html', {'form': form, 'pk': pk })

def delete_member(request, pk):
    member = get_object_or_404(Member, pk=pk)
    if request.method == 'POST':
        member.delete()
        return redirect('member_list')
    return render(request, 'member_delete.html', {'member': member})

def issue_book_to_member(request):
    error_message = None
    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        member_id = request.POST.get('member_id')

        if not book_id or not member_id:
            return HttpResponse("Invalid request: book_id and member_id are required.")
        
        book = get_object_or_404(Book, pk=book_id)
        member = get_object_or_404(Member, pk=member_id)

        if member.outstanding_debt <= 500:
            if book.quantity > 0:
                issuance = BookIssuance(book=book, member=member)
                issuance.save()
                book.quantity -= 1
                book.save() 
                return redirect("issued_books")
            else:
                return ("Sorry, the selected book is not available for issuance.")
        else: 
            error_message = f"{member.member_name} outstanding debt is {member.outstanding_debt} which exceeds KES.500.\
            Cannot issue the book - {book.title} by {book.author}."

    books = Book.objects.all()        
    members = Member.objects.all()
    return render(request, 'issue_book_to_member.html', {"books": books, "members": members, 'error_message': error_message })


def issued_books(request):
    issued_books = BookIssuance.objects.all()
    return render(request, "issued_books.html", {"issued_books": issued_books})

def return_book(request, issuance_id):
    issuance = get_object_or_404(BookIssuance, pk=issuance_id)
    error_message = None
    
    if request.method == 'POST':
        return_date_str = request.POST.get('return_date')
        return_date = datetime.strptime(return_date_str, '%Y-%m-%d').date()
        fee = calculate_fee(issuance.issue_date, return_date)

        if issuance.member.outstanding_debt <= 500:
            issuance.return_date = return_date
            issuance.is_returned = True
            issuance.fee = fee
            issuance.save()


            issuance.member.outstanding_debt += fee
            issuance.member.save()

            issuance.delete()
            return redirect('issued_books')
        else: 
            error_message = f"{issuance.member.member_name} outstanding debt is  {issuance.member.outstanding_debt} which exceeds KES.500.\
                  Cannot return the book - {issuance.book.title} by {issuance.book.author}."
    return render(request, 'return_book.html', {'issuance': issuance, 'error_message': error_message, 'issuance_id': issuance_id })


def search_books(request):
    query = request.GET.get('q')
    if query:
        results = Book.objects.filter(title__icontains=query) | Book.objects.filter(author__icontains=query)
    else:
        results = Book.objects.none()
    return render(request, 'search_results.html', {'books': results })
