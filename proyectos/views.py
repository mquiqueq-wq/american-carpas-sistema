"""
Vistas para el módulo de gestión de proyectos
American Carpas 1 SAS

Vistas completas para todas las 8 fases
"""
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from datetime import date
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime, timedelta
from .models import Proyecto, Actividad

from trabajadores.models import TrabajadorPersonal
from .models import (
    TipoProyecto,
    EstadoProyecto,
    TipoDocumentoProyecto,
    Cliente,
    Proyecto,
    Actividad,
    AsignacionTrabajador,
    DocumentoProyecto,
    EvidenciaFotografica,
    AvanceActividad,
)

from .forms import (
    TipoProyectoForm,
    EstadoProyectoForm,
    TipoDocumentoProyectoForm,
    ClienteForm,
    ProyectoForm,
    ActividadForm,
    AsignacionTrabajadorForm,
    DocumentoProyectoForm,
    EvidenciaFotograficaForm,
    AvanceActividadForm,
)


# =====================================================
# HOME DEL MÓDULO
# =====================================================

def home_proyectos(request):
    """Vista principal del módulo de proyectos"""
    
    # Estadísticas generales
    total_proyectos = Proyecto.objects.filter(activo=True).count()
    total_clientes = Cliente.objects.filter(activo=True).count()
    proyectos_activos = Proyecto.objects.filter(
        activo=True,
        estado_proyecto__es_estado_final=False
    ).count()
    
    context = {
        'total_proyectos': total_proyectos,
        'total_clientes': total_clientes,
        'proyectos_activos': proyectos_activos,
        'show_module_nav': True,
        'active_module': 'proyectos',
    }
    return render(request, 'proyectos/home_proyectos.html', context)


# =====================================================
# FASE 1: VISTAS DE CATÁLOGOS - TIPO PROYECTO
# =====================================================

def tipo_proyecto_list(request):
    """Listado de tipos de proyectos con búsqueda y paginación"""
    query = request.GET.get('q', '')
    
    # Aplicar búsqueda si existe
    if query:
        tipos = TipoProyecto.objects.filter(
            Q(nombre_tipo__icontains=query) |
            Q(descripcion__icontains=query)
        ).order_by('nombre_tipo')
    else:
        tipos = TipoProyecto.objects.all().order_by('nombre_tipo')
    
    # Paginación
    paginator = Paginator(tipos, 10)  # 10 elementos por página
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,  # ✅ Ahora envía 'page_obj'
        'query': query,         # ✅ Envía la búsqueda
        'show_module_nav': True,
        'active_module': 'proyectos',
    }
    return render(request, 'proyectos/catalogos/tipo_proyecto_list.html', context)


def tipo_proyecto_create(request):
    """Crear nuevo tipo de proyecto"""
    if request.method == 'POST':
        form = TipoProyectoForm(request.POST)
        if form.is_valid():
            tipo = form.save()
            messages.success(request, f'✅ Tipo de proyecto "{tipo.nombre_tipo}" creado exitosamente.')
            return redirect('proyectos:tipo_proyecto_list')
    else:
        form = TipoProyectoForm()
    
    context = {
        'form': form,
        'titulo': 'Nuevo Tipo de Proyecto',
        'show_module_nav': True,
        'active_module': 'proyectos',
    }
    return render(request, 'proyectos/catalogos/tipo_proyecto_form.html', context)


def tipo_proyecto_update(request, id_tipo_proyecto):
    """Editar tipo de proyecto"""
    tipo = get_object_or_404(TipoProyecto, id_tipo_proyecto=id_tipo_proyecto)
    
    if request.method == 'POST':
        form = TipoProyectoForm(request.POST, instance=tipo)
        if form.is_valid():
            tipo = form.save()
            messages.success(request, f'✅ Tipo de proyecto "{tipo.nombre_tipo}" actualizado.')
            return redirect('proyectos:tipo_proyecto_list')
    else:
        form = TipoProyectoForm(instance=tipo)
    
    context = {
        'form': form,
        'tipo': tipo,
        'titulo': 'Editar Tipo de Proyecto',
        'show_module_nav': True,
        'active_module': 'proyectos',
    }
    return render(request, 'proyectos/catalogos/tipo_proyecto_form.html', context)


def tipo_proyecto_delete(request, id_tipo_proyecto):
    """Eliminar tipo de proyecto"""
    tipo = get_object_or_404(TipoProyecto, id_tipo_proyecto=id_tipo_proyecto)
    
    if request.method == 'POST':
        nombre = tipo.nombre_tipo
        try:
            tipo.delete()
            messages.success(request, f'✅ Tipo de proyecto "{nombre}" eliminado.')
            return redirect('proyectos:tipo_proyecto_list')
        except Exception as e:
            messages.error(request, f'❌ No se puede eliminar. Tiene proyectos asociados.')
            return redirect('proyectos:tipo_proyecto_list')
    
    context = {
        'tipo': tipo,
        'show_module_nav': True,
        'active_module': 'proyectos',
    }
    return render(request, 'proyectos/catalogos/tipo_proyecto_confirm_delete.html', context)


# =====================================================
# FASE 1: VISTAS DE CATÁLOGOS - ESTADO PROYECTO
# =====================================================

def estado_proyecto_list(request):
    """Listado de estados de proyectos con búsqueda y paginación"""
    query = request.GET.get('q', '')
    
    # Aplicar búsqueda si existe
    if query:
        estados = EstadoProyecto.objects.filter(
            Q(nombre_estado__icontains=query) |
            Q(descripcion__icontains=query)
        ).order_by('orden_visualizacion', 'nombre_estado')
    else:
        estados = EstadoProyecto.objects.all().order_by('orden_visualizacion', 'nombre_estado')
    
    # Paginación
    paginator = Paginator(estados, 10)  # 10 elementos por página
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,  # ✅ Ahora envía 'page_obj'
        'query': query,         # ✅ Envía la búsqueda
        'show_module_nav': True,
        'active_module': 'proyectos',
    }
    return render(request, 'proyectos/catalogos/estado_proyecto_list.html', context)


