from django.shortcuts import render, HttpResponseRedirect, reverse
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q

from .forms import ProductForm, EditProductForm, CustomerForm, SellInfoForm, ShadeNoForm, EditEmployeeForm
from .models import Customer, Product, PaymentCart, ShadeNo
from Product_inventory_app.models import Stock
from datetime import date, timedelta
from django.contrib.auth.decorators import login_required
from .decorators import allowed_users
from datetime import datetime

from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

from Login_app.forms import ProfileForm, SignUpForm
from Login_app.models import User
from Product_record_for_final_calculation_app.views import update_balance_sheet


@login_required
@allowed_users(allowed_roles=['Admin', 'Accountant', 'Manager'])
def purchasing_info_pdf_report(request, shade_id, shade_num, customer_id):
    customer = None
    try:
        customer = Customer.objects.get(pk=customer_id)
        payment_cart = customer.payments.all()
        products = Product.objects.filter(customer_id=customer_id, active=True)
        due_products = Product.objects.filter(customer_id=customer_id, active=True, shade_id=shade_id,
                                              sell_status='Due')
        total_paid = sum(item.paid_amount for item in payment_cart)
        total_pro = sum(item.total_price for item in products)
        total_due = sum(due_item.total_price for due_item in due_products)
        due_remaining = total_pro - total_paid
    except:
        total_pro = 0
        total_due = 0
        total_paid = 0
        due_remaining = 0

    now = datetime.now()
    report_date = now.strftime("%d/%m/%Y %I:%M %p")
    report_by = request.user
    context = {'total_pro': total_pro, 'shade_num': shade_num, 'total_paid': total_paid, 'due_remaining': due_remaining,
               'products': products, 'customer': customer, 'total_due': total_due, 'report_date': report_date,
               'report_by': report_by}

    template_path = 'report/purchasing_info_pdf.html'
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
def payment_history_pdf(request, shade_num, shade_id, customer_id, product_id):
    try:
        product = Product.objects.get(pk=product_id, shade_id=shade_id)
    except Exception as e:
        messages.warning(request, 'Product item not found')
        return HttpResponseRedirect(reverse('Dashboard:customer-purchasing-info',
                                            kwargs={'shade_id': shade_id, 'customer_id': customer_id}))

    payment_carts = PaymentCart.objects.filter(customers_id=customer_id, products_id=product)
    total_paid_amount = sum(item.paid_amount for item in payment_carts)

    now = datetime.now()
    report_date = now.strftime("%d/%m/%Y %I:%M %p")
    report_by = request.user

    context = {
        'payment_carts': payment_carts,
        'total_paid_amount': total_paid_amount,
        'shade_num': shade_num,
        'product': product,
        'report_date': report_date,
        'report_by': report_by
    }
    template_path = 'report/payment_history_pdf.html'
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


# total price counting function !
def total_paid_price_counting(data):
    value = 0
    for payment in data:
        if payment.display_choice == 'show':
            value += payment.paid_amount
    return value


