from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.db.models import Sum, Count, Min
from django.utils import timezone

from django.db.models.functions import TruncDate
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import *
from .models import *


class TotalSalesDashboardView(TemplateView):
    template_name = 'posapp/total_sales_dashboard.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get the date range from the GET request
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')

        # Convert string dates to datetime objects if provided
        if start_date and end_date:
            start_date = timezone.datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = timezone.datetime.strptime(end_date, '%Y-%m-%d').date()

            # Modify the query to filter by date range
            sales_query = (
                ItemOrder.objects
                .values('item_id__item_name', 'order_id__order_date')
                .annotate(
                    total_amount=Sum('line_total'),
                    order_count=Count('order_id')
                )
                # Filter by date range
                .filter(order_id__order_date__range=[start_date, end_date])
                .order_by('order_id__order_date')
            )
        else:
            # Default query without date filtering
            sales_query = (
                ItemOrder.objects
                .values('item_id__item_name', 'order_id__order_date')
                .annotate(
                    total_amount=Sum('line_total'),
                    order_count=Count('order_id')
                )
                .order_by('order_id__order_date')
            )

        total_revenue = sales_query.aggregate(Sum('total_amount'))[
            'total_amount__sum'] or 0

        context['sales_by_date'] = sales_query
        context['total_revenue'] = total_revenue
        return context


def get_item_orders_for_date_range(start_date, end_date):
    item_orders = ItemOrder.filter_by_date(start_date, end_date)
    return item_orders


def posapp(request):
    items = Item.objects.all()
    context = {'items': items}
    return render(request, 'posapp/openpos.html', context)


def itemList(request):
    items = Item.objects.all()
    context = {'items': items}
    return render(request, 'posapp/ItemList.html', context)


def itemAdd(request):
    form = ItemForm()
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/itemList')

    context = {'form': form}
    return render(request, 'posapp/ItemAdd.html', context)


def itemUpdate(request):
    items = Item.objects.all()  

    if request.method == 'POST':
        for item in items:
            form = ItemForm(request.POST, instance=item, prefix=str(item.id))
            if form.is_valid():
                form.save()
        return redirect('/update-items')

    item_forms = {item.id: ItemForm(
        instance=item, prefix=str(item.id)) for item in items}

    context = {'item_forms': item_forms, 'items': items}
    return render(request, 'posapp/ItemUpdate.html', context)


def itemDelete(request, pk):
    item = Item.objects.get(pk=pk)
    item.delete()
    return redirect('/itemList')


def confirm_order(request):
    if request.method == "POST":
        ptype = request.POST.get('payment_method')
        items = request.POST.get('complete_order')
        print(items)
        totamt = request.POST.get('total_amount')
        ord = Order.objects.create(total_amount=totamt, payment_type=ptype)

        item_fixed = items[:-1]
        stuff = item_fixed.split("-")
        for it in stuff:
            item_obj = Item.objects.get(pk=it[0])
            itprice = item_obj.getPrice()
            lt = itprice * int(it[2])
            ItemOrder.objects.create(
                item_id=item_obj, order_id=ord, line_total=lt, quantity=it[2])
            item_obj.depleteStock(int(it[2]))
            item_obj.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
