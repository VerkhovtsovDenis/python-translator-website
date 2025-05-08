from django.db import models
from django.utils import timezone
from django.utils import timezone
now = timezone.now()


class SupportLanguage(models.Model):
    name = models.CharField(primary_key=True,
                            help_text='Язык программирования',
                            max_length=64)

    def __str__(self):
        return self.name

    @classmethod
    def ensure_default_languages(cls):
        """Создаёт языки по умолчанию, если их нет."""
        cls.objects.get_or_create(name='Python')
        cls.objects.get_or_create(name='Go')


class History(models.Model):
    ip_address = models.GenericIPAddressField(help_text='Ip address')
    req_date = models.DateTimeField(help_text='Time and date of request',
                                    default=timezone.now)

    input_code = models.CharField(help_text='Input code', max_length=5000,
                                   blank=True)
    output_code = models.CharField(help_text='Output code', max_length=5000,
                                   blank=True,
                                   null=True)
    language = models.ForeignKey(
        SupportLanguage,
        on_delete=models.CASCADE,
        null=True,  # Разрешить NULL временно
        blank=True,
        to_field='name',  # Указываем ссылку на поле 'name'
        db_column='language_name',  # Опционально: переименовываем столбец в БД
        verbose_name='Выходной язык программирования'
    )

    translating_status = models.CharField(help_text='Translating information',
                                        max_length=150, blank=True)
    translating_errors = models.CharField(help_text='Translating errors',
                                          max_length=300, blank=True)


def __str__(self):
    fields = [
        ('ip_address', self.ip_address),
        ('req_date', self.req_date),
        ('input_code', self.input_code),
        ('output_code', self.output_code),
        ('language', self.language),
        ('translating_status', self.translating_status),
        ('translating_errors', self.translating_errors),
    ]
    return '\n'.join(
        f'{self._meta.get_field(field_name).help_text}: {value}'
        for field_name, value in fields
    )