def home(request):
    today = date.today()
    previous_month = date.today().replace(day=1) - timedelta(days=1)
    today_sell_products = Product.objects.select_related('shade', 'customer', 'select_product').filter(
        created__day=today.day)
    today_due_sell_products = Product.objects.select_related('shade', 'customer', 'select_product').filter(
        created__day=today.day, sell_status='Due')
    current_month_sell_products = Product.objects.select_related('shade', 'customer', 'select_product').filter(
        created__month=today.month)
    current_month_due_sell_products = Product.objects.select_related('shade', 'customer', 'select_product').filter(
        created__month=today.month, sell_status='Due')
    current_year_sell_products = Product.objects.filter(created__year=today.year)
    current_year_due_sell_products = Product.objects.select_related('shade', 'customer', 'select_product').filter(
        created__year=today.year, sell_status='Due')
    prev_month_sell_products = Product.objects.select_related('shade', 'customer', 'select_product').filter(
        created__month=previous_month.month)
    prev_month_due_sell_products = Product.objects.select_related('shade', 'customer', 'select_product').filter(
        created__month=previous_month.month, sell_status='Due')
    stock_products = Stock.objects.select_related('invoice').all().order_by('quantity')
    total_stock_products = Stock.objects.select_related('invoice').all().count()

    today_total_sell = sum(item.total_price for item in today_sell_products)
    current_month_total_sell = sum(item.total_price for item in current_month_sell_products)
    prev_month_sell = sum(item.total_price for item in prev_month_sell_products)
    current_year_sell = sum(item.total_price for item in current_year_sell_products)

    today_total_due_sell = sum(item.total_price for item in today_due_sell_products)
    current_month_due_total_sell = sum(item.total_price for item in current_month_due_sell_products)
    prev_month_due_sell = sum(item.total_price for item in prev_month_due_sell_products)
    current_year_due_sell = sum(item.total_price for item in current_year_due_sell_products)

    today_cash_sale = today_total_sell - today_total_due_sell
    current_month_cash_sale = current_month_total_sell - current_month_due_total_sell
    prev_month_cash_sale = prev_month_sell - prev_month_due_sell
    current_year_cash_sale = current_year_sell - current_year_due_sell

    stock_search = request.GET.get('stock_search')
    if stock_search:
        stock_products = stock_products.filter(
            Q(product_name__icontains=stock_search)
        )
    paginator = Paginator(stock_products, 20)
    page_number = request.GET.get('page')
    stock_products = paginator.get_page(page_number)
    context = {
        'today_total_sell': today_total_sell,
        'current_month_total_sell': current_month_total_sell,
        'prev_month_sell': prev_month_sell,
        'current_year_sell': current_year_sell,

        'today_total_due_sell': today_total_due_sell,
        'current_month_due_total_sell': current_month_due_total_sell,
        'prev_month_due_sell': prev_month_due_sell,
        'current_year_due_sell': current_year_due_sell,

        'today_cash_sale': today_cash_sale,
        'current_month_cash_sale': current_month_cash_sale,
        'prev_month_cash_sale': prev_month_cash_sale,
        'current_year_cash_sale': current_year_cash_sale,

        'today': today,
        'previous_month': previous_month,
        'stock_products': stock_products,
        'total_stock_products': total_stock_products
    }

    return render(request, 'dashboard_app/home.html', context)


@login_required
@allowed_users(allowed_roles=['Admin', 'Accountant', 'Manager'])
def today_sells(request):
    today = date.today()
    products = Product.objects.filter(created__day=today.day)
    total_sell = sum(item.total_price for item in products)
    context = {'products': products, 'today': today, 'total_sell': total_sell}
    return render(request, 'dashboard_app/today_sells.html', context)


@login_required
@allowed_users(allowed_roles=['Admin', 'Accountant', 'Manager'])
def today_due_sell(request):
    today = date.today()
    due_products = Product.objects.filter(created__day=today.day, sell_status='Due')
    total_due_sell = sum(item.total_price for item in due_products)
    context = {'due_products': due_products, 'today': today, 'total_due_sell': total_due_sell}
    return render(request, 'dashboard_app/today_due_sell.html', context)


@login_required
@allowed_users(allowed_roles=['Admin', 'Accountant', 'Manager'])
def today_cash_sell(request):
    today = date.today()
    cash_products = Product.objects.filter(created__day=today.day, sell_status='Paid')
    total_cash_sell = sum(item.total_price for item in cash_products)
    context = {'cash_products': cash_products, 'today': today, 'total_cash_sell': total_cash_sell}
    return render(request, 'dashboard_app/today_cash_sell.html', context)


