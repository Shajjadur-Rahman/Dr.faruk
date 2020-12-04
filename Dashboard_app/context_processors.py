from datetime import date

from .models import PaymentCart



def user_role(request):
    role = None
    if request.user.is_authenticated:
        role = request.user.groups.all()[0].name
        return {'role': role}
    else:
        return {'role': role}



def today_all_payments(request):
    today = date.today()
    all_payments = PaymentCart.objects.select_related('shade', 'customers', 'products').filter(payment_date__day=today.day)[0:4]
    total_payments = PaymentCart.objects.select_related('shade', 'customers', 'products').filter(payment_date__day=today.day).count()
    if all_payments.exists():
        return {'all_payments': all_payments, 'total_payments': total_payments}
    return {'total_payments': 0}


