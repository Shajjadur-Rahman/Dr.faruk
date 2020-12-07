from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render
from datetime import date, datetime
from .forms import AddNewExpenseForm
from .models import BalanceSheet, BalanceYear, Expense, ExpenseYear
from Dashboard_app.models import Product
from Product_inventory_app.models import StockHistory
from django.contrib.auth.decorators import login_required
from Dashboard_app.decorators import allowed_users



def update_balance_sheet(month, year):
    today = date.today()
    current_month_sold = Product.objects.filter(created__month=month, created__year=year)
    total_sold = round(sum(item.total_price for item in current_month_sold), 2)
    sold_qty = sum(item.quantity for item in current_month_sold)
    current_month_imported = StockHistory.objects.filter(date__month=month, date__year=year)
    total_import = round(sum(item.total_price for item in current_month_imported), 2)
    import_qty = sum(item.quantity for item in current_month_imported)
    expenses = Expense.objects.filter(created_at__month=month, created_at__year=year)
    total_expense = round(sum(ex.expense_amount for ex in expenses), 2)

    try:
        balance_year = BalanceYear.objects.get(year=today.year)
        try:
            balance_sheet = BalanceSheet.objects.get(month=today.month, year_id=balance_year.pk)
            balance_sheet.total_import = total_import
            balance_sheet.import_qty = import_qty
            balance_sheet.total_sold = total_sold
            balance_sheet.sold_qty = sold_qty
            balance_sheet.total_expense = total_expense
            balance_sheet.save()
        except Exception as e:
            balance_obj = BalanceSheet(year_id=balance_year.pk, month=today.month, total_import=total_import,
                                       import_qty=import_qty, total_sold=total_sold, sold_qty=sold_qty,
                                       total_expense=total_expense)
            balance_obj.save()
            return None
    except Exception as e:
        balance_year_obj = BalanceYear(year=today.year)
        balance_year_obj.save()
        try:
            balance_sheet = BalanceSheet.objects.get(month=today.month, year_id=balance_year_obj.pk)
            balance_sheet.total_import = total_import
            balance_sheet.import_qty = import_qty
            balance_sheet.total_sold = total_sold
            balance_sheet.sold_qty = sold_qty
            balance_sheet.total_expense = total_expense
            balance_sheet.save()
        except Exception as e:
            balance_obj = BalanceSheet(year_id=balance_year_obj.pk, month=today.month, total_import=total_import,
                                       import_qty=import_qty, total_sold=total_sold, sold_qty=sold_qty,
                                       total_expense=total_expense)
            balance_obj.save()
        return None


def invoice_expense(invoice_no, invoice_instance):
    expense = Expense.objects.get(invoice_no=invoice_no)
    expense.expense_type = invoice_instance.import_expense_type
    expense.expense_amount = invoice_instance.expense_amount
    expense.save()
    return None


def delete_invoice_expense(invoice_no):
    expense = Expense.objects.get(invoice_no=invoice_no)
    expense.delete()
    return None



@login_required
@allowed_users(allowed_roles=['Admin'])
def balance(request):
    years = BalanceYear.objects.all()
    paginator = Paginator(years, 4)
    page_number = request.GET.get('page')
    years = paginator.get_page(page_number)
    context = {'years': years}
    return render(request, 'balance_sheet/balance.html', context)


@login_required
@allowed_users(allowed_roles=['Admin', 'Accountant', 'Manager'])
def daily_expense(request):
    form = AddNewExpenseForm()
    expenses = ExpenseYear.objects.all()
    paginator = Paginator(expenses, 1)
    page_number = request.GET.get('page')
    expenses = paginator.get_page(page_number)
    context = {'expenses': expenses, 'form': form}
    return render(request, 'balance_sheet/daily_expense.html', context)




@login_required
@allowed_users(allowed_roles=['Admin', 'Accountant', 'Manager'])
def expense_in_month(request, month_n, month, year):
    form = AddNewExpenseForm()
    expenses = Expense.objects.filter(month=month, created_at__year=year)
    context = {'expenses': expenses, 'month_n': month_n, 'month': month, 'year': year, 'form': form}
    return render(request, 'balance_sheet/expense_in_month.html', context)


@login_required
@allowed_users(allowed_roles=['Admin', 'Accountant', 'Manager'])
def add_new_expense(request):
    url = request.META.get('HTTP_REFERER')
    form = AddNewExpenseForm()
    if request.method == 'POST':
        expense_date = str(request.POST.get('expense_date'))
        format_date = datetime.strptime(expense_date, '%m/%d/%Y %I:%M %p')
        form = AddNewExpenseForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.month = format_date.month
            instance.created_by = request.user
            try:
                year_obj = ExpenseYear.objects.get(year=format_date.year)
                instance.year_id = year_obj.pk
                instance.created_at = format_date
                instance.save()
            except Exception as e:
                year_obj = ExpenseYear(year=format_date.year)
                year_obj.save()
                instance.year_id = year_obj.pk
                instance.created_at = format_date
                instance.save()

            update_balance_sheet(instance.created_at.month, instance.created_at.year)  # this function called to update balance sheet
            messages.success(request, 'Expense added !')
            return HttpResponseRedirect(url)
    context = {'form': form}
    return render(request, 'balance_sheet/add_new_expense.html', context)


@login_required
@allowed_users(allowed_roles=['Admin'])
def delete_expense(request, ex_id):
    url = request.META.get('HTTP_REFERER')
    try:
        expenses = Expense.objects.get(pk=ex_id)
        expenses_date = expenses.created_at
    except Exception as e:
        messages.warning(request, 'Query does not exists !!')
        return HttpResponseRedirect(url)


    if expenses.invoice_no is not None:
        expense = Expense.objects.get(invoice_no=expenses.invoice_no)
        if expense:
            messages.warning(request, 'Sorry you can not delete this expenditure !! '
                                      'This expense related to product import invoice !!')
            return HttpResponseRedirect(url)
    expenses.delete()
    update_balance_sheet(expenses_date.month, expenses_date.year)  # this function called to update balance sheet
    messages.warning(request, 'Expense deleted !!')
    return HttpResponseRedirect(url)




@login_required
@allowed_users(allowed_roles=['Admin', 'Accountant', 'Manager'])
def final_profit_calculation(request, year_id):
    url = request.META.get('HTTP_REFERER')
    try:
        year = BalanceYear.objects.get(pk=year_id)
    except Exception as e:
        messages.warning(request, 'Query does not exists !!')
        return HttpResponseRedirect(url)

    year.save()
    return HttpResponseRedirect(url)
