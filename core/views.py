import json
from django.shortcuts import render, get_object_or_404
# Http404: excepción que representa el error "no encontrado"; JsonResponse: respuesta en formato JSON
from django.http import Http404, JsonResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
# Importa los 3 modelos relacionados de la app: Categoria -> Producto -> Valoracion
from .models import Categoria, Producto, Valoracion


def index(request):
    """
    Vista principal de la tienda:
    - Serializa todos los productos activos para el motor del carrito en JavaScript.
    - Aplica filtros de categoría y criterios de ordenamiento (A-Z, Z-A, Precios).
    - Pagina los resultados en bloques de 4 productos por página.
    """
    # 1. Obtener todos los productos activos sin paginar para alimentar el carrito en el frontend
    # select_related trae la categoría (FK) en la misma consulta para no hacer una consulta extra por producto
    todos_activos = Producto.objects.filter(activo=True).select_related('categoria')
    catalogo = []
    for p in todos_activos:
        catalogo.append({
            'id': p.sku,
            'name': p.nombre,
            'description': p.descripcion,
            'price': p.precio,
            'image': p.imagen.url if p.imagen else '/static/core/assets/images.jpeg',
            # Como categoria ahora es una FK, se envía el nombre de la categoría (texto) y no el objeto completo
            'category': p.categoria.nombre
        })
    # Convertir el catálogo a JSON para que JS pueda leerlo de forma segura
    catalogo_json = json.dumps(catalogo)

    # 2. Preparar el conjunto de productos para la grilla visual
    # prefetch_related optimiza la consulta a la BD trayendo las valoraciones en una sola consulta
    productos_list = todos_activos.prefetch_related('valoraciones')

    # Captura de parámetros GET de la URL (filtros y orden)
    categoria = request.GET.get('categoria', '').strip()
    orden = request.GET.get('orden', '').strip()
    
    # 3. Filtro por etiqueta (GET): el parámetro ?categoria= recibe el slug de la categoría (ej: ?categoria=audio)
    #    La lista de etiquetas ({{ categorias }}) ya no se envía desde aquí: la entrega a todas las páginas
    #    el procesador de contexto core.context_processors.categorias_tienda
    # Por defecto no hay categoría seleccionada (se muestran todas)
    categoria_seleccionada = None
    # Solo se filtra si llegó un valor en ?categoria= (cadena no vacía)
    if categoria:
        # Busca la categoría por su slug; .first() devuelve None si no existe
        categoria_seleccionada = Categoria.objects.filter(slug=categoria).first()
        # Manejo del error 404: si el valor del filtro no existe se lanza Http404 con un mensaje propio
        # (la app 'errores' captura este error y muestra la página común de error)
        if categoria_seleccionada is None:
            raise Http404(f'La categoría "{categoria}" no existe.')
        # Filtra los productos a través de la relación Producto -> Categoria
        productos_list = productos_list.filter(categoria=categoria_seleccionada)
        
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
        # Categoría elegida (objeto) para marcar la etiqueta activa; None si no hay filtro
        'categoria_seleccionada': categoria_seleccionada,
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
    # select_related trae la categoría de cada producto en la misma consulta (evita una consulta por producto)
    productos = Producto.objects.select_related('categoria')
    return render(request, 'core/gallery.html', {'productos': productos})


def faq(request):
    """Renderiza la página de preguntas frecuentes."""
    return render(request, 'core/faq.html')
