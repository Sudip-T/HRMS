from django import forms
from .models import *


class LeaveForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = ['employee', 'start', 'end',
                  'status', 'leave_type', 'leave_reason']
        widgets = {
            'employee': forms.Select(attrs={'class': 'form-control'}),
            'start': forms.DateInput(attrs={'class': 'form-control datepicker', 'autocomplete': 'off'}),
            'end': forms.DateInput(attrs={'class': 'form-control datepicker', 'autocomplete': 'off'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'leave_type': forms.Select(attrs={'class': 'form-control'}),
            'leave_reason': forms.TextInput(attrs={'class': 'form-control'}),
        }


class LeaveForm2(forms.ModelForm):
    class Meta:
        model = Leave
        fields = ['start', 'end', 'leave_type', 'leave_reason']
        widgets = {
            'start': forms.DateInput(attrs={'class': 'form-control datepicker', 'autocomplete': 'off'}),
            'end': forms.DateInput(attrs={'class': 'form-control datepicker', 'autocomplete': 'off'}),
            'leave_type': forms.Select(attrs={'class': 'form-control'}),
            'leave_reason': forms.TextInput(attrs={'class': 'form-control'}),
        }


class HolidayForm(forms.ModelForm):
    class Meta:
        model = Holiday
        fields = ['title', 'start_date', 'end_date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control datepicker', 'autocomplete': 'off'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control datepicker', 'autocomplete': 'off'}),
        }


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['full_name', 'username', 'email', 'contact', 'date_joined', 'department',
                  'position', 'username', 'birthday', 'address', 'gender', 'profile_img']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'contact': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'date_joined': forms.DateInput(attrs={'class': 'form-control datepicker', 'autocomplete': 'off'}),
            'birthday': forms.DateInput(attrs={'class': 'form-control datepicker', 'autocomplete': 'off'}),
        }


class EmployeePersonalInfoForm(forms.ModelForm):
    class Meta:
        model = EmpPersonalInfo
        fields = ['passport_number', 'passport_expiry',
                  'nationality', 'religion', 'marital_status']
        widgets = {
            'passport_number': forms.TextInput(attrs={'class': 'form-control'}),
            'passport_expiry': forms.DateInput(attrs={'class': 'form-control datepicker', 'autocomplete': 'off'}),
            'nationality': forms.TextInput(attrs={'class': 'form-control'}),
            'religion': forms.TextInput(attrs={'class': 'form-control'}),
            'marital_status': forms.Select(attrs={'class': 'form-control'}),

        }


class EmployeeBankInfoForm(forms.ModelForm):
    class Meta:
        model = EmpBankInfo
        fields = ['bank_name', 'account_number', 'branch_code', 'pan_number']
        widgets = {
            'bank_name': forms.TextInput(attrs={'class': 'form-control'}),
            'account_number': forms.TextInput(attrs={'class': 'form-control'}),
            'branch_code': forms.TextInput(attrs={'class': 'form-control'}),
            'pan_number': forms.TextInput(attrs={'class': 'form-control'}),
        }


class EmployeeInfoForm(forms.ModelForm):
    class Meta:
        model = Employee
        exclude = ['emp_id', 'total_leave_days', 'user']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'birthday': forms.DateInput(attrs={'class': 'form-control datepicker', 'autocomplete': 'off'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'date_joined': forms.DateInput(attrs={'class': 'form-control datepicker', 'autocomplete': 'off'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'gender': forms.TextInput(attrs={'class': 'form-control'}),
            'contact': forms.TextInput(attrs={'class': 'form-control'}),
            'is_admin': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'profile_img': forms.FileInput(attrs={'class': 'form-control'}),
        }


class ProjectSearchForm(forms.Form):
    name = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Project Name'}))
    team_members = forms.ModelChoiceField(queryset=Employee.objects.all(
    ), required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    client = forms.ModelChoiceField(queryset=Client.objects.all(
    ), required=False, widget=forms.Select(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['team_members'].queryset = Employee.objects.all()
        self.fields['team_members'].choices = [
            ('', 'Select Employee')] + [(o.pk, str(o)) for o in Employee.objects.all()]
        self.fields['client'].queryset = Client.objects.all()
        self.fields['client'].choices = [
            ('', 'Select Client')] + [(o.pk, str(o)) for o in Client.objects.all()]

# not used


class EmployeeSearchForm(forms.Form):
    name = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Project Name'}))
    emp_name = forms.ModelChoiceField(queryset=Employee.objects.all(
    ), required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    department = forms.ModelChoiceField(queryset=Department.objects.all(
    ), required=False, widget=forms.Select(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['emp_name'].queryset = Employee.objects.all()
        self.fields['emp_name'].choices = [
            ('', 'Select Employee')] + [(o.pk, str(o)) for o in Employee.objects.all()]
        self.fields['department'].queryset = Client.objects.all()
        self.fields['department'].choices = [
            ('', 'Select Client')] + [(o.pk, str(o)) for o in Client.objects.all()]


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = ClientInvoice
        fields = '__all__'
        widgets = {
            'client': forms.Select(attrs={'class': 'form-control'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control datepicker', 'autocomplete': 'off'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }


class PaymentForm(forms.ModelForm):
    class Meta:
        model = ClientPayment
        fields = '__all__'
        widgets = {
            'client': forms.Select(attrs={'class': 'form-control'}),
            'paid_date': forms.DateInput(attrs={'class': 'form-control datepicker', 'autocomplete': 'off'}),
            'paid_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'payment_method': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ['created_at']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'total_hours': forms.TextInput(attrs={'class': 'form-control'}),
            'cost': forms.TextInput(attrs={'class': 'form-control'}),
            'deadline': forms.DateInput(attrs={'class': 'form-control datepicker', 'autocomplete': 'off'}),
            'client': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            # For multiple team leaders
            'team_leader': forms.SelectMultiple(attrs={'class': 'form-control'}),
            # For multiple team members
            'team_members': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'company': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_img': forms.FileInput(attrs={'class': 'form-control'}),
        }
