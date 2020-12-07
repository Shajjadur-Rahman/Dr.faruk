from django import forms
from .models import ImportInvoice, Stock, StockHistory




class ImportInvoiceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ImportInvoiceForm, self).__init__(*args, **kwargs)
        self.fields['invoice_no'].widget.attrs.update({'class': 'form-control'})
        self.fields['import_expense_type'].widget.attrs.update({'class': 'form-control',
                                                                'placeholder': 'Input import expense type !'
                                                                               ' Like as carrying by pickup / '
                                                                               'van etc......'})
        self.fields['expense_amount'].widget.attrs.update({'class': 'form-control',
                                                           'placeholder': 'Input expense amount'})
        self.fields['created_by'].widget.attrs.update({'class': 'form-control',
                                                       'placeholder': 'Input your name'})

    class Meta:
        model = ImportInvoice
        fields = ['invoice_no', 'import_expense_type', 'expense_amount', 'created_by']

class EditInvoiceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EditInvoiceForm, self).__init__(*args, **kwargs)
        self.fields['import_expense_type'].widget.attrs.update({'class': 'form-control',
                                                                'placeholder': 'Input import expense type !'
                                                                               ' Like as carrying by pickup / '
                                                                               'van etc......'})
        self.fields['expense_amount'].widget.attrs.update({'class': 'form-control',
                                                           'placeholder': 'Input expense amount'})
        self.fields['created_by'].widget.attrs.update({'class': 'form-control',
                                                       'placeholder': 'Input your name'})

    class Meta:
        model = ImportInvoice
        fields = ['import_expense_type', 'expense_amount', 'created_by']


class StockSearchForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(StockSearchForm, self).__init__(*args, **kwargs)
        self.fields['product_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Search by invoice no...'})


    class Meta:
        model = Stock
        fields = ['product_name', ]


class StockForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(StockForm, self).__init__(*args, **kwargs)
        self.fields['product_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Input product name '})
        self.fields['product_no'].widget.attrs.update({'class': 'form-control'})
        self.fields['quantity'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Input product quantity '})
        self.fields['unit_tag'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Input'
                                                                                             ' something'
                                                                                             ' like "Bag", '
                                                                                             '"Package" etc... '})

    class Meta:
        model = Stock
        fields = ['product_name', 'product_no', 'quantity', 'unit_tag']




class AddInvoiceProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddInvoiceProductForm, self).__init__(*args, **kwargs)
        self.fields['invoice'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Input product name '})
        self.fields['rate'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Input product rate '})
        self.fields['supplier'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Input product supplier '})
        self.fields['created_by'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Input your name '})

    class Meta:
        model = StockHistory
        fields = ['invoice', 'rate', 'supplier', 'created_by']


class AddExistingProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddExistingProductForm, self).__init__(*args, **kwargs)
        self.fields['invoice'].widget.attrs.update({'class': 'form-control'})
        self.fields['rate'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Input product rate '})
        self.fields['quantity'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Input product quantity '})
        self.fields['supplier'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Input product supplier '})
        self.fields['created_by'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Input your name '})

    class Meta:
        model = StockHistory
        fields = ['invoice', 'rate', 'quantity', 'supplier', 'created_by']


class EditProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EditProductForm, self).__init__(*args, **kwargs)
        self.fields['invoice'].widget.attrs.update({'class': 'form-control'})
        self.fields['rate'].widget.attrs.update({'class': 'form-control'})
        self.fields['quantity'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Input product quantity '})
        self.fields['supplier'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Input product supplier '})
        self.fields['created_by'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Input your name '})

    class Meta:
        model = StockHistory
        fields = ['invoice', 'rate', 'quantity', 'supplier', 'created_by']





