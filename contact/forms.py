# Formularios de la aplicación 'contact'
# Importa el módulo de formularios de Django (Form, ModelForm, widgets, ValidationError)
from django import forms

# Importa el modelo en el que se basa el formulario (desde models.py de esta misma app)
from .models import MensajeContacto


# ModelForm: formulario que se construye automáticamente a partir de los campos de un modelo
class ContactoForm(forms.ModelForm):
    """Formulario de contacto basado en el modelo MensajeContacto."""

    # Meta: configuración del ModelForm (qué modelo usa, qué campos muestra y cómo se ven)
    class Meta:
        # Modelo del que se toman los campos y sus validaciones (EmailField valida el formato del correo, choices limita el asunto)
        model = MensajeContacto
        # Campos que se muestran en el formulario ('leido' y 'creado' quedan fuera porque no los llena el usuario)
        fields = ['nombre', 'email', 'asunto', 'mensaje']
        # Textos de las etiquetas (<label>) que se muestran junto a cada campo
        labels = {
            'nombre': 'Nombre',                 # Etiqueta del campo nombre
            'email': 'Correo electrónico',      # Etiqueta del campo email
            'asunto': 'Motivo',                 # Etiqueta del campo asunto
            'mensaje': 'Mensaje',               # Etiqueta del campo mensaje
        }
        # Widgets: definen qué elemento HTML se dibuja para cada campo y con qué atributos (clases Bootstrap, placeholder)
        widgets = {
            # <input type="text"> con estilo Bootstrap, texto de ejemplo y autocompletado del nombre
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu nombre', 'autocomplete': 'name'}),
            # <input type="email">: el navegador también ayuda a validar que tenga formato de correo
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'tucorreo@ejemplo.cl', 'autocomplete': 'email'}),
            # <select> con las opciones de ASUNTOS definidas en el modelo
            'asunto': forms.Select(attrs={'class': 'form-select'}),
            # <textarea> de 5 filas para escribir el mensaje
            'mensaje': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Escribe tu consulta...'}),
        }

    # Constructor del formulario: se ejecuta cada vez que se crea un ContactoForm (vacío o con datos)
    def __init__(self, *args, **kwargs):
        # Llama al constructor original de ModelForm para que arme los campos normalmente
        super().__init__(*args, **kwargs)
        # Si el formulario fue enviado con errores, marca los campos inválidos (estilo Bootstrap)
        # is_bound es True cuando el formulario recibió datos (request.POST), False cuando está vacío
        if self.is_bound:
            # self.errors es un diccionario {campo: lista de errores}; se recorre cada campo con error
            for nombre_campo in self.errors:
                # Se ignoran errores generales ('__all__') que no corresponden a un campo concreto
                if nombre_campo in self.fields:
                    # Obtiene el widget (elemento HTML) del campo con error
                    widget = self.fields[nombre_campo].widget
                    # Agrega la clase 'is-invalid' de Bootstrap para pintar el campo en rojo
                    widget.attrs['class'] = widget.attrs.get('class', '') + ' is-invalid'

    # Validación personalizada del campo 'nombre' (Django llama automáticamente a clean_<campo> durante is_valid())
    def clean_nombre(self):
        # cleaned_data tiene el valor ya validado por Django; strip() quita espacios al inicio y al final
        nombre = self.cleaned_data['nombre'].strip()
        # Regla propia: el nombre debe tener al menos 2 caracteres
        if len(nombre) < 2:
            # ValidationError marca el campo como inválido y muestra este mensaje bajo el campo
            raise forms.ValidationError('Ingresa un nombre válido.')
        # Devuelve el valor limpio; es el que se guardará en la BD
        return nombre

    # Validación personalizada del campo 'mensaje'
    def clean_mensaje(self):
        # Toma el mensaje validado y le quita los espacios sobrantes
        mensaje = self.cleaned_data['mensaje'].strip()
        # Regla propia: el mensaje debe tener al menos 10 caracteres
        if len(mensaje) < 10:
            # Si no cumple, el formulario queda inválido con este mensaje de error
            raise forms.ValidationError('El mensaje debe tener al menos 10 caracteres.')
        # Devuelve el mensaje limpio
        return mensaje
