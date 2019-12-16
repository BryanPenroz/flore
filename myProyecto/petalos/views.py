from django.shortcuts import render
from .models import Categoria,Flores,Ticket
from django.contrib.auth.decorators import login_required
#incluimos el sistema de autentificacion de Django,
#le di un alias a 'login'
from django.contrib.auth import authenticate,logout, login as auth_login
from django.contrib.auth import login,authenticate
import datetime;
from .clases import elemento
# Create your views here.

#create views




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
            flor=Flores.objects.get(name=titulo)# lo busca entre las flores
            flor.delete()#elimina
            return render(request,'core/formulario.html',{'listacategoria':categorias,'msg':'elimino'})
        return render(request,'core/formulario.html',{'listacategoria':categorias})
    return render(request,'core/formulario.html',{'listacategoria':categorias})


@login_required(login_url='/login/')
def carros(request):
    x=request.session["carritox"]
    suma=0
    for item in x:
        suma=suma+int(item["total"])           
    return render(request,'core/carrito.html',{'x':x,'total':suma})

@login_required(login_url='/login/')
def grabar_carro(request):
    x=request.session["carritox"]    
    usuario=request.user.username
    suma=0
    try:
        for item in x:        
            titulo=item["nombre"]
            precio=int(item["precio"])
            cantidad=int(item["cantidad"])
            total=int(item["total"])        
            ticket=Ticket(
                usuario=usuario,
                titulo=titulo,
                precio=precio,
                cantidad=cantidad,
                total=total,
                fecha=datetime.date.today()
            )
            ticket.save()
            suma=suma+int(total)  
            print("reg grabado")                 
        mensaje="Grabado"
        request.session["carritox"] = []
    except:
        mensaje="error al grabar"            
    return render(request,'core/carrito.html',{'x':x,'total':suma,'mensaje':mensaje})




def carro_compras(request,id):
    f=Flores.objects.get(name=id)
    x=request.session["carritox"]
    el=elemento(1,f.name,f.precio,1)
    sw=0
    suma=0
    clon=[]
    for item in x:        
        cantidad=item["cantidad"]
        if item["nombre"]==f.name:
            sw=1
            cantidad=int(cantidad)+1
        ne=elemento(1,item["nombre"],item["precio"],cantidad)
        suma=suma+int(ne.total())
        clon.append(ne.toString())
    if sw==0:
        clon.append(el.toString())
    x=clon    
    request.session["carritox"]=x
    flor=Flores.objects.all()    
    return render(request,'core/galeria.html',{'Flores':flor,'total':suma})


def carro_compras_mas(request,id):
    f=Flores.objects.get(name=id)
    x=request.session["carritox"]
    suma=0
    clon=[]
    for item in x:        
        cantidad=item["cantidad"]
        if item["nombre"]==p.name:
            cantidad=int(cantidad)+1
        ne=elemento(1,item["nombre"],item["precio"],cantidad)
        suma=suma+int(ne.total())
        clon.append(ne.toString())
    x=clon    
    request.session["carritox"]=x
    x=request.session["carritox"]        
    return render(request,'core/carrito.html',{'x':x,'total':suma})


def carro_compras_menos(request,id):
    f=Flores.objects.get(name=id)
    x=request.session["carrito"]
    clon=[]
    suma=0
    for item in x:        
        cantidad=item["cantidad"]
        if item["nombre"]==p.name:
            cantidad=int(cantidad)-1
        ne=elemento(1,item["nombre"],item["precio"],cantidad)
        suma=suma+int(ne.total)
        clon.append(ne.toString())
    x=clon    
    request.session["carritox"]=x
    x=request.session["carritox"]    
    return render(request,'core/carrito.html',{'x':x,'total':total})



