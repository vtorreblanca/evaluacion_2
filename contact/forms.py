# Formularios de la aplicación 'contact'
from django import forms

from .models import MensajeContacto


class ContactoForm(forms.ModelForm):
    """Formulario de contacto basado en el modelo MensajeContacto."""

    class Meta:
        model = MensajeContacto
        fields = ['nombre', 'email', 'asunto', 'mensaje']
        labels = {
            'nombre': 'Nombre',
            'email': 'Correo electrónico',
            'asunto': 'Motivo',
            'mensaje': 'Mensaje',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu nombre', 'autocomplete': 'name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'tucorreo@ejemplo.cl', 'autocomplete': 'email'}),
            'asunto': forms.Select(attrs={'class': 'form-select'}),
            'mensaje': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Escribe tu consulta...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si el formulario fue enviado con errores, marca los campos inválidos (estilo Bootstrap)
        if self.is_bound:
            for nombre_campo in self.errors:
                if nombre_campo in self.fields:
                    widget = self.fields[nombre_campo].widget
                    widget.attrs['class'] = widget.attrs.get('class', '') + ' is-invalid'

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre'].strip()
        if len(nombre) < 2:
            raise forms.ValidationError('Ingresa un nombre válido.')
        return nombre

    def clean_mensaje(self):
        mensaje = self.cleaned_data['mensaje'].strip()
        if len(mensaje) < 10:
            raise forms.ValidationError('El mensaje debe tener al menos 10 caracteres.')
        return mensaje
