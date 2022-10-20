from django.views.generic.list import ListView
from django.db.models import Q

from .forms import ExpenseSearchForm
from .models import Expense, Category
from .reports import summary_per_category

from .functions import get_date_list, get_date_str, get_all_tokens


class ExpenseListView(ListView):
    model = Expense
    paginate_by = 5

    queryset = Expense.objects.all()


    def get_context_data(self, *, object_list=None, **kwargs):
        q = self.request.GET.get("q")

        if isinstance(q, str) and q:
            q = q.strip()

            if get_date_str(q):
                date_list = get_date_list(q)

                if len(date_list) == 2:
                    queryset = self.model.objects.filter(Q(date__range=[str(item) for item in date_list]))

                elif len(date_list) == 1:
                    if q[0] == "-":
                        queryset = self.model.objects.filter(Q(date__lte=date_list[0]))

                    elif q[-1] == "-":
                        queryset = self.model.objects.filter(Q(date__gte=date_list[0]))

            else:
                q_list = get_all_tokens(q)

                if len(q_list) > 1:
                    queryset = self.model.objects.filter(Q(name__in=q_list) | Q(category__name__in=q_list))

                else:
                    queryset = self.model.objects.filter(
                        Q(name__icontains=q_list[0]) | Q(category__name__icontains=q_list[0]))

        else:
            queryset = self.model.objects.all()

        return super().get_context_data(
                # form=form,
                object_list=queryset,
                summary_per_category=summary_per_category(queryset),
                **kwargs)


class CategoryListView(ListView):
    model = Category
    paginate_by = 5

# from django.views.generic.list import ListView
#
# from .forms import ExpenseSearchForm
# from .models import Expense, Category
# from .reports import summary_per_category
#
#
# class ExpenseListView(ListView):
#     model = Expense
#     paginate_by = 5
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         queryset = object_list if object_list is not None else self.object_list
#
#         form = ExpenseSearchForm(self.request.GET)
#         if form.is_valid():
#             name = form.cleaned_data.get('name', '').strip()
#             if name:
#                 queryset = queryset.filter(name__icontains=name)
#
#         return super().get_context_data(
#             form=form,
#             object_list=queryset,
#             summary_per_category=summary_per_category(queryset),
#             **kwargs)
#
# class CategoryListView(ListView):
#     model = Category
#     paginate_by = 5