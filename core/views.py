import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Producto, Valoracion

def index(request):
    productos = Producto.objects.filter(activo=True).prefetch_related('valoraciones')
    total_productos = productos.count()
    return render(request, 'core/index.html', {
        'productos': productos,
        'total_productos': total_productos,
    })

@require_POST
def agregar_valoracion(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    try:
        data = json.loads(request.body)
        puntuacion = int(data.get('rating', 0))
        comentario = str(data.get('comment', '')).strip()

        if puntuacion < 1 or puntuacion > 5 or not comentario:
            return JsonResponse({'success': False, 'error': 'Datos inválidos'}, status=400)

        valoracion = Valoracion.objects.create(
            producto=producto,
            puntuacion=puntuacion,
            comentario=comentario
        )

        return JsonResponse({
            'success': True,
            'valoracion': {
                'puntuacion': valoracion.puntuacion,
                'comentario': valoracion.comentario,
                'fecha': valoracion.creado.strftime('%d/%m/%Y %H:%M')
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

def about(request):
    return render(request, 'core/about.html')

def gallery(request):
    productos = Producto.objects.all()
    return render(request, 'core/gallery.html', {'productos': productos})

def faq(request):
    return render(request, 'core/faq.html')
