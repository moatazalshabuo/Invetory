from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from .forms import *
from django.contrib.auth.forms import PasswordChangeForm,SetPasswordForm
from django.contrib.auth.decorators import login_required,permission_required
from Item.Helper import users as getuser,user as get_user
from django.http import JsonResponse
from .models import UserInfo
from django.contrib import messages
from django.contrib.auth.models import Permission
# Create your views here.

def view_login(request):
    message = ''
    if request.method == "POST":
        if request.POST.get('username') and request.POST.get('password'):
            user = authenticate(request,
                                username = request.POST.get('username'),
                                password=request.POST.get('password')
                                )
            if user is not None:
                login(request,user)
                return redirect('index')
            else:
                message='Login failed'
        else:
            message = 'Please check your password and username'
    return render(request,'auth/login.html',{'msg':message})

@login_required
def view_logout(request):
    logout(request)
    return redirect('login')


@login_required
@permission_required(['view_user'])
def users(request):
    users = User.objects.all()
    paginator = Paginator(users,15)
    page_number = request.GET.get('page')
    user = paginator.get_page(page_number)
    return render(request,"users/index.html",{'users':user,'range':range(1,user.paginator.num_pages+1)})


@login_required
@permission_required(['add_user'])
def create_user(request):
    if request.user.is_superuser:
        form = UserForm(request.POST or None)
        message = None
        status = None
        permission = Permission.objects.all()
        if request.method == "POST":
            if 'employee' in request.POST:
                emp = get_user(request.POST['employee'])
                if 'userPrincipalName' in emp:
                    if form.is_valid():
                        user = form.save(commit=False)
                        user.email = emp['userPrincipalName']
                        user.save()
                        UserInfo.objects.create(user=user,id_user=emp['id'])
                        if not user.is_superuser:
                            for perim in request.POST.getlist('permission'):
                                user.user_permissions.add(Permission.objects.get(pk=perim))
                        messages.success(request,"save user done succesfully")
                        form = UserForm()
                else:
                    messages.error(request,'someting wrong with employee place try again')  
            else:
                messages.error(request,'place cohice employee to connect with user')    
        return render(request,'users/create.html',{'form':form,'permission':permission})
    else:
        return render(request,'template/home/page-404.html')
    
@login_required
@permission_required(['change_user'])
def update_user(request,id):
    if request.user.is_superuser:
        user = User.objects.get(pk=id)
        form = UserFormUpdate(request.POST or None,instance=user)
        if request.method == "POST":
            if form.is_valid():
                form.save()
                return redirect('users')
        return render(request,'users/edit.html',{'form':form})
    else:
        return render(request,'template/home/page-404.html')

@login_required
@permission_required(['change_user'])
def change_status(request,id):
    if request.user.is_superuser:
        user = User.objects.get(pk=id)
        user.is_active = not user.is_active
        user.save()
        return redirect('users')
    else:
        return render(request,'template/home/page-404.html')

@login_required
def change_password(request,id):
    user = User.objects.get(pk=id)
    form = PasswordChangeForm(user,request.POST or None)
    message =""
    if request.method == "POST":
        if form.is_valid():
            form.save()
            message = "it's done successfully !"
    return render(request,'users/password.html',{'form':form,"message":message})

@login_required
@permission_required(['change_user'])
def assing_permission(request,id):
    user = User.objects.get(pk=id)
    permission = Permission.objects.all()
    if request.method == "POST":
        for perm in request.POST.getlist('permission'):
            if not user.has_perm(Permission.objects.get(pk=perm)):
                user.user_permissions.add(perm)
        for perm in user.user_permissions.all():
            if str(perm.id) not in request.POST.getlist('permission'):
                user.user_permissions.remove(perm)
    return render(request,'users/assing_permission.html',{'user':user,'permission':permission})

@login_required
def set_password(request,id):
    user = User.objects.get(pk=id)
    form = SetPasswordForm(user,request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('users')
    return render(request,'users/password.html',{'form':form})

@login_required
def index(request):
    return render(request,'index.html')


@login_required
def setting(request):
    return render(request,'setting/index.html')

@login_required
def email(request):
    emails = EmailSenderTo.objects.all()
    
    if request.method == "POST":
        employee = get_user(request.POST['id'])
        if 'userPrincipalName' in employee:
            emailsenderto = EmailSenderTo(email = employee['userPrincipalName'])
            emailsenderto.save()
            messages.success(request,'save done')
        else:
            messages.error(request,'employee worng')
    return render(request,'setting/email.html',{"emails":emails})

@login_required
def delete_email(request,id):
    email = EmailSenderTo.objects.get(pk=id)
    email.delete()
    messages.success(request,'deleted done successfully')
    return redirect('email.setting')