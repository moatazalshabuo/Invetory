from django.shortcuts import render,redirect
from .forms import *
from .models import *
from catogry.models import Catogry
from .serializers import *
from django.http import JsonResponse,HttpResponse
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required,permission_required
from .Helper import *
from django.contrib import messages
from django.urls import reverse
from .Helper import sendMail
# Create your views here.


@login_required
@permission_required(['view_device'])
def index(request):
    dev = Device.objects.all()
    if request.GET.get('catogry'):
        dev = dev.filter(catogry__id = request.GET.get('catogry'))
    if request.GET.get('model'):
        dev = dev.filter(modal__id = request.GET.get('model'))
    if request.GET.get('status'):
        dev = dev.filter(status = request.GET.get('status'))
    if request.GET.get('service_tag'):
        dev = dev.filter(service_tag = request.GET.get('service_tag'))
  
    Devices = Paginator(dev,10)  
    page_number = request.GET.get('page') 
    devices = Devices.get_page(page_number)
    catogry = Catogry.objects.all()
    model = ModelDevice.objects.all()
    employee = Employee.objects.all()
    history = HistoryDeviceForm()
    status = StatusName
    return render(request,'item/index.html',{
        'devices':devices,
        'range':range(1,devices.paginator.num_pages+1),
        'catogry':catogry,
        'model':model,
        'status':status,
        'employee':employee,
        'historyForm':history
        })

@login_required
@permission_required(['add_device'])
def create_device(request):
    message = ''
    list_service = []
    fail_list = []
    type = request.GET.get('type') or 'one'
    form = DeviceForm()
    formfile = FileDeviceForm()
    formModal = ModalForm()
    fileDivece  = None
    if request.method == 'POST':
        
        if request.FILES.get('file') != None:
                formfile = FileDeviceForm(request.POST,request.FILES)
                if formfile.is_valid():
                    fileDivece = formfile.save()
                    
        if request.POST.get('type') == 'one':
            form = DeviceForm(request.POST)
            
            if form.is_valid():
                device = form.save(commit=False)
                if fileDivece != None:
                    device.file = fileDivece
                device.save()
                # Do something with the saved device
                message = "save successfully"
                form = DeviceForm()
                formfile = FileDeviceForm()
        else:
            try:
                for val in request.POST.getlist('sevice_tags[]'):
                    if not Device.objects.filter(service_tag=val).exists():
                        newdevice = Device(
                            catogry=Catogry.objects.get(pk=request.POST.get('catogry')),
                            service_tag=val,
                            modal=ModelDevice.objects.get(pk=request.POST.get('modal')),
                            store=Store.objects.get(pk=request.POST.get('store')),
                            purchase_date=request.POST.get('purchase_date'),
                            supplier=request.POST.get('supplier'),
                            Warranty_date= request.POST.get('Warranty_date')
                            )
                        if fileDivece != None:
                            newdevice.file = fileDivece
                        newdevice.save()
                        list_service.append(val)
                    else:
                        fail_list.append({'sirvec':val,'message':"alredy exist"})
                    
            except Exception as e:
                message = e             
    modal = ModelDevice.objects.all()
    store = Store.objects.all()
    catogry = Catogry.objects.all()
    
    devices = ModelDevice.objects.all()
    return render(request, 
                  'item/create.html', 
                  {'form': form,
                   'modal':modal,
                   'store':store,
                   'catogry':catogry,
                   'message':message,
                   'devices':devices,
                   'type':type,
                   'list_service':list_service,
                   'fail_list':fail_list,
                   'formfile':formfile,
                   'formModal':formModal
                   })

@login_required
@permission_required(['add_modeldevice'])
def addModal(request):
    
    if request.method == "POST":
        form = ModalForm(request.POST)
        if form.is_valid():
            modal_device = form.save()
            return JsonResponse({'data':ModalDeviceSerializer(modal_device).data})
        
        else:
            return JsonResponse({'error':form.errors},status=400)

