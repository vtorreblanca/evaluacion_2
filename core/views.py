import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from .models import Producto, Valoracion


def index(request):
    """
    Vista principal de la tienda:
    - Serializa todos los productos activos para el motor del carrito en JavaScript.
    - Aplica filtros de categoría y criterios de ordenamiento (A-Z, Z-A, Precios).
    - Pagina los resultados en bloques de 4 productos por página.
    """
    # 1. Obtener todos los productos activos sin paginar para alimentar el carrito en el frontend
    todos_activos = Producto.objects.filter(activo=True)
    catalogo = []
    for p in todos_activos:
        catalogo.append({
            'id': p.sku,
            'name': p.nombre,
            'description': p.descripcion,
            'price': p.precio,
            'image': p.imagen.url if p.imagen else '/static/core/assets/images.jpeg',
            'category': p.categoria
        })
    # Convertir el catálogo a JSON para que JS pueda leerlo de forma segura
    catalogo_json = json.dumps(catalogo)

    # 2. Preparar el conjunto de productos para la grilla visual
    # prefetch_related optimiza la consulta a la BD trayendo las valoraciones en una sola consulta
    productos_list = todos_activos.prefetch_related('valoraciones')

    # Captura de parámetros GET de la URL (filtros y orden)
    categoria = request.GET.get('categoria', '').strip()
    orden = request.GET.get('orden', '').strip()
    
    # 3. Filtrado por categoría si el valor coincide con los permitidos
    if categoria in ['Componentes', 'Audio', 'Accesorios']:
        productos_list = productos_list.filter(categoria=categoria)
        
    # 4. Ordenamiento dinámico según la opción seleccionada
    if orden == 'az':
        productos_list = productos_list.order_by('nombre')
    elif orden == 'za':
        productos_list = productos_list.order_by('-nombre')
    elif orden == 'precio_asc':
        productos_list = productos_list.order_by('precio')
    elif orden == 'precio_desc':
        productos_list = productos_list.order_by('-precio')
    else:
        # Orden por defecto: los productos más recientes primero
        productos_list = productos_list.order_by('-creado')

    # Contador de resultados filtrados
    total_productos = productos_list.count()
    
    # 5. Paginación: división en lotes de 4 productos por página
    paginator = Paginator(productos_list, 4)
    page_number = request.GET.get('page')
    productos = paginator.get_page(page_number)
    
    # Renderizado hacia la plantilla con todas las variables necesarias
    return render(request, 'core/index.html', {
        'productos': productos,
        'total_productos': total_productos,
        'categoria_actual': categoria,
        'orden_actual': orden,
        'catalogo_json': catalogo_json,
    })


@require_POST
def agregar_valoracion(request, producto_id):
    """
    Endpoint tipo API (asíncrono vía fetch POST):
    - Recibe puntuación (1 a 5) y comentario en formato JSON.
    - Valida los datos y almacena el registro en el modelo Valoracion.
    - Responde un JsonResponse para actualizar la vista sin recargar la página.
    """
    producto = get_object_or_404(Producto, id=producto_id)
    try:
        # Decodificar el cuerpo de la petición JSON
        data = json.loads(request.body)
        puntuacion = int(data.get('rating', 0))
        comentario = str(data.get('comment', '')).strip()

        # Validación básica en backend
        if puntuacion < 1 or puntuacion > 5 or not comentario:
            return JsonResponse({'success': False, 'error': 'Datos inválidos'}, status=400)

        # Crear y persistir la valoración en la base de datos
        valoracion = Valoracion.objects.create(
            producto=producto,
            puntuacion=puntuacion,
            comentario=comentario
        )

        # Retornar confirmación y datos formateados para inserción directa en el DOM
        return JsonResponse({
            'success': True,
            'valoracion': {
                'puntuacion': valoracion.puntuacion,
                'comentario': valoracion.comentario,
                'fecha': valoracion.creado.strftime('%d/%m/%Y %H:%M')
            }
        })
    except Exception as e:
        # Captura de errores inesperados (formato JSON corrupto, fallas de BD, etc.)
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


def about(request):
    """Renderiza la sección informativa 'Quiénes somos'."""
    return render(request, 'core/about.html')


def gallery(request):
    """Renderiza la galería visual mostrando todos los productos cargados."""
    productos = Producto.objects.all()
    return render(request, 'core/gallery.html', {'productos': productos})


def faq(request):
    """Renderiza la página de preguntas frecuentes."""
    return render(request, 'core/faq.html')
