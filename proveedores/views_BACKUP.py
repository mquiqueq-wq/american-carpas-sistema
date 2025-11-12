from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db import models  # Para usar Q
from .models import TipoProveedor, CategoriaProveedor, TipoDocumentoProveedor
from .forms import TipoProveedorForm, CategoriaProveedorForm, TipoDocumentoProveedorForm


# =====================================================
# PÁGINA DE INICIO DEL MÓDULO
# =====================================================

def home_proveedores(request):
    """Página principal del módulo de proveedores con menú de iconos"""
    context = {
        'total_tipos': TipoProveedor.objects.filter(activo=True).count(),
        'total_categorias': CategoriaProveedor.objects.filter(activo=True).count(),
        'total_tipos_documentos': TipoDocumentoProveedor.objects.filter(activo=True).count(),
        'show_module_nav': True,
        'active_module': 'proveedores'
    }
    return render(request, 'proveedores/home_proveedores.html', context)


# =====================================================
# GESTIÓN DE TIPOS DE PROVEEDORES
# =====================================================

def tipo_proveedor_list(request):
    """Listado de tipos de proveedores con búsqueda y paginación"""
    query = request.GET.get('q', '')
    tipos = TipoProveedor.objects.all()
    
    if query:
        tipos = tipos.filter(nombre_tipo__icontains=query)
    
    tipos = tipos.order_by('orden_visualizacion', 'nombre_tipo')
    
    # Paginación
    paginator = Paginator(tipos, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'query': query,
        'show_module_nav': True,
        'active_module': 'proveedores',
    }
    return render(request, 'proveedores/catalogos/tipo_proveedor_list.html', context)


def tipo_proveedor_create(request):
    """Crear nuevo tipo de proveedor"""
    if request.method == 'POST':
        form = TipoProveedorForm(request.POST)
        if form.is_valid():
            tipo = form.save()
            messages.success(request, f'✅ Tipo de proveedor "{tipo.nombre_tipo}" creado exitosamente.')
            return redirect('proveedores:tipo_proveedor_list')
    else:
        form = TipoProveedorForm()
    
    context = {
        'form': form,
        'titulo': 'Crear Tipo de Proveedor',
        'action': 'Crear',
        'show_module_nav': True,
        'active_module': 'proveedores',
    }
    return render(request, 'proveedores/catalogos/tipo_proveedor_form.html', context)


def tipo_proveedor_update(request, id_tipo_proveedor):
    """Editar tipo de proveedor existente"""
    tipo = get_object_or_404(TipoProveedor, id_tipo_proveedor=id_tipo_proveedor)
    
    if request.method == 'POST':
        form = TipoProveedorForm(request.POST, instance=tipo)
        if form.is_valid():
            tipo = form.save()
            messages.success(request, f'✅ Tipo de proveedor "{tipo.nombre_tipo}" actualizado exitosamente.')
            return redirect('proveedores:tipo_proveedor_list')
    else:
        form = TipoProveedorForm(instance=tipo)
    
    context = {
        'form': form,
        'tipo': tipo,
        'titulo': 'Editar Tipo de Proveedor',
        'action': 'Actualizar',
        'show_module_nav': True,
        'active_module': 'proveedores',
    }
    return render(request, 'proveedores/catalogos/tipo_proveedor_form.html', context)


def tipo_proveedor_delete(request, id_tipo_proveedor):
    """Eliminar tipo de proveedor"""
    tipo = get_object_or_404(TipoProveedor, id_tipo_proveedor=id_tipo_proveedor)
    
    if request.method == 'POST':
        nombre = tipo.nombre_tipo
        tipo.delete()
        messages.success(request, f'🗑️ Tipo de proveedor "{nombre}" eliminado exitosamente.')
        return redirect('proveedores:tipo_proveedor_list')
    
    context = {
        'tipo': tipo,
        'show_module_nav': True,
        'active_module': 'proveedores'
    }
    return render(request, 'proveedores/catalogos/tipo_proveedor_confirm_delete.html', context)


