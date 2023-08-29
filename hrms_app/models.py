# import json
# from datetime import date
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.core.exceptions import ValidationError
from .utils import *
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.forms import PasswordResetForm


class Department(models.Model):
    name = models.CharField(max_length=20)
    
    def __str__(self):
        return self.name



class Employee(models.Model):
    GENDER = (('Male','MALE'), ('Female', 'FEMALE'),('  Other', 'OTHER'))

    # Personal Information
    full_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=125)
    contact = models.CharField(max_length=15)
    address = models.CharField(max_length=100, default='', blank=True)
    birthday = models.DateField()
    gender = models.CharField(choices=GENDER, max_length=10)

    # Employee Information
    emp_id = models.CharField(max_length=10, editable=False)
    department = models.ForeignKey(Department,on_delete=models.SET_NULL, null=True)
    position = models.CharField(max_length=50, null=True, blank=True)
    date_joined = models.DateField()
    total_leave_days = models.IntegerField(default=0)

    # User Account Related
    username = models.CharField(max_length=50)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    profile_img = models.ImageField(upload_to='employees/', null=True, blank=True)

    class Meta:
        ordering = ['date_joined', 'full_name']

    def __str__(self):
        return f' {self.full_name} - {self.position}'
        
    
    def save(self, *args, **kwargs):
        passwd = get_random_string(8)
        if self.pk is None:
            self.set_emp_id()
            # self.user= create_user_account(self.username, self.is_admin, passwd)
            # send_welcome_email(self.username, self.email, passwd)
        super().save(*args, **kwargs)

    def set_emp_id(self):
        if not self.emp_id:
            self.emp_id = generate_id(Employee, 'EID')



class EmpBankInfo(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    bank_name = models.CharField(max_length=50)
    account_number = models.CharField(max_length=50)
    branch_code = models.CharField(max_length=10)
    pan_number = models.CharField(max_length=20)

    def __str__(self):
        return self.employee.full_name



class EmpPersonalInfo(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    passport_number = models.CharField(max_length=15)
    passport_expiry = models.DateField()
    nationality = models.CharField(max_length=15)
    religion = models.CharField(max_length=15)
    status = (('Married','Married'),('Single','Single'),('Divorced', 'Divorced'))
    marital_status = models.CharField(choices=status, max_length=15)

    def __str__(self):
        return self.employee.full_name



class Experience(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='experiences')
    company = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    duration = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.position} at {self.company}"

    

class Leave (models.Model):
    STATUS = (('Approved','APPROVED'),('Pending','PENDING'),('Declined','DECLINED'),('New','NEW'))
    choices = (('Causal Leave','CAUSAL'),('Emergency Leave','EMERGENCY'),('Sick Leave','SICK'))
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='leave')
    start = models.DateField()
    end = models.DateField(null=True, blank=True)
    status = models.CharField(choices=STATUS,  default='New',max_length=15)
    leave_type = models.CharField(choices=choices, max_length=50)
    number_of_days = models.PositiveIntegerField(blank=True, null=True, editable=False)
    leave_reason = models.CharField(max_length=50)

    def __str__(self):
        return self.employee.full_name
    
    def save(self, *args, **kwargs):
        """Overrides the save method to calculate the number of leave days."""
        if self.start and self.end:
            num_days = (self.end - self.start).days
            self.number_of_days = num_days + 1
        else:
            self.number_of_days = 1

        super(Leave, self).save(*args, **kwargs)

    def clean(self):
        if self.start and self.start < timezone.localdate():
            raise ValidationError({'start': 'Start date cannot be in the past.'})
        if self.end and self.end < timezone.localdate():
            raise ValidationError({'end': 'End date cannot be in the past.'})



