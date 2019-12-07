from django.db import models

# Create your models here.

class Categoria(models.Model):
    name=models.CharField(max_length=45,primary_key=True)
    

    def __str__(self):
        return self.name

class Flores(models.Model):
    name=models.CharField(max_length=45,primary_key=True)
    precio=models.IntegerField()
    descripcion=models.TextField()
    imagen=models.ImageField(upload_to='flor',null=True)
    categoria=models.ForeignKey(Categoria,on_delete=models.CASCADE)

    def __str__(self):
        return self.name