@login_required
@allowed_users(allowed_roles=['Admin', 'Accountant', 'Manager'])
def all_shades(request, customer, customer_id):
    shades = ShadeNo.objects.select_related('customer', 'user').filter(customer_id=customer_id, active=True,
                                                                       status='True')
    search = request.GET.get('search_value')
    if search:
        shades = shades.filter(
            Q(shade_num=search)
        )
    context = {'shades': shades, 'customer_id': customer_id, 'customer': customer, 'status': False}
    return render(request, 'dashboard_app/all_shades.html', context)


@login_required
@allowed_users(allowed_roles=['Admin'])
def shade_complete(request, shade_id):
    url = request.META.get('HTTP_REFERER')
    try:
        shade = ShadeNo.objects.get(pk=shade_id)
    except Exception as e:
        messages.warning(request, 'Query does not exists !')
        return HttpResponseRedirect(url)
    products = Product.objects.filter(shade_id=shade_id, sell_status='Due')
    if products.exists():
        messages.warning(request, 'To complete shade account you have to pay all due sold amount !!!')
        return HttpResponseRedirect(url)
    shade.status = 'False'
    shade.active = False
    shade.save()
    return HttpResponseRedirect(url)


@login_required
@allowed_users(allowed_roles=['Admin'])
def undo_shade_complete(request, shade_id):
    url = request.META.get('HTTP_REFERER')
    try:
        shade = ShadeNo.objects.get(pk=shade_id)
    except Exception as e:
        messages.warning(request, 'Query does not exists !')
        return HttpResponseRedirect(url)
    shade.status = 'True'
    shade.active = True
    shade.save()
    return HttpResponseRedirect(url)


@login_required
@allowed_users(allowed_roles=['Admin'])
def delete_shade(request, shade_id, customer, customer_id):
    try:
        shade = ShadeNo.objects.get(pk=shade_id)
        products = Product.objects.filter(shade_id=shade.pk)
        if products.exists():
            messages.warning(request, 'You can not delete this shade account'
                                      ' cause the couple of products have been sold under this shade account !')
            return HttpResponseRedirect(reverse('Dashboard:all-shades', kwargs={'customer': customer,
                                                                                'customer_id': customer_id}))
        messages.warning(request, f'{shade} deleted successfully !')
        shade.delete()
        return HttpResponseRedirect(reverse('Dashboard:all-shades', kwargs={'customer': customer,
                                                                            'customer_id': customer_id}))
    except Exception as e:
        messages.warning(request, 'Query does not exists !')
        return HttpResponseRedirect(reverse('Dashboard:all-shades', kwargs={'customer': customer,
                                                                            'customer_id': customer_id}))


@login_required
@allowed_users(allowed_roles=['Admin', 'Accountant', 'Manager'])
def create_shade(request, customer, customer_id):
    try:
        shade = ShadeNo.objects.filter(customer_id=customer_id).first()
        initial = int(shade.shade_num + 1)
    except Exception as e:
        initial = 1
    initial = {'shade_num': initial}
    try:
        customer = Customer.objects.get(pk=customer_id)
    except Exception as e:
        messages.warning(request, 'Query does not exists !')
        return HttpResponseRedirect(reverse('Dashboard:all-shades', kwargs={'customer': customer,
                                                                            'customer_id': customer_id}))
    form = ShadeNoForm(initial=initial)
    if request.method == 'POST':
        started = str(request.POST.get('started'))
        format_started = datetime.strptime(started, '%m/%d/%Y %I:%M %p')
        form = ShadeNoForm(request.POST)
        if form.is_valid():
            form_obj = form.save(commit=False)
            form_obj.user = request.user
            form_obj.customer = customer
            form_obj.started = format_started
            form_obj.save()
            messages.info(request, 'New shade created successfully !')
            return HttpResponseRedirect(reverse('Dashboard:all-shades', kwargs={'customer': customer,
                                                                                'customer_id': customer_id}))
        messages.warning(request, 'Shade name or Shade number should not duplicate !')
        form = ShadeNoForm(request.POST)
        context = {'form': form, 'customer': customer, 'customer_id': customer_id}
        return render(request, 'dashboard_app/create_shade.html', context)

    context = {'form': form, 'customer': customer, 'customer_id': customer_id}
    return render(request, 'dashboard_app/create_shade.html', context)


