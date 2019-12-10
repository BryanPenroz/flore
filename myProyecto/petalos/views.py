from django.shortcuts import render
from .models import Categoria,Flores
from django.contrib.auth.decorators import login_required
#debemos incluir el modelo de users del sistema
from django.contrib.auth.models import User
#incluimos el sistema de autentificacion de Django, 
#le di un alias a 'login'
from django.contrib.auth import authenticate,logout, login as auth_login
# Create your views here.

#create views
@login_required(login_url='/login/')
def agregar_carrito(request,id):
    #recuperar la lista del carrito desde la sesion
    lista=request.session.get("carrito","")
    #agregar el titulo a listado
    lista=lista+str(id)+str(";")
    #volver a ingresarlo a la sesion
    request.session["carrito"]=lista
    return render(request,"core/carrito.html",{'listaCarrito':lista})
    
def carros(request):
    x=request.session["carritox"]
    suma=0
    for item in x:
        suma=suma+int(item["total"])
    return render(request,'core/carrito.html',{'x':x,'total':suma})    

def eliminar_flores(request,id):
    flor=Flores.objects.get(name=id)#buscar flor
    msg=''
    try:
        flor.delete()# elimino
        msg='Se elimino la flor'
    except:
        msg='No se pudo eliminar'
    flor=Flores.objects.all()# selecciono todo
    return render(request,"core/galeria.html",{'lista':flor,'msg':msg})
    

def login(request):
    return render(request,"core/login.html")

def cerrar_sesion(request):
    logout(request)
    return render(request,"core/login.html",{'msgs':'Cerro Sesión'})
    
def login_acceso(request):
    if request.POST:
        usuario=request.POST.get("txtUser")
        password=request.POST.get("txtPass")
        #creamos un modelo de usuario para autentificar
        us = authenticate(request,username=usuario,password=password)
        if us is not None and us.is_active:
            auth_login(request,us)
            return render(request,"core/index.html")
    return render(request,"core/login.html",{'msg':'Usuario u Contraseña Incorrecta "Intente Otra Vez u Comuniquese con Servicio Tecnico"'})

@login_required(login_url='/login/')    
def index(request):
    return render(request,'core/index.html')

@login_required(login_url='/login/')
def gale(request):
    flor=Flores.objects.all()#select * from Flores
    return render(request,'core/galeria.html',{'lista':flor})

@login_required(login_url='/login/')
def formulario(request):
    categorias=Categoria.objects.all()
    if request.POST:
        accion=request.POST.get("accion")
        if accion=='grabar':           
            titulo=request.POST.get("txtTitulo")
            precio=request.POST.get("txtPrecio")
            imagen=request.FILES.get("txtImagen")
            catego=request.POST.get("cboCategoria")
            obj_categoria=Categoria.objects.get(name=catego)
            
            flor=Flores( 
                name=titulo,
                precio=precio,
                imagen=imagen,
                categoria=obj_categoria
            )
            flor.save() 
            return render(request,'core/formulario.html',{'listacategoria':categorias,'msg':'grabo'})
        if accion=='eliminar':
            titulo=request.POST.get("txtTitulo")#recupera el titulo
            flor=Flores.objects.get(name=titulo)# lo busca entre las peliculas
            flor.delete()#elimina
            return render(request,'core/formulario.html',{'listacategoria':categorias,'msg':'elimino'})
        return render(request,'core/formulario.html',{'listacategoria':categorias})
    return render(request,'core/formulario.html',{'listacategoria':categorias})
