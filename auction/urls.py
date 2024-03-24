from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('parser/', views.ParserPageView.as_view(), name='parser'),
    path('login/', views.LoginPageView.as_view(), name='login'),
    path('logout/', views.LogoutPageView.as_view(), name='logout'),
    path('registration/', views.RegistrationPageView.as_view(), name='registration'),
    path('catalog/', views.CatalogPageView.as_view(), name='catalog'),
    path('catalog/car/<int:car_id>', views.CarPageView.as_view(), name='car'),
    path('workers/', views.WorkersPageView.as_view(), name='workers'),
    path('workers/card/<int:worker_id>', views.WorkersCardPageView.as_view(), name='workers_card'),
    path('buhgalter/', views.BuhgalterPageView.as_view(), name='buhgalter'),
    path('buhgalter/invoice/<int:invoice_id>', views.BuhgalterInvoicePageView.as_view(), name='invoice'),
    path('buhgalter/new_invoice', views.BuhgalterNewInvoicePageView.as_view(), name='buhgalter_new_invoice'),
]