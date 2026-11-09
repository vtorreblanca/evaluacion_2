# render: dibuja una plantilla con datos; redirect: envía al navegador a otra URL
from django.shortcuts import render, redirect

# Importa el formulario de contacto definido en forms.py de esta misma app
from .forms import ContactoForm


# Vista que muestra y procesa el formulario de contacto (URL /contacto/)
def contacto(request):
    """
    Formulario de contacto:
    - GET: muestra el formulario vacío.
    - POST: valida los datos y guarda el mensaje en el modelo MensajeContacto.
    - Tras guardar redirige a la misma página (patrón POST/Redirect/GET) para evitar reenvíos.
    """
    # Si el usuario envió el formulario (botón Enviar), la petición llega por POST
    if request.method == 'POST':
        # Crea el formulario con los datos enviados (formulario "ligado" a datos)
        form = ContactoForm(request.POST)
        # is_valid() ejecuta todas las validaciones: las del modelo y las propias (clean_nombre, clean_mensaje)
        if form.is_valid():
            # Como es un ModelForm, save() crea el registro MensajeContacto en la base de datos
            form.save()
            # Redirige a /contacto/?enviado=1 para mostrar el aviso de éxito y evitar reenviar al recargar
            return redirect(f"{request.path}?enviado=1")
        # Si no es válido, se sigue abajo y se vuelve a mostrar el formulario con sus errores
    # Si la petición es GET (el usuario solo abrió la página)
    else:
        # Crea un formulario vacío
        form = ContactoForm()

    # Dibuja la plantilla del formulario y le envía las variables
    return render(request, 'contact/contacto.html', {
        # El formulario (vacío, o con datos y errores)
        'form': form,
        # True si la URL trae ?enviado=1 (parámetro GET), para mostrar el mensaje de "enviado con éxito"
        'enviado': request.GET.get('enviado') == '1',
    })