@login_required
@permission_required(['view_modeldevice'])
def getModal(request,id):
    modal = Catogry.objects.get(pk=id).modal.all()
    return JsonResponse(ModalDeviceSerializer(modal,many=True).data,safe=False)

@login_required
@permission_required(['change_modeldevice'])
def editModal(request,id):
    modal = ModelDevice.objects.get(pk=id)
    form = ModalForm(request.POST or None,instance = modal)
    if request.method == "POST":
        
        if form.is_valid():
            form.save()
            messages.success(request,'edit modal done successfully')
            detail_url = reverse('categry.show', kwargs={'id': modal.catogry.id})

            # Use the redirect function to redirect to the detail view with the specified ID
            return redirect(detail_url)
    return render(request,"catogry/modalEdit.html",{'modal':modal,'form':form})
    
            
@login_required
@permission_required(['delete_modeldevice'])
def deleteModal(request,id):
    modal = get_object_or_404(ModelDevice,pk=id)
    if len(modal.device.all()) == 0:
        modal.delete()
        message = 'deleted done by seccussfuly'
    else:
        message = "cannot delete this modal"
    modals = ModalDeviceSerializer(ModelDevice.objects.all(),many=True).data
    return JsonResponse({'message':message,'data':modals})

@login_required
@permission_required(['delete_store'])
def deleteStore(request,id):
    store = get_object_or_404(Store,pk=id)
    if len(store.device.all()) + len(store.spare_part.all()) == 0:
        
        store.delete()
        message = 'deleted done by seccussfuly'
    else:
        message = "cannot delete this Store"
    stores = StoreSerializer(Store.objects.all(),many=True).data
    return JsonResponse({'message':message,'data':stores})

@login_required
@permission_required(['add_store'])
def addStore(request):
    if request.method == "POST":
        form = StoreForm(request.POST)
        if form.is_valid():
            store = form.save()
            return JsonResponse({'data':StoreSerializer(store).data})
        else:
            return JsonResponse({'error':form.errors},status=400)

@login_required
@permission_required(['view_employeedevice'])
def gevin(request):
    device = Device.objects.filter(type_device__iexact='Personal')
    history = HistoryDeviceForm()
    content = {
        'device':device,
        'historyForm':history
    }
    return render(request,'gevin/index.html',content)

@login_required
def emp_data(request,id):
    return JsonResponse({'employee':user(id),
         'emoloyee_device':EmployeeDeviceSerializer(EmployeeDevice.objects.filter(employee=id,status=True),many=True).data,
         'device':DeviceSerializer(Device.objects.filter(type_device__iexact="Personal"),many=True).data
         })

# this function for gevin device to employee
@login_required
@permission_required(['add_employeedevice'])
def store_data(request):
    error = []
    if request.method == "POST":
        if request.POST['employee'] == None:
            error.append('You must choise employee')
        if request.POST.getlist('device') == None:
            error.append('You must choise device one or more')
        if len(error) == 0:
            for val in request.POST.getlist('device'):
                emp_device = EmployeeDevice(
                    employee = request.POST['employee'],
                    device = Device.objects.get(pk=val),
                    status = True)
                emp_device.save()
                device = Device.objects.get(id=emp_device.device.id)
                device.status = 2
                device.save()
                history = HistoryDevice(device = device,
                        status=1,
                        type=1,
                        is_to=True,
                        employee = emp_device.employee,
                        created_by=request.user
                        )
                history.save()
               
            return JsonResponse({'status':True,'message':"it's done "})
        else:
             return JsonResponse({'status':False,'message':error})                   

