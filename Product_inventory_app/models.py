from django.db import models
from django.conf import settings


class ImportInvoice(models.Model):
    invoice_no = models.PositiveIntegerField(unique=True)
    import_expense_type = models.CharField(max_length=200)
    expense_amount = models.FloatField()
    created_by_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    active = models.BooleanField(default=True)
    created_by = models.CharField(max_length=200)
    date = models.DateTimeField()

    def __str__(self):
        return "Invoice " + str(self.invoice_no)


    class Meta:
        ordering = ['-invoice_no']



class Stock(models.Model):
    invoice = models.ForeignKey(ImportInvoice, on_delete=models.SET_NULL, null=True, blank=True)
    product_name = models.CharField(max_length=250, unique=True)
    product_no = models.PositiveIntegerField(default=0, unique=True)
    quantity = models.PositiveIntegerField()
    unit_tag = models.CharField(max_length=200)



    def __str__(self):
        return str(f"{self.product_name} Qty = {self.quantity}")

    class Meta:
        ordering = ['-product_no']


class StockHistory(models.Model):
    invoice = models.ForeignKey(ImportInvoice, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    product_name = models.CharField(max_length=250)
    product_no = models.PositiveIntegerField(default=0)
    rate = models.FloatField(default=0.00)
    quantity = models.PositiveIntegerField()
    unit_tag = models.CharField(max_length=200)
    total_price = models.FloatField()
    supplier = models.CharField(max_length=200, null=True, blank=True)
    created_by = models.CharField(max_length=200)
    active = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.product_name)


    def save(self, *args, **kwargs):
        self.total_price = round(self.rate * self.quantity, 2)
        super(StockHistory, self).save(*args, **kwargs)


