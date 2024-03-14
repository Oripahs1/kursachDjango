from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('parser/', views.ParserPageView.as_view(), name='parser'),
    path('login/', views.LoginPageView.as_view(), name='login'),
    path('logout/', views.LogoutPageView.as_view(), name='logout'),
    path('registration/', views.RegistrationPageView.as_view(), name='registration'),
    # path('car/', views.CarPageView.as_view(), name='parser'),

]
