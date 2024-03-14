from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('parser/', views.ParserPageView.as_view(), name='parser'),
    path('catalog/', views.CatalogPageView.as_view(), name='catalog'),
    # path('car/', views.CarPageView.as_view(), name='parser'),

]