from django.shortcuts import render,redirect,get_object_or_404
from .import forms
from django.contrib.auth.decorators import user_passes_test
# Create your views here.
from . import models
from django.views.generic import View,ListView
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.contrib import messages
from django.views.generic.detail import DetailView
from django.views.generic import TemplateView
from . models import Books,Category
from .models import BorrowedBook

def book(request,category_slug=None):
    data= Books.objects.all()
    if category_slug is not None:
        # category=Category.objects.get(slug=category_slug)
        category=get_object_or_404(Category,slug=category_slug)
        data=Books.objects.filter(category=category)
    categories=Category.objects.all()
    return render(request,'Bookpage.html',{'data':data,'category':categories})

def my_check(user):
    return user.is_superuser


@user_passes_test(my_check,login_url='homepage', redirect_field_name='next')
def add_category(request):
    if request.method=='POST':
        CategoryForm=forms.categoryForm(request.POST)
        if CategoryForm.is_valid():
            CategoryForm.save()
            return redirect('homepage')
    else:
        CategoryForm=forms.categoryForm()
    return render (request,'add_category.html',{'form_data':CategoryForm})


# class bookDetailsView(DetailView):
#     model = Books 
#     template_name = 'Bookpage.html'
#     context_object_name= 'book'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         book = self.get_object()
#         comments = book.comments.all()
#         context['form'] = forms.CommentForm()
#         context['comments'] = comments
#         return context

#     def post(self, request, *args, **kwargs):
#         book = self.get_object()
#         form = forms.CommentForm(request.POST)

#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.book = book
#             comment.save()
#             return redirect('details', pk=book.id)

        
#         return self.render_to_response(self.get_context_data(form=form))

class bookDetailsView(DetailView):
    model=models.Books
    template_name='details.html'
    pk_url_kwarg='id'

    def post(self,request,*args,**kargs):
        comment_form=forms.ComentForm(data=self.request.POST)
        book=self.get_object()
        if comment_form.is_valid():
            new_comment=comment_form.save(commit=False)
            new_comment.book=book
            new_comment.save()
        return self.get(request,*args,**kargs)
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        books = self.object #book model er object ekhnae store korlam
        comments = books.comments.all()
        # if self.request.method == 'POST':
        #     comment_form=forms.ComentForm(data=self.request.POST)
        #     if comment_form.is_valid():
        #         new_comment=comment_form.save(commit=False)
        #         new_comment.books=books
        #         new_comment.save()
        # comment_form=forms.ComentForm()
        comment_form=forms.ComentForm()
        context['comments'] = comments
        context['comment_form'] = comment_form
        return context

class BookBorrowView(LoginRequiredMixin,View):
    def get(self,request,id, **kwargs):
        book = get_object_or_404(Books, id = id)
        user = self.request.user
        if user.account.balance > book.borrowing_price:
            user.account.balance -= book.borrowing_price
            messages.success(request, 'book borrowed successful')
            user.account.save(update_fields=['balance'])
            BorrowedBook.objects.create(
                book = book,
                user = request.user.account,
                created_on=timezone.now(),
            )
            return redirect ('borrow_book_lists')
        else:
            messages.error(request, 'low balance to borrow the book')
            return redirect('homepage')
        
class BorrowBookListView(LoginRequiredMixin, ListView):
    model = BorrowedBook
    template_name = 'borrowedBook.html'
    context_object_name= 'borrowed_books'

    def get_queryset(self):
        user_id = self.request.user.id
        queryset = BorrowedBook.objects.filter(user__user_id = user_id)
        return queryset
    
class BookReturnView(LoginRequiredMixin, View):
    def get(self,request,id, **kwargs):
        book = get_object_or_404(BorrowedBook, id = id)
        user = self.request.user
        user.account.balance += book.book.borrowing_price
        messages.success(request, 'book return successful')
        user.account.save(update_fields=['balance'])
        # send_email(user,book.book.borrowed_price, 'return_book', 'Book Return Message','transactions/email_template.html')
        book.delete()
        return redirect('borrow_book_lists') 
