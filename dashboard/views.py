# dashboard/admin_views.py
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.contrib import admin
from .services import get_dashboard_data, get_asuntos_data_service, get_citas_municipios, get_citas_nivel, get_meta_mes
from django.http import JsonResponse

@staff_member_required
def dashboard_view(request):
    dashboard_data = get_dashboard_data()
    data_meta = get_meta_mes()

    # Obtener el contexto del admin site
    context = {
        **admin.site.each_context(request),  # Esto mantiene el sidebar y toda la UI del admin
        'title': 'Dashboard', 
        'custom_data': 'tu data aquí',
        **dashboard_data,
        **data_meta
    }
    
    return render(request, 'admin/dashboard.html', context)


@staff_member_required
def get_asuntos_data(request):
    """
    Vista que retorna los datos de asuntos en formato JSON
    """
    data = get_asuntos_data_service()
    return JsonResponse(data)


@staff_member_required
def get_citas_muni(request):
    """
    Vista que retorna los datos de asuntos en formato JSON
    """

    data = get_citas_municipios()
    return JsonResponse(data)


@staff_member_required
def get_citas_niv(request):
    """
    Vista que retorna los datos de asuntos en formato JSON
    """

    data = get_citas_nivel()
    return JsonResponse(data)