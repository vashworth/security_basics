from django.conf import settings
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone
from django.contrib.auth.decorators import login_required
from homepage import models as m
from django import forms
from django.http import  HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User

############### LIST SECURITY FLAWS ###############
@view_function
@login_required(login_url='/index')
def process_request(request):
    '''Lists the security flaws in a table on the page'''

    #require login
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/index')

    #get all security flaws from DB
    flaws = m.SecurityFlaw.objects.all()

    p = User.objects.raw('SELECT * FROM auth_user WHERE username=test')
    print(p)

    context = {
        'flaws': flaws,
    }

    return request.dmp_render('securityflaws.html', context)


############### CREATE SECURITY FLAW ###############
@view_function
@login_required(login_url='/index')
def create(request):
    '''Creates a new security flaw using a form'''

    #require login
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/index')

    form = CreateSecurityFlawForm()
    if request.method == 'POST':
        form = CreateSecurityFlawForm(request.POST)
        if form.is_valid():
            #create new security flaw
            s = m.SecurityFlaw()
            s.name = form.cleaned_data.get('name')
            s.description = form.cleaned_data.get('description')
            s.exploitability = form.cleaned_data.get('exploitability')
            s.prevalence = form.cleaned_data.get('prevalence')
            s.detectability = form.cleaned_data.get('detectability')
            s.impact = form.cleaned_data.get('impact')
            s.OWASP = form.cleaned_data.get('OWASP')
            s.save()

            return HttpResponse('''
            <script>
                window.location.href = '/securityflaws';
            </script>
            ''')

    context = {
        'form': form,
    }
    return request.dmp_render('securityflaws.create.html', context)

class CreateSecurityFlawForm(forms.Form):
    name = forms.CharField(label='Name', required=True, max_length=100, widget=forms.TextInput(attrs={ 'class' : "form-control" }))
    description = forms.CharField(label='Description', required=True, max_length=100, widget=forms.TextInput(attrs={ 'class' : "form-control" }))
    exploitability = forms.CharField(label='Exploitability', required=True, max_length=100, widget=forms.TextInput(attrs={ 'class' : "form-control" }))
    prevalence = forms.CharField(label='Prevalence', required=True, max_length=100, widget=forms.TextInput(attrs={ 'class' : "form-control" }))
    detectability = forms.CharField(label='Detectability', required=True, max_length=100, widget=forms.TextInput(attrs={ 'class' : "form-control" }))
    impact = forms.CharField(label='Impact', required=True, max_length=100, widget=forms.TextInput(attrs={ 'class' : "form-control" }))
    OWASP = forms.CharField(label='OWASP Link', required=True, max_length=100, widget=forms.TextInput(attrs={ 'class' : "form-control" }))


############### EDIT SECURITY FLAW ###############
@view_function
@login_required(login_url='/index')
def edit(request):
    '''Edits/Updates a preexisting security flaw using a form'''

    #require login
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/index')

    #get security flaw by id
    try:
        flaw = m.SecurityFlaw.objects.get(id=request.urlparams[0])
    except m.SecurityFlaw.DoesNotExist:
        return HttpResponseRedirect('/securityflaws')

    #initalize form
    form = EditSecurityFlawForm(initial={
        'name': flaw.name,
        'description': flaw.description,
        'exploitability': flaw.exploitability,
        'prevalence': flaw.prevalence,
        'detectability': flaw.detectability,
        'impact': flaw.impact,
        'OWASP': flaw.OWASP,
    })

    if request.method == 'POST':
        form = EditSecurityFlawForm(request.POST)
        if form.is_valid():
            #get security flaw by id and update values
            s = m.SecurityFlaw.objects.get(id=request.urlparams[0])
            s.name = form.cleaned_data.get('name')
            s.description = form.cleaned_data.get('description')
            s.exploitability = form.cleaned_data.get('exploitability')
            s.prevalence = form.cleaned_data.get('prevalence')
            s.detectability = form.cleaned_data.get('detectability')
            s.impact = form.cleaned_data.get('impact')
            s.OWASP = form.cleaned_data.get('OWASP')

            s.save()

            return HttpResponseRedirect('/securityflaws')

    context = {
        'flaw': flaw,
        'form': form,
    }
    return request.dmp_render('securityflaws.edit.html', context)

class EditSecurityFlawForm(forms.Form):
    name = forms.CharField(label='Name', required=True, max_length=100, widget=forms.TextInput(attrs={ 'class' : "form-control" }))
    description = forms.CharField(label='Description', required=True, max_length=100, widget=forms.TextInput(attrs={ 'class' : "form-control" }))
    exploitability = forms.CharField(label='Exploitability', required=True, max_length=100, widget=forms.TextInput(attrs={ 'class' : "form-control" }))
    prevalence = forms.CharField(label='Prevalence', required=True, max_length=100, widget=forms.TextInput(attrs={ 'class' : "form-control" }))
    detectability = forms.CharField(label='Detectability', required=True, max_length=100, widget=forms.TextInput(attrs={ 'class' : "form-control" }))
    impact = forms.CharField(label='Impact', required=True, max_length=100, widget=forms.TextInput(attrs={ 'class' : "form-control" }))
    OWASP = forms.CharField(label='OWASP Link', required=True, max_length=100, widget=forms.TextInput(attrs={ 'class' : "form-control" }))



############### DELETE SECURITY FLAW ###############
@view_function
@login_required(login_url='/index')
def delete(request):
    '''Deletes a preexisting security SecurityFlaw from DB'''

    #require login
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/index')

    #get security flaw
    try:
        flaw = m.SecurityFlaw.objects.get(id=request.urlparams[0])
    except m.SecurityFlaw.DoesNotExist:
        return HttpResponseRedirect('/securityflaws')

    #delete secuirty flaw
    flaw.delete()

    return HttpResponse('''
    <script>
        window.location.href = '/securityflaws';
    </script>
    ''')
