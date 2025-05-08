from django.shortcuts import render, redirect
from .forms import TranslateForm
from django.http import JsonResponse
from .main_service import return_python_code_with_console_log, \
                         return_history_objects, \
                         delete_all_history_objects


def index(request):
    template_name = 'main/index.html'
    console = []
    code: str = ''

    if request.method == "POST":
        form = TranslateForm(request.POST)

        if form.is_valid():
            code, console = return_python_code_with_console_log(
                request=request,
                form=form
            )
        else:
            return JsonResponse({'success': False,
                                 'message': 'Form is invalid'})
    else:
        form = TranslateForm()

    return render(request, template_name, {'console': console,
                                           'form': form,
                                           'python_code': code})


def about(request):
    template_name = 'pages/about.html'
    return render(request, template_name)


def history(request):
    template_name = 'main/history.html'
    history = return_history_objects()
    return render(request, template_name, {'history': history})


def history_del(request):
    delete_all_history_objects()
    print('delete')
    return redirect('/history/', request)
