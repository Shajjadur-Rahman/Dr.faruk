from django.urls import path
from . import views

app_name = 'Inventory'

urlpatterns = [
    path('all-invoice/', views.all_invoice, name='all-invoice'),
    path('hide-invoice/<int:invoice_id>', views.hide_invoice, name='hide-invoice'),
    path('undo-hide-invoice/<int:invoice_id>', views.undo_hide_invoice, name='undo-hide-invoice'),
    path('previous-invoice/', views.view_previous_invoice, name='previous-invoice'),
    path('add-invoice/', views.add_invoice, name='add-invoice'),
    path('edit-invoice/<int:invoice_id>', views.edit_invoice, name='edit-invoice'),
    path('delete-invoice/<int:invoice_id>', views.delete_invoice, name='delete-invoice'),
    path('all-stock-products/', views.all_stock_products, name='all-stock-products'),
    path('add-stock-product/', views.add_stock_product, name='add-stock-product'),
    path('delete-stock-product/<int:product_no>', views.delete_stock_product, name='delete-stock-product'),
    path('stock-product-detail/<int:product_no>/<str:product>', views.stock_product_detail,
         name='stock-product-detail'),
    path('add-existing-product/<int:product_id>', views.add_existing_product,
         name='add-existing-product'),
    path('invoice-product/<int:invoice_id>', views.invoice_related_all_product, name='invoice-product'),
    path('edit-product/<int:product_id>/<int:product_no>', views.edit_product, name='edit-product'),
    path('delete-product/<int:product_id>/<int:product_no>', views.delete_product, name='delete-product'),
    path('product-import-history/', views.product_import_history, name='product-import-history'),
    path('imports-current-year/<year>', views.all_imports_current_year, name='imports-current-year'),
    path('imports-current-month/<month_n>/<month>', views.all_imports_current_month, name='imports-current-month'),
    path('product-import-history-pdf/<p_name>/<supplier>', views.product_import_history_pdf,
         name='product-import-history-pdf'),
    path('import-current-month-pdf/<month_n>/<month>', views.import_current_month_pdf_report,
         name='import-current-month-pdf'),
    path('expense-current-month-pdf/<month_n>/<month>', views.expense_current_month_pdf_report,
         name='expense-current-month-pdf'),

    # stock product report generating
    path('stock_product_report_pdf/', views.stock_product_report_pdf, name='stock_product_report_pdf'),
]