def estado_proyecto_create(request):
    """Crear nuevo estado de proyecto"""
    if request.method == 'POST':
        form = EstadoProyectoForm(request.POST)
        if form.is_valid():
            estado = form.save()
            messages.success(request, f'✅ Estado "{estado.nombre_estado}" creado exitosamente.')
            return redirect('proyectos:estado_proyecto_list')
    else:
        form = EstadoProyectoForm()
    
    context = {
        'form': form,
        'titulo': 'Nuevo Estado de Proyecto',
        'show_module_nav': True,
        'active_module': 'proyectos',
    }
    return render(request, 'proyectos/catalogos/estado_proyecto_form.html', context)


def estado_proyecto_update(request, id_estado_proyecto):
    """Editar estado de proyecto"""
    estado = get_object_or_404(EstadoProyecto, id_estado_proyecto=id_estado_proyecto)
    
    if request.method == 'POST':
        form = EstadoProyectoForm(request.POST, instance=estado)
        if form.is_valid():
            estado = form.save()
            messages.success(request, f'✅ Estado "{estado.nombre_estado}" actualizado.')
            return redirect('proyectos:estado_proyecto_list')
    else:
        form = EstadoProyectoForm(instance=estado)
    
    context = {
        'form': form,
        'estado': estado,
        'titulo': 'Editar Estado de Proyecto',
        'show_module_nav': True,
        'active_module': 'proyectos',
    }
    return render(request, 'proyectos/catalogos/estado_proyecto_form.html', context)


def estado_proyecto_delete(request, id_estado_proyecto):
    """Eliminar estado de proyecto"""
    estado = get_object_or_404(EstadoProyecto, id_estado_proyecto=id_estado_proyecto)
    
    if request.method == 'POST':
        nombre = estado.nombre_estado
        try:
            estado.delete()
            messages.success(request, f'✅ Estado "{nombre}" eliminado.')
            return redirect('proyectos:estado_proyecto_list')
        except Exception as e:
            messages.error(request, f'❌ No se puede eliminar. Tiene proyectos asociados.')
            return redirect('proyectos:estado_proyecto_list')
    
    context = {
        'estado': estado,
        'show_module_nav': True,
        'active_module': 'proyectos',
    }
    return render(request, 'proyectos/catalogos/estado_proyecto_confirm_delete.html', context)


# =====================================================
# FASE 1: VISTAS DE CATÁLOGOS - TIPO DOCUMENTO
# =====================================================

def tipo_documento_list(request):
    """Listado de tipos de documentos"""
    tipos = TipoDocumentoProyecto.objects.all().order_by('orden_visualizacion', 'nombre_tipo_documento')
    
    context = {
        'tipos': tipos,
        'show_module_nav': True,
        'active_module': 'proyectos',
    }
    return render(request, 'proyectos/catalogos/tipo_documento_list.html', context)


def tipo_documento_create(request):
    """Crear nuevo tipo de documento"""
    if request.method == 'POST':
        form = TipoDocumentoProyectoForm(request.POST)
        if form.is_valid():
            tipo = form.save()
            messages.success(request, f'✅ Tipo de documento "{tipo.nombre_tipo_documento}" creado.')
            return redirect('proyectos:tipo_documento_list')
    else:
        form = TipoDocumentoProyectoForm()
    
    context = {
        'form': form,
        'titulo': 'Nuevo Tipo de Documento',
        'show_module_nav': True,
        'active_module': 'proyectos',
    }
    return render(request, 'proyectos/catalogos/tipo_documento_form.html', context)


def tipo_documento_update(request, id_tipo_documento):
    """Editar tipo de documento"""
    tipo = get_object_or_404(TipoDocumentoProyecto, id_tipo_documento=id_tipo_documento)
    
    if request.method == 'POST':
        form = TipoDocumentoProyectoForm(request.POST, instance=tipo)
        if form.is_valid():
            tipo = form.save()
            messages.success(request, f'✅ Tipo de documento "{tipo.nombre_tipo_documento}" actualizado.')
            return redirect('proyectos:tipo_documento_list')
    else:
        form = TipoDocumentoProyectoForm(instance=tipo)
    
    context = {
        'form': form,
        'tipo': tipo,
        'titulo': 'Editar Tipo de Documento',
        'show_module_nav': True,
        'active_module': 'proyectos',
    }
    return render(request, 'proyectos/catalogos/tipo_documento_form.html', context)


def tipo_documento_delete(request, id_tipo_documento):
    """Eliminar tipo de documento"""
    tipo = get_object_or_404(TipoDocumentoProyecto, id_tipo_documento=id_tipo_documento)
    
    if request.method == 'POST':
        nombre = tipo.nombre_tipo_documento
        try:
            tipo.delete()
            messages.success(request, f'✅ Tipo de documento "{nombre}" eliminado.')
            return redirect('proyectos:tipo_documento_list')
        except Exception as e:
            messages.error(request, f'❌ No se puede eliminar. Tiene documentos asociados.')
            return redirect('proyectos:tipo_documento_list')
    
    context = {
        'tipo': tipo,
        'show_module_nav': True,
        'active_module': 'proyectos',
    }
    return render(request, 'proyectos/catalogos/tipo_documento_confirm_delete.html', context)


# =====================================================
# FASE 2: VISTAS DE CLIENTES
# =====================================================

def cliente_list(request):
    """Listado de clientes con búsqueda"""
    query = request.GET.get('q', '')
    clientes = Cliente.objects.all()
    
    if query:
        clientes = clientes.filter(
            Q(razon_social__icontains=query) |
            Q(nombre_comercial__icontains=query) |
            Q(numero_documento__icontains=query)
        )
    
    clientes = clientes.order_by('razon_social')
    
    # Paginación
    paginator = Paginator(clientes, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'query': query,
        'show_module_nav': True,
        'active_module': 'proyectos',
    }
    return render(request, 'proyectos/clientes/cliente_list.html', context)


