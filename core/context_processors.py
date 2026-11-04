# Procesadores de contexto de la app 'core'
# Un procesador de contexto es una función que Django ejecuta en CADA página renderizada:
# lo que devuelve (un diccionario) queda disponible como variable en todos los templates,
# sin tener que enviarlo desde cada vista.

# Count: cuenta registros relacionados; Q: permite poner una condición dentro del Count
from django.db.models import Count, Q

# Importa el modelo Categoria de esta misma app
from .models import Categoria


def categorias_tienda(request):
    """
    Entrega a todos los templates la lista de categorías de la tienda,
    cada una con la cantidad de productos activos que tiene (campo calculado 'total').
    Se usa en el pie de página (base.html), en las etiquetas de filtro (index.html)
    y en la página común de error 404 (app 'errores').
    """
    # annotate agrega a cada categoría el campo calculado 'total' (no se guarda en la BD)
    # La consulta es "perezosa": solo se ejecuta si el template realmente usa la variable
    categorias = Categoria.objects.annotate(
        # Cuenta los productos relacionados (related_name='productos'), solo los activos
        total=Count('productos', filter=Q(productos__activo=True))
    )

    # El diccionario devuelto se agrega al contexto de todos los templates
    return {
        # Variable {{ categorias }} disponible en cualquier template
        'categorias': categorias,
    }
