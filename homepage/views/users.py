from django.conf import settings
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone
from django.contrib.auth.decorators import login_required
from homepage import models as m
from django import forms
from django.http import  HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


############### LIST USERS ###############
@view_function
@login_required(login_url='/index')
def process_request(request):
    '''Lists the users in a table on the page'''

    #require login
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/index')

    #get all users from DB
    users = User.objects.all()

    context = {
        'users': users,
    }

    return request.dmp_render('users.html', context)

############### CREATE USER ###############
@view_function
@login_required(login_url='/index')
def create(request):
    '''Creates a new user using a form'''

    #require login
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/index')

    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            u = User()
            u.username = form.cleaned_data.get('username')
            u.email = form.cleaned_data.get('username')
            u.first_name = form.cleaned_data.get('first_name')
            u.last_name = form.cleaned_data.get('last_name')
            u.set_password(form.cleaned_data.get('password'))
            u.save()

    context = {
        'form': form,
    }

    return request.dmp_render('users.create.html', context)


class CreateUserForm(forms.Form):
    username = forms.EmailField(label='Email', required=True, max_length=100, widget=forms.EmailInput(attrs={ 'class' : 'form-control'}))
    first_name = forms.CharField(label='First Name', required=True, max_length=100, widget=forms.TextInput(attrs={ 'class' : 'form-control'}))
    last_name = forms.CharField(label='Last Name', required=True, max_length=100, widget=forms.TextInput(attrs={ 'class' : 'form-control'}))
    password = forms.CharField(label='Password', required=True, max_length=100, widget=forms.PasswordInput(attrs={ 'class': 'form-control', 'minlength': '6' }))
    password2 = forms.CharField(label='Confirm Password', required=True, max_length=100, widget=forms.PasswordInput(attrs={ 'class': 'form-control' }))

    def clean_username(self):
        username = self.cleaned_data.get('username')

        users = User.objects.filter(username = self.cleaned_data.get('username')) #this would give you a list
        if len(users) > 0:
            raise forms.ValidationError('This username has been taken')
        return username

    def clean(self):
        if self.cleaned_data.get('password') != self.cleaned_data.get('password2'):
            raise forms.ValidationError('Your passwords do not match') #this is a return statement
        return self.cleaned_data


############### EDIT USER ###############
@view_function
@login_required(login_url='/user/login')
def edit(request):
    '''Edits/Updates a preexisting user using a form'''

    #require login
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/index')

    #get user by id
    try:
        user = User.objects.get(id=request.urlparams[0])
    except User.DoesNotExist:
        return HttpResponseRedirect('/users')

    # initalize form
    form = EditUserForm(initial={
        'user_id': user.id,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
    })

    if request.method == 'POST':
        form = EditUserForm(request.POST)
        if form.is_valid():
            u = User.objects.get(id=request.urlparams[0])
            u.first_name = form.cleaned_data.get('first_name')
            u.last_name = form.cleaned_data.get('last_name')
            u.email = form.cleaned_data.get('email')

            u.save()

            return HttpResponse('''
            <script>
                window.location.href = '/users';
            </script>
            ''')

    context = {
        'form': form,
        'user': user,
    }

    return request.dmp_render('users.edit.html', context)

class EditUserForm(forms.Form):
    user_id = forms.CharField(label='ID', required=False, disabled=True, widget=forms.TextInput(attrs={ 'class' : "form-control" }))
    username = forms.CharField(label='Username', required=False, disabled=True, widget=forms.TextInput(attrs={ 'class' : "form-control" }))
    first_name = forms.CharField(label='First Name', required=True, max_length=100, widget=forms.TextInput(attrs={ 'class': 'form-control' }))
    last_name = forms.CharField(label='Last Name', required=True, max_length=100, widget=forms.TextInput(attrs={ 'class': 'form-control' }))
    email = forms.EmailField(label='Email', required=True, max_length=100, widget=forms.EmailInput(attrs={ 'class': 'form-control' }))



############### DELETE USER ###############
@view_function
@login_required(login_url='/index')
def delete(request):
    '''Deletes a preexisting user from DB'''

    #require login
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/index')

    #get user
    try:
        user = User.objects.get(id=request.urlparams[0])
    except User.DoesNotExist:
        return HttpResponseRedirect('/users')

    #delete user
    user.delete()

    return HttpResponse('''
    <script>
        window.location.href = '/users';
    </script>
    ''')