@login_required
@allowed_users(allowed_roles=['Admin', 'Accountant', 'Manager'])
def create_customer(request):
    try:
        customer = Customer.objects.all().first()
        initial = int(customer.num + 1)
    except Exception as e:
        initial = 1
    initial = {'num': initial}
    form = CustomerForm(initial=initial)
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, f'Customer created successfully !')
            return HttpResponseRedirect(reverse('Dashboard:all-customer'))
        messages.warning(request, 'This phone number is existing or invalid ! Try another number please .........')
        form = CustomerForm(request.POST)
        context = {
            'form': form
        }
        return render(request, 'dashboard_app/create_and_edit_customer.html', context)

    context = {
        'form': form
    }
    return render(request, 'dashboard_app/create_and_edit_customer.html', context)



@login_required
@allowed_users(allowed_roles=['Admin', 'Accountant', 'Manager'])
def all_customer(request):
    customers = Customer.objects.all()
    total_customer = customers.count()

    search = request.GET.get('search_value')
    if search:
        customers = customers.filter(
            Q(name__icontains=search) |
            Q(village__icontains=search) |
            Q(ps__icontains=search) |
            Q(district__icontains=search) |
            Q(phone=search) |
            Q(created__icontains=search)
        )
    paginator = Paginator(customers, 20)
    page_number = request.GET.get('page')
    customers = paginator.get_page(page_number)
    context = {
        'customers': customers,
        'total_customer': total_customer
    }
    return render(request, 'dashboard_app/all_customer.html', context)



@login_required
@allowed_users(allowed_roles=['Admin'])
def edit_customer(request, customer_id):
    try:
        customer = Customer.objects.get(pk=customer_id)
    except:
        customer = None
    if customer is not None:
        form = CustomerForm(instance=customer)
        if request.method == 'POST':
            form = CustomerForm(request.POST, instance=customer)
            if form.is_valid():
                form.save()
                messages.info(request, f'Customer "{customer}" updated successfully !')
                return HttpResponseRedirect(reverse('Dashboard:all-customer'))

        context = {
            'form': form,
            'customer_id': customer_id,
            'customer': customer
        }
        return render(request, 'dashboard_app/create_and_edit_customer.html', context)


@login_required
@allowed_users(allowed_roles=['Admin'])
def delete_customer(request, customer_id):
    url = request.META.get('HTTP_REFERER')
    customer = Customer.objects.get(pk=customer_id)
    products = Product.objects.filter(customer_id=customer_id)
    if products.exists():
        messages.warning(request, f'You can not delete customer " {customer.name} " ! Couple of products sold under'
                                  f' this customer')
        return HttpResponseRedirect(url)
    messages.warning(request, f'Customer " {customer.name} " deleted from database !!')
    customer.delete()
    return HttpResponseRedirect(reverse('Dashboard:all-customer'))


