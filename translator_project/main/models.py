from django.db import models
from django.utils import timezone
from django.utils import timezone
now = timezone.now()


# Create your models here.
class History(models.Model):
    ip_address = models.GenericIPAddressField(help_text='Ip address')
    req_date = models.DateTimeField(help_text='Time and date of request',
                                    default=timezone.now)

    pascal_code = models.CharField(help_text='Pascal code', max_length=5000,
                                   blank=True)
    python_code = models.CharField(help_text='Python code', max_length=5000,
                                   blank=True,
                                   null=True)

    translating_status = models.CharField(help_text='Translating information',
                                        max_length=150, blank=True)
    translating_errors = models.CharField(help_text='Translating errors',
                                          max_length=300, blank=True)


def __str__(self):
    fields = [
        ('ip_address', self.ip_address),
        ('req_date', self.req_date),
        ('pascal_code', self.pascal_code),
        ('python_code', self.python_code),
        ('translating_status', self.translating_status),
        ('translating_errors', self.translating_errors),
    ]
    return '\n'.join(
        f'{self._meta.get_field(field_name).help_text}: {value}'
        for field_name, value in fields
    )