def cliente_create(request):
    """Crear nuevo cliente"""
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save()
            messages.success(request, f'✅ Cliente "{cliente.razon_social}" creado exitosamente.')
            return redirect('proyectos:cliente_list')
    else:
        form = ClienteForm()
    
    context = {
        'form': form,
        'titulo': 'Registrar Nuevo Cliente',
        'action': 'Crear',
        'show_module_nav': True,
        'active_module': 'proyectos',
    }
    return render(request, 'proyectos/clientes/cliente_form.html', context)


def cliente_update(request, id_cliente):
    """Editar cliente"""
    cliente = get_object_or_404(Cliente, id_cliente=id_cliente)
    
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            cliente = form.save()
            messages.success(request, f'✅ Cliente "{cliente.razon_social}" actualizado.')
            return redirect('proyectos:cliente_detail', id_cliente=cliente.id_cliente)
    else:
        form = ClienteForm(instance=cliente)
    
    context = {
        'form': form,
        'cliente': cliente,
        'titulo': 'Editar Cliente',
        'action': 'Actualizar',
        'show_module_nav': True,
        'active_module': 'proyectos',
    }
    return render(request, 'proyectos/clientes/cliente_form.html', context)


def cliente_detail(request, id_cliente):
    """Vista detalle del cliente"""
    cliente = get_object_or_404(Cliente, id_cliente=id_cliente)
    proyectos_activos = cliente.get_proyectos_activos()
    total_proyectos = cliente.get_total_proyectos()
    
    context = {
        'cliente': cliente,
        'proyectos_activos': proyectos_activos,
        'total_proyectos': total_proyectos,
        'show_module_nav': True,
        'active_module': 'proyectos',
    }
    return render(request, 'proyectos/clientes/cliente_detail.html', context)


def cliente_delete(request, id_cliente):
    """Eliminar cliente"""
    cliente = get_object_or_404(Cliente, id_cliente=id_cliente)
    
    if request.method == 'POST':
        razon_social = cliente.razon_social
        try:
            cliente.delete()
            messages.success(request, f'✅ Cliente "{razon_social}" eliminado.')
            return redirect('proyectos:cliente_list')
        except Exception as e:
            messages.error(request, f'❌ No se puede eliminar. Tiene proyectos asociados.')
            return redirect('proyectos:cliente_detail', id_cliente=id_cliente)
    
    context = {
        'cliente': cliente,
        'show_module_nav': True,
        'active_module': 'proyectos',
    }
    return render(request, 'proyectos/clientes/cliente_confirm_delete.html', context)


# =====================================================
# FASE 3: VISTAS DE PROYECTOS
# =====================================================

