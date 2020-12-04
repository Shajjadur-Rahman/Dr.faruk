from datetime import datetime
from Dashboard_app.decorators import allowed_users
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.template.loader import get_template
from django.urls import reverse
from xhtml2pdf import pisa

from .models import Stock, StockHistory, ImportInvoice
from Dashboard_app.models import Product
from Product_record_for_final_calculation_app.models import Expense, ExpenseYear
from .forms import StockForm, AddExistingProductForm, EditProductForm, ImportInvoiceForm,\
    EditInvoiceForm, AddInvoiceProductForm
from Product_record_for_final_calculation_app.views import update_balance_sheet, invoice_expense, delete_invoice_expense


@login_required
@allowed_users(allowed_roles=['Admin', 'Accountant', 'Manager'])
def all_invoice(request):
    try:
        invoice = ImportInvoice.objects.filter(active=True).first()
        initial = int(invoice.invoice_no + 1)
    except Exception as e:
        initial = 1
    initial = {'invoice_no': initial}
    invoices = ImportInvoice.objects.filter(active=True)
    form = ImportInvoiceForm(initial=initial)
    search = request.GET.get('invoice_no')
    if search:
        invoices = invoices.filter(
            Q(invoice_no=search)
        )
    context = {'form': form, 'invoices': invoices}
    return render(request, 'inventory/all_invoice.html', context)


@login_required
@allowed_users(allowed_roles=['Admin', 'Accountant', 'Manager'])
def hide_invoice(request, invoice_id):
    url = request.META.get('HTTP_REFERER')
    try:
        invoice = ImportInvoice.objects.get(pk=invoice_id)
    except Exception as e:
        messages.warning(request, 'Query does not exists !!')
        return HttpResponseRedirect(reverse('Inventory:all-invoice'))

    invoice.active = False
    invoice.save()
    return HttpResponseRedirect(url)


@login_required
@allowed_users(allowed_roles=['Admin', 'Accountant', 'Manager'])
def undo_hide_invoice(request, invoice_id):
    url = request.META.get('HTTP_REFERER')
    try:
        invoice = ImportInvoice.objects.get(pk=invoice_id)
    except Exception as e:
        messages.warning(request, 'Query does not exists !!')
        return HttpResponseRedirect(reverse('Inventory:all-invoice'))

    invoice.active = True
    invoice.save()
    return HttpResponseRedirect(url)



@login_required
@allowed_users(allowed_roles=['Admin', 'Accountant', 'Manager'])
def view_previous_invoice(request):
    try:
        invoice = ImportInvoice.objects.all().first()
        initial = int(invoice.invoice_no + 1)
    except Exception as e:
        initial = 1
    initial = {'invoice_no': initial}
    invoices = ImportInvoice.objects.filter(active=False)
    form = ImportInvoiceForm(initial=initial)
    search = request.GET.get('invoice_no')
    if search:
        invoices = invoices.filter(
            Q(invoice_no=search)
        )
    paginator = Paginator(invoices, 20)
    page_number = request.GET.get('page')
    invoices = paginator.get_page(page_number)
    context = {'form': form, 'invoices': invoices}
    return render(request, 'inventory/view_previous_invoice.html', context)





@login_required
@allowed_users(allowed_roles=['Admin', 'Accountant'])
def add_invoice(request):
    form = ImportInvoiceForm()
    if request.method == 'POST':
        date = str(request.POST.get('import_date'))
        format_date = datetime.strptime(date, '%m/%d/%Y %I:%M %p')
        format_month = format_date.month
        format_year = format_date.year
        form = ImportInvoiceForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.invoice_no = int(request.POST['invoice_no'])
            instance.created_by_user = request.user
            instance.date = format_date
            instance.save()
            try:
                year = ExpenseYear.objects.get(year=format_year)
                expense_obj = Expense(year_id=year.pk, month=format_month, invoice_no=instance.invoice_no,
                                      expense_type=instance.import_expense_type,
                                      expense_amount=instance.expense_amount,
                                      created_by=request.user, created_at=instance.date)
                expense_obj.save()
            except Exception as e:
                year_obj = ExpenseYear(year=format_year)
                year_obj.save()
                expense_obj = Expense(year_id=year_obj.pk, month=format_month, invoice_no=instance.invoice_no,
                                      expense_type=instance.import_expense_type,
                                      expense_amount=instance.expense_amount,
                                      created_by=request.user, created_at=instance.date)
                expense_obj.save()
            update_balance_sheet()  # this function called to update balance sheet
            messages.success(request, f'{instance.invoice_no} invoice created !!')
            return HttpResponseRedirect(reverse('Inventory:all-invoice'))
    context = {'form': form}
    return render(request, 'inventory/all_invoice.html', context)


