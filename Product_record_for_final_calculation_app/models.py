from django.db import models
from django.conf import settings
import math




class BalanceYear(models.Model):
    year = models.CharField(max_length=100)
    n_profit = models.FloatField(default=0.00)

    def __str__(self):
        return str(self.year)

    def total_imported(self):
        total = sum(item.total_import for item in self.balancesheet_set.all())
        return total

    def total_sold(self):
        total = sum(item.total_sold for item in self.balancesheet_set.all())
        return total

    def total_expense(self):
        total = sum(item.total_expense for item in self.balancesheet_set.all())
        return total


    def save(self, *args, **kwargs):
        self.n_profit = math.ceil((self.total_sold() - self.total_imported()) - self.total_expense())
        super(BalanceYear, self).save(*args, **kwargs)





MONTH = (
    ('1', 'January'),
    ('2', 'February'),
    ('3', 'March'),
    ('4', 'April'),
    ('5', 'May'),
    ('6', 'June'),
    ('7', 'July'),
    ('8', 'August'),
    ('9', 'September'),
    ('10', 'October'),
    ('11', 'November'),
    ('12', 'December'),
)


class BalanceSheet(models.Model):
    year = models.ForeignKey(BalanceYear, on_delete=models.PROTECT)
    month = models.CharField(max_length=20, choices=MONTH)
    total_import = models.FloatField(default=0.00)
    import_qty = models.PositiveIntegerField()
    total_sold = models.FloatField(default=0.00)
    sold_qty = models.PositiveIntegerField()
    total_expense = models.FloatField(default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.year)



class ExpenseYear(models.Model):
    year = models.CharField(max_length=100)

    def __str__(self):
        return str(self.year)


EXPENSE_MONTH = (
    ('1', 'January'),
    ('2', 'February'),
    ('3', 'March'),
    ('4', 'April'),
    ('5', 'May'),
    ('6', 'June'),
    ('7', 'July'),
    ('8', 'August'),
    ('9', 'September'),
    ('10', 'October'),
    ('11', 'November'),
    ('12', 'December'),
)


class Expense(models.Model):
    year = models.ForeignKey(ExpenseYear, on_delete=models.PROTECT)
    month = models.CharField(max_length=20, choices=EXPENSE_MONTH)
    invoice_no = models.PositiveIntegerField(null=True, blank=True)
    expense_type = models.CharField(max_length=250)
    expense_amount = models.FloatField(default=0.00)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.expense_type)
