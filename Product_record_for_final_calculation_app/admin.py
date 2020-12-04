from django.contrib import admin
from .models import BalanceSheet, BalanceYear, Expense, ExpenseYear

admin.site.register(BalanceSheet)
admin.site.register(BalanceYear)
admin.site.register(Expense)
admin.site.register(ExpenseYear)
