from .forms import *
from .utils import *
from .models import *
from django.apps import apps
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from datetime import date

@login_required
def index(request):
    today = date.today()
    approved_leaves_count = Leave.objects.filter(status='Approved', start=today).count()
    print(approved_leaves_count)
    if request.user.is_superuser:
        context = multiple_model_data()
        context['approved_leaves_count'] = approved_leaves_count
        return render(request, 'index.html', context)
    else:
        return redirect('empdashboard')


@login_required
def allclients(request):
    clients = Client.objects.all()
    form = ClientForm()
    if 'Search_clients' in request.GET:
        search_params_client = {
        'phone': 'data_id',
        'full_name': 'data_name',
        'company': 'data_more',
        }
        results = generic_search(Client, search_params_client, request)
        context = {'clients':results}
        return render(request, 'allclients.html',context)
    if request.method == 'POST':
        form = ClientForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('allclients')
    context = {'clients': clients,'form':form}
    return render(request, 'allclients.html', context)


@login_required
def client(request, company):
    client = Client.objects.get(company=company)
    projects = Project.objects.filter(client=client)
    form = ClientForm(instance=client)
    form2 = ProjectForm()
    if request.method == 'POST':
        if 'edit_client' in request.POST:
            form = ClientForm(request.POST, request.FILES ,instance=client)
            if form.is_valid():
                form.save()
                return redirect('client', company)
        if 'add_project' in request.POST:
            add_form = ProjectForm(request.POST)
            if add_form.is_valid():
                project = add_form.save(commit=False)
                project.save()
                add_form.save_m2m()
                return redirect('client', company)

    return render(request, 'client.html', {'client': client, 'projects': projects,'form':form, 'add_project':form2})


@login_required
def projectDetails(request, id):
    project = Project.objects.get(id=id)
    status_count = project.tasks.values('task_status').annotate(count=Count('task_status'))
    form = ProjectForm(instance=project)
    if request.method == 'POST':
        form = ProjectForm(request.POST ,instance=project)
        if form.is_valid():
            project  = form.save(commit=False)
            project .created_by = request.user
            project .save()
            form.save_m2m()
            return redirect('projectdetails',id)
    return render(request, 'projectdetail.html', {'project': project, 'status_count':status_count,'form':form})


@login_required
def employeeDetails(request, id):
    employee = Employee.objects.get(pk=id)
    projects = employee.leading_projects.all().union(employee.assigned_projects.all())

    emp_info = get_or_none(Employee, id=id)
    emp_infor = EmployeeInfoForm(instance=emp_info)

    emp_info_instance = get_or_none(EmpPersonalInfo, employee=employee)
    empinfo = EmployeePersonalInfoForm(instance=emp_info_instance)

    emp_bank_info_instance = get_or_none(EmpBankInfo, employee=employee)
    bankinfo = EmployeeBankInfoForm(instance=emp_bank_info_instance)

    if request.method == 'POST':
        if 'personalinfo' in request.POST:
            empinfo = EmployeePersonalInfoForm(
                request.POST, instance=emp_info_instance)
            if empinfo.is_valid():
                emp_info_instance = empinfo.save(commit=False)
                emp_info_instance.employee = employee
                emp_info_instance.save()
                return redirect('employeedetails', id=id)

        if 'bankinfo' in request.POST:
            bankinfo = EmployeeBankInfoForm(
                request.POST, instance=emp_bank_info_instance)
            if bankinfo.is_valid():
                emp_bank_info_instance = bankinfo.save(commit=False)
                emp_bank_info_instance.employee = employee
                emp_bank_info_instance.save()
                return redirect('employeedetails', id=id)

        if 'editempinfo' in request.POST:
            emp_info = EmployeeInfoForm(
                request.POST, request.FILES, instance=emp_info)
            if emp_info.is_valid():
                emp_info_instance = emp_info.save(commit=False)
                emp_info_instance.employee = employee
                emp_info_instance.save()
                return redirect('employeedetails', id=id)
    context = {
        'employee': employee,
        'projects': projects,
        'info_form': empinfo,
        'bank_info': bankinfo,
        'emp_infor': emp_infor
    }
    return render(request, 'employeedetails.html', context)


@login_required
def allEmployees(request):
    department = Department.objects.all()
    employees = Employee.objects.all()

    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('allemployees')
    else:
        form = EmployeeForm()

    return render(request, 'allemployees.html', {'employees': employees, 'department': department, 'form': form})


