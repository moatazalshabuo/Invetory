from django.core.paginator import Paginator
from django.shortcuts import render,redirect
from .models import *
from .forms import *
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
@login_required
def index(request):    
    if request.GET.get('query'):
        catogrys = Catogry.objects.filter(name__contains = request.GET['query'])
    else:
        catogrys = Catogry.objects.all()
    paginator = Paginator(catogrys,15)
    page_number = request.GET.get('page')
    catogry = paginator.get_page(page_number)
    form = CatogryForm()
    return render(request,'catogry/index.html',{'catogry':catogry,'form':form,'range':range(1,catogry.paginator.num_pages+1)})

@login_required
def store(request):
    if request.method == "POST":
        print(request.POST)
        form = CatogryForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'status':True,'message':'it\'s done by successfuly with for reload'})
        else:
            return JsonResponse({'status':False,'message':form.errors})
    else:
        return JsonResponse({'message':'error'},status=400)

@login_required   
def delete(request,uuid):
    catogry = get_object_or_404(Catogry,pk=uuid)
    
    if catogry.countDevices == 0:
        catogry.delete()
    else:
        message = "Cannot delete this category it has "+ str(catogry.countDevices())+" devices"
        messages.error(request,message)
    referring_url = request.META.get('HTTP_REFERER')
    return redirect(referring_url)

@login_required
def show(request,id):
    category = get_object_or_404(Catogry,pk=id)
    return render(request,"catogry/show.html",{'category':category})

@login_required
def update_category(request,id):
    category = Catogry.objects.get(pk=id)
    form = CatogryForm(request.POST or None,instance=category)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('catogry.index')
    return render(request,'catogry/edit.html',{'form':form})