@login_required
@allowed_users(allowed_roles=['Admin', 'Accountant', 'Manager'])
def customer_purchasing_info(request, shade_id, customer_id):
    form = SellInfoForm()
    try:
        customer = Customer.objects.get(pk=customer_id)
    except Exception as e:
        messages.warning(request, "Customer query does not exists !")
        return HttpResponseRedirect(reverse("Dashboard:all-customer"))
    try:
        shade = ShadeNo.objects.get(pk=shade_id)
    except Exception as e:
        messages.warning(request, "shade not fount !")
        return HttpResponseRedirect(reverse('Dashboard:all-shades', kwargs={'customer': customer.name,
                                                                            'customer_id': customer_id}))
    payment_cart = customer.payments.select_related('shade', 'customers', 'products').filter(shade_id=shade_id,
                                                                                             display_choice='show')
    due_products = Product.objects.select_related('shade', 'customer').filter(customer_id=customer_id,
                                                                              shade_id=shade_id,
                                                                              sell_status='Due')
    products = Product.objects.select_related('shade', 'customer').filter(customer_id=customer_id,
                                                                          active=True,
                                                                          shade_id=shade_id)
    total_due = sum(item.total_price for item in due_products)
    total_product_price = sum(item.total_price for item in products)
    total_paid = sum(item.paid_amount for item in payment_cart)
    due_remaining = total_due - total_paid

    if request.method == 'POST':
        sell_status = request.POST['sell_status']
        start_date = str(request.POST.get('start_date'))
        input_date_start = datetime.strptime(start_date, '%m/%d/%Y %I:%M %p')
        input_date_start = input_date_start.date()
        if input_date_start and sell_status:
            products = products.filter(sell_status=sell_status, created__date=input_date_start)
        else:
            products = products.filter(
                Q(created__date=input_date_start)
            )
        paginator = Paginator(products, 6)
        page_number = request.GET.get('page')
        products = paginator.get_page(page_number)
        form = SellInfoForm(request.POST)
        context = {
            'products': products,
            'customer_name': customer,
            'total_product_price': total_product_price,
            'total_due': total_due,
            'total_paid': total_paid,
            'due_remaining': due_remaining,
            'sell_status': sell_status,
            'input_date_start': input_date_start,
            'form': form,
            'customer_id': customer_id,
            'shade': shade,
            'shade_id': shade_id
        }
        return render(request, 'dashboard_app/customer_purchasing_info.html', context)
    else:

        context = {
            'products': products,
            'customer_name': customer,
            'total_product_price': total_product_price,
            'total_due': total_due,
            'total_paid': total_paid,
            'due_remaining': due_remaining,
            'form': form,
            'customer_id': customer_id,
            'shade': shade,
            'shade_id': shade_id
        }
        return render(request, 'dashboard_app/customer_purchasing_info.html', context)


@login_required
@allowed_users(allowed_roles=['Admin', 'Accountant', 'Manager'])
def few_payment(request, shade_id, customer_id, product_id, product_name):
    url = request.META.get('HTTP_REFERER')
    try:
        shade = ShadeNo.objects.get(pk=shade_id)
    except Exception as e:
        messages.warning(request, 'Shade query does not exists !')
        return HttpResponseRedirect(reverse('Dashboard:customer-purchasing-info',
                                            kwargs={'shade_id': shade_id, 'customer_id': customer_id}))
    try:
        product = Product.objects.get(pk=product_id, sell_status='Due')
    except Exception as e:
        return HttpResponseRedirect(reverse('Dashboard:customer-purchasing-info',
                                            kwargs={'shade_id': shade_id, 'customer_id': customer_id}))
    try:
        customer = Customer.objects.get(pk=customer_id)
    except Exception as e:
        messages.warning(request, 'Customer query does not exists !')
        return HttpResponseRedirect(reverse('Dashboard:all-customer'))

    payment_carts = PaymentCart.objects.filter(products=product, display_choice='show', shade_id=shade_id)

    total_due = product.total_price
    total_paid_amount = total_paid_price_counting(payment_carts)  # total_paid_price_counting func define above
    remaining_due = total_due - total_paid_amount
    if request.method == 'POST':
        paid_amount = float(request.POST.get('paid_amount'))
        if remaining_due > 0.0 and 0.0 < paid_amount < remaining_due:
            payment_obj = PaymentCart(shade=shade, customers=customer, products=product, paid_amount=paid_amount,
                                      display_choice='show')
            payment_obj.save()
            messages.info(request, f'{paid_amount} added successfully !')
            return HttpResponseRedirect(reverse('Dashboard:customer-purchasing-info',
                                                kwargs={'shade_id': product.shade.pk, 'customer_id': customer_id}))


        elif remaining_due > paid_amount > 0.0:
            payment_obj = PaymentCart(shade=shade, customers=customer, products=product, paid_amount=paid_amount,
                                      display_choice='show')
            payment_obj.product_name = product.name
            payment_obj.save()
            messages.info(request, f'{paid_amount} added successfully !')
            return HttpResponseRedirect(reverse('Dashboard:customer-purchasing-info',
                                                kwargs={'shade_id': product.shade.pk, 'customer_id': customer_id}))

        elif paid_amount == remaining_due:
            payment_obj = PaymentCart(shade=shade, customers=customer, products=product, paid_amount=paid_amount,
                                      display_choice='show')
            payment_obj.save()
            PaymentCart.objects.filter(products=product, display_choice='show', shade_id=shade_id).update(
                display_choice='hide')
            product.sell_status = 'Paid'
            product.save()
            messages.info(request, f'{paid_amount} added successfully !')
            return HttpResponseRedirect(reverse('Dashboard:customer-purchasing-info',
                                                kwargs={'shade_id': product.shade.pk, 'customer_id': customer_id}))
        messages.warning(request, f'{paid_amount} Not added ! Input valid amount please ...........')
        return HttpResponseRedirect(url)

    context = {
        'total_due': total_due,
        'total_paid_amount': total_paid_amount,
        'remaining_due': remaining_due,
        'product': product,
        'shade_id': product.shade.pk,
        'customer': customer,
        'product_name': product_name,
    }
    return render(request, 'dashboard_app/few_payment.html', context)