@login_required
def search_results(request):
    search_query_emp_id = request.GET.get('emp_id')
    search_query_emp_name = request.GET.get('emp_name')
    search_query_designation = request.GET.get('designation')

    results = Employee.objects.all()

    if search_query_emp_id:
        results = results.filter(emp_id__icontains=search_query_emp_id)
    if search_query_emp_name:
        results = results.filter(full_name__icontains=search_query_emp_name)
    if search_query_designation:
        results = results.filter(
            department__name__icontains=search_query_designation)

    results = results
    department = Department.objects.all()
    return render(request, 'employeesearch.html', {'results': results, 'department': department})


@login_required
def leaves(request, leave_id=None):
    if request.method == 'POST':
        if 'create' in request.POST:
            form = LeaveForm(request.POST)
            if form.is_valid():
                form.save()
        return redirect('leaves')
    else:
        form = LeaveForm()
    leaves = Leave.objects.all()
    pending_count = Leave.objects.filter(status='Pending').count()
    new_leaves = Leave.objects.filter(status='New').count()
    context = {
        'employees': Employee.objects.all(),
        'leaves': leaves,
        'form': form,
        'pending_count': pending_count,
        'new_leaves': new_leaves
    }
    return render(request, 'leaves.html', context)


@login_required
def departments(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        department = Department(name=name)
        department.save()
        return redirect('departments')
    department = Department.objects.annotate(num_employees=Count('employee'))
    context = {'department': department}
    return render(request, 'departments.html', context)


@login_required
def holidays(request):
    if request.method == 'POST':
        form = HolidayForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('holidays')
    else:
        form = HolidayForm()
    holidays = Holiday.objects.filter(start_date__gte=timezone.now()).order_by('start_date')
    return render(request, 'holidays.html', {'holidays': holidays, 'form': form})


# generic delete function
@login_required
def delete(request, model_name, id, redirect_url_name):
    model = apps.get_model(app_label='hrms_app', model_name=model_name)
    object_to_delete = get_object_or_404(model, id=id)
    object_to_delete.delete()
    return redirect(redirect_url_name)


@login_required
def allprojects(request):
    projects = Project.objects.all()
    add_form = ProjectForm()
    form = ProjectSearchForm(request.GET or None) #used for search_query
    if form.is_valid():
        results = filter_projects(form)
        return render(request, 'search_results.html', {'form': form, 'results': results})
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('allprojects')
    context = {'projects': projects, 'form': form, 'add_form':add_form}
    return render(request, 'allprojects.html', context)


@login_required
def employeedashboard(request):
    user = request.user
    employee = user.employee
    leave_objects = Leave.objects.filter(employee=employee).order_by('-start')
    projects = Project.objects.filter(Q(team_members=employee) | Q(team_leader=employee))
    taken_leave = Leave.objects.filter(employee=request.user.employee, status='Approved').count()
    if request.method == "POST":
        form = LeaveForm2(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.employee = request.user.employee
            leave.save()
            messages.success(
                request, 'Leave Application submitted successfully.')
            return redirect('empdashboard')
    else:
        form = LeaveForm2()

    context = get_multiple_model_data()
    context['form'] = form
    context['leave_obj'] = leave_objects
    context['projects'] = projects
    context['taken_leave'] = taken_leave
    return render(request, 'employeedashboard.html', context)


@login_required
def clientInvoices(request):
    invoices = ClientInvoice.objects.all()
    form = InvoiceForm()
    if request.method == "POST":
        form = InvoiceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Invoice Created Successfully')
            return redirect('client_invoices')

    context = {'invoices':invoices, 'form':form}
    return render(request, 'clientinvoices.html',context)


@login_required
def clientPayments(request):
    payments = ClientPayment.objects.all()
    form = PaymentForm()
    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, 'Payment Created Successfully')
            return redirect('client_payments')

    context = {'payments':payments, 'form':form}
    return render(request, 'clientpayments.html',context)


# generic edit
@login_required
def generic_edit_data(request, id, form_class, model_class, redirect_url):
    data_object = get_object_or_404(model_class, id=id)
    form = form_class(instance=data_object)
    if request.method == "POST":
        form = form_class(request.POST, instance=data_object)
        if form.is_valid():
            form.save()
            return redirect(redirect_url)
    return render(request, 'edit_data.html', {'form': form, 'go_back':redirect_url})