@login_required
@permission_required(['change_employeedevice'])
def receiveEmployee(request,id,type_device):
    if request.method == "POST":
        if type_device == "Personal": 
            emp_device = get_object_or_404(EmployeeDevice,pk=id)
            type = 1
        else:
            emp_device = get_object_or_404(DeprtDevice,pk=id)
            type = 4
        device = get_object_or_404(Device,pk=emp_device.device.id)
        if request.POST['status']:
            if type == 1:
                history = HistoryDevice(device = emp_device.device,
                    status=request.POST.get('status'),
                    type=type,
                    is_from=True,
                    employee = emp_device.employee,
                    detiles = request.POST.get('detiles'),
                    created_by = request.user
                    )
            else:
                history = HistoryDevice(device = emp_device.device,
                    status=request.POST.get('status'),
                    type=type,
                    is_from=True,
                    departDevice = emp_device,
                    detiles = request.POST.get('detiles'),
                    created_by = request.user
                    )
            history.save()
            if int(request.POST.get('status')) == 1:
                device.status = 1
            elif int(request.POST.get('status')) == 3:
                device.status = 4
            elif int(request.POST.get('status')) == 4:
                device.status = 5
            device.save()
            emp_device.status = False
            emp_device.save()
        else:
            return JsonResponse({'status':False,'message':'you need to choise status as will'})
        return JsonResponse({'status':True,'message':'receiveing done succesfuly'})

@login_required
def devices(request):
    return JsonResponse({'devices':DeviceSerializer(Device.objects.filter(type_device__iexact="Personal"),many=True).data})

@login_required
def device(request,id):
    own_device = get_object_or_404(Device,pk=id)
    return JsonResponse(DeviceSerializer(own_device).data)

@login_required
@permission_required(['change_employeedevice'])
def Expire(request,id):
    own_device = Device.objects.get(pk=id)
    own_device.status = 4
    own_device.save()
    hes = HistoryDevice(device=own_device,status=2,type = 3,created_by = request.user)
    hes.save()
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)

@login_required
@permission_required(['change_employeedevice'])  
def sendToServecing(request,id):
    if request.method == "POST":
        device = get_object_or_404(Device,pk=id)
        history = HistoryDevice(device = device,
                        status=4,
                        type=2,
                        is_to=True,
                        store = request.POST.get('store'),
                        detiles = request.POST.get('details')
                        ,created_by = request.user)
        history.save()
        device.status = 3
        device.save()
        
        return JsonResponse({'status':True,'message':'receiveing done succesfuly'})

@login_required
@permission_required(['change_employeedevice'])
def recivefromServecing(request,id):
    if request.method == "POST":
        device = get_object_or_404(Device,pk=id)
        lastHistory = HistoryDevice.objects.filter(type=2,is_to=True).first()
        history = HistoryDevice(device = device,
                        status=request.POST.get('status'),
                        type=2,
                        is_from=True,
                        store = lastHistory.store,
                        detiles = request.POST.get('details'),
                        created_by = request.user
                        )
        history.save()
        if int(request.POST.get('status')) == 1:
            device.status = 1
        elif int(request.POST.get('status')) == 3:
            device.status = 4
        elif int(request.POST.get('status')) == 4:
            device.status = 5
        device.save()
        
        return JsonResponse({'status':True,'message':'receiveing done succesfuly'})

@login_required
def test(request):
    return JsonResponse(users(),safe=False)

@login_required
def history(request,id):
    device = get_object_or_404(Device,pk=id)
    return render(request,"item/history.html",{'device':device})

@login_required
@permission_required(['view_departments'])
def department(request):
    if request.GET.get('query'):
        departments = Departments.objects.filter(name__contains = request.GET['query'])
    else:
        departments = Departments.objects.all()
    paginator = Paginator(departments,15)
    page_number = request.GET.get('page')
    department = paginator.get_page(page_number)
    form = DepartmentsForm()
    department = Departments.objects.all()
    return render(request,'departments/index.html',{'department':department,'form':form})

@login_required
@permission_required(['add_departments'])
def create_department(request):
    if request.method == 'POST':
        form = DepartmentsForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'status':True,'message':'it\'s done by successfuly with for reload'})
        else:
            return JsonResponse({'status':False,'message':form.errors})
    else:
        return JsonResponse({'message':'error'},status=400)