class Holiday(models.Model):
    title = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    number_of_days = models.PositiveIntegerField(blank=True, null=True, editable=False)

    def __str__(self):
        return self.title
    
    @property
    def is_passed(self):
        return self.start_date < timezone.localdate()
    
    def clean(self):
        if self.start_date and self.start_date < timezone.localdate():
            raise ValidationError({'start_date': 'Holiday start date cannot be in the past.'})
        if self.end_date and self.end_date < self.start_date:
            raise ValidationError({'end_date': 'Holiday end date cannot be before the start date.'})

    def save(self, *args, **kwargs):
        if self.start_date and self.end_date:
            num_days = (self.end_date - self.start_date).days
            self.number_of_days = num_days + 1
        else:
            self.number_of_days = 1

        super(Holiday, self).save(*args, **kwargs)

    @property
    def duration(self):
        if self.end_date:
            return (self.end_date - self.start_date).days + 1
        else:
            return 1
        

class Client(models.Model):
    GENDER = (('Male','MALE'), ('Female', 'FEMALE'),('Other', 'OTHER'))
    full_name = models.CharField(max_length=50, null=False)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=125, null=False)
    address = models.CharField(max_length=100, default='')
    gender = models.CharField(choices=GENDER, max_length=10)
    position = models.CharField(max_length=100)
    company = models.CharField(max_length=200)
    profile_img = models.ImageField(upload_to='clients/', null=True, blank=True)

    def __str__(self):
        return self.company



class Project(models.Model):
    name = models.CharField(max_length=50, null=False)
    deadline = models.DateField()
    created_at = models.DateField(auto_now_add=True)
    total_hours = models.CharField(max_length=5)
    Priority = (('Low','LOW'),('Normal','NORMAL'),('High','HIGH'))
    Status = (('New','New'),('Pending','PENDING'),('Working','WORKING'),('Completed','Completed'))
    status = models.CharField(choices=Status, max_length=10, null=True, default='New')
    priority = models.CharField(choices=Priority, max_length=10)
    cost = models.CharField(max_length=20)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    team_leader = models.ManyToManyField(Employee, related_name='leading_projects')
    team_members = models.ManyToManyField(Employee, related_name='assigned_projects')
    project_info = models.TextField(max_length=700)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, editable=False)
    def __str__(self):
        return self.name
   


class ClientInvoice(models.Model):
    STATUS = (('Paid', 'PAID'),('Unpaid','UNPAID'),('Partially Paid','PARTIALLY PAID'))
    invoice_id = models.CharField(max_length=10, unique=True, editable=False)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    due_date = models.DateField()
    amount = models.IntegerField()
    status = models.CharField(choices=STATUS, max_length=20,default='Unpaid')

    def save(self, *args, **kwargs):
        if not self.invoice_id:
            self.invoice_id = generate_invoice_id(ClientInvoice, 'CLTINV')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.client.company



class ClientPayment(models.Model):
    invoice_id = models.CharField(max_length=10, unique=True, editable=False)
    client = models.ForeignKey(ClientInvoice, on_delete=models.CASCADE)
    paid_date = models.DateField()
    paid_amount = models.IntegerField()
    payment_method = models.CharField(max_length=20, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.set_invoice_id()
        super().save(*args, **kwargs)
        self.update_invoice_status()
   
    def set_invoice_id(self):
        if not self.invoice_id:
            self.invoice_id = generate_invoice_id(ClientPayment, 'CLTPM')

    def update_invoice_status(self):
        # Update ClientInvoice status
        client_invoice = ClientInvoice.objects.get(invoice_id=self.client.invoice_id)
        paid_amount = self.paid_amount

        # Check if the paid_amount is equal to the total amount of the invoice
        if paid_amount >= client_invoice.amount:
            client_invoice.status = 'Paid'
        elif 0 < paid_amount < client_invoice.amount:
            client_invoice.status = 'Partially Paid'
        else:
            client_invoice.status = 'Unpaid'

        client_invoice.save()

    def __str__(self):
        return self.invoice_id


class Task(models.Model):
    STATUS_CHOICES = (
        ('New', 'New'),
        ('Pending', 'Pending'),
        ('Working', 'Working'),
        ('Completed', 'Completed'),
    )

    task_name = models.CharField(max_length=50)
    task_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='New')
    parent_project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')

    def __str__(self):
        return self.task_name
