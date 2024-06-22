from django.urls import path
from . import views
import os
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('duties/', views.DutiesPageView.as_view(), name='duties'),
    path('duty_new/', views.DutyNewPageView.as_view(), name='duty_new'),
    path('duties/<int:duty_id>', views.DutyPageView.as_view(), name='duty'),

    path('prices/', views.PricesPageView.as_view(), name='prices'),
    path('price_new/', views.PriceNewPageView.as_view(), name='price_new'),
    path('prices/<int:price_id>', views.PricePageView.as_view(), name='price'),

    path('customs_dutys/', views.CustomsDutysPageView.as_view(), name='customs_dutys'),
    path('customs_duty_new/', views.CustomsDutyNewPageView.as_view(), name='customs_duty_new'),
    path('customs_dutys/<int:customs_duty_id>', views.CustomsDutyPageView.as_view(), name='customs_duty'),

    path('excises/', views.ExcisesPageView.as_view(), name='excises'),
    path('excises_new/', views.ExciseNewPageView.as_view(), name='excise_new'),
    path('excises/<int:excise_id>', views.ExcisePageView.as_view(), name='excise'),


    path('', views.HomePageView.as_view(), name='home'),
    path('parser/', views.ParserPageView.as_view(), name='parser'),
    path('login/', views.LoginPageView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),  ##!!!!!
    path('registration/', views.RegistrationPageView.as_view(), name='registration'),
    path('catalog/', views.CatalogPageView.as_view(), name='catalog'),
    path('catalog/car/<int:car_id>', views.CarPageView.as_view(), name='car'),
    path('workers/', views.WorkersPageView.as_view(), name='workers'),
    path('workers/card/<int:worker_id>', views.WorkersCardPageView.as_view(), name='workers_card'),
    path('buhgalter/', views.BuhgalterPageView.as_view(), name='buhgalter'),
    path('buhgalter/invoice/<int:invoice_id>', views.BuhgalterInvoicePageView.as_view(), name='invoice'),
    path('buhgalter/new_invoice', views.BuhgalterNewInvoicePageView.as_view(), name='buhgalter_new_invoice'),

    path('customer/<int:customer_id>', views.CustomerPageView.as_view(), name='customer'),
    path('customers/', views.CustomersPageView.as_view(), name='customers'),
    path('customer_new/', views.CustomerNewPageView.as_view(), name='customer_new'),
    path('customer_new/<int:car_id>', views.CustomerNewPageView.as_view(), name='customer_new_for_order'),

    path('order/<int:car_id>', views.OrderPageView.as_view(), name='order'),
    path('order/<int:car_id>/<int:customer_id>', views.OrderPageView.as_view(), name='order_with_customer'),
    path('orders/', views.OrdersPageView.as_view(), name='orders'),
    path('orders/<int:order_id>', views.OrderInOrdersPageView.as_view(), name='order_in_orders'),
    path('order_photo/<int:order_id>', views.order_photo, name='order_photo'),

    path('transport_companies/', views.TransportCompaniesPageView.as_view(), name='transport_companies'),
    path('transport_company_new/', views.TransportCompanyNewPageView.as_view(), name='transport_company_new'),
    path('transport_companies/<int:transport_company_id>', views.TransportCompanyPageView.as_view(),
         name='transport_company'),

    path('transport_company_prices_new/<int:tk_id>', views.TransportCompanyPricesNewPageView.as_view(),
         name='transport_company_prices_new'),
    path('transport_company_prices/<int:transport_company_prices_id>', views.TransportCompanyPricesPageView.as_view(),
         name='transport_company_prices'),
    path('transport_company_price/<int:price_id>', views.TransportCompanyPricePageView.as_view(),
         name='transport_company_price'),

    path('orders/ajax/', views.orders, name='orders'),
    path('customers/ajax/', views.customers, name='customer'),
    path('transport_companies/ajax/', views.transport_companies, name='transport_companies'),
    path('catalog/ajax/', views.catalog, name='catalog'),
    path('duties/ajax/', views.duties, name='duties'),
    path('customs_dutys/ajax/', views.customs_dutys, name='customs_dutys'),
    path('excises/ajax/', views.excises, name='excises'),
    path('orders/<int:order_id>/download_all_documents/', views.download_all_documents, name='download_all_documents'),
    path('orders/transport/', views.OrderTransportView.as_view(), name='order_transport'),
    path('update_transport_companies/', views.update_transport_companies, name='update_transport_companies'),
]

urlpatterns += static('/media/', document_root=os.path.join(settings.BASE_DIR, 'media'))
