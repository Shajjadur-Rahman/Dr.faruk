from .models import Expense, BalanceYear
from django import forms



class BalanceYearForm(forms.ModelForm):
    class Meta:
        model = BalanceYear
        fields = '__all__'




class AddNewExpenseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddNewExpenseForm, self).__init__(*args, *kwargs)
        self.fields['expense_type'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Input import expense type !'
                                                     ' Like as carrying by pickup / '
                                                     'van etc......'})
        self.fields['expense_amount'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Expense
        fields = ['expense_type', 'expense_amount']


class SearchBalanceYear(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SearchBalanceYear, self).__init__(*args, **kwargs)
        self.fields['year'].widget.attrs.update({'class': 'form-control'})


    class Meta:
        model = BalanceYear
        fields = ['year', ]
