from django.shortcuts import render
from .models import Categoria,Flores
from django.contrib.auth.decorators import login_required
#debemos incluir el modelo de users del sistema
from django.contrib.auth.models import User
from .forms import CustomUserForm
#incluimos el sistema de autentificacion de Django, 
#le di un alias a 'login'
from django.contrib.auth import authenticate,logout, login as auth_login
# Create your views here.

#create views
def registro_usuario(request):
    data={
        'form':CustomUserForm()
    }
    if request.method=='POST':
        formulario=CustomUserForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            usuario=formulario.cleaned_data['username']
            password=formulario.cleaned_data['password1']
            user=authenticate(username=usuario,password=password)
            login(request,user)
            return redirect(to='Home')
    return render (request,'registration/registro.html',data)        

def login_iniciar(request):
    if request.POST:
        usuario=request.POST.get("txtUser")
        password=request.POST.get("txtPass")
        use=authenticate(request,txtUser=usuario,txtPass=password)
        if use is not None and use.is_active:
            if use.is_staff:
                auth_login(request,use)
                arreglo={'nombre':usuario,'contraseña':password, 'tipo':'administrador'}
                return render(request,'core/index.html',arreglo)
            else:
                arreglo={'nombre':usuario,'contraseña':password, 'tipo':'cliente'}
                return render(request,'core/registro.html',arreglo)
        variables={
            'msg':'No Existe Usuario Registrado con ese Nombre'
        }
        return remder(request,'core/login.html',variables)          

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



@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("core:order-summary")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("core:order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("core:order-summary")


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            messages.info(request, "This item was removed from your cart.")
            return redirect("core:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:product", slug=slug)


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("core:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:product", slug=slug)
