from django.contrib import admin
from .models import (
    Employee,
    Client,
    Project,
    ClientInvoice,
    ClientPayment,
    Leave,
    Department,
    EmpBankInfo,
    EmpPersonalInfo,
    Experience,
    Holiday,
    Task
)

class ClientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'company','position','email','phone')

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('emp_id','full_name','email','department','position','date_joined')
    exclude = ('user',)

class ClientInvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_id','client','amount','status')

class ClientPaymentAdmin(admin.ModelAdmin):
    list_display = ('invoice_id','client','paid_date','payment_method','paid_amount')

class LeaveAdmin(admin.ModelAdmin):
    list_display = ('employee','employee_department','start','end','number_of_days','status')

    def employee_department(self, obj):
        return obj.employee.department

    employee_department.short_description = 'Employee Department'

class EmpPersonalInfoAdmin(admin.ModelAdmin):
    list_display = ('employee','passport_number','religion')

class HolidayAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date','is_passed')

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at','created_by')


class TaskAdmin(admin.ModelAdmin):
    list_display = ('task_name', 'task_status','parent_project')

    # def save_model(self, request, obj, form, change):
    #     if not change:  # Only set created_by during the first save.
    #         obj.created_by = request.user
    #     super().save_model(request, obj, form, change)


admin.site.register(Project, ProjectAdmin)
admin.site.register(Department)
admin.site.register(EmpBankInfo)
admin.site.register(Leave, LeaveAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Holiday, HolidayAdmin)
admin.site.register(Employee,EmployeeAdmin)
admin.site.register(ClientInvoice, ClientInvoiceAdmin)
admin.site.register(ClientPayment, ClientPaymentAdmin)
admin.site.register(EmpPersonalInfo,EmpPersonalInfoAdmin)
admin.site.register(Task, TaskAdmin)

