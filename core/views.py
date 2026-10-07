# Módulo estándar de Python para serializar y deserializar datos en formato JSON
import json

# Funciones de conveniencia de Django para renderizar HTML y obtener objetos o disparar un HTTP 404
from django.shortcuts import render, get_object_or_404

# Clase para emitir respuestas HTTP con cabecera application/json de forma nativa
from django.http import JsonResponse

# Decorador que restringe una vista para que solo acepte peticiones vía método POST
from django.views.decorators.http import require_POST

# Clase utilitaria de Django para segmentar listas o QuerySets en páginas numeradas
from django.core.paginator import Paginator

# Importa los modelos definidos en models.py dentro de la misma aplicación
from .models import Producto, Valoracion


# Vista del catálogo principal y portada de la tienda (acepta peticiones GET)
def index(request):
    # Consulta base: filtra solo productos disponibles (activo=True)
    # prefetch_related('valoraciones') precarga todas las reseñas en una sola consulta adicional, evitando el problema N+1
    productos_list = Producto.objects.filter(activo=True).prefetch_related('valoraciones')
    
    # Extrae parámetros de la query string (URL ?categoria=...&orden=...) eliminando espacios en blanco accidentales
    categoria = request.GET.get('categoria', '').strip()
    orden = request.GET.get('orden', '').strip()
    
    # 1. Filtro por Categoría: valida contra una lista blanca permitida para evitar inyecciones o valores espurios
    if categoria in ['Componentes', 'Audio', 'Accesorios']:
        productos_list = productos_list.filter(categoria=categoria)
        
    # 2. Ordenamiento: evalúa la opción recibida y reordena el QuerySet a nivel de base de datos (SQL ORDER BY)
    if orden == 'az':
        productos_list = productos_list.order_by('nombre')            # Alfabético ascendente (A-Z)
    elif orden == 'za':
        productos_list = productos_list.order_by('-nombre')           # Alfabético descendente (Z-A)
    elif orden == 'precio_asc':
        productos_list = productos_list.order_by('precio')            # De menor a mayor precio
    elif orden == 'precio_desc':
        productos_list = productos_list.order_by('-precio')           # De mayor a menor precio
    else:
        productos_list = productos_list.order_by('-creado')           # Valor por defecto: los más nuevos primero

    # Ejecuta un conteo SQL (SELECT COUNT(*)) con los filtros aplicados para informar el total de resultados
    total_productos = productos_list.count()
    
    # Inicializa el paginador dividiendo el QuerySet en bloques de 4 elementos por página
    paginator = Paginator(productos_list, 4)
    
    # Obtiene el número de página solicitado desde la query string (?page=2)
    page_number = request.GET.get('page')
    
    # Retorna la página solicitada; si el parámetro no es válido o está vacío, entrega de forma segura la página 1
    productos = paginator.get_page(page_number)
    
    # Compila el contexto y renderiza la plantilla HTML enviando los objetos paginados y el estado de los filtros
    return render(request, 'core/index.html', {
        'productos': productos,
        'total_productos': total_productos,
        'categoria_actual': categoria,
        'orden_actual': orden,
    })


# Vista endpoint tipo API para añadir valoraciones; rechaza automáticamente cualquier método que no sea POST (405 Method Not Allowed)
@require_POST
def agregar_valoracion(request, producto_id):
    # Busca el producto por su clave primaria o responde con un error 404 si el ID no existe en la base de datos
    producto = get_object_or_404(Producto, id=producto_id)
    try:
        # Decodifica el cuerpo en crudo de la petición HTTP (JSON enviado típicamente por fetch o Axios en JavaScript)
        data = json.loads(request.body)
        
        # Convierte el puntaje a entero (con valor por defecto 0) y limpia el texto del comentario
        puntuacion = int(data.get('rating', 0))
        comentario = str(data.get('comment', '')).strip()

        # Validación de reglas de negocio: el puntaje debe estar entre 1 y 5, y el comentario no puede estar vacío
        if puntuacion < 1 or puntuacion > 5 or not comentario:
            # Retorna una respuesta JSON informando el error con código de estado HTTP 400 (Bad Request)
            return JsonResponse({'success': False, 'error': 'Datos inválidos'}, status=400)

        # Inserta el nuevo registro en la base de datos vinculado al producto
        valoracion = Valoracion.objects.create(
            producto=producto,
            puntuacion=puntuacion,
            comentario=comentario
        )

        # Retorna confirmación exitosa (HTTP 200) serializando los datos recién creados y formateando la fecha
        return JsonResponse({
            'success': True,
            'valoracion': {
                'puntuacion': valoracion.puntuacion,
                'comentario': valoracion.comentario,
                'fecha': valoracion.creado.strftime('%d/%m/%Y %H:%M')
            }
        })
    except Exception as e:
        # Captura errores imprevistos (JSON malformado, fallas de casteo) y responde con HTTP 500 (Internal Server Error)
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


# Vista estática informativa: renderiza la sección institucional o "Quiénes Somos"
def about(request):
    return render(request, 'core/about.html')


# Vista de galería: consulta todos los productos en la base de datos y los envía a la plantilla visual
def gallery(request):
    productos = Producto.objects.all()
    return render(request, 'core/gallery.html', {'productos': productos})


# Vista estática de soporte: renderiza la página de Preguntas Frecuentes (FAQ)
def faq(request):
    return render(request, 'core/faq.html')