@login_required
@allowed_users(allowed_roles=['Admin', 'Accountant', 'Manager'])
def few_payment_history(request, shade_num, shade_id, customer_id, product_id, customer_name):
    try:
        product = Product.objects.get(pk=product_id, shade_id=shade_id)
    except Exception as e:
        messages.warning(request, 'Product item not found')
        return HttpResponseRedirect(reverse('Dashboard:customer-purchasing-info',
                                            kwargs={'shade_id': shade_id, 'customer_id': customer_id}))

    payment_carts = PaymentCart.objects.filter(customers_id=customer_id, products_id=product)
    total_paid_amount = sum(item.paid_amount for item in payment_carts)

    context = {
        'payment_carts': payment_carts,
        'customer_name': customer_name,
        'customer_id': customer_id,
        'shade_id': shade_id,
        'total_paid_amount': total_paid_amount,
        'shade_num': shade_num,
        'product_id': product_id,
    }
    return render(request, 'dashboard_app/few_payment_history.html', context)


@login_required
@allowed_users(allowed_roles=['Admin'])
def delete_few_payment_history(request, shade_id, customer_id, product_id, cart_id):
    url = request.META.get('HTTP_REFERER')
    try:
        product = Product.objects.get(pk=product_id, shade_id=shade_id)
    except Exception as e:
        messages.warning(request, 'Product item not found')
        return HttpResponseRedirect(reverse('Dashboard:customer-purchasing-info',
                                            kwargs={'shade_id': shade_id, 'customer_id': customer_id}))

    PaymentCart.objects.get(pk=cart_id).delete()
    payment_carts = PaymentCart.objects.filter(customers_id=customer_id, products_id=product)
    if payment_carts.exists():
        product.sell_status = 'Due'
        product.save()
        messages.warning(request, 'Payment record deleted from database !')
        return HttpResponseRedirect(url)
    return HttpResponseRedirect(reverse('Dashboard:customer-purchasing-info',
                                        kwargs={'shade_id': shade_id, 'customer_id': customer_id}))


@login_required
@allowed_users(allowed_roles=['Admin', 'Accountant', 'Manager'])
def today_payment(request):
    today = date.today()
    payments = PaymentCart.objects.filter(payment_date__day=today.day)
    total_paid = sum(item.paid_amount for item in payments)
    context = {'payments': payments, 'total_paid': total_paid}
    return render(request, 'dashboard_app/today_payment.html', context)


# =======================================================================


# =======================================================================

