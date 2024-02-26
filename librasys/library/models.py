from django.db import models
from django.utils import timezone
# Create your models here.

class Book(models.Model):
    book_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50, null=True)
    author = models.CharField(max_length=50, null=True)
    quantity = models.IntegerField(default=0, null=True)

    def __str__(self):
        return self.title
    

class Member(models.Model):
    member_id = models.AutoField(primary_key=True)
    member_name = models.CharField(max_length=200, null=True)
    member_email = models.EmailField(unique=True, null=True)
    outstanding_debt = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.member_name

    
class BookIssuance(models.Model):
    issuance_id = models.AutoField(primary_key=True, unique=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    issue_date = models.DateField(default=timezone.now)
    return_date = models.DateField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)
    fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.book.title + " is issued to " + self.member.member_name
    
