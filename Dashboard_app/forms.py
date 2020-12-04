from django import forms
from Login_app.models import User
from django.contrib.auth.models import Group
from .models import *



class CustomerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        self.fields['num'].widget.attrs.update({'class': 'form-control', 'id': 'defaultconfig'})
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'id': 'defaultconfig', 'placeholder': 'Input customer name'})
        self.fields['village'].widget.attrs.update({'class': 'form-control', 'id': 'defaultconfig-2', 'placeholder': 'Input customer village'})
        self.fields['ps'].widget.attrs.update({'class': 'form-control', 'id': 'defaultconfig-3', 'placeholder': 'Input customer PS'})
        self.fields['district'].widget.attrs.update({'class': 'form-control', 'id': 'defaultconfig-4', 'placeholder': 'Input customer district'})
        self.fields['phone'].widget.attrs.update({'class': 'form-control', 'id': 'defaultconfig-4', 'placeholder': 'Input customer phone no'})

    class Meta:
        model = Customer
        fields = '__all__'





class ShadeNoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ShadeNoForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control',
                                                 'placeholder': 'Input like " Shade one / two / three / four etc "'})
        self.fields['shade_num'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = ShadeNo
        fields = ['name', 'shade_num', ]


class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['select_product'].widget.attrs.update({'class': 'form-control'})
        self.fields['price'].widget.attrs.update({'class': 'form-control', 'id': 'defaultconfig-2',
                                                  'placeholder': 'Input product price'})
        self.fields['quantity'].widget.attrs.update({'class': 'form-control', 'id': 'defaultconfig-3'})
        self.fields['discount_per_unit'].widget.attrs.update({'class': 'form-control', 'id': 'defaultconfig-4'})

        self.fields['sell_status'].widget.attrs.update({'class': 'form-control', 'id': 'defaultconfig-4'})

    class Meta:
        model = Product
        exclude = ['customer', ]
        fields = ['select_product', 'price', 'quantity', 'discount_per_unit', 'sell_status']



class EditProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EditProductForm, self).__init__(*args, **kwargs)
        self.fields['price'].widget.attrs.update({'class': 'form-control', 'id': 'defaultconfig-2',
                                                  'placeholder': 'Input product price'})
        self.fields['quantity'].widget.attrs.update({'class': 'form-control', 'id': 'defaultconfig-3'})
        self.fields['discount_per_unit'].widget.attrs.update({'class': 'form-control', 'id': 'defaultconfig-4'})

        self.fields['sell_status'].widget.attrs.update({'class': 'form-control', 'id': 'defaultconfig-4'})

    class Meta:
        model = Product
        exclude = ['customer', ]
        fields = ['price', 'quantity', 'discount_per_unit', 'sell_status']



class SellInfoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SellInfoForm, self).__init__(*args, **kwargs)
        self.fields['sell_status'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Product
        fields = ['sell_status']




class EditEmployeeForm(forms.ModelForm):
    role = forms.ModelChoiceField(queryset=Group.objects.all())

    class Meta:
        model = User
        fields = ['is_active', 'is_staff', 'is_superuser']

    def __init__(self, *args, **kwargs):
        super(EditEmployeeForm, self).__init__(*args, **kwargs)
        if kwargs.get('instance'):
            initial = kwargs.setdefault('initial', {})
            if kwargs['instance'].groups.all():
                initial['role'] = kwargs['instance'].groups.all()[0]
            else:
                initial['role'] = None
        forms.ModelForm.__init__(self, *args, **kwargs)

    def save(self, commit=True):
        role = self.cleaned_data.pop('role')
        u = super().save()
        u.groups.set([role])
        u.save()
        return u



