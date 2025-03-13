from django.urls import path, include

from . import views

urlpatterns = [
    path('payment_process/', views.payment_process, name='payment_process'),
    path('checkout/', views.checkout, name='checkout'),
    path('billing_info/', views.billing_info, name='billing_info'),
    path('process_order/', views.process_order, name='process_order'),
    path('unshipped', views.dashboard_outstanding, name='outstanding'),
    path('shipped', views.dashboard_shipped, name='shipped'),
    path('orders/<int:pk>', views.orders, name='orders'),
]