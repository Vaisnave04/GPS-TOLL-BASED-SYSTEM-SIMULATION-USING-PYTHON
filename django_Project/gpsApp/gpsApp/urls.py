"""
URL configuration for gpsApp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from gpsTollApp import views
from django.urls import get_resolver

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home),   
    path('home_page',views.home, name='home_page'),
    path('logout_btn',views.home),
    path('register_action', views.register_action, name='register_action'),
    path('success_page', views.success_page, name='success_page'),
    path('login_action',views.login_action,name='login_action'),
    path('login', views.login, name="login"),
    path('admin', views.admin, name="admin"),
    path('user/', views.user_list, name='user_list'),
    path('register', views.register, name="register"),
    path('main_view', views.main_view, name='main_view'),
    path('top/', views.top_frame, name='top_frame'),
    path('mid/viewhistory/', views.choose, name="choose"),
    path('Simulate/', views.Simulate, name="Simulate"),
    path('display_map', views.display_map, name='display_map'),
    path('simulate_vehicle', views.simulate_vehicle, name='simulate_vehicle'),
    path('map/', views.display_map, name='display_map'),
    path('viewhistory', views.viewhistory, name='viewhistory'),
    path('vehicle_category', views.vehicle_category, name='vehicle_category'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('paymentpg/', views.paymentpg, name='paymentpg'),
    path('user/', views.user, name='user'),
    path('report_pass/', views.report_pass, name='report_pass'),
    path('pass_vehicle/', views.pass_vehicle, name='pass_vehicle'),
    path('changepassword/', views.changepassword, name='changepassword'),
    path('report_receipt/', views.report_receipt, name='report_receipt'),
    path('editPass/', views.editPass, name='editPass'),
    path('deletePass/', views.deletePass, name='deletePass'),
    path('chart-data/', views.chart_data, name='chart_data'),
]

# Debugging code to print URL patterns
resolver = get_resolver()
print("URL patterns:", resolver.reverse_dict.keys())