@login_required
@allowed_users(allowed_roles=['Admin', 'Accountant', 'Manager'])
def sell_product(request, shade_id, customer_id):
    shade = ShadeNo.objects.get(pk=shade_id)
    customer = Customer.objects.get(pk=customer_id)
    form = ProductForm(request.POST or None)
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product_obj = form.save(commit=False)
            product_obj.customer = customer
            product_obj.shade = shade
            product_obj.sold_by = request.user
            stock_product = Stock.objects.get(pk=product_obj.select_product.pk)
            if stock_product.quantity >= form.cleaned_data['quantity'] > 0:
                stock_product.quantity -= form.cleaned_data['quantity']
                if stock_product.quantity == 0:
                    stock_product.save()
                    product_obj.name = stock_product.product_name
                    product_obj.save()
                    update_balance_sheet()  # this function called to update balance sheet

                stock_product.save()
                product_obj.name = stock_product.product_name
                product_obj.save()
                update_balance_sheet()  # this function called to update balance sheet
            else:
                messages.warning(request, 'Input product qty is greater than stock qty or invalid qty !')
                form = ProductForm(request.POST)
                context = {
                    'form': form,
                    'customer': customer,
                    'shade': shade,
                    'shade_id': shade.pk
                }
                return render(request, 'dashboard_app/sell_product.html', context)

            return HttpResponseRedirect(reverse('Dashboard:customer-purchasing-info',
                                                kwargs={'shade_id': shade_id, 'customer_id': customer_id}))

    context = {
        'form': form,
        'customer': customer,
        'shade': shade,
        'shade_id': shade.pk
    }
    return render(request, 'dashboard_app/sell_product.html', context)


# =======================================================================

# =======================================================================

@login_required
@allowed_users(allowed_roles=['Admin'])
def edit_sold_product(request, shade_id, product_id, customer_id):
    try:
        product = Product.objects.get(pk=product_id, shade_id=shade_id)
        stock_product = Stock.objects.get(product_no=product.select_product.product_no)
        stock_qty = stock_product.quantity
        sold_qty = product.quantity
    except Exception as e:
        messages.warning(request, 'Product does not exist !')
        return HttpResponseRedirect(reverse('Dashboard:customer-purchasing-info', kwargs={'customer_id': customer_id,
                                                                                          'shade_id': shade_id}))

    form = EditProductForm(instance=product)
    if request.method == 'POST':
        form = EditProductForm(request.POST, instance=product)
        if form.is_valid():
            instance = form.save(commit=False)
            if sold_qty == instance.quantity:
                instance.save()
                update_balance_sheet()  # this function called to update balance sheet
            elif sold_qty > instance.quantity > 0:
                editable_qty = sold_qty - instance.quantity
                stock_product.quantity += editable_qty
                stock_product.save()
                instance.save()
                update_balance_sheet()  # this function called to update balance sheet
            else:
                editable_qty = instance.quantity - sold_qty
                if editable_qty <= stock_qty and instance.quantity > 0:
                    stock_product.quantity -= editable_qty
                    stock_product.save()
                    instance.save()
                    update_balance_sheet()  # this function called to update balance sheet
                else:
                    messages.warning(request, 'Invalid input product qty !!!!!')
                    form = EditProductForm(request.POST)
                    context = {'form': form, 'product': product, 'shade_id': shade_id, 'stock_product': stock_product}
                    return render(request, 'dashboard_app/edit_sold_product.html', context)
            messages.success(request, f'{product.name}Product updated !!')
            return HttpResponseRedirect(reverse('Dashboard:customer-purchasing-info',
                                                kwargs={'shade_id': shade_id, 'customer_id': customer_id}))

    context = {'form': form, 'product': product, 'shade_id': shade_id, 'stock_product': stock_product}
    return render(request, 'dashboard_app/edit_sold_product.html', context)