# =====================================================
# GESTIÓN DE CATEGORÍAS DE PROVEEDORES
# =====================================================

def categoria_proveedor_list(request):
    """Listado de categorías con búsqueda y paginación"""
    query = request.GET.get('q', '')
    categorias = CategoriaProveedor.objects.all()
    
    if query:
        categorias = categorias.filter(nombre_categoria__icontains=query)
    
    categorias = categorias.order_by('orden_visualizacion', 'nombre_categoria')
    
    # Paginación
    paginator = Paginator(categorias, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'query': query,
        'show_module_nav': True,
        'active_module': 'proveedores'
    }
    return render(request, 'proveedores/catalogos/categoria_proveedor_list.html', context)


def categoria_proveedor_create(request):
    """Crear nueva categoría"""
    if request.method == 'POST':
        form = CategoriaProveedorForm(request.POST)
        if form.is_valid():
            categoria = form.save()
            messages.success(request, f'✅ Categoría "{categoria.nombre_categoria}" creada exitosamente.')
            return redirect('proveedores:categoria_proveedor_list')
    else:
        form = CategoriaProveedorForm()
    
    context = {
        'form': form,
        'titulo': 'Crear Categoría de Proveedor',
        'action': 'Crear',
        'show_module_nav': True,
        'active_module': 'proveedores',
    }
    return render(request, 'proveedores/catalogos/categoria_proveedor_form.html', context)


def categoria_proveedor_update(request, id_categoria):
    """Editar categoría existente"""
    categoria = get_object_or_404(CategoriaProveedor, id_categoria=id_categoria)
    
    if request.method == 'POST':
        form = CategoriaProveedorForm(request.POST, instance=categoria)
        if form.is_valid():
            categoria = form.save()
            messages.success(request, f'✅ Categoría "{categoria.nombre_categoria}" actualizada exitosamente.')
            return redirect('proveedores:categoria_proveedor_list')
    else:
        form = CategoriaProveedorForm(instance=categoria)
    
    context = {
        'form': form,
        'categoria': categoria,
        'titulo': 'Editar Categoría de Proveedor',
        'action': 'Actualizar',
        'show_module_nav': True,
        'active_module': 'proveedores',
    }
    return render(request, 'proveedores/catalogos/categoria_proveedor_form.html', context)


def categoria_proveedor_delete(request, id_categoria):
    """Eliminar categoría"""
    categoria = get_object_or_404(CategoriaProveedor, id_categoria=id_categoria)
    
    if request.method == 'POST':
        nombre = categoria.nombre_categoria
        categoria.delete()
        messages.success(request, f'🗑️ Categoría "{nombre}" eliminada exitosamente.')
        return redirect('proveedores:categoria_proveedor_list')
    
    context = {
        'categoria': categoria,
        'show_module_nav': True,
        'active_module': 'proveedores'
    }
    return render(request, 'proveedores/catalogos/categoria_proveedor_confirm_delete.html', context)


# =====================================================
# GESTIÓN DE TIPOS DE DOCUMENTOS
# =====================================================

def tipo_documento_list(request):
    """Listado de tipos de documentos con búsqueda y paginación"""
    query = request.GET.get('q', '')
    tipos = TipoDocumentoProveedor.objects.all()
    
    if query:
        tipos = tipos.filter(nombre_tipo_documento__icontains=query)
    
    tipos = tipos.order_by('orden_visualizacion', 'nombre_tipo_documento')
    
    # Paginación
    paginator = Paginator(tipos, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'query': query,
        'show_module_nav': True,
        'active_module': 'proveedores'
    }
    return render(request, 'proveedores/catalogos/tipo_documento_list.html', context)