@login_required
@allowed_users(allowed_roles=['Admin', 'Accountant'])
def edit_invoice(request, invoice_id):
    try:
        invoice = ImportInvoice.objects.get(pk=invoice_id)
    except Exception as e:
        messages.warning(request, 'Query does not exists !!!')
        return HttpResponseRedirect(reverse('Inventory:all-invoice'))
    form = EditInvoiceForm(instance=invoice)
    if request.method == 'POST':
        form = EditInvoiceForm(request.POST, instance=invoice)
        if form.is_valid():
            invoice_instance = form.save(commit=False)
            invoice_instance.save()
            invoice_expense(invoice.invoice_no, invoice_instance)  # this function called to update balance sheet
            update_balance_sheet()  # this function called to update balance sheet
            messages.success(request, 'Invoice updated !')
            if invoice.active:
                return HttpResponseRedirect(reverse('Inventory:all-invoice'))
            return HttpResponseRedirect(reverse('Inventory:previous-invoice'))
    context = {'form': form, 'invoice': invoice}
    return render(request, 'inventory/edit_invoice.html', context)


@login_required
@allowed_users(allowed_roles=['Admin'])
def delete_invoice(request, invoice_id):
    url = request.META.get('HTTP_REFERER')
    stock_products = StockHistory.objects.filter(invoice_id=invoice_id)
    if stock_products.exists():
        messages.warning(request, 'You can not delete this invoice , To delete  you have to delete '
                                  'all imported products history  !')
        return HttpResponseRedirect(reverse('Inventory:all-invoice'))
    try:
        invoice = ImportInvoice.objects.get(pk=invoice_id)
    except Exception as e:
        messages.warning(request, 'Query does not exists !')
        return HttpResponseRedirect(url)
    messages.warning(request, f'{invoice.invoice_no} no invoice deleted !')
    delete_invoice_expense(invoice.invoice_no)  # this function called to delete invoice expense which added
    # in Expense Table
    invoice.delete()
    update_balance_sheet()  # this function called to update balance sheet
    return HttpResponseRedirect(url)



@login_required
@allowed_users(allowed_roles=['Admin', 'Accountant', 'Manager'])
def all_stock_products(request):
    products = Stock.objects.all()
    search = request.GET.get("search_product")
    if search:
        products = products.filter(
            Q(product_name__icontains=search)
        )
    context = {'products': products}
    return render(request, 'inventory/all_stock_products.html', context)


@login_required
@allowed_users(allowed_roles=['Admin', 'Accountant', 'Manager'])
def invoice_related_all_product(request, invoice_id):
    try:
        invoice = ImportInvoice.objects.get(pk=invoice_id)
    except Exception as e:
        messages.warning(request, 'Query does not exists !!')
        return HttpResponseRedirect(reverse('Inventory:all-invoice'))
    invoice_products = StockHistory.objects.filter(invoice_id=invoice_id)
    total = invoice_products.count()
    total_amount = sum(item.total_price for item in invoice_products)
    context = {'invoice_products': invoice_products, 'invoice': invoice, 'total': total,
               'total_amount': total_amount}
    return render(request, 'inventory/invoice_related_all_product.html', context)


@login_required
@allowed_users(allowed_roles=['Admin', 'Accountant', 'Manager'])
def all_imports_current_year(request, year):
    products = StockHistory.objects.filter(date__year=year)
    context = {'products': products, 'year': year}
    return render(request, 'inventory/all_imports_current_year.html', context)



@login_required
@allowed_users(allowed_roles=['Admin', 'Accountant', 'Manager'])
def all_imports_current_month(request, month_n, month):
    products = StockHistory.objects.filter(date__month=month)
    context = {'products': products, 'month_n': month_n, 'month': month}
    return render(request, 'inventory/all_imports_current_month.html', context)



@login_required
@allowed_users(allowed_roles=['Admin', 'Accountant', 'Manager'])
def add_stock_product(request):
    invoice = ImportInvoice.objects.filter(active=True).first()
    try:
        stock = Stock.objects.all().first()
        initial = int(stock.product_no + 1)
    except Exception as e:
        initial = 1
    initial = {'product_no': initial, 'invoice': invoice}
    form = StockForm(initial=initial)
    history_form = AddInvoiceProductForm(request.POST or None, initial=initial)
    if request.method == 'POST':
        form = StockForm(request.POST)
        history_form = AddInvoiceProductForm(request.POST)
        if form.is_valid() and history_form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            history_obj = history_form.save(commit=False)
            history_obj.user = request.user
            history_obj.product_name = instance.product_name
            history_obj.product_no = instance.product_no
            history_obj.quantity = instance.quantity
            history_obj.unit_tag = instance.unit_tag
            history_obj.save()
            update_balance_sheet()  # this function called to update balance sheet
            messages.success(request, 'Product added !!')
            return HttpResponseRedirect(reverse('Inventory:all-stock-products'))
        form = StockForm(request.POST)
        history_form = AddInvoiceProductForm(request.POST)
        context = {'form': form, 'history_form': history_form}
        return render(request, 'inventory/add_stock_product.html', context)
    context = {'form': form, 'history_form': history_form}
    return render(request, 'inventory/add_stock_product.html', context)