def proyecto_list(request):
    """Listado de proyectos con búsqueda y filtros"""
    query = request.GET.get('q', '')
    estado_filtro = request.GET.get('estado', '')
    tipo_filtro = request.GET.get('tipo', '')
    cliente_filtro = request.GET.get('cliente', '')
    
    proyectos = Proyecto.objects.select_related(
        'cliente', 'tipo_proyecto', 'estado_proyecto'
    ).all()
    
    # Filtros
    if query:
        proyectos = proyectos.filter(
            Q(codigo_proyecto__icontains=query) |
            Q(nombre_proyecto__icontains=query) |
            Q(cliente__razon_social__icontains=query)
        )
    
    if estado_filtro:
        proyectos = proyectos.filter(estado_proyecto_id=estado_filtro)
    
    if tipo_filtro:
        proyectos = proyectos.filter(tipo_proyecto_id=tipo_filtro)
    
    if cliente_filtro:
        proyectos = proyectos.filter(cliente_id=cliente_filtro)
    
    proyectos = proyectos.order_by('-fecha_registro')
    
    # Paginación
    paginator = Paginator(proyectos, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Para los selects de filtro
    estados = EstadoProyecto.objects.filter(activo=True)
    tipos = TipoProyecto.objects.filter(activo=True)
    clientes = Cliente.objects.filter(activo=True)
    
    context = {
        'page_obj': page_obj,
        'query': query,
        'estados': estados,
        'tipos': tipos,
        'clientes': clientes,
        'estado_filtro': estado_filtro,
        'tipo_filtro': tipo_filtro,
        'cliente_filtro': cliente_filtro,
        'show_module_nav': True,
        'active_module': 'proyectos',
    }
    return render(request, 'proyectos/proyectos/proyecto_list.html', context)


def proyecto_create(request):
    """Crear nuevo proyecto"""
    if request.method == 'POST':
        form = ProyectoForm(request.POST)
        if form.is_valid():
            proyecto = form.save()
            messages.success(request, f'✅ Proyecto "{proyecto.codigo_proyecto}" creado exitosamente.')
            return redirect('proyectos:proyecto_detail', id_proyecto=proyecto.id_proyecto)
    else:
        form = ProyectoForm()
    
    context = {
        'form': form,
        'titulo': 'Nuevo Proyecto',
        'action': 'Crear',
        'show_module_nav': True,
        'active_module': 'proyectos',
    }
    return render(request, 'proyectos/proyectos/proyecto_form.html', context)


def proyecto_update(request, id_proyecto):
    """Editar proyecto"""
    proyecto = get_object_or_404(Proyecto, id_proyecto=id_proyecto)
    
    if request.method == 'POST':
        form = ProyectoForm(request.POST, instance=proyecto)
        if form.is_valid():
            proyecto = form.save()
            messages.success(request, f'✅ Proyecto "{proyecto.codigo_proyecto}" actualizado.')
            return redirect('proyectos:proyecto_detail', id_proyecto=proyecto.id_proyecto)
    else:
        form = ProyectoForm(instance=proyecto)
    
    context = {
        'form': form,
        'proyecto': proyecto,
        'titulo': 'Editar Proyecto',
        'action': 'Actualizar',
        'show_module_nav': True,
        'active_module': 'proyectos',
    }
    return render(request, 'proyectos/proyectos/proyecto_form.html', context)


def proyecto_detail(request, id_proyecto):
    """Vista detalle del proyecto tipo dashboard"""
    proyecto = get_object_or_404(
        Proyecto.objects.select_related(
            'cliente', 'tipo_proyecto', 'estado_proyecto'
        ),
        id_proyecto=id_proyecto
    )
    
    # Obtener datos relacionados
    actividades = proyecto.actividades.filter(activo=True).order_by('orden_visualizacion', 'numero_actividad')
    trabajadores = proyecto.asignaciones.filter(activo=True).select_related('trabajador')
    documentos = proyecto.documentos.filter(activo=True).order_by('-fecha_carga')[:5]
    evidencias = proyecto.evidencias.filter(activo=True).order_by('-fecha_captura')[:6]
    
    context = {
        'proyecto': proyecto,
        'actividades': actividades,
        'trabajadores': trabajadores,
        'documentos': documentos,
        'evidencias': evidencias,
        'show_module_nav': True,
        'active_module': 'proyectos',
    }
    return render(request, 'proyectos/proyectos/proyecto_detail.html', context)


def proyecto_delete(request, id_proyecto):
    """Eliminar proyecto"""
    proyecto = get_object_or_404(Proyecto, id_proyecto=id_proyecto)
    
    if request.method == 'POST':
        codigo = proyecto.codigo_proyecto
        try:
            proyecto.delete()
            messages.success(request, f'✅ Proyecto "{codigo}" eliminado.')
            return redirect('proyectos:proyecto_list')
        except Exception as e:
            messages.error(request, f'❌ Error al eliminar el proyecto: {str(e)}')
            return redirect('proyectos:proyecto_detail', id_proyecto=id_proyecto)
    
    context = {
        'proyecto': proyecto,
        'show_module_nav': True,
        'active_module': 'proyectos',
    }
    return render(request, 'proyectos/proyectos/proyecto_confirm_delete.html', context)

# =====================================================
# FASE 4: VISTAS DE ACTIVIDADES
# =====================================================

def actividad_list(request, id_proyecto):
    """
    Listado de actividades de un proyecto con soporte de jerarquía padre-hijo.
    Solo muestra actividades padre (las que no tienen actividad_padre) y sus hijas.
    """
    proyecto = get_object_or_404(Proyecto, id_proyecto=id_proyecto)
    
    # Obtener solo las actividades padre (las que no tienen padre)
    actividades_padre = proyecto.actividades.filter(
        activo=True,
        actividad_padre__isnull=True
    ).order_by('orden_visualizacion', 'numero_actividad')
    
    # Construir lista jerárquica
    actividades_jerarquicas = []
    for padre in actividades_padre:
        actividades_jerarquicas.append({
            'actividad': padre,
            'es_padre': padre.es_actividad_padre(),
            'nivel': 0,
        })
        
        # Agregar hijas si existen
        if padre.es_actividad_padre():
            hijas = padre.get_actividades_hijas()
            for hija in hijas:
                actividades_jerarquicas.append({
                    'actividad': hija,
                    'es_padre': False,
                    'nivel': 1,
                })
    
    context = {
        'proyecto': proyecto,
        'actividades': actividades_jerarquicas,  # Lista jerárquica
        'show_module_nav': True,
        'active_module': 'proyectos',
    }
    return render(request, 'proyectos/actividades/actividad_list.html', context)

def actividad_create(request, id_proyecto):
    """Crear nueva actividad"""
    proyecto = get_object_or_404(Proyecto, id_proyecto=id_proyecto)
    
    if request.method == 'POST':
        # ✅ CORRECCIÓN: Pasar proyecto=proyecto al formulario
        form = ActividadForm(request.POST, proyecto=proyecto)
        if form.is_valid():
            actividad = form.save()
            messages.success(request, f'✅ Actividad "{actividad.numero_actividad}" creada.')
            return redirect('proyectos:actividad_list', id_proyecto=proyecto.id_proyecto)
    else:
        # ✅ CORRECCIÓN: Pasar proyecto=proyecto al formulario
        form = ActividadForm(initial={'proyecto': proyecto}, proyecto=proyecto)
    
    context = {
        'form': form,
        'proyecto': proyecto,
        'titulo': 'Nueva Actividad',
        'show_module_nav': True,
        'active_module': 'proyectos',
    }
    return render(request, 'proyectos/actividades/actividad_form.html', context)


# =====================================================
# ACTIVIDAD UPDATE - CORREGIDA
# =====================================================

def actividad_update(request, id_actividad):
    """Editar actividad"""
    actividad = get_object_or_404(Actividad, id_actividad=id_actividad)
    proyecto = actividad.proyecto
    
    if request.method == 'POST':
        # ✅ CORRECCIÓN: Pasar proyecto=proyecto al formulario
        form = ActividadForm(request.POST, instance=actividad, proyecto=proyecto)
        if form.is_valid():
            actividad = form.save()
            messages.success(request, f'✅ Actividad "{actividad.numero_actividad}" actualizada.')
            return redirect('proyectos:actividad_list', id_proyecto=proyecto.id_proyecto)
    else:
        # ✅ CORRECCIÓN: Pasar proyecto=proyecto al formulario
        form = ActividadForm(instance=actividad, proyecto=proyecto)
    
    context = {
        'form': form,
        'actividad': actividad,
        'proyecto': proyecto,
        'titulo': 'Editar Actividad',
        'show_module_nav': True,
        'active_module': 'proyectos',
    }
    return render(request, 'proyectos/actividades/actividad_form.html', context)



def actividad_delete(request, id_actividad):
    """Eliminar actividad"""
    actividad = get_object_or_404(Actividad, id_actividad=id_actividad)
    proyecto = actividad.proyecto
    
    if request.method == 'POST':
        numero = actividad.numero_actividad
        actividad.delete()
        messages.success(request, f'✅ Actividad "{numero}" eliminada.')
        return redirect('proyectos:actividad_list', id_proyecto=proyecto.id_proyecto)
    
    context = {
        'actividad': actividad,
        'proyecto': proyecto,
        'show_module_nav': True,
        'active_module': 'proyectos',
    }
    return render(request, 'proyectos/actividades/actividad_confirm_delete.html', context)

# ====
# FASE 4.1: VISTAS DE AVANCES DE ACTIVIDADES
# ====

def avance_list(request, id_actividad):
    """Listado de avances de una actividad"""
    actividad = get_object_or_404(Actividad, id_actividad=id_actividad)
    proyecto = actividad.proyecto

    avances = actividad.avances.all()  # gracias a related_name='avances'
    
    context = {
        'proyecto': proyecto,
        'actividad': actividad,
        'avances': avances,
        'show_module_nav': True,
        'active_module': 'proyectos',
    }
    return render(request, 'proyectos/actividades/avance_list.html', context)


def avance_create(request, id_actividad):
    """Registrar un nuevo avance de actividad"""
    actividad = get_object_or_404(Actividad, id_actividad=id_actividad)
    proyecto = actividad.proyecto

    if request.method == 'POST':
        form = AvanceActividadForm(request.POST, actividad=actividad)
        if form.is_valid():
            avance = form.save()
            messages.success(
                request,
                f'✅ Avance de {avance.cantidad_ejecutada} {actividad.unidad_medida} '
                f'registrado para la actividad "{actividad.numero_actividad}".'
            )
            # La actividad se recalcula en el save() del modelo AvanceActividad
            return redirect('proyectos:avance_list', id_actividad=actividad.id_actividad)
    else:
        form = AvanceActividadForm(
            actividad=actividad,
            initial={'fecha_avance': date.today()}
        )

    context = {
        'form': form,
        'proyecto': proyecto,
        'actividad': actividad,
        'titulo': 'Registrar Avance de Actividad',
        'show_module_nav': True,
        'active_module': 'proyectos',
    }
    return render(request, 'proyectos/actividades/avance_form.html', context)

def avance_update(request, id_avance):
    """Editar un avance de actividad"""
    avance = get_object_or_404(AvanceActividad, id_avance=id_avance)
    actividad = avance.actividad
    proyecto = actividad.proyecto

    if request.method == 'POST':
        form = AvanceActividadForm(request.POST, instance=avance, actividad=actividad)
        if form.is_valid():
            avance = form.save()
            messages.success(
                request,
                f'✅ Avance actualizado para la actividad "{actividad.numero_actividad}".'
            )
            # Se recalcula en save()
            return redirect('proyectos:avance_list', id_actividad=actividad.id_actividad)
    else:
        form = AvanceActividadForm(instance=avance, actividad=actividad)

    context = {
        'form': form,
        'avance': avance,
        'actividad': actividad,
        'proyecto': proyecto,
        'titulo': 'Editar Avance de Actividad',
        'show_module_nav': True,
        'active_module': 'proyectos',
    }
    return render(request, 'proyectos/actividades/avance_form.html', context)


def avance_delete(request, id_avance):
    """Eliminar un avance de actividad"""
    avance = get_object_or_404(AvanceActividad, id_avance=id_avance)
    actividad = avance.actividad
    proyecto = actividad.proyecto

    if request.method == 'POST':
        cantidad = avance.cantidad_ejecutada
        avance.delete()  # recalcula en delete()
        messages.success(
            request,
            f'✅ Avance de {cantidad} {actividad.unidad_medida} eliminado '
            f'de la actividad "{actividad.numero_actividad}".'
        )
        return redirect('proyectos:avance_list', id_actividad=actividad.id_actividad)

    context = {
        'avance': avance,
        'actividad': actividad,
        'proyecto': proyecto,
        'show_module_nav': True,
        'active_module': 'proyectos',
    }
    return render(request, 'proyectos/actividades/avance_confirm_delete.html', context)

def proyecto_gantt_data(request, proyecto_id):
    """
    Devuelve los datos de las actividades de un proyecto
    en formato JSON para consumir desde un diagrama de Gantt.
    """
    proyecto = get_object_or_404(Proyecto, pk=proyecto_id)

    actividades = proyecto.actividades.filter(activo=True).order_by(
        'actividad_padre__id_actividad', 'orden_visualizacion', 'numero_actividad'
    )

    tasks = []
    for act in actividades:
        # Fechas: usa las estimadas como base. Si falta alguna, la dejamos en None.
        start = act.fecha_inicio_estimada
        end = act.fecha_fin_estimada

        # Algunas librerías de Gantt requieren end_date inclusive o exclusiva.
        # Por ahora devolvemos tal cual el campo de la BD.
        tasks.append({
            "id": act.id_actividad,
            "text": f"{act.numero_actividad} - {act.nombre_actividad}",
            "start_date": start.isoformat() if start else None,
            "end_date": end.isoformat() if end else None,
            "progress": float(act.porcentaje_avance or 0) / 100.0,
            "parent": act.actividad_padre.id_actividad if act.actividad_padre else 0,
            "open": True,  # para que las ramas aparezcan abiertas
        })

    return JsonResponse({
        "data": tasks,
    }, safe=False)

def proyecto_gantt_view(request, proyecto_id):
    """
    Renderiza la página del diagrama de Gantt para un proyecto.
    El JS en el template consumirá la vista JSON `proyecto_gantt_data`.
    """
    proyecto = get_object_or_404(Proyecto, pk=proyecto_id)
    return render(request, 'proyectos/proyecto_gantt.html', {
        'proyecto': proyecto,
    })

# =====================================================
# FASE 5: VISTAS DE ASIGNACIONES DE TRABAJADORES
# =====================================================

def asignacion_list(request, id_proyecto):
    """Listar trabajadores asignados a un proyecto con advertencias de multi-proyecto"""
    proyecto = get_object_or_404(Proyecto, id_proyecto=id_proyecto)

    asignaciones = AsignacionTrabajador.objects.filter(
        proyecto=proyecto
    ).select_related('trabajador', 'proyecto').order_by('-fecha_asignacion')

    # Calcular advertencia de multi-proyecto para cada asignación
    for asignacion in asignaciones:
        trabajador = asignacion.trabajador
        fecha_asignacion = asignacion.fecha_asignacion
        fecha_desasignacion = asignacion.fecha_desasignacion

        inicio_nuevo = fecha_asignacion
        fin_nuevo = fecha_desasignacion  # puede ser None

        # Otras asignaciones del mismo trabajador en otros proyectos
        otras_asignaciones = AsignacionTrabajador.objects.filter(
            trabajador=trabajador
        ).exclude(proyecto=proyecto).select_related('proyecto')

        proyectos_conflicto = set()
        for a in otras_asignaciones:
            inicio_otro = a.fecha_asignacion
            fin_otro = a.fecha_desasignacion

            # Lógica de solapamiento
            if fin_nuevo is None:
                # Esta asignación no tiene fin (sigue activa)
                if fin_otro is None or fin_otro >= inicio_nuevo:
                    proyectos_conflicto.add(a.proyecto)
            else:
                # Esta asignación tiene fin
                if fin_otro is None:
                    # La otra no tiene fin
                    if inicio_otro <= fin_nuevo:
                        proyectos_conflicto.add(a.proyecto)
                else:
                    # Ambas tienen fin
                    if inicio_otro <= fin_nuevo and fin_otro >= inicio_nuevo:
                        proyectos_conflicto.add(a.proyecto)

        # Asignar advertencia como atributo del objeto
        if proyectos_conflicto:
            num_proyectos = len(proyectos_conflicto)
            codigos = ', '.join(p.codigo_proyecto for p in proyectos_conflicto)
            asignacion.alerta_multi_proyecto = (
                f'El trabajador se encuentra asignado a {num_proyectos} '
                f'otro(s) proyecto(s) en este período: {codigos}.'
            )
        else:
            asignacion.alerta_multi_proyecto = ''

    context = {
        'proyecto': proyecto,
        'asignaciones': asignaciones,
        'show_module_nav': True,
        'active_module': 'proyectos',
    }
    return render(request, 'proyectos/asignaciones/asignacion_list.html', context)
    
def asignacion_create(request, id_proyecto):
    """Asignar trabajador a proyecto con buscador de trabajadores"""
    proyecto = get_object_or_404(Proyecto, id_proyecto=id_proyecto)

    query = request.GET.get('q', '').strip()

    trabajadores_qs = TrabajadorPersonal.objects.all()
    if query:
        trabajadores_qs = trabajadores_qs.filter(
            Q(id_trabajador__icontains=query) |
            Q(nombres__icontains=query) |
            Q(apellidos__icontains=query)
        )

    total_trabajadores = trabajadores_qs.count()

    if request.method == 'POST':
        form = AsignacionTrabajadorForm(
            request.POST,
            proyecto=proyecto,
            trabajadores_qs=trabajadores_qs
        )
        if form.is_valid():
            asignacion = form.save(commit=False)
            asignacion.proyecto = proyecto

            trabajador = asignacion.trabajador
            fecha_asignacion = asignacion.fecha_asignacion
            fecha_desasignacion = asignacion.fecha_desasignacion

            # Buscar otras asignaciones del mismo trabajador en otros proyectos
            otras_asignaciones = AsignacionTrabajador.objects.filter(
                trabajador=trabajador
            ).exclude(proyecto=proyecto)

            # Filtrar solo las que se solapan en fechas
            inicio_nuevo = fecha_asignacion
            fin_nuevo = fecha_desasignacion  # puede ser None

            proyectos_conflicto = set()
            for a in otras_asignaciones:
                inicio_otro = a.fecha_asignacion
                fin_otro = a.fecha_desasignacion

                if fin_nuevo is None:
                    # Esta asignación no tiene fin
                    if fin_otro is None or fin_otro >= inicio_nuevo:
                        proyectos_conflicto.add(a.proyecto)
                else:
                    # Esta asignación tiene fin
                    if fin_otro is None:
                        if inicio_otro <= fin_nuevo:
                            proyectos_conflicto.add(a.proyecto)
                    else:
                        if inicio_otro <= fin_nuevo and fin_otro >= inicio_nuevo:
                            proyectos_conflicto.add(a.proyecto)

            # Si hay conflictos, mostramos advertencia
            num_proyectos_conflicto = len(proyectos_conflicto)
            if num_proyectos_conflicto > 0:
                nombres_proyectos = ', '.join(
                    f'{p.codigo_proyecto}' for p in proyectos_conflicto
                )
                messages.warning(
                    request,
                    f'⚠️ El trabajador ya se encuentra asignado a {num_proyectos_conflicto} '
                    f'otro(s) proyecto(s) en este período: {nombres_proyectos}.'
                )

            asignacion.save()
            messages.success(request, '✅ Trabajador asignado al proyecto.')
            return redirect('proyectos:asignacion_list', id_proyecto=proyecto.id_proyecto)
    else:
        form = AsignacionTrabajadorForm(
            proyecto=proyecto,
            trabajadores_qs=trabajadores_qs
        )

    context = {
        'form': form,
        'proyecto': proyecto,
        'titulo': 'Asignar Trabajador',
        'query': query,
        'total_trabajadores': total_trabajadores,
        'show_module_nav': True,
        'active_module': 'proyectos',
    }
    return render(request, 'proyectos/asignaciones/asignacion_form.html', context)
    
def asignacion_update(request, id_asignacion):
    """Editar asignación de trabajador"""
    asignacion = get_object_or_404(AsignacionTrabajador, id_asignacion=id_asignacion)
    proyecto = asignacion.proyecto
    
    if request.method == 'POST':
        form = AsignacionTrabajadorForm(request.POST, instance=asignacion)
        if form.is_valid():
            asignacion = form.save()
            messages.success(request, f'✅ Asignación actualizada.')
            return redirect('proyectos:asignacion_list', id_proyecto=proyecto.id_proyecto)
    else:
        form = AsignacionTrabajadorForm(instance=asignacion)
    
    context = {
        'form': form,
        'asignacion': asignacion,
        'proyecto': proyecto,
        'titulo': 'Editar Asignación',
        'show_module_nav': True,
        'active_module': 'proyectos',
    }
    return render(request, 'proyectos/asignaciones/asignacion_form.html', context)


def asignacion_delete(request, id_asignacion):
    """Eliminar asignación de trabajador"""
    asignacion = get_object_or_404(AsignacionTrabajador, id_asignacion=id_asignacion)
    proyecto = asignacion.proyecto
    
    if request.method == 'POST':
        asignacion.delete()
        messages.success(request, f'✅ Asignación eliminada.')
        return redirect('proyectos:asignacion_list', id_proyecto=proyecto.id_proyecto)
    
    context = {
        'asignacion': asignacion,
        'proyecto': proyecto,
        'show_module_nav': True,
        'active_module': 'proyectos',
    }
    return render(request, 'proyectos/asignaciones/asignacion_confirm_delete.html', context)


# =====================================================
# FASE 6: VISTAS DE DOCUMENTOS
# =====================================================

def documento_list(request, id_proyecto):
    """Listado de documentos de un proyecto"""
    proyecto = get_object_or_404(Proyecto, id_proyecto=id_proyecto)
    documentos = proyecto.documentos.filter(activo=True).order_by('-fecha_carga')
    
    context = {
        'proyecto': proyecto,
        'documentos': documentos,
        'show_module_nav': True,
        'active_module': 'proyectos',
    }
    return render(request, 'proyectos/documentos/documento_list.html', context)


def documento_create(request, id_proyecto):
    """Subir nuevo documento"""
    proyecto = get_object_or_404(Proyecto, id_proyecto=id_proyecto)
    
    if request.method == 'POST':
        form = DocumentoProyectoForm(request.POST, request.FILES)
        if form.is_valid():
            documento = form.save()
            messages.success(request, f'✅ Documento "{documento.nombre_documento}" subido.')
            return redirect('proyectos:documento_list', id_proyecto=proyecto.id_proyecto)
    else:
        form = DocumentoProyectoForm(initial={'proyecto': proyecto})
    
    context = {
        'form': form,
        'proyecto': proyecto,
        'titulo': 'Subir Documento',
        'show_module_nav': True,
        'active_module': 'proyectos',
    }
    return render(request, 'proyectos/documentos/documento_form.html', context)


def documento_delete(request, id_documento):
    """Eliminar documento"""
    documento = get_object_or_404(DocumentoProyecto, id_documento=id_documento)
    proyecto = documento.proyecto
    
    if request.method == 'POST':
        nombre = documento.nombre_documento
        documento.delete()
        messages.success(request, f'✅ Documento "{nombre}" eliminado.')
        return redirect('proyectos:documento_list', id_proyecto=proyecto.id_proyecto)
    
    context = {
        'documento': documento,
        'proyecto': proyecto,
        'show_module_nav': True,
        'active_module': 'proyectos',
    }
    return render(request, 'proyectos/documentos/documento_confirm_delete.html', context)


# =====================================================
# FASE 7: VISTAS DE EVIDENCIAS FOTOGRÁFICAS
# =====================================================

def evidencia_list(request, id_proyecto):
    """Listado de evidencias fotográficas"""
    proyecto = get_object_or_404(Proyecto, id_proyecto=id_proyecto)
    evidencias = proyecto.evidencias.filter(activo=True).order_by('-fecha_captura')
    
    context = {
        'proyecto': proyecto,
        'evidencias': evidencias,
        'show_module_nav': True,
        'active_module': 'proyectos',
    }
    return render(request, 'proyectos/evidencias/evidencia_list.html', context)


def evidencia_create(request, id_proyecto):
    """Subir nueva evidencia fotográfica"""
    proyecto = get_object_or_404(Proyecto, id_proyecto=id_proyecto)
    
    if request.method == 'POST':
        form = EvidenciaFotograficaForm(request.POST, request.FILES)
        if form.is_valid():
            evidencia = form.save()
            messages.success(request, f'✅ Evidencia "{evidencia.titulo}" subida.')
            return redirect('proyectos:evidencia_list', id_proyecto=proyecto.id_proyecto)
    else:
        form = EvidenciaFotograficaForm(initial={'proyecto': proyecto})
    
    context = {
        'form': form,
        'proyecto': proyecto,
        'titulo': 'Subir Evidencia Fotográfica',
        'show_module_nav': True,
        'active_module': 'proyectos',
    }
    return render(request, 'proyectos/evidencias/evidencia_form.html', context)


def evidencia_delete(request, id_evidencia):
    """Eliminar evidencia fotográfica"""
    evidencia = get_object_or_404(EvidenciaFotografica, id_evidencia=id_evidencia)
    proyecto = evidencia.proyecto
    
    if request.method == 'POST':
        titulo = evidencia.titulo
        evidencia.delete()
        messages.success(request, f'✅ Evidencia "{titulo}" eliminada.')
        return redirect('proyectos:evidencia_list', id_proyecto=proyecto.id_proyecto)
    
    context = {
        'evidencia': evidencia,
        'proyecto': proyecto,
        'show_module_nav': True,
        'active_module': 'proyectos',
    }
    return render(request, 'proyectos/evidencias/evidencia_confirm_delete.html', context)

@login_required
def proyecto_gantt_view(request, proyecto_id):
    """
    Vista principal del diagrama de Gantt
    Renderiza el template con el proyecto y permisos
    """
    proyecto = get_object_or_404(Proyecto, id_proyecto=proyecto_id)
    
    # Determinar si el usuario puede editar
    # Ajusta esta lógica según tus reglas de negocio
    puede_editar = request.user.is_staff or request.user.is_superuser
    # O si tienes un sistema de permisos más específico:
    # puede_editar = request.user.has_perm('proyectos.change_actividad')
    
    context = {
        'proyecto': proyecto,
        'puede_editar': puede_editar,
    }
    
    return render(request, 'proyectos/proyecto_gantt_completo.html', context)


@login_required
def proyecto_gantt_data(request, proyecto_id):
    """
    Endpoint JSON que devuelve los datos del proyecto en formato dhtmlxGantt
    """
    proyecto = get_object_or_404(Proyecto, id_proyecto=proyecto_id)
    
    # Obtener todas las actividades del proyecto
    actividades = Actividad.objects.filter(
        proyecto=proyecto
    ).select_related('actividad_padre').order_by('fecha_inicio')
    
    # Construir estructura de datos para dhtmlxGantt
    data = []
    
    for actividad in actividades:
        # Determinar estado
        estado = determinar_estado_actividad(actividad)
        
        # Calcular progreso (asumiendo que tienes un campo de avance)
        # Si no tienes este campo, ajusta según tu modelo
        progreso = getattr(actividad, 'porcentaje_avance', 0) / 100.0
        
        task_data = {
            'id': actividad.id_actividad,
            'text': actividad.nombre_actividad,
            'start_date': actividad.fecha_inicio.strftime('%Y-%m-%d'),
            'duration': calcular_duracion_dias(actividad.fecha_inicio, actividad.fecha_fin),
            'progress': progreso,
            'open': True,  # Expandir por defecto
            'estado': estado,  # Para los colores
        }
        
        # Si tiene actividad padre
        if actividad.actividad_padre:
            task_data['parent'] = actividad.actividad_padre.id_actividad
        
        data.append(task_data)
    
    # dhtmlxGantt espera un objeto con 'data'
    response_data = {
        'data': data
    }
    
    return JsonResponse(response_data, safe=False)

def proyecto_gantt_view(request, proyecto_id):
    """Vista principal del diagrama de Gantt"""
    proyecto = get_object_or_404(Proyecto, id_proyecto=proyecto_id)
    
    # Sin login: todos pueden editar (temporal)
    puede_editar = True
    
    context = {
        'proyecto': proyecto,
        'puede_editar': puede_editar,
    }
    
    return render(request, 'proyectos/proyecto_gantt_completo.html', context)


def proyecto_gantt_data(request, proyecto_id):
    """Endpoint JSON con datos del Gantt"""
    proyecto = get_object_or_404(Proyecto, id_proyecto=proyecto_id)
    
    actividades = Actividad.objects.filter(
        proyecto=proyecto,
        activo=True
    ).select_related('actividad_padre').order_by('orden_visualizacion', 'numero_actividad')
    
    data = []
    
    for actividad in actividades:
        # Determinar estado automáticamente
        estado = determinar_estado_actividad(actividad)
        
        # Convertir porcentaje a decimal (0.0 a 1.0)
        progreso = float(actividad.porcentaje_avance) / 100.0 if actividad.porcentaje_avance else 0.0
        
        # Usar fechas estimadas
        fecha_inicio = actividad.fecha_inicio_estimada
        fecha_fin = actividad.fecha_fin_estimada
        
        # Fallback a fechas reales si no hay estimadas
        if not fecha_inicio:
            fecha_inicio = actividad.fecha_inicio_real
        if not fecha_fin:
            fecha_fin = actividad.fecha_fin_real
            
        # Fallback a fecha del proyecto
        if not fecha_inicio and proyecto.fecha_inicio:
            fecha_inicio = proyecto.fecha_inicio
        if not fecha_fin and fecha_inicio:
            fecha_fin = fecha_inicio + timedelta(days=7)
        
        # Último fallback: hoy
        if not fecha_inicio:
            fecha_inicio = datetime.now().date()
            fecha_fin = fecha_inicio + timedelta(days=7)
        
        # Calcular duración
        duracion = calcular_duracion_dias(fecha_inicio, fecha_fin)
        
        task_data = {
            'id': actividad.id_actividad,
            'text': f"{actividad.numero_actividad} - {actividad.nombre_actividad}",
            'start_date': fecha_inicio.strftime('%Y-%m-%d'),
            'duration': duracion,
            'progress': progreso,
            'open': True,
            'estado': estado,
        }
        
        # Agregar padre si existe
        if actividad.actividad_padre:
            task_data['parent'] = actividad.actividad_padre.id_actividad
        
        data.append(task_data)
    
    return JsonResponse({'data': data}, safe=False)


@require_http_methods(["POST"])
@csrf_exempt  # Temporal: sin CSRF hasta implementar login
def proyecto_gantt_save(request, proyecto_id):
    """Endpoint para guardar cambios del Gantt"""
    proyecto = get_object_or_404(Proyecto, id_proyecto=proyecto_id)
    
    try:
        data = json.loads(request.body)
        
        actividad_id = data.get('id')
        actividad = get_object_or_404(
            Actividad, 
            id_actividad=actividad_id, 
            proyecto=proyecto
        )
        
        # Actualizar nombre si cambió
        if 'text' in data:
            text = data['text']
            if ' - ' in text:
                _, nombre = text.split(' - ', 1)
                actividad.nombre_actividad = nombre
        
        # Guardar en fechas estimadas
        if 'start_date' in data:
            actividad.fecha_inicio_estimada = datetime.strptime(
                data['start_date'], 
                '%Y-%m-%d'
            ).date()
        
        if 'duration' in data and 'start_date' in data:
            fecha_inicio = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
            duracion_dias = int(data['duration'])
            actividad.fecha_fin_estimada = fecha_inicio + timedelta(days=duracion_dias)
        
        # Actualizar progreso si cambió
        if 'progress' in data:
            actividad.porcentaje_avance = data['progress'] * 100
        
        actividad.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Actividad actualizada correctamente'
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Datos JSON inválidos'
        }, status=400)
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


def determinar_estado_actividad(actividad):
    """Determina el estado automáticamente"""
    hoy = datetime.now().date()
    
    fecha_inicio = actividad.fecha_inicio_estimada or actividad.fecha_inicio_real
    fecha_fin = actividad.fecha_fin_estimada or actividad.fecha_fin_real
    
    if not fecha_inicio or not fecha_fin:
        return 'planificado'
    
    porcentaje = float(actividad.porcentaje_avance or 0)
    
    if porcentaje >= 100:
        return 'completado'
    
    if fecha_fin < hoy and porcentaje < 100:
        return 'retrasado'
    
    if fecha_inicio <= hoy <= fecha_fin:
        return 'en-curso'
    
    if fecha_inicio > hoy:
        return 'planificado'
    
    return 'planificado'


def calcular_duracion_dias(fecha_inicio, fecha_fin):
    """Calcula la duración en días entre dos fechas"""
    if not fecha_inicio or not fecha_fin:
        return 1
    
    delta = fecha_fin - fecha_inicio
    return max(delta.days, 1)
