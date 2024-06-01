from django.contrib import admin
from django.urls import path
from app1.views import home, login_view, register, about, contacts, documents, accounts, payments, logout, home1, paymenthandler,homepage,notify,setting,webcam_view,main
urlpatterns = [
    path('', home, name='home'),
    path('login/', login_view, name='login_view'),
    path('register/', register, name='register'),
    path('about/', about, name='about'),
    path('contacts/', contacts, name='contacts'),
    path('documents/', documents, name='documents'),
    path('accounts/', accounts, name='accounts'),
    path('logout/', logout, name='logout'),
    path('home1/', home1, name='home1'),
    path('notify/',notify,name='notify'),
    path('homepage/', homepage, name='homepage'),
    path('paymenthandler/', paymenthandler, name='paymenthandler'),
    path('homepage/paymenthandler/', paymenthandler, name='paymenthandler'),
    path('setting/',setting,name='setting'),
    path('webcam_view/', webcam_view, name='webcam_view'),
    path('main/',main,name='main'),
 
    path('admin/', admin.site.urls),
]