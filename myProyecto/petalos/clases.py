class elemento:
    name=""
    precio=0
    cantidad=0

    def __init__(self,name,precio,cantidad):
        
        self.name=name
        self.precio=precio
        self.cantidad=cantidad
    
    def toString(self):
        return {
            'nombre': self.name,
            'precio': str(self.precio),
            'cantidad': str(self.cantidad),
            'total':str(self.total())
        }
    def total(self):
        return str(int(self.precio)*int(self.cantidad))