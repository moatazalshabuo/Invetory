from django.urls import path
from .views import *
urlpatterns = [
    path('',index,name="item.index"),
    path('create/',create_device,name='Item.create'),
    path('create-model/',addModal,name="modal.create"),
    path('create-store/',addStore,name="store.create"),
    path('delete-store/<uuid:id>/',deleteStore,name="store.delete"),
    path('delete-modal/<uuid:id>/',deleteModal,name="modal.delete"),
    path("modal/<uuid:id>/",getModal, name="get.modal"),
    path('edit-model/<uuid:id>/',editModal,name="edit.modal"),
    path('gevin/',gevin,name='item.gevin'),
    path('emp_data/<str:id>/',emp_data,name='employee.data'),
    path('store_data/',store_data,name="store_data.gevin"),
    path('recive/<int:id>/<str:type_device>/',receiveEmployee,name='recive.emp_device'),
    path('get-devices/',devices,name='get.devices'),
    path('get-device/<uuid:id>/',device,name="device-data"),
    path('expired/<uuid:id>/',Expire,name="expired"),
    path('send-to-servecing/<uuid:id>/',sendToServecing,name='sendToServecing'),
    path('recive-from-servecing/<uuid:id>/',recivefromServecing,name='sendToServecing'),
    path('history/<uuid:id>/',history,name="history"),
    path("department/",department,name="department.index"),
    path('department-create/',create_department,name="department.store"),
    path('departments/<int:id>/',deleteDepartment,name="department.delete"),
    path('depatment/<int:id>/',depart_info,name="deprtament.info"),
    path('department/<int:id>/edit/',edit_department,name="department.edit"),
    path('office-store/',office_store,name="office.store"),
    path('depart/<int:id>/',department_show,name="department.show"),
    path('office-delete/<int:id>/',delete_office,name='office.delete'),
    path('gevin-office/',gevin_office,name="gevin.office"),
    path('get-office/<int:id>/',get_office,name="get.office"),
    path('test/',test),
    path('test-mail/',test_mail),
    path('spare-part/',indexSpare,name="spare_parts.index"),
    path('spare-part/given/',givenSpare,name="spare.given"),
    path('create/spare-part/',create_spare_part,name='Item.create.sparepart'),
    path('create-model-spare/',addModal_spareParts,name="modalspare.create"),
    path('delete-modal-spare/<uuid:id>/',deleteModal_spareParts,name="modalspare.delete"),
    path('reterun/devices/',returnDevice,name="returen.device"),
    path('history/employee/',EmployeeHistory,name="employee.history"),
    path('sendEmailTest/',sendEmailTest)
]