@login_required
@allowed_users(allowed_roles=['Admin'])
def delete_stock_product(request, product_no):
    url = request.META.get('HTTP_REFERER')
    try:
        product = Stock.objects.get(product_no=product_no)
    except Exception as e:
        messages.warning(request, 'Query does not exists !!')
        return HttpResponseRedirect(url)
    history_products = StockHistory.objects.filter(product_no=product.product_no, active=True)
    if history_products.exists():
        messages.warning(request, 'You can not delete stock product ! To delete stock product.....  '
                                  ' You have to delete import records  !')
        return HttpResponseRedirect(url)
    messages.warning(request, f'{product.product_name} deleted !!')
    product.delete()
    update_balance_sheet()  # this function called to update balance sheet
    return HttpResponseRedirect(url)



@login_required
@allowed_users(allowed_roles=['Admin', 'Accountant', 'Manager'])
def stock_product_detail(request, product_no, product):
    products = StockHistory.objects.filter(product_no=product_no, active=True)
    context = {'products': products, 'product': product}
    return render(request, 'inventory/stock_product_detail.html', context)



@login_required
@allowed_users(allowed_roles=['Admin', 'Accountant', 'Manager'])
def add_existing_product(request, product_id):
    invoice = ImportInvoice.objects.all().first()
    initial = {'invoice': invoice}
    try:
        product = Stock.objects.get(pk=product_id)
    except Exception as e:
        messages.warning(request, 'Product query does not exists !!')
        return HttpResponseRedirect(reverse('Inventory:all-stock-products'))
    form = AddExistingProductForm(initial=initial)
    if request.method == 'POST':
        form = AddExistingProductForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.product_name = product.product_name
            instance.product_no = product.product_no
            instance.unit_tag = product.unit_tag
            product.quantity += instance.quantity
            instance.save()
            product.save()
            update_balance_sheet()  # this function called to update balance sheet
            messages.success(request, f'{product.product_name} quantity updated !!')
            return HttpResponseRedirect(reverse('Inventory:all-stock-products'))
    context = {'form': form, 'product': product}
    return render(request, 'inventory/add_existing_product.html', context)




@login_required
@allowed_users(allowed_roles=['Admin', 'Accountant', 'Manager'])
def edit_product(request, product_id, product_no):
    try:
        history_product = StockHistory.objects.get(pk=product_id)
        qty = history_product.quantity
    except Exception as e:
        messages.warning(request, 'Product query does not exists !!')
        return HttpResponseRedirect(reverse('Inventory:all-stock-products'))
    try:
        stock_product = Stock.objects.get(product_no=product_no)
    except Exception as e:
        messages.warning(request, 'Product query does not exists !!')
        return HttpResponseRedirect(reverse('Inventory:all-stock-products'))
    form = EditProductForm(instance=history_product)
    if request.method == 'POST':
        form = EditProductForm(request.POST, instance=history_product)
        if form.is_valid():
            instance = form.save(commit=False)
            if qty < instance.quantity > 0:
                editable_qty = instance.quantity - qty
                stock_product.quantity += editable_qty
                instance.save()
                stock_product.save()
            elif qty > instance.quantity <= stock_product.quantity and instance.quantity > 0:
                editable_qty = qty - instance.quantity
                stock_product.quantity -= editable_qty
                instance.save()
                stock_product.save()
            elif qty == instance.quantity > 0:
                instance.save()
                messages.success(request, f'{history_product.product_name} updated !!')
                return HttpResponseRedirect(reverse('Inventory:stock-product-detail',
                                                    kwargs={'product_no': stock_product.product_no,
                                                            'product': stock_product.product_name}))
            else:
                error = 'Sorry you submitted invalid qty or submitted qty is greater than stock qty !'
                form = EditProductForm(request.POST)
                context = {'form': form, 'history_product': history_product, 'product_no': stock_product.product_no,
                           'product': stock_product.product_name, 'error': error}
                return render(request, 'Inventory/edit_product.html', context)


            update_balance_sheet()  # this function called to update balance sheet
            messages.success(request, f'{history_product.product_name} updated !!')
            if history_product.invoice.active:
                return HttpResponseRedirect(reverse('Inventory:stock-product-detail',
                                                    kwargs={'product_no': stock_product.product_no,
                                                            'product': stock_product.product_name}))
            else:
                return HttpResponseRedirect(reverse('Inventory:stock-product-detail',
                                                    kwargs={'product_no': stock_product.product_no,
                                                            'product': stock_product.product_name}))
    context = {'form': form, 'history_product': history_product, 'product_no': stock_product.product_no,
               'product': stock_product.product_name}
    return render(request, 'inventory/edit_product.html', context)



