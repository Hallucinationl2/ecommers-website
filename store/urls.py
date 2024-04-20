from django.urls import path
from . import views
from .views import LoginUserView, LogoutUserView


urlpatterns = (
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('product/<int:pk>', views.product, name='product'),
    path('category/<str:slug>', views.category, name='category',),
    path('category_summary/', views.category_summary, name='category_summary',),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('register/', views.register_user, name='register'),
    path('update_user/', views.update_user, name='update_user'),
    path('update_info/', views.update_info, name='update_info'),
    path('update_password/', views.update_password, name='update_password'),
    path('search/', views.search, name='search'),

)
