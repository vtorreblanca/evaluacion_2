from django.shortcuts import render
from .models import Producto

def index(request):
    productos = Producto.objects.filter(activo=True)
    total_productos = productos.count()
    return render(request, 'core/index.html', {
        'productos': productos,
        'total_productos': total_productos,
    })

def about(request):
    return render(request, 'core/about.html')

def gallery(request):
    productos = Producto.objects.all()
    return render(request, 'core/gallery.html', {'productos': productos})

def faq(request):
    return render(request, 'core/faq.html')
