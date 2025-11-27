"""
Vistas para el módulo de Inventario de Carpas
American Carpas 1 SAS

Versión: 2.0 - Fase 2: Catálogos Básicos
"""

from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib import messages
from django.db.models import Q

from .models import (
    UbicacionAlmacen,
    TipoLona, AnchoLona, ColorLona, TratamientoLona,
    TipoEstructura, MedidaTubo, Calibre, MaterialEstructura, AcabadoEstructura,
    TipoAccesorio,
    InventarioLona, InventarioEstructura, InventarioAccesorio,
    OrdenProduccion, OrdenProduccionItem,
)
from .forms import (
    UbicacionAlmacenForm,
    TipoLonaForm, AnchoLonaForm, ColorLonaForm, TratamientoLonaForm,
    TipoEstructuraForm, MedidaTuboForm, CalibreForm, MaterialEstructuraForm, AcabadoEstructuraForm,
    TipoAccesorioForm,
    InventarioLonaForm, InventarioEstructuraForm, InventarioAccesorioForm,
    OrdenProduccionForm, OrdenProduccionItemForm,
)


# =============================================================================
# MIXIN PARA NAVEGACIÓN DE MÓDULOS
# =============================================================================

class InventarioContextMixin:
    """Mixin que agrega el contexto de navegación a todas las vistas"""
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['show_module_nav'] = True
        context['active_module'] = 'inventarios'
        return context


# =============================================================================
# HOME
# =============================================================================

#@login_required
def home_inventario(request):
    """Vista principal del módulo de inventario"""
    context = {
        'titulo': 'Módulo de Inventario de Carpas',
        'mensaje': 'Módulo en desarrollo - Fase de migración completada',
        'show_module_nav': True,
        'active_module': 'inventarios',
    }
    return render(request, 'inventario/home_inventario.html', context)


# =============================================================================
# UBICACIONES DE ALMACÉN
# =============================================================================

class UbicacionAlmacenListView(LoginRequiredMixin, InventarioContextMixin, ListView):
    model = UbicacionAlmacen
    template_name = 'inventario/ubicacion_list.html'
    context_object_name = 'ubicaciones'
    paginate_by = 15
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Filtro por búsqueda
        search = self.request.GET.get('search', '')
        if search:
            queryset = queryset.filter(nombre__icontains=search)
        return queryset


class UbicacionAlmacenCreateView(LoginRequiredMixin, InventarioContextMixin, CreateView):
    model = UbicacionAlmacen
    form_class = UbicacionAlmacenForm
    template_name = 'inventario/ubicacion_form.html'
    success_url = reverse_lazy('inventario:ubicacion_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Ubicación creada exitosamente.')
        return super().form_valid(form)


class UbicacionAlmacenUpdateView(LoginRequiredMixin, InventarioContextMixin, UpdateView):
    model = UbicacionAlmacen
    form_class = UbicacionAlmacenForm
    template_name = 'inventario/ubicacion_form.html'
    success_url = reverse_lazy('inventario:ubicacion_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Ubicación actualizada exitosamente.')
        return super().form_valid(form)


class UbicacionAlmacenDeleteView(LoginRequiredMixin, InventarioContextMixin, DeleteView):
    model = UbicacionAlmacen
    template_name = 'inventario/ubicacion_confirm_delete.html'
    success_url = reverse_lazy('inventario:ubicacion_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Ubicación eliminada exitosamente.')
        return super().delete(request, *args, **kwargs)


# =============================================================================
# TIPOS DE LONA
# =============================================================================

class TipoLonaListView(LoginRequiredMixin, InventarioContextMixin, ListView):
    model = TipoLona
    template_name = 'inventario/catalogo_list.html'
    context_object_name = 'items'
    paginate_by = 15
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Tipos de Lona'
        context['create_url'] = 'inventario:tipolona_create'
        context['update_url'] = 'inventario:tipolona_update'
        context['delete_url'] = 'inventario:tipolona_delete'
        context['campos'] = ['codigo', 'nombre', 'activo']
        return context


