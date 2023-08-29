from django.urls import path
from .views import *


urlpatterns = [
    path('', index, name='index'),
    path('holidays/', holidays, name='holidays'),
    path('holidays/<int:id>/', holidays, name='edit_holiday'),
    path('employee/leaves/', leaves, name='leaves'),
    path('client/<company>/', client, name='client'),
    path('allclients/', allclients, name='allclients'),
    path('allprojects/', allprojects, name='allprojects'),
    path('allemployees/', allEmployees, name='allemployees'),
    path('employee/departments/', departments, name='departments'),
    path('search/results/', search_results, name='search_results'),
    path('employeedashboard', employeedashboard, name='empdashboard'),
    path('projectdetails/<int:id>/', projectDetails, name='projectdetails'),
    path('employeedetails/<int:id>/', employeeDetails, name='employeedetails'),
    path('delete/<str:model_name>/<int:id>/<str:redirect_url_name>/', delete, name='delete_object'),
    path('client-invoices/', clientInvoices, name='client_invoices'),
    path('client-payments/', clientPayments, name='client_payments'),
    
    
    path('edit_client_payment/<int:id>', generic_edit_data, {'form_class': PaymentForm, 'model_class': ClientPayment, 'redirect_url': 'client_payments'}, name='edit_client_payment'),
    path('edit_client_invoice/<int:id>', generic_edit_data, {'form_class': InvoiceForm, 'model_class': ClientInvoice, 'redirect_url': 'client_invoices'}, name='edit_client_invoice'),
    path('edit_holiday/<int:id>', generic_edit_data, {'form_class': HolidayForm, 'model_class': Holiday, 'redirect_url': 'holidays'}, name='edit_holiday'),
    path('edit_department/<int:id>', generic_edit_data, {'form_class': DepartmentForm, 'model_class': Department, 'redirect_url': 'departments'}, name='edit_department'),
    path('admin_edit_leave/<int:id>', generic_edit_data, {'form_class': LeaveForm, 'model_class': Leave, 'redirect_url': 'leaves'}, name='admin_edit_leave'),

    
]