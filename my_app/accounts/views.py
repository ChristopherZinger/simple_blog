#djagno import
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.views.generic import View

# from django.contrib.auth.tokens import default_token_generator

import time

# local imports
from accounts.models import User
from accounts.forms import (
    UserForm, UserInfoForm, ResetPasswordForm, UserUpdateForm
)



def user_home(request, user_slug):
    if request.user.is_authenticated and request.user.slug == user_slug:
        user = request.user
        return render(request,'accounts/user_home.html',{'user': user, 'user_info':user.user_info,})
    else:
        messages.error(request, 'You need to log in first.')
        return redirect('index')


def user_info_update(request, user_slug):
    if request.user.is_authenticated and request.user.slug == user_slug:
        if request.method == "POST":
            user = User.objects.get(slug=user_slug)
            user_info_form = UserInfoForm(request.POST)
            if user_info_form.is_valid():
                user.user_info.first_name = request.POST.get('first_name')
                user.user_info.last_name = request.POST.get('last_name')
                user.user_info.save()
            return redirect('accounts:user_home', user_slug=request.user.slug)
        else:
            user_info_form = UserInfoForm(initial={
                'first_name':request.user.user_info.first_name,
                'last_name':request.user.user_info.last_name,
            })

            return render(request, 'accounts/user_info_update.html', {'user_info_form':user_info_form, })
    else:
        messages.error('Sorry. Error occured while proccesing your request.')
        return redirect('index')



@login_required
def user_update(request, user_slug):
    if request.method == "POST" and user_slug == request.user.slug :
        form = UserUpdateForm(request.POST)
        user = get_object_or_404(User, slug=user_slug)
        if form.is_valid():
            email = request.POST.get('email')
            new_password = request.POST.get('new_password')
            repeat_password = request.POST.get('repeat_password')
            current_password = request.POST.get('current_password')
            # check if email already exists
            if User.objects.filter(email=email).exists() and email != user.email:
                messages.error(request, 'This email is already taken, try another.')
                return redirect('accounts:user_update', user_slug=user_slug)


            #check password
            if user.check_password(current_password):
                #check if password is to be updated
                if  new_password != '' :
                    if new_password == repeat_password :
                        user.set_password(new_password)
                    else:
                        print( 'new password : {}, repeat: {}'.format(new_password, repeat_password))
                        messages.error(request, 'New password repeated incorrectly, try again.')
                        return redirect('accounts:user_update', user_slug=user_slug)
                #save email
                user.email = email
                user.save()
                messages.success(request, 'Credentials were updated successfuly.')
                # log in user with new credentials
                user = authenticate(request, username=email, password=new_password)
                login(request, user)
                return redirect('accounts:user_home', user_slug=user_slug)
            else: # wrong password
                messages.error(request, 'Wrong Password')
                return redirect('accounts:user_update', user_slug=user_slug)

        else: # invalid form
            messages.error(request, 'Ups. Something went wrong.')

        return redirect('accounts:user_home', user_slug=user_slug)
    else:
        form = UserUpdateForm(initial={
            'email': request.user.email,
        })
        return render(request, 'accounts/user_update.html',{
            'user_update_form':form,
        })

def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        # check if user Exists and have a unique email
        try:
            user = User.objects.get(email=email)
        except User.MultipleObjectsReturned:
            messages.error(request, 'Error. There is a problem with your accout. Please contact web administrator.')
            user = None
            return redirect('accounts:login',)
        except User.DoesNotExist:
            messages.error(request, 'Email not found.')
            return redirect('accounts:login')

        # Authenticate user
        user = authenticate(request, username=email, password=password)
        if user is not None:
            # Procced to Log In the user
            login(request, user)
            # check for next value in case user is already logged in
            # and want to change password or email for example
            if 'next' in request.POST:
                return redirect(request.POST.get('next')) # next is taken form the form hidden input
            return redirect('accounts:user_home', user_slug=user.slug)
        else:
            # Wrong Passowrd
            messages.error(request, 'Wrong passowrd .')
            return redirect('accounts:login',)
    else: # If method is GET
        return render(request,'accounts/login.html')


def user_logout(request):
    logout(request)
    messages.success(request, 'Your are logged out.') # ignored
    return redirect('index')


def user_create(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        user_info_form = UserInfoForm(data=request.POST)

        email = request.POST.get('email')
        password = request.POST.get('password')
        #check if user already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'This email is already reserved.')
            return redirect('accounts:user_create')
        # save new user
        if user_form.is_valid() and user_info_form.is_valid():

            user = user_form.save(commit=False)
            password = user_form.cleaned_data['password']
            email = user_form.cleaned_data['email']

            user.set_password(password)
            user.email = email
            user.save()
            #save user profile form
            user_info = user_info_form.save(commit=False)
            user_info.user = user

            '''
            uncoment below in case there is a photo to save
            '''
            #check if profile picture is ready to be saved
            # if 'profile_pic' in request.FILES:
            #     user_info.profile_pic = request.FILES['profile_pic']
            #     user_info.save()
            # else:
            #     print(user_form.errors, profile_form.errors)

            user_info.save()
        else:
            messages.error(request, 'Login Error. The credentials are incorrect.')
            return redirect('index',)

        # log in user after creating him/her
        messages.error(request, ' Welcome! Your account has been created.')
        user = authenticate(request, username=email, password=password)
        login(request, user)
        if 'next' in request.POST:
            return redirect(request.POST.get('next')) # next is taken form the form hidden input
        return redirect('accounts:user_home', user_slug=user.slug)

    else:
        user_info_form = UserInfoForm()
        user_form = UserForm()
        return render(request, 'accounts/user_create.html',
            {"user_form":user_form, "user_info_form":user_info_form}
        )


# def user_update(request, user.slug)
