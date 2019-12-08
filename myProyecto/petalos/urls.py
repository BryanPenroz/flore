from django.contrib import admin
from django.urls import path,include
from .views import index,gale,formulario,login,login_acceso,cerrar_sesion,eliminar_flores

urlpatterns = [
    path('', index,name='IND'),
    path('galeria/',gale,name='GAL'),
    path('formulario/',formulario,name='FORMU'),
    path('login/',login,name='LOGIN'),
    path('login_acceso/',login_acceso,name='LOGINACCESO'),
    path('cerrar_sesion/',cerrar_sesion,name='CERRARSESION'),
    path('eliminar_flores/<id>/',eliminar_flores,name='ELIMINA'),
   
  
]
