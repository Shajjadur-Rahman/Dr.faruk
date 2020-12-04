from django.urls import path
from . import views

app_name = 'Dashboard'

urlpatterns = [
    path('', views.home, name='home'),
    path('today-sell/', views.today_sells, name='today-sell'),
    path('today-due-sell/', views.today_due_sell, name='today-due-sell'),
    path('today-cash-sell/', views.today_cash_sell, name='today-cash-sell'),
    path('all-customer/', views.all_customer, name='all-customer'),
    path('all-shades/<customer>/<int:customer_id>', views.all_shades, name='all-shades'),
    path('create-shade/<customer>/<int:customer_id>', views.create_shade, name='create-shade'),
    path('shade-complete/<int:shade_id>', views.shade_complete, name='shade-complete'),
    path('undo-shade-complete/<int:shade_id>', views.undo_shade_complete, name='undo-shade-complete'),
    path('expired-shades/<customer>/<int:customer_id>', views.expired_shades, name='expired-shades'),
    path('delete-shade/<int:shade_id>/<customer>/<int:customer_id>', views.delete_shade, name='delete-shade'),
    path('customer-purchasing-info/<int:shade_id>/<int:customer_id>',
         views.customer_purchasing_info, name='customer-purchasing-info'),
    path('few-payment/<int:shade_id>/<int:customer_id>/<int:product_id>/<product_name>', views.few_payment, name='few-payment'),
    path('few-payment-history/<shade_num>/<int:shade_id>/<int:customer_id>/<int:product_id>/<customer_name>',
         views.few_payment_history, name='few-payment-history'),
    path('delete-few-payment-history/<int:shade_id>/<int:customer_id>/<int:product_id>/<int:cart_id>',
         views.delete_few_payment_history, name='delete-few-payment-history'),
    path('today-payment/', views.today_payment, name='today-payment'),

    path('sell-product/<int:shade_id>/<str:customer_id>', views.sell_product, name='sell-product'),
    path('edit-sold-product/<int:shade_id>/<int:product_id>/<str:customer_id>', views.edit_sold_product,
         name='edit-sold-product'),
    path('delete-sold-product/<int:shade_id>/<int:product_id>/<int:customer_id>', views.delete_sold_product,
         name='delete-sold-product'),
    path('sold-in-current-month/<month_n>/<month>', views.sold_in_current_month, name='sold-in-current-month'),
    path('create-customer/', views.create_customer, name='create-customer'),
    path('edit-customer/<int:customer_id>', views.edit_customer, name='edit-customer'),
    path('delete-customer/<int:customer_id>', views.delete_customer, name='delete-customer'),


    # report generating path

    path('purchasing_info_pdf_report/<int:shade_id>/<shade_num>/<int:customer_id>', views.purchasing_info_pdf_report,
         name='purchasing_info_pdf_report'),
    path('payment-history-pdf/<shade_num>/<int:shade_id>/<int:customer_id>/<int:product_id>',
         views.payment_history_pdf, name='payment-history-pdf'),

    # creating employee
    path('all-employees/', views.all_employees, name='all-employees'),
    path('create-employee/', views.create_employee, name='create-employee'),
    path('edit-employee/<int:employee_id>', views.edit_employee, name='edit-employee'),
    path('employee-profile/<int:user_id>', views.employee_profile, name='employee-profile'),

]
