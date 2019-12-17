from django.db import models

# Create your models here.

class Categoria(models.Model):
    name=models.CharField(max_length=45,primary_key=True)
    

    def __str__(self):
        return self.name

class Flores(models.Model):
    name=models.CharField(max_length=45,primary_key=True)
    precio=models.IntegerField()
    imagen=models.ImageField(upload_to='flor',null=True)
    categoria=models.ForeignKey(Categoria,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Ticket(models.Model):
    usuario=models.CharField(max_length=100)
    titulo=models.CharField(max_length=100)
    precio=models.IntegerField()
    cantidad=models.IntegerField()
    total=models.IntegerField()
    fecha=models.DateField()

    def __str__(self):
        return str(self.usuario)+' '+str(self.titulo)

