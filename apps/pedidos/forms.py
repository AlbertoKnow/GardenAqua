"""
Formularios para la app de pedidos.
"""
from django import forms


class CheckoutForm(forms.Form):
    """
    Formulario para el proceso de checkout.
    
    Captura los datos mínimos necesarios para procesar un pedido:
    - Datos de contacto (nombre, email, teléfono opcional)
    - Datos de envío (dirección, ciudad, código postal)
    - Notas adicionales (opcional)
    """
    
    # Datos de contacto
    nombre = forms.CharField(
        max_length=200,
        label='Nombre completo',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Tu nombre completo',
            'autocomplete': 'name',
        })
    )
    
    email = forms.EmailField(
        label='Correo electrónico',
        help_text='Te enviaremos la confirmación y actualizaciones del pedido',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'tu@email.com',
            'autocomplete': 'email',
        })
    )
    
    telefono = forms.CharField(
        max_length=17,
        required=False,
        label='Teléfono (opcional)',
        help_text='Para contactarte si hay algún problema con el envío',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+52 1234567890',
            'autocomplete': 'tel',
        })
    )
    
    # Datos de envío
    direccion = forms.CharField(
        label='Dirección de envío',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Calle, número, colonia...',
            'rows': 2,
            'autocomplete': 'street-address',
        })
    )
    
    ciudad = forms.CharField(
        max_length=100,
        label='Ciudad',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ciudad',
            'autocomplete': 'address-level2',
        })
    )
    
    codigo_postal = forms.CharField(
        max_length=10,
        label='Código Postal',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '00000',
            'autocomplete': 'postal-code',
        })
    )
    
    # Notas adicionales
    notas = forms.CharField(
        required=False,
        label='Notas adicionales (opcional)',
        help_text='Instrucciones especiales de entrega',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: Dejar con el portero, llamar antes de entregar...',
            'rows': 2,
        })
    )