def tipo_documento_create(request):
    """Crear nuevo tipo de documento"""
    if request.method == 'POST':
        form = TipoDocumentoProveedorForm(request.POST)
        if form.is_valid():
            tipo = form.save()
            messages.success(request, f'✅ Tipo de documento "{tipo.nombre_tipo_documento}" creado exitosamente.')
            return redirect('proveedores:tipo_documento_list')
    else:
        form = TipoDocumentoProveedorForm()
    
    context = {
        'form': form,
        'titulo': 'Crear Tipo de Documento',
        'action': 'Crear',
        'show_module_nav': True,
        'active_module': 'proveedores',
    }
    return render(request, 'proveedores/catalogos/tipo_documento_form.html', context)


def tipo_documento_update(request, id_tipo_documento):
    """Editar tipo de documento existente"""
    tipo = get_object_or_404(TipoDocumentoProveedor, id_tipo_documento=id_tipo_documento)
    
    if request.method == 'POST':
        form = TipoDocumentoProveedorForm(request.POST, instance=tipo)
        if form.is_valid():
            tipo = form.save()
            messages.success(request, f'✅ Tipo de documento "{tipo.nombre_tipo_documento}" actualizado exitosamente.')
            return redirect('proveedores:tipo_documento_list')
    else:
        form = TipoDocumentoProveedorForm(instance=tipo)
    
    context = {
        'form': form,
        'tipo': tipo,
        'titulo': 'Editar Tipo de Documento',
        'action': 'Actualizar',
        'show_module_nav': True,
        'active_module': 'proveedores',
    }
    return render(request, 'proveedores/catalogos/tipo_documento_form.html', context)


def tipo_documento_delete(request, id_tipo_documento):
    """Eliminar tipo de documento"""
    tipo = get_object_or_404(TipoDocumentoProveedor, id_tipo_documento=id_tipo_documento)
    
    if request.method == 'POST':
        nombre = tipo.nombre_tipo_documento
        tipo.delete()
        messages.success(request, f'🗑️ Tipo de documento "{nombre}" eliminado exitosamente.')
        return redirect('proveedores:tipo_documento_list')
    
    context = {
        'tipo': tipo,
        'show_module_nav': True,
        'active_module': 'proveedores',
    }
    return render(request, 'proveedores/catalogos/tipo_documento_confirm_delete.html', context)


# =====================================================
# CRUD PROVEEDORES - FASE 2
# =====================================================

from .models import Proveedor
from .forms import ProveedorForm


