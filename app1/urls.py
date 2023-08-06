from django.contrib import admin
from django.urls import path,include
from app1 import views

urlpatterns = [
   
    path('signup',views.Signuppage,name='signup'),
    path('',views.Loginpage,name='login'),
    path('home/',views.Homepage,name='home'),
    path('logout/',views.LogoutPage,name='logout'),



    path('admin_view/',views.admin_view, name="admin_view"),
    path('is_admin/',views.is_admin,name='is_admin'),
    path('index_admin/',views.index_admin,name='index_admin'),
    path('admin_signout/',views.admin_signout,name='admin_signout'),
    path('index_admin/add/',views.add,name='add'),
    path('add_user/',views.add_user,name='add_user'),
    path('index_admin/update/<int:id>/',views.update,name='update'),
    path('index_admin/updatedata/<int:id>/',views.updatedata,name='updatedata'),
    path('index_admin/delete/<int:id>/',views.delete,name='delete'),
    path('index_admin/search',views.search,name='search'),

    
    ]