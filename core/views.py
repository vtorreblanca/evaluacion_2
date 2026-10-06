import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from .models import Producto, Valoracion

def index(request):
    # Obtenemos los productos activos
    productos_list = Producto.objects.filter(activo=True).prefetch_related('valoraciones')
    
    # Parámetros GET
    categoria = request.GET.get('categoria', '').strip()
    orden = request.GET.get('orden', '').strip()
    
    # 1. Filtro por Categoría
    if categoria in ['Componentes', 'Audio', 'Accesorios']:
        productos_list = productos_list.filter(categoria=categoria)
        
    # 2. Ordenamiento (Alfabético y Precios)
    if orden == 'az':
        productos_list = productos_list.order_by('nombre')
    elif orden == 'za':
        productos_list = productos_list.order_by('-nombre')
    elif orden == 'precio_asc':
        productos_list = productos_list.order_by('precio')
    elif orden == 'precio_desc':
        productos_list = productos_list.order_by('-precio')
    else:
        productos_list = productos_list.order_by('-creado')

    total_productos = productos_list.count()
    
    # Paginación (4 productos por página)
    paginator = Paginator(productos_list, 4)
    page_number = request.GET.get('page')
    productos = paginator.get_page(page_number)
    
    return render(request, 'core/index.html', {
        'productos': productos,
        'total_productos': total_productos,
        'categoria_actual': categoria,
        'orden_actual': orden,
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
