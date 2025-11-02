from django.contrib import admin
from django import forms
from .models import (
    TrabajadorPersonal, TrabajadorLaboral, TrabajadorAfiliaciones,
    TrabajadorDotacion, TrabajadorCurso, TrabajadorRol,
    TipoCurso, TipoDotacion
)


# =====================================================
# FORMULARIO 100% FUNCIONAL PARA ADMIN
# =====================================================

class TrabajadorDotacionAdminForm(forms.ModelForm):
    """Formulario con tallas que funcionan desde el inicio"""
    
    # Definir el campo talla como CharField para que acepte cualquier valor
    talla = forms.CharField(
        max_length=20,
        required=False,
        label='Talla',
        help_text='Ingrese la talla manualmente. Validación automática según el tipo.',
        widget=forms.TextInput(attrs={
            'class': 'vTextField',
            'placeholder': 'Ej: 40, M, L, XL'
        })
    )
    
    class Meta:
        model = TrabajadorDotacion
        fields = [
            'id_trabajador',
            'tipo_dotacion_catalogo',
            'talla',
            'cantidad',
            'fecha_entrega',
            'fecha_vencimiento',
            'estado',
            'fecha_devolucion',
            'motivo_devolucion',
            'observaciones'
        ]
        widgets = {
            'observaciones': forms.Textarea(attrs={'rows': 3}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        tipo_catalogo = cleaned_data.get('tipo_dotacion_catalogo')
        talla = cleaned_data.get('talla')
        
        if tipo_catalogo:
            # Validar talla si es requerida
            if tipo_catalogo.requiere_talla:
                if not talla or talla.strip() == '':
                    raise forms.ValidationError({
                        'talla': f'Este tipo de dotación requiere talla. Disponibles: {tipo_catalogo.tallas_disponibles}'
                    })
                
                # Limpiar espacios
                talla = talla.strip()
                
                # Validar que la talla sea válida
                if tipo_catalogo.tallas_disponibles:
                    tallas_validas = tipo_catalogo.get_tallas_lista()
                    if talla not in tallas_validas:
                        raise forms.ValidationError({
                            'talla': f'Talla "{talla}" no válida. Disponibles: {", ".join(tallas_validas)}'
                        })
                
                cleaned_data['talla'] = talla
            else:
                # Si no requiere talla, poner N/A
                cleaned_data['talla'] = 'N/A'
        
        return cleaned_data


# =====================================================
# ADMIN 100% FUNCIONAL
# =====================================================

@admin.register(TrabajadorDotacion)
class TrabajadorDotacionAdmin(admin.ModelAdmin):
    """Admin totalmente funcional"""
    
    form = TrabajadorDotacionAdminForm
    
    list_display = [
        'id_dotacion',
        'id_trabajador',
        'tipo_dotacion',
        'talla',
        'cantidad',
        'fecha_entrega',
        'estado'
    ]
    
    list_filter = ['estado', 'tipo_dotacion_catalogo', 'fecha_entrega']
    search_fields = ['id_trabajador__nombres', 'id_trabajador__apellidos', 'tipo_dotacion']
    
    fieldsets = (
        ('👤 Trabajador', {
            'fields': ('id_trabajador',)
        }),
        ('📦 Dotación', {
            'fields': (
                'tipo_dotacion_catalogo',
                'talla',
                'cantidad',
            ),
            'description': (
                '<div style="background: #e3f2fd; padding: 15px; border-left: 4px solid #2196f3; margin: 10px 0;">'
                '<strong>📝 Instrucciones:</strong><br><br>'
                '<strong>1.</strong> Seleccione el <strong>Tipo de dotación</strong><br>'
                '<strong>2.</strong> Escriba la <strong>Talla</strong> manualmente (se validará automáticamente)<br>'
                '<strong>3.</strong> Complete cantidad y fecha de entrega<br>'
                '<strong>4.</strong> Guarde<br><br>'
                '<em>💡 Consejo: Para ver las tallas disponibles, revise el tipo de dotación en el catálogo.</em>'
                '</div>'
            )
        }),
        ('📅 Fechas', {
            'fields': ('fecha_entrega', 'fecha_vencimiento')
        }),
        ('📊 Estado y Observaciones', {
            'fields': ('estado', 'fecha_devolucion', 'motivo_devolucion', 'observaciones'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        """Autocompletar campos al guardar"""
        # Autocompletar tipo_dotacion
        if obj.tipo_dotacion_catalogo:
            obj.tipo_dotacion = obj.tipo_dotacion_catalogo.nombre_tipo_dotacion
            
            # Calcular fecha de vencimiento
            if not obj.fecha_vencimiento and obj.fecha_entrega:
                from datetime import timedelta
                obj.fecha_vencimiento = obj.fecha_entrega + timedelta(
                    days=obj.tipo_dotacion_catalogo.vida_util_dias
                )
        
        # Estado por defecto
        if not obj.estado:
            obj.estado = 'ACTIVO'
        
        super().save_model(request, obj, form, change)


# =====================================================
# ADMIN PARA TIPOS DE DOTACIÓN
# =====================================================

@admin.register(TipoDotacion)
class TipoDotacionAdmin(admin.ModelAdmin):
    list_display = ['nombre_tipo_dotacion', 'vida_util_dias', 'requiere_talla', 'mostrar_tallas', 'activo']
    list_filter = ['activo', 'requiere_talla']
    search_fields = ['nombre_tipo_dotacion']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre_tipo_dotacion', 'vida_util_dias', 'activo')
        }),
        ('Tallas', {
            'fields': ('requiere_talla', 'tallas_disponibles'),
            'description': (
                '<div style="background: #fff3cd; padding: 15px; border-left: 4px solid #ffc107;">'
                '<strong>⚠️ FORMATO DE TALLAS:</strong><br><br>'
                '<strong style="color: green;">✅ CORRECTO:</strong> <code>35,36,37,38,39,40</code> (sin espacios)<br>'
                '<strong style="color: red;">❌ INCORRECTO:</strong> <code>35, 36, 37</code> (con espacios)'
                '</div>'
            )
        }),
        ('Otros', {
            'fields': ('normativa_referencia', 'descripcion'),
            'classes': ('collapse',)
        }),
    )
    
    def mostrar_tallas(self, obj):
        if obj.requiere_talla and obj.tallas_disponibles:
            tallas = obj.get_tallas_lista()
            return f"{len(tallas)} tallas: {', '.join(tallas[:5])}{'...' if len(tallas) > 5 else ''}"
        return 'N/A'
    mostrar_tallas.short_description = 'Tallas'
    
    def save_model(self, request, obj, form, change):
        if obj.requiere_talla and obj.tallas_disponibles:
            tallas = [t.strip() for t in obj.tallas_disponibles.split(',')]
            obj.tallas_disponibles = ','.join(t for t in tallas if t)
        super().save_model(request, obj, form, change)


# Registrar los demás modelos
admin.site.register(TipoCurso)
admin.site.register(TrabajadorPersonal)
admin.site.register(TrabajadorLaboral)
admin.site.register(TrabajadorAfiliaciones)
admin.site.register(TrabajadorCurso)
admin.site.register(TrabajadorRol)