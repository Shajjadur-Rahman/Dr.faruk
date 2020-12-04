from celery import shared_task
from time import sleep
from datetime import date
from .models import BalanceSheet, Expense
from Dashboard_app.models import Product
from Product_inventory_app.models import StockHistory


@shared_task
def update_balance_sheet(duration):
    today = date.today()
    current_month_sold = Product.objects.filter(created__month=today.month)
    total_sold = sum(item.total_price for item in current_month_sold)
    total_profit = sum(item.total_profit for item in current_month_sold)
    sold_qty = sum(item.quantity for item in current_month_sold)
    current_month_imported = StockHistory.objects.filter(date__month=today.month)
    total_import = sum(item.total_price for item in current_month_imported)
    import_qty = sum(item.quantity for item in current_month_imported)
    expenses = Expense.objects.filter(created_at__month=today.month)
    total_expense = sum(ex.expense_amount for ex in expenses)

    if today.month == 1:
        try:
            balance = BalanceSheet.objects.get(month='January', year=today.year)
            balance.total_import = total_import
            balance.import_qty = import_qty
            balance.total_sold = total_sold
            balance.sold_qty = sold_qty
            balance.total_expense = total_expense
            balance.total_profit = total_profit
            balance.save()
        except Exception as e:
            balance_obj = BalanceSheet(month='January', total_import=total_import,
                                       import_qty=import_qty, total_sold=total_sold, sold_qty=sold_qty,
                                       total_expense=total_expense, total_profit=total_profit, year=today.year)
            balance_obj.save()
    elif today.month == 2:
        try:
            balance = BalanceSheet.objects.get(month='February', year=today.year)
            balance.total_import = total_import
            balance.import_qty = import_qty
            balance.total_sold = total_sold
            balance.sold_qty = sold_qty
            balance.total_expense = total_expense
            balance.total_profit = total_profit
            balance.save()
        except Exception as e:
            balance_obj = BalanceSheet(month='February', total_import=total_import,
                                       import_qty=import_qty, total_sold=total_sold, sold_qty=sold_qty,
                                       total_expense=total_expense, total_profit=total_profit, year=today.year)
            balance_obj.save()

    elif today.month == 3:
        try:
            balance = BalanceSheet.objects.get(month='March', year=today.year)
            balance.total_import = total_import
            balance.import_qty = import_qty
            balance.total_sold = total_sold
            balance.sold_qty = sold_qty
            balance.total_expense = total_expense
            balance.total_profit = total_profit
            balance.save()
        except Exception as e:
            balance_obj = BalanceSheet(month='March', total_import=total_import,
                                       import_qty=import_qty, total_sold=total_sold, sold_qty=sold_qty,
                                       total_expense=total_expense, total_profit=total_profit, year=today.year)
            balance_obj.save()
    elif today.month == 4:
        try:
            balance = BalanceSheet.objects.get(month='April', year=today.year)
            balance.total_import = total_import
            balance.import_qty = import_qty
            balance.total_sold = total_sold
            balance.sold_qty = sold_qty
            balance.total_expense = total_expense
            balance.total_profit = total_profit
            balance.save()
        except Exception as e:
            balance_obj = BalanceSheet(month='April', total_import=total_import,
                                       import_qty=import_qty, total_sold=total_sold, sold_qty=sold_qty,
                                       total_expense=total_expense, total_profit=total_profit, year=today.year)
            balance_obj.save()
    elif today.month == 5:
        try:
            balance = BalanceSheet.objects.get(month='May', year=today.year)
            balance.total_import = total_import
            balance.import_qty = import_qty
            balance.total_sold = total_sold
            balance.sold_qty = sold_qty
            balance.total_expense = total_expense
            balance.total_profit = total_profit
            balance.save()
        except Exception as e:
            balance_obj = BalanceSheet(month='May', total_import=total_import,
                                       import_qty=import_qty, total_sold=total_sold, sold_qty=sold_qty,
                                       total_expense=total_expense, total_profit=total_profit, year=today.year)
            balance_obj.save()
    elif today.month == 6:
        try:
            balance = BalanceSheet.objects.get(month='June', year=today.year)
            balance.total_import = total_import
            balance.import_qty = import_qty
            balance.total_sold = total_sold
            balance.sold_qty = sold_qty
            balance.total_expense = total_expense
            balance.total_profit = total_profit
            balance.save()
        except Exception as e:
            balance_obj = BalanceSheet(month='June', total_import=total_import,
                                       import_qty=import_qty, total_sold=total_sold, sold_qty=sold_qty,
                                       total_expense=total_expense, total_profit=total_profit, year=today.year)
            balance_obj.save()
    elif today.month == 7:
        try:
            balance = BalanceSheet.objects.get(month='July', year=today.year)
            balance.total_import = total_import
            balance.import_qty = import_qty
            balance.total_sold = total_sold
            balance.sold_qty = sold_qty
            balance.total_expense = total_expense
            balance.total_profit = total_profit
            balance.save()
        except Exception as e:
            balance_obj = BalanceSheet(month='July', total_import=total_import,
                                       import_qty=import_qty, total_sold=total_sold, sold_qty=sold_qty,
                                       total_expense=total_expense, total_profit=total_profit, year=today.year)
            balance_obj.save()
    elif today.month == 8:
        try:
            balance = BalanceSheet.objects.get(month='August', year=today.year)
            balance.total_import = total_import
            balance.import_qty = import_qty
            balance.total_sold = total_sold
            balance.sold_qty = sold_qty
            balance.total_expense = total_expense
            balance.total_profit = total_profit
            balance.save()
        except Exception as e:
            balance_obj = BalanceSheet(month='August', total_import=total_import,
                                       import_qty=import_qty, total_sold=total_sold, sold_qty=sold_qty,
                                       total_expense=total_expense, total_profit=total_profit, year=today.year)
            balance_obj.save()
    elif today.month == 9:
        try:
            balance = BalanceSheet.objects.get(month='September', year=today.year)
            balance.total_import = total_import
            balance.import_qty = import_qty
            balance.total_sold = total_sold
            balance.sold_qty = sold_qty
            balance.total_expense = total_expense
            balance.total_profit = total_profit
            balance.save()
        except Exception as e:
            balance_obj = BalanceSheet(month='September', total_import=total_import,
                                       import_qty=import_qty, total_sold=total_sold, sold_qty=sold_qty,
                                       total_expense=total_expense, total_profit=total_profit, year=today.year)
            balance_obj.save()
    elif today.month == 10:
        try:
            balance = BalanceSheet.objects.get(month='October', year=today.year)
            balance.total_import = total_import
            balance.import_qty = import_qty
            balance.total_sold = total_sold
            balance.sold_qty = sold_qty
            balance.total_expense = total_expense
            balance.total_profit = total_profit
            balance.save()
        except Exception as e:
            balance_obj = BalanceSheet(month='October', total_import=total_import,
                                       import_qty=import_qty, total_sold=total_sold, sold_qty=sold_qty,
                                       total_expense=total_expense, total_profit=total_profit, year=today.year)
            balance_obj.save()

    elif today.month == 11:
        try:
            balance = BalanceSheet.objects.get(month='November', year=str(today.year))
            balance.total_import = total_import
            balance.import_qty = import_qty
            balance.total_sold = total_sold
            balance.sold_qty = sold_qty
            balance.total_expense = total_expense
            balance.total_profit = total_profit
            balance.save()
        except Exception as e:
            balance_obj = BalanceSheet(month='November', total_import=total_import,
                                       import_qty=import_qty, total_sold=total_sold, sold_qty=sold_qty,
                                       total_expense=total_expense, total_profit=total_profit, year=today.year)
            balance_obj.save()
    else:
        try:
            balance = BalanceSheet.objects.get(month='December', year=today.year)
            balance.total_import = total_import
            balance.import_qty = import_qty
            balance.total_sold = total_sold
            balance.sold_qty = sold_qty
            balance.total_expense = total_expense
            balance.total_profit = total_profit
            balance.save()
        except Exception as e:
            balance_obj = BalanceSheet(month='December', total_import=total_import,
                                       import_qty=import_qty, total_sold=total_sold, sold_qty=sold_qty,
                                       total_expense=total_expense, total_profit=total_profit, year=today.year)
            balance_obj.save()

    sleep(duration)
    return None


    # ====================================================

    # celery -A Shop_management worker --pool=solo -l info

    # celery -A Shop_management beat -l info

    # ====================================================
