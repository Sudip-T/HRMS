# def save(self, *args, **kwargs):
#     if not self.invoice_id:
#         last_invoice = ClientInvoice.objects.order_by('-invoice_id').first()
#         if last_invoice:
#             last_invoice_id = int(last_invoice.invoice_id.split('-')[1])
#             next_invoice_id = last_invoice_id + 1
#         else:
#             next_invoice_id = 1
#         self.invoice_id = f'CLTINV-{next_invoice_id:04d}'
#     super().save(*args, **kwargs)



# def save(self, *args, **kwargs):
#     if not self.invoice_id:
#         last_invoice = ClientPayment.objects.order_by('-invoice_id').first()
#         if last_invoice:
#             last_invoice_id = int(last_invoice.invoice_id.split('-')[1])
#             next_invoice_id = last_invoice_id + 1
#         else:
#             next_invoice_id = 1
#         self.invoice_id = f'CLTPM-{next_invoice_id:04d}'
#     super().save(*args, **kwargs)

#     # Update ClientInvoice status
#     client_invoice = ClientInvoice.objects.get(invoice_id=self.client.invoice_id)
#     paid_amount = self.paid_amount

#     # Check if the paid_amount is equal to the total amount of the invoice
#     if paid_amount >= client_invoice.amount:
#         client_invoice.status = 'Paid'
#     elif 0 < paid_amount < client_invoice.amount:
#         client_invoice.status = 'Partially Paid'
#     else:
#         client_invoice.status = 'Unpaid'

#     client_invoice.save()



#     emp_id = models.CharField(max_length=10, editable=False)
#     profile_img = models.ImageField(upload_to='employees/', null=True, blank=True)
#     full_name = models.CharField(max_length=50, null=False)
#     contact = models.CharField(max_length=15)
#     email = models.EmailField(max_length=125, null=False)
#     address = models.CharField(max_length=100, default='')
#     gender = models.CharField(choices=GENDER, max_length=10)
#     department = models.ForeignKey(Department,on_delete=models.SET_NULL, null=True)
#     position = models.CharField(max_length=50, null=True, blank=True)
#     date_joined = models.DateField()
#     birthday = models.DateField()
#     total_leave_days = models.IntegerField(default=0)
#     username = models.CharField(max_length=50)
#     is_admin = models.BooleanField(default=False)
#     user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)



#     def save(self, *args, **kwargs):
#         if self.pk is None:
#             # Generate the emp_id
#             last_employee = Employee.objects.order_by('-emp_id').first()
#             if last_employee:
#                 last_employee_id = int(last_employee.emp_id.split('-')[1])
#                 next_employee_id = last_employee_id + 1
#             else:
#                 next_employee_id = 1
#             self.emp_id = f'EID-{next_employee_id:04d}'


#             username = self.username
#             password = get_random_string(8)

#             user = User.objects.create_user(username=username, password=password)
#             user.is_staff = self.is_admin
#             user.is_superuser = self.is_admin
#             user.save()
#             self.user = user


#             send_mail(
#                 'Hello',
#                 f'Your username is {username} and your password is {password}',
#                 settings.EMAIL_HOST_USER,
#                 ['jbbmk3sdpt1992@gmail.com'],
#             )


#             Send password reset email
#             form = PasswordResetForm({'email': self.email})
#             if form:
#                 print('true')
#             assert form.is_valid()
#             form.save(
#                 subject_template_name='registration/password_reset_subject.txt',
#                 email_template_name='registration/password_reset_email.html',
#                 from_email=settings.EMAIL_HOST_USER,
#                 use_https=True,
#                 domain_override='localhost:8000',
#             )

#         super().save(*args, **kwargs)



#     def create_user_account(self):
#         username = self.username
#         password = get_random_string(8)

#         user = User.objects.create_user(username=username, password=password)
#         user.is_staff = self.is_admin
#         user.is_superuser = self.is_admin
#         user.save()
#         self.user = user



# def send_welcome_email(self):
#     send_mail(
#         'Hello',
#         f'Your username is {self.username} and your password is {get_random_string(8)}',
#         settings.EMAIL_HOST_USER,
#         [self.email],  # Send the email to the employee's email
#     )



#     <form method="GET" action="{% url 'search_results' %}" class="row staff-grid-row" id="myForm">
#                 {% csrf_token %}
#                 <div class="col-md-4 col-sm-6 col-12 col-lg-4 col-xl-3">
#                     <div class="form-group">
#                         <input type="text" class="form-control floating" placeholder="Employee ID" name="emp_id">
#                     </div>
#                 </div>
#                 <div class="col-md-4 col-sm-6 col-12 col-lg-4 col-xl-3">
#                     <div class="form-group">
#                         <input type="text" class="form-control floating" placeholder="Employee Name" name="emp_name">
#                     </div>
#                 </div>
#                 <div class="col-md-4 col-sm-6 col-12 col-lg-4 col-xl-3">
#                     <div class="form-group">
#                         <select class="form-control" id="exampleFormControlSelect1" name="designation">
#                             <option disabled selected>Select Designation</option>
#                             {% for item in department %}
#                             <option value="{{ item }}">{{item}}</option>
#                             {% endfor %}
#                         </select>
#                     </div>
#                 </div>
#                 <div class="col-md-4 col-sm-6 col-12 col-lg-4 col-xl-3">
#                     <div class="d-grid">
#                         <input type="submit" name="search" class="btn btn-success w-100">
#                     </div>
#                 </div>
#             </form>


#             <form method="GET" action="{% url 'search_results' %}" class="row staff-grid-row" id="myForm">
#                 {% csrf_token %}
#                 <div class="col-md-4 col-sm-6 col-12 col-lg-4 col-xl-3">
#                     <div class="form-group">
#                         <input type="text" class="form-control floating" placeholder="Employee ID" name="emp_id">
#                     </div>
#                 </div>
#                 <div class="col-md-4 col-sm-6 col-12 col-lg-4 col-xl-3">
#                     <div class="form-group">
#                         <input type="text" class="form-control floating" placeholder="Employee Name" name="emp_name">
#                     </div>
#                 </div>
#                 <div class="col-md-4 col-sm-6 col-12 col-lg-4 col-xl-3">
#                     <div class="form-group">
#                         <select class="form-control" id="exampleFormControlSelect1" name="designation">
#                             <option disabled selected>Select Designation</option>
#                             {% for item in department %}
#                             <option value="{{ item }}">{{item}}</option>
#                             {% endfor %}
#                         </select>
#                     </div>
#                 </div>
#                 <div class="col-md-4 col-sm-6 col-12 col-lg-4 col-xl-3">
#                     <div class="d-grid">
#                         <input type="submit" name="search" class="btn btn-success w-100">
#                     </div>
#                 </div>
#             </form>
    


#             name = form.cleaned_data.get('name')
#         employee = form.cleaned_data.get('team_members')
#         client = form.cleaned_data.get('client')

#         results = Project.objects.all()

#         if name:
#             results = results.filter(name__icontains=name)
#         if employee:
#             results = results.filter(Q(team_leader__in=[employee]) | Q(
#                 team_members__in=[employee])).distinct()
#         if client:
#             results = results.filter(client=client)




#             def edit_leave(request, leave_id):
#     leave = get_object_or_404(Leave, id=leave_id)
#     if request.method == 'POST':
#         form = LeaveForm(request.POST, instance=leave)
#         if form.is_valid():
#             form.save()
#             return redirect('leaves')
#     else:
#         form = LeaveForm(instance=leave)
#     return render(request, 'edit_leave.html', {'form': form, 'leave_id': leave_id})