def proveedor_list(request):
    """Listado de proveedores con búsqueda y filtros"""
    query = request.GET.get('q', '')
    estado_filtro = request.GET.get('estado', '')
    tipo_filtro = request.GET.get('tipo', '')
    
    proveedores = Proveedor.objects.select_related(
        'tipo_proveedor', 'categoria_principal'
    ).all()
    
    # Filtros
    if query:
        proveedores = proveedores.filter(
            models.Q(razon_social__icontains=query) |
            models.Q(nombre_comercial__icontains=query) |
            models.Q(numero_documento__icontains=query)
        )
    
    if estado_filtro:
        proveedores = proveedores.filter(estado=estado_filtro)
    
    if tipo_filtro:
        proveedores = proveedores.filter(tipo_proveedor__id_tipo_proveedor=tipo_filtro)
    
    proveedores = proveedores.order_by('razon_social')
    
    # Paginación
    paginator = Paginator(proveedores, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Para los filtros
    from .models import TipoProveedor, ESTADO_PROVEEDOR_CHOICES
    tipos_proveedor = TipoProveedor.objects.filter(activo=True)
    
    context = {
        'page_obj': page_obj,
        'query': query,
        'estado_filtro': estado_filtro,
        'tipo_filtro': tipo_filtro,
        'tipos_proveedor': tipos_proveedor,
        'estados': ESTADO_PROVEEDOR_CHOICES,
        'show_module_nav': True,
        'active_module': 'proveedores'
    }
    return render(request, 'proveedores/proveedor_list.html', context)


def proveedor_detail(request, id_proveedor):
    """Detalle completo del proveedor"""
    proveedor = get_object_or_404(
        Proveedor.objects.select_related(
            'tipo_proveedor', 'categoria_principal'
        ).prefetch_related('contactos', 'documentos', 'productos_servicios'),
        id_proveedor=id_proveedor
    )
    
    # Actualizar estado de todos los documentos
    for doc in proveedor.documentos.all():
        doc.actualizar_estado()
        doc.save()
    
    context = {
        'proveedor': proveedor,
        'show_module_nav': True,
        'active_module': 'proveedores'
    }
    return render(request, 'proveedores/proveedor_detail.html', context)


def proveedor_create(request):
    """Crear nuevo proveedor"""
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            proveedor = form.save(commit=False)
            # Registrar quién creó el proveedor (puedes usar request.user si tienes auth)
            proveedor.registrado_por = 'Admin'  # O request.user.username
            proveedor.save()
            messages.success(
                request, 
                f'✅ Proveedor "{proveedor.razon_social}" creado exitosamente.'
            )
            return redirect('proveedores:proveedor_detail', id_proveedor=proveedor.id_proveedor)
    else:
        form = ProveedorForm()
    
    context = {
        'form': form,
        'titulo': 'Registrar Nuevo Proveedor',
        'action': 'Crear',
        'show_module_nav': True,
        'active_module': 'proveedores',
    }
    return render(request, 'proveedores/proveedor_form.html', context)


def proveedor_update(request, id_proveedor):
    """Editar proveedor existente"""
    proveedor = get_object_or_404(Proveedor, id_proveedor=id_proveedor)
    
    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            proveedor = form.save()
            messages.success(
                request, 
                f'✅ Proveedor "{proveedor.razon_social}" actualizado exitosamente.'
            )
            return redirect('proveedores:proveedor_detail', id_proveedor=proveedor.id_proveedor)
    else:
        form = ProveedorForm(instance=proveedor)
    
    context = {
        'form': form,
        'proveedor': proveedor,
        'titulo': 'Editar Proveedor',
        'action': 'Actualizar',
        'show_module_nav': True,
        'active_module': 'proveedores',
    }
    return render(request, 'proveedores/proveedor_form.html', context)


def proveedor_delete(request, id_proveedor):
    """Eliminar proveedor"""
    proveedor = get_object_or_404(Proveedor, id_proveedor=id_proveedor)
    
    if request.method == 'POST':
        razon_social = proveedor.razon_social
        proveedor.delete()
        messages.success(request, f'🗑️ Proveedor "{razon_social}" eliminado exitosamente.')
        return redirect('proveedores:proveedor_list')
    
    context = {
        'proveedor': proveedor,
        'show_module_nav': True,
        'active_module': 'proveedores',
    }
    return render(request, 'proveedores/proveedor_confirm_delete.html', context)


# =====================================================
# GESTIÓN DE CONTACTOS - FASE 3
# =====================================================

from .models import ContactoProveedor
from .forms import ContactoProveedorForm


def contacto_create(request, id_proveedor):
    """Crear nuevo contacto para un proveedor"""
    proveedor = get_object_or_404(Proveedor, id_proveedor=id_proveedor)
    
    if request.method == 'POST':
        form = ContactoProveedorForm(request.POST)
        if form.is_valid():
            contacto = form.save(commit=False)
            contacto.id_proveedor = proveedor
            contacto.save()
            messages.success(
                request,
                f'✅ Contacto "{contacto.nombre_completo}" agregado exitosamente.'
            )
            return redirect('proveedores:proveedor_detail', id_proveedor=proveedor.id_proveedor)
    else:
        form = ContactoProveedorForm(initial={'id_proveedor': proveedor})
    
    context = {
        'form': form,
        'proveedor': proveedor,
        'titulo': 'Agregar Contacto',
        'action': 'Guardar',
        'show_module_nav': True,
        'active_module': 'proveedores',
    }
    return render(request, 'proveedores/contacto_form.html', context)


def contacto_update(request, id_contacto):
    """Editar contacto existente"""
    contacto = get_object_or_404(ContactoProveedor, id_contacto=id_contacto)
    proveedor = contacto.id_proveedor
    
    if request.method == 'POST':
        form = ContactoProveedorForm(request.POST, instance=contacto)
        if form.is_valid():
            contacto = form.save()
            messages.success(
                request,
                f'✅ Contacto "{contacto.nombre_completo}" actualizado exitosamente.'
            )
            return redirect('proveedores:proveedor_detail', id_proveedor=proveedor.id_proveedor)
    else:
        form = ContactoProveedorForm(instance=contacto)
    
    context = {
        'form': form,
        'contacto': contacto,
        'proveedor': proveedor,
        'titulo': 'Editar Contacto',
        'action': 'Actualizar',
        'show_module_nav': True,
        'active_module': 'proveedores',
    }
    return render(request, 'proveedores/contacto_form.html', context)


def contacto_delete(request, id_contacto):
    """Eliminar contacto"""
    contacto = get_object_or_404(ContactoProveedor, id_contacto=id_contacto)
    proveedor = contacto.id_proveedor
    
    if request.method == 'POST':
        nombre = contacto.nombre_completo
        contacto.delete()
        messages.success(request, f'🗑️ Contacto "{nombre}" eliminado exitosamente.')
        return redirect('proveedores:proveedor_detail', id_proveedor=proveedor.id_proveedor)
    
    context = {
        'contacto': contacto,
        'proveedor': proveedor,
        'show_module_nav': True,
        'active_module': 'proveedores',
    }
    return render(request, 'proveedores/contacto_confirm_delete.html', context)


# =====================================================
# GESTIÓN DE DOCUMENTOS - FASE 4
# =====================================================

from .models import DocumentoProveedor
from .forms import DocumentoProveedorForm
from django.http import FileResponse, Http404


def documento_create(request, id_proveedor):
    """Cargar nuevo documento para un proveedor"""
    proveedor = get_object_or_404(Proveedor, id_proveedor=id_proveedor)
    
    if request.method == 'POST':
        form = DocumentoProveedorForm(request.POST, request.FILES, proveedor=proveedor)
        if form.is_valid():
            documento = form.save(commit=False)
            documento.id_proveedor = proveedor
            documento.cargado_por = 'Admin'  # O request.user.username si tienes auth
            documento.save()
            messages.success(
                request,
                f'✅ Documento "{documento.id_tipo_documento.nombre_tipo_documento}" cargado exitosamente.'
            )
            return redirect('proveedores:proveedor_detail', id_proveedor=proveedor.id_proveedor)
    else:
        form = DocumentoProveedorForm(proveedor=proveedor)
    
    context = {
        'form': form,
        'proveedor': proveedor,
        'titulo': 'Cargar Documento',
        'action': 'Guardar',
        'show_module_nav': True,
        'active_module': 'proveedores',
    }
    return render(request, 'proveedores/documento_form.html', context)


def documento_update(request, id_documento):
    """Editar información de un documento"""
    documento = get_object_or_404(DocumentoProveedor, id_documento=id_documento)
    proveedor = documento.id_proveedor
    
    if request.method == 'POST':
        form = DocumentoProveedorForm(
            request.POST, 
            request.FILES, 
            instance=documento,
            proveedor=proveedor
        )
        if form.is_valid():
            documento = form.save()
            messages.success(
                request,
                f'✅ Documento "{documento.id_tipo_documento.nombre_tipo_documento}" actualizado exitosamente.'
            )
            return redirect('proveedores:proveedor_detail', id_proveedor=proveedor.id_proveedor)
    else:
        form = DocumentoProveedorForm(instance=documento, proveedor=proveedor)
    
    context = {
        'form': form,
        'documento': documento,
        'proveedor': proveedor,
        'titulo': 'Editar Documento',
        'action': 'Actualizar',
        'show_module_nav': True,
        'active_module': 'proveedores',
    }
    return render(request, 'proveedores/documento_form.html', context)


def documento_delete(request, id_documento):
    """Eliminar documento"""
    documento = get_object_or_404(DocumentoProveedor, id_documento=id_documento)
    proveedor = documento.id_proveedor
    
    if request.method == 'POST':
        tipo = documento.id_tipo_documento.nombre_tipo_documento
        # Eliminar el archivo físico
        if documento.archivo:
            documento.archivo.delete()
        documento.delete()
        messages.success(request, f'🗑️ Documento "{tipo}" eliminado exitosamente.')
        return redirect('proveedores:proveedor_detail', id_proveedor=proveedor.id_proveedor)
    
    context = {
        'documento': documento,
        'proveedor': proveedor,
        'show_module_nav': True,
        'active_module': 'proveedores'
    }
    return render(request, 'proveedores/documento_confirm_delete.html', context)


def documento_download(request, id_documento):
    """Descargar documento"""
    documento = get_object_or_404(DocumentoProveedor, id_documento=id_documento)
    
    try:
        return FileResponse(
            documento.archivo.open('rb'),
            as_attachment=True,
            filename=documento.nombre_archivo_original
        )
    except FileNotFoundError:
        raise Http404("El archivo no existe")


# =====================================================
# GESTIÓN DE PRODUCTOS/SERVICIOS - FASE 5
# =====================================================

from .models import ProductoServicioProveedor
from .forms import ProductoServicioProveedorForm


def producto_create(request, id_proveedor):
    """Agregar producto/servicio a un proveedor"""
    proveedor = get_object_or_404(Proveedor, id_proveedor=id_proveedor)
    
    if request.method == 'POST':
        form = ProductoServicioProveedorForm(request.POST, proveedor=proveedor)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.id_proveedor = proveedor
            producto.save()
            messages.success(
                request,
                f'✅ Producto/Servicio "{producto.nombre}" agregado exitosamente.'
            )
            return redirect('proveedores:proveedor_detail', id_proveedor=proveedor.id_proveedor)
    else:
        form = ProductoServicioProveedorForm(proveedor=proveedor)
    
    context = {
        'form': form,
        'proveedor': proveedor,
        'titulo': 'Agregar Producto/Servicio',
        'action': 'Guardar',
        'show_module_nav': True,
        'active_module': 'proveedores',
    }
    return render(request, 'proveedores/producto_form.html', context)


def producto_update(request, id_producto_servicio):
    """Editar producto/servicio"""
    producto = get_object_or_404(
        ProductoServicioProveedor, 
        id_producto_servicio=id_producto_servicio
    )
    proveedor = producto.id_proveedor
    
    if request.method == 'POST':
        form = ProductoServicioProveedorForm(
            request.POST,
            instance=producto,
            proveedor=proveedor
        )
        if form.is_valid():
            producto = form.save()
            messages.success(
                request,
                f'✅ Producto/Servicio "{producto.nombre}" actualizado exitosamente.'
            )
            return redirect('proveedores:proveedor_detail', id_proveedor=proveedor.id_proveedor)
    else:
        form = ProductoServicioProveedorForm(instance=producto, proveedor=proveedor)
    
    context = {
        'form': form,
        'producto': producto,
        'proveedor': proveedor,
        'titulo': 'Editar Producto/Servicio',
        'action': 'Actualizar',
        'show_module_nav': True,
        'active_module': 'proveedores',
    }
    return render(request, 'proveedores/producto_form.html', context)


def producto_delete(request, id_producto_servicio):
    """Eliminar producto/servicio"""
    producto = get_object_or_404(
        ProductoServicioProveedor,
        id_producto_servicio=id_producto_servicio
    )
    proveedor = producto.id_proveedor
    
    if request.method == 'POST':
        nombre = producto.nombre
        producto.delete()
        messages.success(request, f'🗑️ Producto/Servicio "{nombre}" eliminado exitosamente.')
        return redirect('proveedores:proveedor_detail', id_proveedor=proveedor.id_proveedor)
    
    context = {
        'producto': producto,
        'proveedor': proveedor,
        'show_module_nav': True,
        'active_module': 'proveedores',
    }
    return render(request, 'proveedores/producto_confirm_delete.html', context)
