from django.urls import path
from .views import *
urlpatterns = [
    path('',index,name='catogry.index'),
    path('store/',store,name="catogry.store"),
    path('delete/<uuid:uuid>/',delete,name='catogry.delete'),
    path('category/<uuid:id>/',update_category,name="edit.category"),
    path("<uuid:id>/",show,name="categry.show")
]
