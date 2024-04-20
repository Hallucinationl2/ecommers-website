from django.urls import path
from . import views
from .views import CartSummaryView, CartUpdateView, CartAddView

urlpatterns = [
    path('', CartSummaryView.as_view(), name='cart_summary'),
    path('add/', CartAddView.as_view(), name='cart_add'),
    path('delete/', views.cart_delete, name='cart_delete'),
    path('update', CartUpdateView.as_view(), name='cart_update'),
]