@login_required
@permission_required(['change_departments'])
def edit_department(request,id):
    department = Departments.objects.get(pk=id)
    form = DepartmentsForm(request.POST or None,instance=department)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request,"edit done successfully")
            return redirect('department.index')
    return render(request,'departments/edit.html',{'form':form})

@login_required
@permission_required(['delete_departments'])
def deleteDepartment(request,id):
    department = get_object_or_404(Departments,pk=id)
    if department.CountConnect == 0:
        department.delete()
    else:
        messages.error(request,'cannot delete this department')
    referring_url = request.META.get('HTTP_REFERER')
    return redirect(referring_url)

@login_required
@permission_required(['view_departments'])
def depart_info(request,id):
    department = get_object_or_404(Departments,pk=id)
    return JsonResponse(DepartmentSerializer(department).data)

@login_required
@permission_required(['add_office'])
def office_store(request):
    if request.method == "POST":
        form = officeForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'status':True,'message':'it\'s done by successfuly'})
        else:
            return JsonResponse({'status':False,'message':form.errors})
    else:
        return JsonResponse({'message':'error'},status=400)

@login_required
@permission_required(['view_departments'])
def department_show(request,id):
    department = get_object_or_404(Departments,pk=id)
    return render(request,'departments/show.html',{'department':department})

@login_required
@permission_required(['delete_office'])
def delete_office(request,id):
    office = get_object_or_404(Office,pk=id)
    if len(office.deprt_device.all()) == 0:
        office.delete()
    else:
        messages.error(request,"You cannot delete this office it has device")
    referring_url = request.META.get('HTTP_REFERER')
    return redirect(referring_url)

@login_required
@permission_required(['add_deprtdevice'])
def gevin_office(request):
    department = Departments.objects.all()
    devices = Device.objects.filter(type_device='office')
    error = None
    message = None
    if request.method == "POST":
        form = DeprtDeviceForm(request.POST)
        if form.is_valid():
            debartDevice = form.save()
            device = Device.objects.get(id=debartDevice.device.id)
            device.status = 2
            device.save()
            history = HistoryDevice(device = device,
                        status=1,
                        type=4,
                        is_to=True,
                        departDevice = debartDevice,
                        created_by = request.user)
            history.save()
            message = "save successfuly !"
        else:
            error = form.errors
    return render(request,'gevin/office.html',{'departments':department,
                                               'devices':devices,
                                               'error':error,
                                               'message':message})

@login_required
@permission_required(['change_deprtdevice'])
def get_office(request,id):
    office = Office.objects.filter(department__id = id)
    return JsonResponse(officeSerealizer(office,many=True).data,safe=False)

@login_required
def test_mail(reques):
    return JsonResponse(search(reques.GET['name']),safe=False)

@login_required
@permission_required(['view_sparepart'])
def indexSpare(request):
    dev = SparePart.objects.all()
    if request.GET.get('model'):
        dev = dev.filter(model__id = request.GET.get('model'))
    if request.GET.get('status'):
        dev = dev.filter(status = request.GET.get('status'))
    if request.GET.get('service_tag'):
        dev = dev.filter(service_tag = request.GET.get('service_tag'))
  
    Spare_parts = Paginator(dev,10)  
    page_number = request.GET.get('page') 
    spare_parts = Spare_parts.get_page(page_number)
    model = ModelSparePart.objects.all()
    store = Store.objects.all()
    devices = Device.objects.all() 
    return render(request,'spare_part/index.html',{
        'spare_parts':spare_parts,
        'range':range(1,spare_parts.paginator.num_pages+1),
        'model':model,
        'store':store,
        'devices':devices
        })
    
