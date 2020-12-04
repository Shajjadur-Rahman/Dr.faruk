from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from Product_inventory_app.models import Stock
from django.conf import settings


class Customer(models.Model):
    num = models.PositiveIntegerField(default=0, unique=True)
    name = models.CharField(max_length=100)
    village = models.CharField(max_length=50)
    ps = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    phone = PhoneNumberField()
    display_status = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_customer_info(self):
        return f'Name : {self.name}, Village : {self.village}, PS : {self.ps}, District : {self.district},' \
               f' Phone : {self.phone}'

    class Meta:
        ordering = ('-num',)
        unique_together = ('phone', )


class ShadeNo(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False')
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=200)
    shade_num = models.PositiveIntegerField(default=0)
    started = models.DateTimeField()
    status = models.CharField(max_length=6, choices=STATUS, default='True')
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    completed = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        ordering = ['-created', ]



class Product(models.Model):
    SELL_STATUS = [
        ('Due', 'Due'),
        ('Paid', 'Paid')
    ]
    select_product = models.ForeignKey(Stock, on_delete=models.SET_NULL, null=True, blank=True)
    shade = models.ForeignKey(ShadeNo, on_delete=models.SET_NULL, null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, related_name='product')
    sold_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=50)
    price = models.FloatField()
    quantity = models.PositiveIntegerField(default=1)
    discount_per_unit = models.FloatField(default=0.00)
    total_discount = models.FloatField(default=0.00)
    total_price = models.FloatField()
    active = models.BooleanField(default=True)
    sell_status = models.CharField(max_length=6, choices=SELL_STATUS)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name + " " + str(self.created.strftime('%b %d %y %r'))

    class Meta:
        ordering = ('-created',)

    def created_date(self):
        return str(self.created.strftime('%b %d %y %r'))

    def total_product_price(self):
        value = 0
        if self.discount_per_unit:
            value += (self.quantity * self.price) - (self.quantity * self.discount_per_unit)
            return value
        else:
            value += self.quantity * self.price
        return round(value, 2)

    def save(self, *args, **kwargs):
        self.total_price = self.total_product_price()
        self.total_discount = round(self.quantity * self.discount_per_unit, 2)
        super(Product, self).save(*args, **kwargs)

    def total_paid(self):
        value = 0
        cart_item = self.products.all().select_related('products')
        value += sum(item.paid_amount for item in cart_item)
        return round(value, 2)

    def rest_price(self):
        total = self.total_product_price() - self.total_paid()
        return round(total, 2)

class PaymentCart(models.Model):
    DISPLAY_CHOICE = [
        ('show', 'show'),
        ('hide', 'hide')
    ]
    shade = models.ForeignKey(ShadeNo, on_delete=models.SET_NULL, blank=True, null=True)
    customers = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')
    products = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='products')
    product_name = models.CharField(max_length=300, null=True, blank=True)
    paid_amount = models.FloatField()
    active = models.BooleanField(default=True)
    display_choice = models.CharField(max_length=6, choices=DISPLAY_CHOICE, default='show')
    payment_date = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.paid_amount)

    class Meat:
        ordering = ['-payment_date', ]

