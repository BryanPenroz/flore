from django.contrib import admin
from django.urls import path,include
from .views import index,gale,formulario,login,login_acceso,cerrar_sesion,eliminar_flores,carro_compras,carros,carro_compras_mas,carro_compras_menos,grabar_carro

urlpatterns = [
    path('', index,name='IND'),
    path('galeria/',gale,name='GAL'),
    path('formulario/',formulario,name='FORMU'),
    path('login/',login,name='LOGIN'),
    path('login_acceso/',login_acceso,name='LOGINACCESO'),
    path('cerrar_sesion/',cerrar_sesion,name='CERRARSESION'),
    path('eliminar_flores/<id>/',eliminar_flores,name='ELIMINA'),
    path('agregar_carro/<id>/',carro_compras,name='AGREGAR_CARRO'),
    path('carro/',carros,name='CARRITO'),
    path('carro_mas/<id>/',carro_compras_mas,name='CARRO_MAS'),
    path('carro_menos/<id>/',carro_compras_menos,name='CARRO_MENOS'),
    path('grabar_carro/',grabar_carro,name='GRABAR_CARRO'),
    path('',include('pwa.urls')),
]
