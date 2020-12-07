from django.urls import path
from . import views

app_name = 'Balance'

urlpatterns = [
    path('balance/', views.balance, name='balance'),
    path('daily-expense-list/', views.daily_expense, name='daily-expense-list'),
    path('expense-in-month/<month_n>/<month>/<year>', views.expense_in_month, name='expense-in-month'),
    path('add-new-expense/', views.add_new_expense, name='add-new-expense'),
    path('delete-expense/<int:ex_id>', views.delete_expense, name='delete-expense'),
    path('profit-calc/<int:year_id>', views.final_profit_calculation, name='profit-calc')
]
