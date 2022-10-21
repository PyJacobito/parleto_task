from django.views.generic.list import ListView
from django.db.models import Q

from .forms import ExpenseSearchForm
from .models import Expense, Category
from .reports import summary_per_category, summary_per_year_month, total_items
from .functions import get_date_str, get_date_list, get_all_tokens


class ExpenseListView(ListView):
    model = Expense
    paginate_by = 5


    def get_context_data(self, *, object_list=None, ordering=None, **kwargs):
        queryset = object_list if object_list is not None else self.object_list

        form = ExpenseSearchForm(self.request.GET)
        if form.is_valid():
            query = form.cleaned_data.get('query', '').strip()

            if query:
                if get_date_str(query):
                    date_list = get_date_list(query)

                    if len(date_list) == 2:
                        queryset = queryset.filter(Q(date__range=[str(item) for item in date_list]))

                    elif len(date_list) == 1:
                        if query[0] == "-":
                            queryset = queryset.filter(Q(date__lte=date_list[0]))

                        elif query[-1] == "-":
                            queryset = queryset.filter(Q(date__gte=date_list[0]))

                else:
                    query_list = get_all_tokens(query)

                    if len(query_list) > 1:
                        queryset = queryset.filter(Q(name__in=query_list) | Q(category__name__in=query_list))

                    else:
                        queryset = queryset.filter(
                            Q(name__icontains=query_list[0]) | Q(category__name__iexact=query_list[0])
                        )

        return super().get_context_data(
            form=form,
            object_list=queryset,
            summary_per_category=summary_per_category(queryset),
            total_amount_spent=sum(summary_per_category(queryset).values()),
            summary_per_year_month=summary_per_year_month(queryset),
            total_items=total_items(queryset),
            **kwargs)

    def get_ordering(self):
        order = self.ordering
        form = ExpenseSearchForm(self.request.GET)

        if form.is_valid():
            sorting_token = form.cleaned_data.get('sorting', '').strip()

            if sorting_token == "1":
                order = ('-category', 'pk')

            elif sorting_token == "2":
                order = ('category', 'pk')

            elif sorting_token == "3":
                order = ('-date', 'pk')

            elif sorting_token == "4":
                order = ('date', 'pk')

        return order


class CategoryListView(ListView):
    model = Category
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["extra"] = total_items(Expense.objects)
        return context
