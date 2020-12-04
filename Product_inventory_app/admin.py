from django.contrib import admin
from .models import ImportInvoice, Stock,  StockHistory

admin.site.register(ImportInvoice)
admin.site.register(Stock)
admin.site.register(StockHistory)


