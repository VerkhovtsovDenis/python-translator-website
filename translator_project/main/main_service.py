from .models import History, SupportLanguage
from typing import Optional, Deque, Union, List
from .forms import TranslateForm
from .Mediator import CodeToken, TranslatorManager
from django.http import JsonResponse
from enum import Enum
from dataclasses import dataclass
import time
from main.Mediator import logging


Status = Enum('status', [('success', 1), ('error', 2), ('info', 3)])


@dataclass
class ConsoleData:
    time_now: str
    status: Enum
    message: str

    @staticmethod
    def time_to_str():
        time_now = time.localtime(time.time())
        formst = time.strftime("%Y-%B-%d %H:%M:%S", time_now)
        return formst

    def __init__(self, status, message):
        self.time_now = ConsoleData.time_to_str()
        self.status = status
        self.message = message


console_list: List[ConsoleData] = []


def return_python_code_with_console_log(request: dict,
                                        form: TranslateForm) -> \
                                    Union[Optional[str], List[ConsoleData]]:
    """Возвращает транслированный Python код с инорфмацией для консоли"""
    input_code: str = ''

    try:
        input_code = form.cleaned_data['input_code']
        language = form.cleaned_data['language']

    except ValueError:
        return JsonResponse({'success': False,
                             'message': 'Передайте форму с кодом'})

    translator = TranslatorManager()
    translator.add_task(input_code, language)

    while not translator.queue_answers:
        time.sleep(2)

    if not translator.queue_answers:
        return JsonResponse({'success': False, 'message': 'Ошибка API'})

    code_token, console = _generate_console_data_from_task(
        queue=translator.queue_answers)

    _create_history_from_code(request=request,
                              code_token=code_token)

    console_list.append(console)

    return code_token.output_code, console_list


def return_history_objects() -> List[object]:
    print(History.objects.all())
    return History.objects.all()


def delete_all_history_objects() -> None:
    History.objects.all().delete()
    print("del obj")


def _generate_console_data_from_task(queue: Deque[CodeToken]):
    task: CodeToken = queue.popleft()
    console: ConsoleData

    if task.output_code:
        console = ConsoleData(Status.success, "Перевод кода на Python выполнен\
                               успешно")
    elif task.errors:
        console = ConsoleData(Status.error, task.errors)
    else:
        console = ConsoleData(Status.info, 'Перевод в процессе...')

    return task, console


def _create_history_from_code(request: dict,
                              code_token: CodeToken) -> None:
    """Создает запись в таблице History с данными кода Паскаль pascal_code,\
       кода Питона python_code, ошибок компиляции translate_errors"""
    print(code_token)
    History.objects.get_or_create(
        ip_address=_get_user_ip_address_from_request(
            request_meta=request.META
        ),
        language=SupportLanguage.objects.get(name=code_token.language.capitalize()),
        input_code=code_token.input_code,
        output_code=code_token.output_code or '',
        translating_status=code_token.status,
        translating_errors=code_token.errors,
    )


def _get_user_ip_address_from_request(request_meta: dict) -> str:
    """Возвращает индентификатор пользователя по метаданным \
       запроса request_meta"""

    if x_forwarded_for := request_meta.get('HTTP_X_FORWARDED_FOR'):
        return str(x_forwarded_for.split(',')[0])
    else:
        return str(request_meta.get('REMOTE_ADDR'))