class TipoLonaCreateView(LoginRequiredMixin, InventarioContextMixin, CreateView):
    model = TipoLona
    form_class = TipoLonaForm
    template_name = 'inventario/catalogo_form.html'
    success_url = reverse_lazy('inventario:tipolona_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Nuevo Tipo de Lona'
        context['list_url'] = 'inventario:tipolona_list'
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Tipo de lona creado exitosamente.')
        return super().form_valid(form)


class TipoLonaUpdateView(LoginRequiredMixin, InventarioContextMixin, UpdateView):
    model = TipoLona
    form_class = TipoLonaForm
    template_name = 'inventario/catalogo_form.html'
    success_url = reverse_lazy('inventario:tipolona_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Tipo de Lona'
        context['list_url'] = 'inventario:tipolona_list'
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Tipo de lona actualizado exitosamente.')
        return super().form_valid(form)


class TipoLonaDeleteView(LoginRequiredMixin, InventarioContextMixin, DeleteView):
    model = TipoLona
    template_name = 'inventario/catalogo_confirm_delete.html'
    success_url = reverse_lazy('inventario:tipolona_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Tipo de Lona'
        context['list_url'] = 'inventario:tipolona_list'
        return context


# =============================================================================
# ANCHOS DE LONA
# =============================================================================

class AnchoLonaListView(LoginRequiredMixin, InventarioContextMixin, ListView):
    model = AnchoLona
    template_name = 'inventario/catalogo_list.html'
    context_object_name = 'items'
    paginate_by = 15
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Anchos de Lona'
        context['create_url'] = 'inventario:ancholona_create'
        context['update_url'] = 'inventario:ancholona_update'
        context['delete_url'] = 'inventario:ancholona_delete'
        context['campos'] = ['valor_metros', 'descripcion', 'activo']
        return context


class AnchoLonaCreateView(LoginRequiredMixin, InventarioContextMixin, CreateView):
    model = AnchoLona
    form_class = AnchoLonaForm
    template_name = 'inventario/catalogo_form.html'
    success_url = reverse_lazy('inventario:ancholona_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Nuevo Ancho de Lona'
        context['list_url'] = 'inventario:ancholona_list'
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Ancho de lona creado exitosamente.')
        return super().form_valid(form)


class AnchoLonaUpdateView(LoginRequiredMixin, InventarioContextMixin, UpdateView):
    model = AnchoLona
    form_class = AnchoLonaForm
    template_name = 'inventario/catalogo_form.html'
    success_url = reverse_lazy('inventario:ancholona_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Ancho de Lona'
        context['list_url'] = 'inventario:ancholona_list'
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Ancho de lona actualizado exitosamente.')
        return super().form_valid(form)


class AnchoLonaDeleteView(LoginRequiredMixin, InventarioContextMixin, DeleteView):
    model = AnchoLona
    template_name = 'inventario/catalogo_confirm_delete.html'
    success_url = reverse_lazy('inventario:ancholona_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Ancho de Lona'
        context['list_url'] = 'inventario:ancholona_list'
        return context


# =============================================================================
# COLORES DE LONA
# =============================================================================

class ColorLonaListView(LoginRequiredMixin, InventarioContextMixin, ListView):
    model = ColorLona
    template_name = 'inventario/catalogo_list.html'
    context_object_name = 'items'
    paginate_by = 15
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Colores de Lona'
        context['create_url'] = 'inventario:colorlona_create'
        context['update_url'] = 'inventario:colorlona_update'
        context['delete_url'] = 'inventario:colorlona_delete'
        context['campos'] = ['nombre', 'codigo_hex', 'activo']
        context['tiene_color'] = True
        return context


class ColorLonaCreateView(LoginRequiredMixin, InventarioContextMixin, CreateView):
    model = ColorLona
    form_class = ColorLonaForm
    template_name = 'inventario/catalogo_form.html'
    success_url = reverse_lazy('inventario:colorlona_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Nuevo Color de Lona'
        context['list_url'] = 'inventario:colorlona_list'
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Color de lona creado exitosamente.')
        return super().form_valid(form)


class ColorLonaUpdateView(LoginRequiredMixin, InventarioContextMixin, UpdateView):
    model = ColorLona
    form_class = ColorLonaForm
    template_name = 'inventario/catalogo_form.html'
    success_url = reverse_lazy('inventario:colorlona_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Color de Lona'
        context['list_url'] = 'inventario:colorlona_list'
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Color de lona actualizado exitosamente.')
        return super().form_valid(form)


class ColorLonaDeleteView(LoginRequiredMixin, InventarioContextMixin, DeleteView):
    model = ColorLona
    template_name = 'inventario/catalogo_confirm_delete.html'
    success_url = reverse_lazy('inventario:colorlona_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Color de Lona'
        context['list_url'] = 'inventario:colorlona_list'
        return context


# =============================================================================
# TRATAMIENTOS DE LONA
# =============================================================================

class TratamientoLonaListView(LoginRequiredMixin, InventarioContextMixin, ListView):
    model = TratamientoLona
    template_name = 'inventario/catalogo_list.html'
    context_object_name = 'items'
    paginate_by = 15
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Tratamientos de Lona'
        context['create_url'] = 'inventario:tratamientolona_create'
        context['update_url'] = 'inventario:tratamientolona_update'
        context['delete_url'] = 'inventario:tratamientolona_delete'
        context['campos'] = ['codigo', 'nombre', 'activo']
        return context


class TratamientoLonaCreateView(LoginRequiredMixin, InventarioContextMixin, CreateView):
    model = TratamientoLona
    form_class = TratamientoLonaForm
    template_name = 'inventario/catalogo_form.html'
    success_url = reverse_lazy('inventario:tratamientolona_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Nuevo Tratamiento de Lona'
        context['list_url'] = 'inventario:tratamientolona_list'
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Tratamiento de lona creado exitosamente.')
        return super().form_valid(form)


class TratamientoLonaUpdateView(LoginRequiredMixin, InventarioContextMixin, UpdateView):
    model = TratamientoLona
    form_class = TratamientoLonaForm
    template_name = 'inventario/catalogo_form.html'
    success_url = reverse_lazy('inventario:tratamientolona_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Tratamiento de Lona'
        context['list_url'] = 'inventario:tratamientolona_list'
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Tratamiento de lona actualizado exitosamente.')
        return super().form_valid(form)


class TratamientoLonaDeleteView(LoginRequiredMixin, InventarioContextMixin, DeleteView):
    model = TratamientoLona
    template_name = 'inventario/catalogo_confirm_delete.html'
    success_url = reverse_lazy('inventario:tratamientolona_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Tratamiento de Lona'
        context['list_url'] = 'inventario:tratamientolona_list'
        return context


# =============================================================================
# TIPOS DE ESTRUCTURA
# =============================================================================

class TipoEstructuraListView(LoginRequiredMixin, InventarioContextMixin, ListView):
    model = TipoEstructura
    template_name = 'inventario/catalogo_list.html'
    context_object_name = 'items'
    paginate_by = 15
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Tipos de Estructura'
        context['create_url'] = 'inventario:tipoestructura_create'
        context['update_url'] = 'inventario:tipoestructura_update'
        context['delete_url'] = 'inventario:tipoestructura_delete'
        context['campos'] = ['codigo', 'nombre', 'activo']
        return context


class TipoEstructuraCreateView(LoginRequiredMixin, InventarioContextMixin, CreateView):
    model = TipoEstructura
    form_class = TipoEstructuraForm
    template_name = 'inventario/catalogo_form.html'
    success_url = reverse_lazy('inventario:tipoestructura_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Nuevo Tipo de Estructura'
        context['list_url'] = 'inventario:tipoestructura_list'
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Tipo de estructura creado exitosamente.')
        return super().form_valid(form)


class TipoEstructuraUpdateView(LoginRequiredMixin, InventarioContextMixin, UpdateView):
    model = TipoEstructura
    form_class = TipoEstructuraForm
    template_name = 'inventario/catalogo_form.html'
    success_url = reverse_lazy('inventario:tipoestructura_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Tipo de Estructura'
        context['list_url'] = 'inventario:tipoestructura_list'
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Tipo de estructura actualizado exitosamente.')
        return super().form_valid(form)


class TipoEstructuraDeleteView(LoginRequiredMixin, InventarioContextMixin, DeleteView):
    model = TipoEstructura
    template_name = 'inventario/catalogo_confirm_delete.html'
    success_url = reverse_lazy('inventario:tipoestructura_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Tipo de Estructura'
        context['list_url'] = 'inventario:tipoestructura_list'
        return context


# =============================================================================
# MEDIDAS DE TUBO
# =============================================================================

class MedidaTuboListView(LoginRequiredMixin, InventarioContextMixin, ListView):
    model = MedidaTubo
    template_name = 'inventario/catalogo_list.html'
    context_object_name = 'items'
    paginate_by = 15
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Medidas de Tubo'
        context['create_url'] = 'inventario:medidatubo_create'
        context['update_url'] = 'inventario:medidatubo_update'
        context['delete_url'] = 'inventario:medidatubo_delete'
        context['campos'] = ['valor_medida', 'descripcion', 'activo']
        context['campo_nombre'] = 'valor_medida'
        return context


class MedidaTuboCreateView(LoginRequiredMixin, InventarioContextMixin, CreateView):
    model = MedidaTubo
    form_class = MedidaTuboForm
    template_name = 'inventario/catalogo_form.html'
    success_url = reverse_lazy('inventario:medidatubo_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Nueva Medida de Tubo'
        context['list_url'] = 'inventario:medidatubo_list'
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Medida de tubo creada exitosamente.')
        return super().form_valid(form)


class MedidaTuboUpdateView(LoginRequiredMixin, InventarioContextMixin, UpdateView):
    model = MedidaTubo
    form_class = MedidaTuboForm
    template_name = 'inventario/catalogo_form.html'
    success_url = reverse_lazy('inventario:medidatubo_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Medida de Tubo'
        context['list_url'] = 'inventario:medidatubo_list'
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Medida de tubo actualizada exitosamente.')
        return super().form_valid(form)


class MedidaTuboDeleteView(LoginRequiredMixin, InventarioContextMixin, DeleteView):
    model = MedidaTubo
    template_name = 'inventario/catalogo_confirm_delete.html'
    success_url = reverse_lazy('inventario:medidatubo_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Medida de Tubo'
        context['list_url'] = 'inventario:medidatubo_list'
        return context


# =============================================================================
# CALIBRES
# =============================================================================

class CalibreListView(LoginRequiredMixin, InventarioContextMixin, ListView):
    model = Calibre
    template_name = 'inventario/catalogo_list.html'
    context_object_name = 'items'
    paginate_by = 15
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Calibres'
        context['create_url'] = 'inventario:calibre_create'
        context['update_url'] = 'inventario:calibre_update'
        context['delete_url'] = 'inventario:calibre_delete'
        context['campos'] = ['valor_calibre', 'descripcion', 'activo']
        context['campo_nombre'] = 'valor_calibre'
        return context


class CalibreCreateView(LoginRequiredMixin, InventarioContextMixin, CreateView):
    model = Calibre
    form_class = CalibreForm
    template_name = 'inventario/catalogo_form.html'
    success_url = reverse_lazy('inventario:calibre_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Nuevo Calibre'
        context['list_url'] = 'inventario:calibre_list'
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Calibre creado exitosamente.')
        return super().form_valid(form)


class CalibreUpdateView(LoginRequiredMixin, InventarioContextMixin, UpdateView):
    model = Calibre
    form_class = CalibreForm
    template_name = 'inventario/catalogo_form.html'
    success_url = reverse_lazy('inventario:calibre_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Calibre'
        context['list_url'] = 'inventario:calibre_list'
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Calibre actualizado exitosamente.')
        return super().form_valid(form)


class CalibreDeleteView(LoginRequiredMixin, InventarioContextMixin, DeleteView):
    model = Calibre
    template_name = 'inventario/catalogo_confirm_delete.html'
    success_url = reverse_lazy('inventario:calibre_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Calibre'
        context['list_url'] = 'inventario:calibre_list'
        return context


# =============================================================================
# MATERIALES DE ESTRUCTURA
# =============================================================================

class MaterialEstructuraListView(LoginRequiredMixin, InventarioContextMixin, ListView):
    model = MaterialEstructura
    template_name = 'inventario/catalogo_list.html'
    context_object_name = 'items'
    paginate_by = 15
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Materiales de Estructura'
        context['create_url'] = 'inventario:material_create'
        context['update_url'] = 'inventario:material_update'
        context['delete_url'] = 'inventario:material_delete'
        context['campos'] = ['codigo', 'nombre', 'activo']
        return context


class MaterialEstructuraCreateView(LoginRequiredMixin, InventarioContextMixin, CreateView):
    model = MaterialEstructura
    form_class = MaterialEstructuraForm
    template_name = 'inventario/catalogo_form.html'
    success_url = reverse_lazy('inventario:material_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Nuevo Material'
        context['list_url'] = 'inventario:material_list'
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Material creado exitosamente.')
        return super().form_valid(form)


class MaterialEstructuraUpdateView(LoginRequiredMixin, InventarioContextMixin, UpdateView):
    model = MaterialEstructura
    form_class = MaterialEstructuraForm
    template_name = 'inventario/catalogo_form.html'
    success_url = reverse_lazy('inventario:material_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Material'
        context['list_url'] = 'inventario:material_list'
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Material actualizado exitosamente.')
        return super().form_valid(form)


class MaterialEstructuraDeleteView(LoginRequiredMixin, InventarioContextMixin, DeleteView):
    model = MaterialEstructura
    template_name = 'inventario/catalogo_confirm_delete.html'
    success_url = reverse_lazy('inventario:material_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Material'
        context['list_url'] = 'inventario:material_list'
        return context


# =============================================================================
# ACABADOS DE ESTRUCTURA
# =============================================================================

class AcabadoEstructuraListView(LoginRequiredMixin, InventarioContextMixin, ListView):
    model = AcabadoEstructura
    template_name = 'inventario/catalogo_list.html'
    context_object_name = 'items'
    paginate_by = 15
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Acabados de Estructura'
        context['create_url'] = 'inventario:acabado_create'
        context['update_url'] = 'inventario:acabado_update'
        context['delete_url'] = 'inventario:acabado_delete'
        context['campos'] = ['codigo', 'nombre', 'activo']
        return context


class AcabadoEstructuraCreateView(LoginRequiredMixin, InventarioContextMixin, CreateView):
    model = AcabadoEstructura
    form_class = AcabadoEstructuraForm
    template_name = 'inventario/catalogo_form.html'
    success_url = reverse_lazy('inventario:acabado_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Nuevo Acabado'
        context['list_url'] = 'inventario:acabado_list'
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Acabado creado exitosamente.')
        return super().form_valid(form)


class AcabadoEstructuraUpdateView(LoginRequiredMixin, InventarioContextMixin, UpdateView):
    model = AcabadoEstructura
    form_class = AcabadoEstructuraForm
    template_name = 'inventario/catalogo_form.html'
    success_url = reverse_lazy('inventario:acabado_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Acabado'
        context['list_url'] = 'inventario:acabado_list'
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Acabado actualizado exitosamente.')
        return super().form_valid(form)


class AcabadoEstructuraDeleteView(LoginRequiredMixin, InventarioContextMixin, DeleteView):
    model = AcabadoEstructura
    template_name = 'inventario/catalogo_confirm_delete.html'
    success_url = reverse_lazy('inventario:acabado_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Acabado'
        context['list_url'] = 'inventario:acabado_list'
        return context


# =============================================================================
# TIPOS DE ACCESORIO
# =============================================================================

class TipoAccesorioListView(LoginRequiredMixin, InventarioContextMixin, ListView):
    model = TipoAccesorio
    template_name = 'inventario/catalogo_list.html'
    context_object_name = 'items'
    paginate_by = 15
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Tipos de Accesorio'
        context['create_url'] = 'inventario:tipoaccesorio_create'
        context['update_url'] = 'inventario:tipoaccesorio_update'
        context['delete_url'] = 'inventario:tipoaccesorio_delete'
        context['campos'] = ['codigo', 'nombre', 'activo']
        return context


class TipoAccesorioCreateView(LoginRequiredMixin, InventarioContextMixin, CreateView):
    model = TipoAccesorio
    form_class = TipoAccesorioForm
    template_name = 'inventario/catalogo_form.html'
    success_url = reverse_lazy('inventario:tipoaccesorio_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Nuevo Tipo de Accesorio'
        context['list_url'] = 'inventario:tipoaccesorio_list'
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Tipo de accesorio creado exitosamente.')
        return super().form_valid(form)


class TipoAccesorioUpdateView(LoginRequiredMixin, InventarioContextMixin, UpdateView):
    model = TipoAccesorio
    form_class = TipoAccesorioForm
    template_name = 'inventario/catalogo_form.html'
    success_url = reverse_lazy('inventario:tipoaccesorio_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Tipo de Accesorio'
        context['list_url'] = 'inventario:tipoaccesorio_list'
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Tipo de accesorio actualizado exitosamente.')
        return super().form_valid(form)


class TipoAccesorioDeleteView(LoginRequiredMixin, InventarioContextMixin, DeleteView):
    model = TipoAccesorio
    template_name = 'inventario/catalogo_confirm_delete.html'
    success_url = reverse_lazy('inventario:tipoaccesorio_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Tipo de Accesorio'
        context['list_url'] = 'inventario:tipoaccesorio_list'
        return context


# =============================================================================
# INVENTARIO DE LONAS
# =============================================================================

class InventarioLonaListView(LoginRequiredMixin, InventarioContextMixin, ListView):
    model = InventarioLona
    template_name = 'inventario/lona_list.html'
    context_object_name = 'lonas'
    paginate_by = 15
    
    def get_queryset(self):
        queryset = super().get_queryset().select_related(
            'tipo_lona', 'ancho_lona', 'color_lona', 'ubicacion'
        )
        search = self.request.GET.get('search', '')
        if search:
            queryset = queryset.filter(codigo_rollo__icontains=search)
        return queryset


class InventarioLonaDetailView(LoginRequiredMixin, InventarioContextMixin, DetailView):
    model = InventarioLona
    template_name = 'inventario/lona_detail.html'
    context_object_name = 'lona'


class InventarioLonaCreateView(LoginRequiredMixin, InventarioContextMixin, CreateView):
    model = InventarioLona
    form_class = InventarioLonaForm
    template_name = 'inventario/lona_form.html'
    success_url = reverse_lazy('inventario:lona_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Rollo de lona registrado exitosamente.')
        return super().form_valid(form)


class InventarioLonaUpdateView(LoginRequiredMixin, InventarioContextMixin, UpdateView):
    model = InventarioLona
    form_class = InventarioLonaForm
    template_name = 'inventario/lona_form.html'
    success_url = reverse_lazy('inventario:lona_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Rollo de lona actualizado exitosamente.')
        return super().form_valid(form)


class InventarioLonaDeleteView(LoginRequiredMixin, InventarioContextMixin, DeleteView):
    model = InventarioLona
    template_name = 'inventario/lona_confirm_delete.html'
    success_url = reverse_lazy('inventario:lona_list')


# =============================================================================
# INVENTARIO DE ESTRUCTURA
# =============================================================================

class InventarioEstructuraListView(LoginRequiredMixin, InventarioContextMixin, ListView):
    model = InventarioEstructura
    template_name = 'inventario/estructura_list.html'
    context_object_name = 'estructuras'
    paginate_by = 15
    
    def get_queryset(self):
        queryset = super().get_queryset().select_related(
            'tipo_estructura', 'medida_tubo', 'calibre', 'material', 'ubicacion'
        )
        search = self.request.GET.get('search', '')
        if search:
            queryset = queryset.filter(codigo_lote__icontains=search)
        return queryset


class InventarioEstructuraDetailView(LoginRequiredMixin, InventarioContextMixin, DetailView):
    model = InventarioEstructura
    template_name = 'inventario/estructura_detail.html'
    context_object_name = 'estructura'


class InventarioEstructuraCreateView(LoginRequiredMixin, InventarioContextMixin, CreateView):
    model = InventarioEstructura
    form_class = InventarioEstructuraForm
    template_name = 'inventario/estructura_form.html'
    success_url = reverse_lazy('inventario:estructura_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Lote de estructura registrado exitosamente.')
        return super().form_valid(form)


class InventarioEstructuraUpdateView(LoginRequiredMixin, InventarioContextMixin, UpdateView):
    model = InventarioEstructura
    form_class = InventarioEstructuraForm
    template_name = 'inventario/estructura_form.html'
    success_url = reverse_lazy('inventario:estructura_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Lote de estructura actualizado exitosamente.')
        return super().form_valid(form)


class InventarioEstructuraDeleteView(LoginRequiredMixin, InventarioContextMixin, DeleteView):
    model = InventarioEstructura
    template_name = 'inventario/estructura_confirm_delete.html'
    success_url = reverse_lazy('inventario:estructura_list')


# =============================================================================
# INVENTARIO DE ACCESORIOS
# =============================================================================

class InventarioAccesorioListView(LoginRequiredMixin, InventarioContextMixin, ListView):
    model = InventarioAccesorio
    template_name = 'inventario/accesorio_list.html'
    context_object_name = 'accesorios'
    paginate_by = 15
    
    def get_queryset(self):
        queryset = super().get_queryset().select_related(
            'tipo_accesorio', 'ubicacion'
        )
        search = self.request.GET.get('search', '')
        if search:
            queryset = queryset.filter(nombre__icontains=search)
        return queryset


class InventarioAccesorioDetailView(LoginRequiredMixin, InventarioContextMixin, DetailView):
    model = InventarioAccesorio
    template_name = 'inventario/accesorio_detail.html'
    context_object_name = 'accesorio'


class InventarioAccesorioCreateView(LoginRequiredMixin, InventarioContextMixin, CreateView):
    model = InventarioAccesorio
    form_class = InventarioAccesorioForm
    template_name = 'inventario/accesorio_form.html'
    success_url = reverse_lazy('inventario:accesorio_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Accesorio registrado exitosamente.')
        return super().form_valid(form)


class InventarioAccesorioUpdateView(LoginRequiredMixin, InventarioContextMixin, UpdateView):
    model = InventarioAccesorio
    form_class = InventarioAccesorioForm
    template_name = 'inventario/accesorio_form.html'
    success_url = reverse_lazy('inventario:accesorio_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Accesorio actualizado exitosamente.')
        return super().form_valid(form)


class InventarioAccesorioDeleteView(LoginRequiredMixin, InventarioContextMixin, DeleteView):
    model = InventarioAccesorio
    template_name = 'inventario/accesorio_confirm_delete.html'
    success_url = reverse_lazy('inventario:accesorio_list')


# =============================================================================
# VISTAS - ÓRDENES DE PRODUCCIÓN
# =============================================================================

class OrdenProduccionListView(LoginRequiredMixin, InventarioContextMixin, ListView):
    """Vista de lista de órdenes de producción"""
    model = OrdenProduccion
    template_name = 'inventario/orden_list.html'
    context_object_name = 'ordenes'
    paginate_by = 15
    ordering = ['-fecha_orden', '-numero_orden']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtro por estado
        estado = self.request.GET.get('estado')
        if estado:
            queryset = queryset.filter(estado=estado)
        
        # Filtro por urgente
        urgente = self.request.GET.get('urgente')
        if urgente == '1':
            queryset = queryset.filter(es_urgente=True)
        
        # Filtro por proyecto
        proyecto = self.request.GET.get('proyecto')
        if proyecto:
            queryset = queryset.filter(proyecto_id=proyecto)
        
        # Búsqueda
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                Q(numero_orden__icontains=q) |
                Q(cliente__icontains=q) |
                Q(proyecto__nombre__icontains=q)
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Estadísticas
        from django.db.models import Count
        context['stats'] = {
            'total': OrdenProduccion.objects.count(),
            'pendientes': OrdenProduccion.objects.filter(estado='PENDIENTE').count(),
            'en_proceso': OrdenProduccion.objects.filter(estado='EN_PROCESO').count(),
            'completadas': OrdenProduccion.objects.filter(estado='COMPLETADA').count(),
            'urgentes': OrdenProduccion.objects.filter(es_urgente=True, estado__in=['PENDIENTE', 'EN_PROCESO']).count(),
        }
        
        return context


class OrdenProduccionDetailView(LoginRequiredMixin, InventarioContextMixin, DetailView):
    """Vista de detalle de orden de producción"""
    model = OrdenProduccion
    template_name = 'inventario/orden_detail.html'
    context_object_name = 'orden'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orden = self.get_object()
        
        # Obtener ítems relacionados
        context['items'] = orden.items.all()
        context['consumo_lonas'] = orden.lonas_consumidas.all()
        context['consumo_estructura'] = orden.estructura_consumida.all()
        context['consumo_accesorios'] = orden.accesorios_consumidos.all()
        
        return context


class OrdenProduccionCreateView(LoginRequiredMixin, InventarioContextMixin, CreateView):
    """Vista de creación de orden de producción"""
    model = OrdenProduccion
    form_class = OrdenProduccionForm
    template_name = 'inventario/orden_form.html'
    success_url = '/inventario/ordenes/'
    
    def form_valid(self, form):
        form.instance.creado_por = self.request.user
        messages.success(self.request, f'Orden de producción creada exitosamente')
        return super().form_valid(form)


class OrdenProduccionUpdateView(LoginRequiredMixin, InventarioContextMixin, UpdateView):
    """Vista de edición de orden de producción"""
    model = OrdenProduccion
    form_class = OrdenProduccionForm
    template_name = 'inventario/orden_form.html'
    
    def get_success_url(self):
        return f'/inventario/ordenes/{self.object.pk}/'
    
    def form_valid(self, form):
        messages.success(self.request, f'Orden {self.object.numero_orden} actualizada exitosamente')
        return super().form_valid(form)


class OrdenProduccionDeleteView(LoginRequiredMixin, InventarioContextMixin, DeleteView):
    """Vista de eliminación de orden de producción"""
    model = OrdenProduccion
    template_name = 'inventario/orden_confirm_delete.html'
    success_url = '/inventario/ordenes/'
    
    def delete(self, request, *args, **kwargs):
        orden = self.get_object()
        messages.success(request, f'Orden {orden.numero_orden} eliminada exitosamente')
        return super().delete(request, *args, **kwargs)


# Vista para agregar ítems a una orden
class OrdenItemCreateView(LoginRequiredMixin, InventarioContextMixin, CreateView):
    """Vista para agregar ítem a una orden"""
    model = OrdenProduccionItem
    form_class = OrdenProduccionItemForm
    template_name = 'inventario/orden_item_form.html'
    
    def dispatch(self, request, *args, **kwargs):
        self.orden = get_object_or_404(OrdenProduccion, pk=kwargs['orden_pk'])
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orden'] = self.orden
        return context
    
    def form_valid(self, form):
        form.instance.orden = self.orden
        messages.success(self.request, f'Ítem agregado a la orden {self.orden.numero_orden}')
        return super().form_valid(form)
    
    def get_success_url(self):
        return f'/inventario/ordenes/{self.orden.pk}/'
