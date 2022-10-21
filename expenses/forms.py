from django import forms
from .models import Expense


class ExpenseSearchForm(forms.Form):

    sorting_choices = (("1", "descending by category"),
                       ("2", "ascending by category"),
                       ("3", "descending by date"),
                       ("4", "ascending by date")
                       )

    query = forms.CharField(label="Search",
                            required=False,
                            widget=forms.TextInput(attrs={'placeholder': 'Lookup by name/category/date', 'size': '40'})
                            )

    sorting = forms.ChoiceField(required=False, choices=sorting_choices)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["query"]