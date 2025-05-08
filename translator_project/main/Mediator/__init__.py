from dataclasses import dataclass
from collections import deque
from threading import Thread, Lock
from typing import Optional, Deque
import logging
import requests
from django.conf import settings


@dataclass
class CodeToken:
    language: Optional[str] = None
    input_code: Optional[str] = None
    output_code: Optional[str] = None
    status: Optional[str] = None
    errors: Optional[str] = None


class TranslatorManager:
    def __init__(self, max_queue_size: int = 10):
        self.queue_request: Deque[CodeToken] = deque(maxlen=max_queue_size)
        self.queue_answers: Deque[CodeToken] = deque(maxlen=2*max_queue_size)
        self.active = True  # Флаг активности
        self.lock = Lock()
        self.worker_thread = Thread(target=self._process_queue, daemon=True)
        self.worker_thread.start()

        logging.basicConfig(
            filename="translator.log",
            level=logging.DEBUG,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )
        logging.debug("TranslatorManager initialized.")

    def stop(self):
        """Завершение обработки задач."""
        self.active = False
        self.worker_thread.join()
        logging.info("TranslatorManager stopped.")

    def _process_queue(self):
        while self.active or self.queue_request:
            task: Optional[CodeToken] = None

            with self.lock:
                if self.queue_request:
                    task = self.queue_request.popleft()

            if task:
                logging.debug(f"Processing task: {task.input_code}")
                self._translate(task)
                self.queue_answers.append(task)

    def add_task(self, input_code: str, language: str):
        with self.lock:
            if len(self.queue_request) < self.queue_request.maxlen:
                self.queue_request.append(CodeToken(input_code=input_code, language=language))
                logging.info("Task added." +
                             f"Queue size:{len(self.queue_request)}/" +
                             f"{self.queue_request.maxlen}")
            else:
                logging.warning("Queue is full. Task rejected.")

    def _translate(self, task: CodeToken):
        logging.debug('start debugging')
        try:
            logging.debug(f"Translation are start translate code: {task}")

            response = requests.post(
                settings.TRANSLATOR_API_URL,
                json={
                    "pascal_code": task.input_code,
                    "target_language": task.language
                },
                timeout=1000
            )
            print(response.status_code)
            logging.debug(f"Translation are get response: {response}")

            response.raise_for_status()
            task.output_code = response.json().get('result_code')
            task.errors = response.json().get('errors')

            task.status = 'success' if task.output_code else 'warning'

            logging.info(f"Translation complete: \t {task.output_code}," +
                         f" \n {task.errors}")

        except Exception as ex:
            task.status = "danger"
            task.errors = f"Unexpected {type(ex)=}: {ex=}\n" + \
                          "Стоит обратиться к администратору системы."
            logging.error(task.errors)

    def __str__(self):
        if len(self.queue_answers) != 0:
            return f"""deque has {len(self.queue_answers)} elenemts:\n""" +\
                ', '.join(*self.queue_answers)
        else:
            return 'deque is empty'


if __name__ == '__main__':
    translator = TranslatorManager()

    input_code = "program aaa var i, j: real; b: string; begin i := 1.9 " + \
                 "+ 0.1; writeln(i); end."
    language = 'python'
    translator.add_task(input_code, language)

    # Дождаться завершения обработки
    import time
    time.sleep(2)  # Небольшая задержка для выполнения задач
    translator.stop()  # Корректное завершение
