from django.urls import path
from django.conf import settings
from . import views
from django.views.decorators.csrf import csrf_exempt

app_name = 'posapp'
urlpatterns = [
    path('',views.posapp, name='posapp'),
    path('list',views.itemList, name='item_list'),
    path('add-menu',views.itemAdd, name='item_add'),
    path('update-items/', views.itemUpdate, name="item_update"),
    path('delete-menu/<str:pk>', views.itemDelete, name="item_delete"),
    path('confirm_order', views.confirm_order, name='confirm_order'),
    path('sales-dashboard/', views.TotalSalesDashboardView.as_view(),
         name='sales_dashboard'),

]