# Módulo estándar de Python para convertir datos a texto JSON (json.dumps) y leer JSON (json.loads)
import json
# render: dibuja una plantilla con datos; get_object_or_404: busca un objeto o lanza error 404 si no existe
from django.shortcuts import render, get_object_or_404
# Http404: excepción que representa el error "no encontrado"; JsonResponse: respuesta en formato JSON
from django.http import Http404, JsonResponse
# Decorador que obliga a que la vista solo acepte peticiones POST (si llega GET responde 405)
from django.views.decorators.http import require_POST
# Clase de Django que divide una lista de resultados en páginas
from django.core.paginator import Paginator
# Importa los 3 modelos relacionados de la app: Categoria -> Producto -> Valoracion
from .models import Categoria, Producto, Valoracion


# Vista de la página principal (URL /): catálogo, filtro por categoría, orden y paginación
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
    # Lista vacía donde se guardará cada producto como diccionario (formato que entiende JavaScript)
    catalogo = []
    # Recorre cada producto activo
    for p in todos_activos:
        # Agrega un diccionario con los datos que necesita el carrito
        catalogo.append({
            'id': p.sku,                         # Identificador del producto en el carrito (el SKU)
            'name': p.nombre,                    # Nombre del producto
            'description': p.descripcion,        # Descripción del producto
            'price': p.precio,                   # Precio en pesos
            # URL de la imagen; si el producto no tiene imagen se usa una imagen por defecto
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
    # request.GET.get('categoria', '') lee ?categoria=... ; si no viene devuelve '' ; strip() quita espacios
    categoria = request.GET.get('categoria', '').strip()
    # Lee ?orden=... (az, za, precio_asc, precio_desc) de la misma forma
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
            # Lanza el error 404; el texto entre paréntesis se muestra en la página de error
            raise Http404(f'La categoría "{categoria}" no existe.')
        # Filtra los productos a través de la relación Producto -> Categoria
        productos_list = productos_list.filter(categoria=categoria_seleccionada)
        
    # 4. Ordenamiento dinámico según la opción seleccionada
    # ?orden=az : nombre de la A a la Z
    if orden == 'az':
        productos_list = productos_list.order_by('nombre')
    # ?orden=za : nombre de la Z a la A (el '-' invierte el orden)
    elif orden == 'za':
        productos_list = productos_list.order_by('-nombre')
    # ?orden=precio_asc : precio de menor a mayor
    elif orden == 'precio_asc':
        productos_list = productos_list.order_by('precio')
    # ?orden=precio_desc : precio de mayor a menor
    elif orden == 'precio_desc':
        productos_list = productos_list.order_by('-precio')
    # Si no llegó orden (o llegó uno desconocido)
    else:
        # Orden por defecto: los productos más recientes primero
        productos_list = productos_list.order_by('-creado')

    # Contador de resultados filtrados
    # count() hace un SELECT COUNT(*) en la BD (no trae los productos completos)
    total_productos = productos_list.count()
    
    # 5. Paginación: división en lotes de 4 productos por página
    paginator = Paginator(productos_list, 4)
    # Lee el número de página desde la URL (?page=2); si no viene es None
    page_number = request.GET.get('page')
    # get_page devuelve la página pedida; si el número es inválido devuelve la primera o la última (no falla)
    productos = paginator.get_page(page_number)
    
    # Renderizado hacia la plantilla con todas las variables necesarias
    return render(request, 'core/index.html', {
        'productos': productos,                  # Productos de la página actual (para la grilla)
        'total_productos': total_productos,      # Cantidad total de productos encontrados
        'categoria_actual': categoria,           # Texto del filtro recibido por GET (slug)
        'orden_actual': orden,                   # Orden elegido, para mantenerlo al cambiar de página
        'catalogo_json': catalogo_json,          # Catálogo completo en JSON para el carrito en JavaScript
        # Categoría elegida (objeto) para marcar la etiqueta activa; None si no hay filtro
        'categoria_seleccionada': categoria_seleccionada,
    })


# Solo acepta POST: las valoraciones se envían desde JavaScript con fetch
@require_POST
# Vista que guarda una valoración para el producto cuyo id viene en la URL (/producto/<id>/valorar/)
def agregar_valoracion(request, producto_id):
    """
    Endpoint tipo API (asíncrono vía fetch POST):
    - Recibe puntuación (1 a 5) y comentario en formato JSON.
    - Valida los datos y almacena el registro en el modelo Valoracion.
    - Responde un JsonResponse para actualizar la vista sin recargar la página.
    """
    # Busca el producto por id; si no existe responde automáticamente con error 404
    producto = get_object_or_404(Producto, id=producto_id)
    # try: si algo falla dentro del bloque, se salta al except en vez de romper el servidor
    try:
        # Decodificar el cuerpo de la petición JSON
        # request.body trae el texto enviado por fetch; json.loads lo convierte en diccionario de Python
        data = json.loads(request.body)
        # Lee la puntuación ('rating'); si no viene usa 0; int() la convierte a número entero
        puntuacion = int(data.get('rating', 0))
        # Lee el comentario ('comment'), lo convierte a texto y le quita los espacios sobrantes
        comentario = str(data.get('comment', '')).strip()

        # Validación básica en backend
        # La puntuación debe estar entre 1 y 5 y el comentario no puede estar vacío
        if puntuacion < 1 or puntuacion > 5 or not comentario:
            # Responde con JSON de error y código HTTP 400 (petición incorrecta)
            return JsonResponse({'success': False, 'error': 'Datos inválidos'}, status=400)

        # Crear y persistir la valoración en la base de datos
        # objects.create() hace el INSERT en la tabla core_valoracion y devuelve el objeto creado
        valoracion = Valoracion.objects.create(
            producto=producto,          # Relación con el producto (llena la FK producto_id)
            puntuacion=puntuacion,      # Estrellas (1 a 5)
            comentario=comentario       # Texto de la opinión
        )

        # Retornar confirmación y datos formateados para inserción directa en el DOM
        return JsonResponse({
            'success': True,                                             # Indica a JavaScript que todo salió bien
            'valoracion': {
                'puntuacion': valoracion.puntuacion,                     # Estrellas guardadas
                'comentario': valoracion.comentario,                     # Comentario guardado
                'fecha': valoracion.creado.strftime('%d/%m/%Y %H:%M')    # Fecha formateada como dd/mm/aaaa hh:mm
            }
        })
    # Captura cualquier error ocurrido dentro del try y lo guarda en la variable e
    except Exception as e:
        # Captura de errores inesperados (formato JSON corrupto, fallas de BD, etc.)
        # Responde con el error en JSON y código HTTP 500 (error interno del servidor)
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


# Vista de la página "Quiénes somos" (URL /about/)
def about(request):
    """Renderiza la sección informativa 'Quiénes somos'."""
    # Dibuja la plantilla sin enviar datos extra (las categorías llegan por el procesador de contexto)
    return render(request, 'core/about.html')


# Vista de la galería (URL /gallery/)
def gallery(request):
    """Renderiza la galería visual mostrando todos los productos cargados."""
    # select_related trae la categoría de cada producto en la misma consulta (evita una consulta por producto)
    productos = Producto.objects.select_related('categoria')
    # Dibuja la galería enviando la lista de productos
    return render(request, 'core/gallery.html', {'productos': productos})


# Vista de preguntas frecuentes (URL /faq/)
def faq(request):
    """Renderiza la página de preguntas frecuentes."""
    # Dibuja la plantilla de preguntas frecuentes
    return render(request, 'core/faq.html')
