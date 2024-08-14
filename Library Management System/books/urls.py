from django.urls import path
from . import views
urlpatterns = [
    
    path('add_category/',views.add_category,name='category_add'),
    path('Books/',views.book,name='books'),
    path('category/<slug:category_slug>',views.book,name='category_wise_book'),
    path('details/<int:id>/',views.bookDetailsView.as_view(),name='details'),
    path('borrow/<int:id>',views.BookBorrowView.as_view(),name='borrow'),
    path('borrow_book_lists/',views.BorrowBookListView.as_view(), name='borrow_book_lists'),
    path('return_book/<int:id>/', views.BookReturnView.as_view(), name='return_book'),
    # path('details/<int:pk>/add_comment/', views.bookDetailsView.as_view(), name='add_comment'),

    
]