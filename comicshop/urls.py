
from django.urls import path


from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('details/<int:pk>/', views.details, name='details'),
    path('product_entry/', views.product_entry, name='product_entry'),
    path('categories/<str:foo>', views.categories, name='categories'),
    path('search/', views.search, name='search'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('update_user/', views.update_user, name='update_user'),
    path('update_password/', views.update_password, name='update_password'),
    path('update_profile/', views.update_profile, name='update_profile'),
]