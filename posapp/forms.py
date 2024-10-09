from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field
from django import forms
from .models import Item


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('item_name', 'item_price', 'stock_quantity')

    def __init__(self, *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Field('item_name'),
            Field('item_price'),
            Field('stock_quantity'),
            Submit('submit', 'Submit', css_class='btn-primary')
        )
