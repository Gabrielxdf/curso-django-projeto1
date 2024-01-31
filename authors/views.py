from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect, render

from .forms import RegisterForm


def register_view(request):

    # getting the session data
    register_form_data = request.session.get('register_form_data', None)

    request.session['number'] = request.session.get('number') or 1
    request.session['number'] += 1

    # bound form, a form that has data if not None.
    form = RegisterForm(register_form_data)

    return render(request, 'authors/pages/register_view.html', context={
        'form': form
    })


def register_create(request):
    if not request.POST:
        raise Http404()

    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterForm(POST)

    if form.is_valid():
        form.save()
        messages.success(request, 'Your user is created, please log in.')

        del (request.session['register_form_data'])

    return redirect('authors:register')
