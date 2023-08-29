from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q


def get_or_none(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None


def get_multiple_model_data():
    now = timezone.now()
    from .models import Holiday
    data= {
        'holiday': Holiday.objects.filter(start_date__gte=now).order_by('start_date').first()
    }
    return data


def multiple_model_data():
    from .models import Employee,Client,Project,ClientInvoice,ClientPayment,Leave,Task
    data = {
        'tasks':Task.objects.all(),
        'emp':Employee.objects.all(),
        'clients' : Client.objects.all(),
        'leave' : Leave.objects.all()[:2],
        'clients2' : Client.objects.all()[:3],
        'projects': Project.objects.all()[:3],
        'emp_count':Employee.objects.all().count(),
        'project_count':Project.objects.all().count(),
        'clientinvoice' : ClientInvoice.objects.all()[:3],
        'clientpayment' : ClientPayment.objects.all()[:3],
        'total_invoice':ClientInvoice.objects.all().count(),
        'new_tasks_count': Task.objects.filter(task_status='New').count(),
        'pending_project': Project.objects.filter(status='Pending').count(),
        'pending_invoice': ClientInvoice.objects.filter(status='Paid').count(),
        'working_tasks_count': Task.objects.filter(task_status='Working').count(),
        'pending_tasks_count': Task.objects.filter(task_status='Pending').count(),
        'completed_tasks_count': Task.objects.filter(task_status='Completed').count(),
    }
    return data

# generates ids for client payment and client invoice
def generate_invoice_id(model_class, prefix):
    last_invoice = model_class.objects.order_by('-invoice_id').first()
    if last_invoice:
        last_invoice_id = int(last_invoice.invoice_id.split('-')[1])
        next_invoice_id = last_invoice_id + 1
    else:
        next_invoice_id = 1
    return f'{prefix}-{next_invoice_id:04d}'


# generates employee id
def generate_id(model_class, prefix):
    last_object = model_class.objects.order_by('-emp_id').first()
    if last_object:
        last_id = int(last_object.emp_id.split('-')[1])
        next_id = last_id + 1
    else:
        next_id = 1
    return f'{prefix}-{next_id:04d}'


# employee model - user account creation after employee registration
def create_user_account(username, is_admin, passwd):
    # password = get_random_string(8)

    user = User.objects.create_user(username=username, password=passwd)
    user.is_staff = is_admin
    user.is_superuser = is_admin
    user.save()

    return user

def send_welcome_email(username, email, passwd):
    send_mail(
        'Hello',
        f'Your username is {username} and your password is {passwd}',
        settings.EMAIL_HOST_USER,
        [email],  # Send the email to the employee's email
    )


def generic_search(model, search_params, request):
    results = model.objects.all()
    for key,value in search_params.items():
        search_query = request.GET.get(value)

        if search_query:
            kwargs = {f'{key}__icontains': search_query}
            results = results.filter(**kwargs)
            
    return results



def filter_projects(form):
    from .models import Project
    name = form.cleaned_data.get('name')
    employee = form.cleaned_data.get('team_members')
    client = form.cleaned_data.get('client')

    results = Project.objects.all()

    if name:
        results = results.filter(name__icontains=name)
    if employee:
        results = results.filter(Q(team_leader__in=[employee]) | Q( team_members__in=[employee])).distinct()
    if client:
        results = results.filter(client=client)

    return results