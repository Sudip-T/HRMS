from django.db.models.signals import pre_delete
from django.db.models.signals import post_save
from .models import Employee,Holiday
from django.dispatch import receiver
from django.db.models import F


@receiver(post_save, sender=Holiday)
def update_employee_leave_days(sender, instance, created, **kwargs):
    if created:  # only for newly created holidays
        Employee.objects.update(total_leave_days=F('total_leave_days')+instance.duration)

@receiver(pre_delete, sender=Holiday)
def decrement_employee_leave_days(sender, instance, **kwargs):
    if not instance.is_passed:
        Employee.objects.update(total_leave_days=F('total_leave_days')-instance.duration)


# @receiver(post_save, sender=Holiday)
# def update_employee_leave_days(sender, instance, created, **kwargs):
#     if created:  # only for newly created holidays
#         Employee.objects.update(total_leave_days=F('total_leave_days')+1)


# @receiver(pre_delete, sender=Holiday)
# def decrement_employee_leave_days(sender, instance, **kwargs):
#     Employee.objects.update(total_leave_days=F('total_leave_days')-1)
