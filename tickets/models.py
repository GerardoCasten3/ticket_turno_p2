from django.db import models

# Create your models here.    
class Municipio(models.Model):
    cve_municipio = models.CharField(max_length=3)
    nombre = models.CharField(max_length=80)
    contador = models.IntegerField()

    class Meta:
        verbose_name = 'CAT01 - Municipio'
        verbose_name_plural = 'CAT01 - Municipios'
        ordering = ['cve_municipio']

    def __str__(self):
        return self.nombre
    

class NivelEducativo(models.Model):
    nombre = models.CharField(max_length=80)

    class Meta:
        verbose_name = 'CAT02 - Nivel Educativo'
        verbose_name_plural = 'CAT02 - Niveles Educativos'
        ordering = ['id']

    def __str__(self):
        return self.nombre
    
class Asuntos(models.Model):
    descripcion = models.CharField(max_length=250)

    class Meta:
        verbose_name = 'CAT03 - Asunto'
        verbose_name_plural = 'CAT03 - Asuntos'
        ordering = ['id']

    def __str__(self):
        return self.descripcion
    
class Status(models.Model):
    descripcion = models.CharField(max_length=80)

    class Meta:
        verbose_name = 'CAT04 - Estatus'
        verbose_name_plural = 'CAT04 - Estatus'
        ordering = ['id']

    def __str__(self):
        return self.descripcion

class AlumnoCita(models.Model):
    curp = models.CharField(max_length=18, primary_key=True)
    nombre = models.CharField(max_length=80)
    apellido_paterno = models.CharField(max_length=80)
    apellido_materno = models.CharField(max_length=80)
    telefono = models.CharField(max_length=10)
    celular = models.CharField(max_length=10)
    email = models.EmailField(max_length=254)

    class Meta:
        verbose_name = 'INF01 - Alumno registrado en cita'
        verbose_name_plural = 'INF01 - Alumnos registrados en citas'
        ordering = ['curp']

    def __str__(self):
        return f"{self.nombre} {self.apellido_paterno} {self.apellido_materno}"
    
class Cita(models.Model):
    turno = models.CharField(max_length=250)
    nombre_interesado = models.CharField(max_length=250)
    alumno_cita = models.ForeignKey(AlumnoCita, on_delete=models.CASCADE)
    asunto = models.ForeignKey(Asuntos, on_delete=models.CASCADE)
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE)
    nivel_educativo = models.ForeignKey(NivelEducativo, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    fecha_cita = models.DateTimeField()
    fecha_creado = models.DateTimeField(auto_now_add=True)

    class Meta: 
        verbose_name = 'INF02 - Cita'
        verbose_name_plural = 'INF02 - Citas'
        ordering = ['-fecha_creado']

    def __str__(self):
        return f"Cita: {self.id}"