@login_required
@permission_required(['add_sparepart'])
def create_spare_part(request):
    message = ''
    list_service = []
    fail_list = []
    type = request.GET.get('type') or 'one'
    form = SepraPartForms()
    formfile = FileDeviceForm()
    fileDivece  = None
    if request.method == 'POST':
        
        if request.FILES.get('file') != None:
                formfile = FileDeviceForm(request.POST,request.FILES)
                if formfile.is_valid():
                    fileDivece = formfile.save()
                    
        if request.POST.get('type') == 'one':
            form = SepraPartForms(request.POST)
            
            if form.is_valid():
                device = form.save(commit=False)
                if fileDivece != None:
                    device.file = fileDivece
                device.created_by = request.user
                device.save()
                # Do something with the saved device
                message = "save successfully"
                form = SepraPartForms()
                formfile = FileDeviceForm()
        else:
            try:
                for val in request.POST.getlist('sevice_tags[]'):
                    if not SparePart.objects.filter(service_tag=val).exists():
                        newdevice = SparePart(
                            service_tag=val,
                            model=ModelSparePart.objects.get(pk=request.POST.get('modal')),
                            store=Store.objects.get(pk=request.POST.get('store')),
                            purchase_date=request.POST.get('purchase_date'),
                            supplier=request.POST.get('supplier'),
                            Warranty_date= request.POST.get('Warranty_date'),
                            created_by = request.user
                            )
                        if fileDivece != None:
                            newdevice.file = fileDivece
                        newdevice.save()
                        list_service.append(val)
                    else:
                        fail_list.append({'sirvec':val,'message':"alredy exist"})
                    
            except Exception as e:
                message = e             
    modal = ModelSparePart.objects.all()
    store = Store.objects.all()
    
    return render(request, 
                  'spare_part/create.html', 
                  {'form': form,
                   'modal':modal,
                   'store':store,
                   'message':message,
                   'type':type,
                   'list_service':list_service,
                   'fail_list':fail_list,
                   'formfile':formfile
                   })

@login_required
@permission_required(['add_modelsparepart'])
def addModal_spareParts(request): 
    if request.method == "POST":
        form = ModelSparePartForm(request.POST)
        if form.is_valid():
            modal_device = form.save()
            return JsonResponse({'data':ModalSparePartSerializer(modal_device).data})
        else:
            return JsonResponse({'error':form.errors},status=400)

@login_required
@permission_required(['delete_modelsparepart'])
def deleteModal_spareParts(request,id):
    modal = get_object_or_404(ModelSparePart,pk=id)
    if len(modal.spare_part.all()) == 0:
        modal.delete()
        message = 'deleted done by seccussfuly'
    else:
        message = "cannot delete this item"
    modals = ModalSparePartSerializer(ModelSparePart.objects.all(),many=True).data
    return JsonResponse({'message':message,'data':modals})

@login_required
@permission_required(['change_sparepart'])
def givenSpare(request):
    if request.method == "POST":
        device = get_object_or_404(Device,pk=request.POST['device'])
        spare_part =get_object_or_404(SparePart,pk=request.POST['spare_parts'])
        spare_part.device = device
        spare_part.modify_by = request.user
        spare_part.status = 0
        spare_part.save()
        
        return JsonResponse({'status':True,'message':'it\'s done successfully'}) 
    
    
@login_required
@permission_required(['change_device'])
def returnDevice(request):
    listDevice = request.GET.getlist('item[]')
    for li in listDevice:
        device = Device.objects.get(pk=li)
        device.deleted = True
        device.save()
    return JsonResponse({'message':request.GET.getlist('item[]')})

@login_required
def EmployeeHistory(request):
    myuser = []
    history = []
    if request.method == "POST":
        id = request.POST['id']
        myuser = user(id)
        history = HistoryDevice.objects.filter(employee=id)
    return render(request,"employee/history.html",{"history":history,'employee':myuser})

def sendEmailTest(reqest):
    # sendMail(5)
    return HttpResponse(sendMail(5))