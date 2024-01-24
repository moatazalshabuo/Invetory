from rest_framework import serializers
from catogry.models import Catogry
from .models import *

class ModalDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelDevice
        fields = ['id','name',]
        
class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['id','name',]
        
class EmployeeSerialzers(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id','name','zalaf_id','email']


class CatogrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Catogry
        fields = '__all__'
        
class DeviceSerializer(serializers.ModelSerializer):
    modal= ModalDeviceSerializer(read_only=True)
    catogry = CatogrySerializer(read_only=True)
    class Meta:
        model = Device
        fields =  [ "id","catogry","service_tag","modal" ,"store" ,"purchase_date","supplier","status","file","Warranty_date","status_name","created_at","ubdate_at",]
        

class ModalSparePartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelSparePart
        fields = ['id','name',]
        
class SparePartSerializer(serializers.ModelSerializer):
    model= ModalSparePartSerializer(read_only=True)
    class Meta:
        model = SparePart
        fields =  ["id","service_tag","model" ,"store" ,"purchase_date","supplier","status","file","Warranty_date","created_at",]
        


class EmployeeDeviceSerializer(serializers.ModelSerializer):
    # employee = EmployeeSerialzers()
    device = DeviceSerializer(read_only=True)
    
    class Meta:
        model = EmployeeDevice
        fields = ['id','employee','device','formatted_created_at']
        
        
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departments
        fields = '__all__'
        
        
class officeSerealizer(serializers.ModelSerializer):
    class Meta:
        model = Office
        fields = '__all__'