@login_required
@allowed_users(allowed_roles=['Admin'])
def delete_sold_product(request, shade_id, product_id, customer_id):
    url = request.META.get('HTTP_REFERER')
    try:
        product = Product.objects.get(pk=product_id, shade_id=shade_id, customer_id=customer_id)
        stock_product = Stock.objects.get(product_no=product.select_product.product_no)
    except Exception as e:
        messages.warning(request, 'Query does not exists !!!')
        return HttpResponseRedirect(url)
    payment_cart = PaymentCart.objects.filter(shade_id=shade_id, customers_id=customer_id, products_id=product_id)
    if payment_cart.exists():
        messages.warning(request, 'Sorry you can not delete this product ! Some transaction completed under this product item !')
        return HttpResponseRedirect(url)
    stock_product.quantity += product.quantity
    stock_product.save()
    messages.warning(request, f'{product.name} deleted !!')
    product.delete()
    update_balance_sheet()  # this function called to update balance sheet
    return HttpResponseRedirect(url)


@login_required
@allowed_users(allowed_roles=['Admin', 'Accountant', 'Manager'])
def sold_in_current_month(request, month_n, month):
    sold_products = Product.objects.filter(created__month=month)  # all sold product in current month
    payment_cart = PaymentCart.objects.filter(payment_date__month=month)  # all payment in current month
    due_products = Product.objects.filter(sell_status='Due',
                                          created__month=month)  # all due sold product in current month
    total_due = round(sum(item.total_price for item in due_products), 2)
    total_paid = round(sum(item.paid_amount for item in payment_cart), 2)
    total_sold = round(sum(item.total_price for item in sold_products), 2)
    due_remaining = total_due - total_paid
    context = {'sold_products': sold_products, 'month_n': month_n, 'due_remaining': due_remaining,
               'total_due': total_due, 'total_paid': total_paid, 'total_sold': total_sold}
    return render(request, 'dashboard_app/sold_in_current_month.html', context)


# ========================================================================


@login_required
@allowed_users(allowed_roles=['Admin'])
def create_employee(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'New employee created !')
            return HttpResponseRedirect(reverse('Dashboard:all-employees'))
    context = {'form': form}
    return render(request, 'dashboard_app/create_employee.html', context)


@login_required
@allowed_users(allowed_roles=['Admin'])
def all_employees(request):
    employees = User.objects.all().exclude(is_superuser=True)
    context = {'employees': employees}
    return render(request, 'dashboard_app/all_employees.html', context)


@login_required
@allowed_users(allowed_roles=['Admin', ])
def edit_employee(request, employee_id):
    try:
        employee = User.objects.get(pk=employee_id)
    except Exception as e:
        messages.warning(request, 'Employee does not exists !')
        return HttpResponseRedirect(reverse('Dashboard:all-employees'))
    form = EditEmployeeForm(instance=employee)
    if request.method == 'POST':
        form = EditEmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, f'"{employee}" updated successfully !')
            return HttpResponseRedirect(reverse('Dashboard:all-employees'))
    context = {'form': form, 'employee': employee}
    return render(request, 'dashboard_app/edit_employee.html', context)


@login_required
@allowed_users(allowed_roles=['Admin'])
def employee_profile(request, user_id):
    try:
        profile = User.objects.get(pk=user_id)
    except Exception as e:
        messages.warning(request, 'Employee does not exists !')
        return HttpResponseRedirect(reverse('Dashboard:all-employees'))
    context = {'profile': profile}
    return render(request, 'dashboard_app/profile.html', context)


@login_required
@allowed_users(allowed_roles=['Admin', 'Accountant', 'Manager'])
def expired_shades(request, customer, customer_id):
    shades = ShadeNo.objects.filter(customer_id=customer_id, status='False', active=False)
    search = request.GET.get('search_value')
    if search:
        shades = shades.filter(
            Q(shade_num=search)
        )
    context = {'shades': shades, 'customer_id': customer_id, 'customer': customer}
    return render(request, 'dashboard_app/expired_shades.html', context)
