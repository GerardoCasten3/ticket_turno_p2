from django.contrib import admin
from .models import Municipio, NivelEducativo, Asuntos, Status, AlumnoCita, Cita

# Register your models here.
class MunicipioAdmin(admin.ModelAdmin):
    list_display = ('cve_municipio', 'nombre')
    search_fields = ('cve_municipio', 'nombre')
    ordering = ('cve_municipio',)

class NivelEducativoAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)
    ordering = ('id',)

class AsuntosAdmin(admin.ModelAdmin):
    list_display = ('descripcion',)
    search_fields = ('descripcion',)
    ordering = ('id',)

class StatusAdmin(admin.ModelAdmin):
    list_display = ('descripcion',)
    search_fields = ('descripcion',)
    ordering = ('id',)

class AlumnoCitaAdmin(admin.ModelAdmin):
    list_display = ('curp', 'nombre', 'apellido_paterno', 'apellido_materno', 'telefono', 'celular', 'email')
    search_fields = ('curp', 'nombre')
    ordering = ('curp',)

class CitaAdmin(admin.ModelAdmin):
    list_display = ('id', 'turno', 'nombre_interesado', 'alumno_cita', 'asunto', 'status', 'fecha_cita')
    search_fields = ('alumno_cita__nombre', 'alumno_cita__curp', 'turno')
    ordering = ('id',)

admin.site.register(Municipio, MunicipioAdmin)
admin.site.register(NivelEducativo, NivelEducativoAdmin)
admin.site.register(Asuntos, AsuntosAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(AlumnoCita, AlumnoCitaAdmin)
admin.site.register(Cita, CitaAdmin)