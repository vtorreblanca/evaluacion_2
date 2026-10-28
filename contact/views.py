from django.shortcuts import render, redirect

from .forms import ContactoForm


def contacto(request):
    """
    Formulario de contacto:
    - GET: muestra el formulario vacío.
    - POST: valida los datos y guarda el mensaje en el modelo MensajeContacto.
    - Tras guardar redirige a la misma página (patrón POST/Redirect/GET) para evitar reenvíos.
    """
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(f"{request.path}?enviado=1")
    else:
        form = ContactoForm()

    return render(request, 'contact/contacto.html', {
        'form': form,
        'enviado': request.GET.get('enviado') == '1',
    })
