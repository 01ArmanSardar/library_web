from django.db import models
from Core.models import UserBankAccount
from django.utils import timezone
# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=100)
    slug=models.SlugField(max_length=100,unique=True,null=True,blank=True)


    def __str__(self):
        return f'category Name : {self.name}'
    
class Books(models.Model):
    title=models.CharField(max_length=50)
    content=models.TextField()
    category=models.ManyToManyField(Category)  
    image=models.ImageField(upload_to='upload/',blank=True,null=True) 
    borrowing_price=models.IntegerField()
    user_reviews=models.TextField()

    def __str__(self):
        return f'{self.title}'
    

class Comment(models.Model):
    book=models.ForeignKey(Books,on_delete=models.CASCADE,related_name='comments')
    name=models.CharField(max_length=30)
    email=models.EmailField()
    content=models.TextField()
    date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name}'
    
class BorrowedBook(models.Model):
    book = models.ForeignKey(Books, on_delete=models.CASCADE, related_name='books')
    user = models.ForeignKey(UserBankAccount, on_delete=models.CASCADE, related_name='users')
    created_on = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['created_on']

    def __str__(self) :
        return self.book.title