@login_required
@allowed_users(allowed_roles=['Admin'])
def delete_product(request, product_id, product_no):
    url = request.META.get('HTTP_REFERER')
    try:
        history_product = StockHistory.objects.get(pk=product_id, product_no=product_no)
        stock_product = Stock.objects.get(product_no=product_no)
    except Exception as e:
        messages.warning(request, 'Product query does not exists !!')
        return HttpResponseRedirect(url)
    sold_products = Product.objects.all()
    if sold_products.exists():
        if stock_product.quantity >= history_product.quantity:
            stock_product.quantity -= history_product.quantity
            stock_product.save()
            messages.warning(request, f'Product {history_product.product_name} deleted !')
            history_product.delete()
            update_balance_sheet()  # this function called to update balance sheet
            return HttpResponseRedirect(url)
        else:
            messages.warning(request, 'You can not delete this product ! No item qty is available to delete in stock !')
            return HttpResponseRedirect(url)
    else:
        if stock_product.quantity >= history_product.quantity:
            stock_product.quantity -= history_product.quantity
            if stock_product.quantity == 0:
                messages.warning(request, f'Product {history_product.product_name} deleted !')
                history_product.delete()
                stock_product.save()
                update_balance_sheet()  # this function called to update balance sheet
                return HttpResponseRedirect(url)
            else:
                messages.warning(request, f'Product {history_product.product_name} deleted !')
                history_product.delete()
                stock_product.save()
                update_balance_sheet()  # this function called to update balance sheet
                return HttpResponseRedirect(url)
        else:
            messages.warning(request, 'Can not deleted ! Product qty is greater than stock qty or invalid qty !!')
            return HttpResponseRedirect(url)






# stock pdf report generating

@login_required
@allowed_users(allowed_roles=['Admin', 'Accountant', 'Manager'])
def stock_product_report_pdf(request):
    s_products = Stock.objects.all()
    now = datetime.now()
    report_date = now.strftime("%d/%m/%Y %I:%M %p")
    report_by = request.user
    context = {
        's_products': s_products,
        'report_date': report_date,
        'report_by': report_by
    }
    template_path = 'report/stock_product_report_pdf.html'
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response




@login_required
@allowed_users(allowed_roles=['Admin', 'Accountant', 'Manager'])
def product_import_history(request):
    products = StockHistory.objects.all()
    paginator = Paginator(products, 20)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    context = {'products': products}
    return render(request, 'inventory/product_import_history.html', context)


@login_required
@allowed_users(allowed_roles=['Admin', 'Accountant', 'Manager'])
def product_import_history_pdf(request, p_name, supplier):
    products = StockHistory.objects.filter(product_name__icontains=p_name, supplier__icontains=supplier)
    total_price = sum(item.total_price for item in products)
    total_qty = sum(item.quantity for item in products)

    now = datetime.now()
    report_date = now.strftime("%d/%m/%Y %I:%M %p")
    report_by = request.user
    context = {
        'report_date': report_date,
        'report_by': report_by,
        'products': products,
        'total_price': total_price,
        'total_qty': total_qty
    }
    template_path = 'report/product_import_history_pdf.html'
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response



@login_required
@allowed_users(allowed_roles=['Admin', 'Accountant', 'Manager'])
def import_current_month_pdf_report(request, month_n, month):
    products = StockHistory.objects.filter(date__month=month)
    total_price = sum(item.total_price for item in products)
    total_qty = sum(item.quantity for item in products)

    now = datetime.now()
    report_date = now.strftime("%d/%m/%Y %I:%M %p")
    report_by = request.user
    context = {
        'report_date': report_date,
        'report_by': report_by,
        'products': products,
        'total_price': total_price,
        'total_qty': total_qty,
        'month_n': month_n
    }
    template_path = 'report/imports_current_month_pdf.html'
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response



@login_required
@allowed_users(allowed_roles=['Admin', 'Accountant', 'Manager'])
def expense_current_month_pdf_report(request, month_n, month):
    expenses = Expense.objects.filter(created_at__month=month)
    total_expense = sum(item.expense_amount for item in expenses)
    now = datetime.now()
    report_date = now.strftime("%d/%m/%Y %I:%M %p")
    report_by = request.user
    context = {
        'report_date': report_date,
        'report_by': report_by,
        'expenses': expenses,
        'total_expense': total_expense,
        'month_n': month_n
    }
    template_path = 'report/expense_current_month_pdf.html'
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
