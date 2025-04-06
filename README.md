# Вебсайт транслятора множества языка программирования pascal в python

Интерфейс для транслятора с Turbo Pascal на Python 3.6 на основе Django 5.1.4. Создан командой студентов Департамента программной инженерии и исскуственного интелекта Дальневосточного федерального университета в рамках дисциплин Теория языков программирования и компиляторы и Коллективная разработка в 2024-2025 учебном году (4 курс). 
Транслятор реализован на Python 3.9, имеет API - [https://github.com/VerkhovtsovDenis/python-translator-api](https://github.com/VerkhovtsovDenis/python-translator-api)

## Запуск
0. Установка python, git
    1. Установить Python 3.12.3: https://www.python.org/downloads/
    2. Установить Git: https://git-scm.com/downloads
1. Клонировать репозиторий
```bash
git clone https://github.com/VerkhovtsovDenis/python-translator-website.git
```
2. Создание и настройка виртуального окружения
```bash
cd python-translator-website
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
```
3. Миграции и запуск
```bash
python translator_project/manage.py makemigrations
python translator_project/manage.py migrate
python translator_project/manage.py runserver 8000
```
Если проект уже установлен
```bash
translator_project/manage.py runserver 192.168.1.37:8000
```

4. Перейти по [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Деплой
Для деплоя используется инструмент ci/cd werf. Werf автоматизирует сборку образа и его доставку в k8s. 

Деплой запускается командой `werf converge --repo omelchenkomaxim/translator-website`.

Перед запуском команды необходимо подключить kubectl к нужному кластеру, подключить docker к нужному registry и прокинуть креды от registry в k8s.

Подробнее с началом работы с werf можно ознакомится [тут](https://ru.werf.io/guides/django/100_basic/20_cluster.html).

Приложение разворачивается по адресу `http://158.160.180.43/translator-website/`
