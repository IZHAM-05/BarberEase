# BarberEaseApp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name='home'),

    # auth
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('signup/customer/', views.signup_customer, name='signup_customer'),
    path('signup/owner/', views.signup_owner, name='signup_owner'),

    # admin
    path('admin_home/', views.Admin_home, name='Admin_home'),
    path('approve_shop/<int:shop_id>/', views.approve_shop, name='approve_shop'),
    path('reject_shop/<int:shop_id>/', views.reject_shop, name='reject_shop'),
    path("manage_shops/", views.manage_shops, name="manage_shops"),
    path('admin_shop/<int:shop_id>/', views.admin_shop_detail, name='admin_shop_detail'),
    path("manage_customers/", views.manage_customers, name="manage_customers"),
    path("customer/<int:customer_id>/", views.customer_detail, name="customer_detail"),


    # owner
    path('shopowner_home/', views.ShopOwner_home, name='shopowner_home'),
    path('owner/add_service/', views.add_service, name='add_service'),
    path('owner/approve_appointment/<int:appointment_id>/', views.approve_appointment, name='approve_appointment'),
    path('owner/reject_appointment/<int:appointment_id>/', views.reject_appointment, name='reject_appointment'),
    path("shop/images/", views.manage_shop_images, name="manage_shop_images"),
    path("manage_appointments/", views.manage_appointments, name="manage_appointments"),
    path("owner/<int:shop_id>/services/", views.manage_services, name="manage_services"),
    path("shopowner/<int:shop_id>/", views.shop_detail, name="shop_detail"),
    path('owner/complete_appointment/<int:appointment_id>/', views.complete_appointment, name='complete_appointment'),
    path("owner/appointments/", views.owner_appointments, name="owner_appointments"), 
    path("owner/reports/", views.owner_reports, name="owner_reports"),

    
    # customer
    path('customer_home/', views.Customer_home, name='customer_home'),
    path("customer/profile/", views.customer_profile, name="customer_profile"),
    path('book/<int:shop_id>/<int:service_id>/', views.book_appointment, name='book_appointment'),
    path('review/add/<int:shop_id>/', views.add_review, name='add_review'),
    path("reports/", views.reports, name="reports"),
    path("shop/<int:shop_id>/", views.shop_detail_customer, name="shop_detail_customer"),
    path('shops/', views.shop_list, name='shop_list'),  

]
