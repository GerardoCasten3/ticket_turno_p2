# dashboard/services.py
from tickets.models import Cita, Asuntos
from django.db.models import Count
from django.utils.timezone import now
from django.db.models.functions import TruncMonth

def get_dashboard_data():
    total = Cita.objects.count()
    attended = Cita.objects.filter(status__descripcion='Completado').count()
    percentage = (attended / total) * 100 

    data = {
        'total_citas': total,
        'citas_atendidas': attended,
        'porcentaje_atendidas': percentage,
    }
    return data


def get_asuntos_data_service():
    """
    Retorna los datos agrupados por asunto para la gráfica de dona
    """
    # Agrupa las citas por asunto y cuenta cuántas hay de cada uno
    asuntos_count = Cita.objects.values(
        'asunto__descripcion'
    ).annotate(
        total=Count('id')
    ).order_by('-total')
    
    # Prepara los datos en formato para Chart.js
    labels = []
    data = []
    
    for item in asuntos_count:
        if item['asunto__descripcion']:  # Evita asuntos nulos
            labels.append(item['asunto__descripcion'])
            data.append(item['total'])
    
    return {
        'labels': labels,
        'data': data
    }


def get_citas_municipios():
    """
    Retorna los las citas por municipio
    """
    
    municipios_count = Cita.objects.values(
        'municipio__nombre'
    ).annotate(
        total=Count('id')
    ).order_by('-total')

    labels = []
    data = [] 

    for item in municipios_count:
         if item['municipio__nombre']:
            labels.append(item['municipio__nombre'])
            data.append(item['total'])

    return {
        'labels': labels,
        'data': data
    }

def get_citas_nivel():
    """
    Retorna los las citas por municipio
    """
    
    municipios_count = Cita.objects.values(
        'nivel_educativo__nombre'
    ).annotate(
        total=Count('id')
    ).order_by('-total')

    labels = []
    data = [] 

    for item in municipios_count:
         if item['nivel_educativo__nombre']:
            labels.append(item['nivel_educativo__nombre'])
            data.append(item['total'])

    return {
        'labels': labels,
        'data': data
    }



def get_meta_mes():
    """
    Obtener la meta actual de mes de citas completadas
    """

    mes_actual = now().month
    citas_mes = Cita.objects.filter(fecha_creado__month=mes_actual).filter(status__descripcion='Completado').count()
    meta = 100  # puedes cambiarlo según tus objetivos
    porcentaje = (citas_mes / meta) * 100 if meta > 0 else 0

    data = {
        'mes_actual':mes_actual,
        'citas_mes': citas_mes,
        'meta': meta,
        'porcentaje_meta': porcentaje
    }

    return data