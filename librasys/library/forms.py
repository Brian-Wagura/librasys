from django import forms

from .models import Book, Member


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'quantity']

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['member_name', 'member_email']