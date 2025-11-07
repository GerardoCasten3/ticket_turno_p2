from datetime import datetime, timedelta, time
import random
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from .models import Asuntos, Cita, Municipio, NivelEducativo, AlumnoCita, Status
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from captcha.fields import CaptchaField
from django import forms


@require_http_methods(["GET"])
def ticket_view(request):
    context = {}
    niveles = NivelEducativo.objects.all()
    asuntos = Asuntos.objects.all()
    municipios = Municipio.objects.all()

    context['niveles'] = niveles
    context['asuntos'] = asuntos
    context['municipios'] = municipios
    return render(request, 'form_ticket_turno.html', context)

def obtener_siguiente_fecha_cita():
    horarios = [time(8, 0), time(10, 0), time(12, 0), time(14, 0), time(16, 0)]

    ultima_cita = Cita.objects.order_by('-fecha_cita').first()
    hoy = timezone.localdate()

    # === Caso 1: No hay citas ===
    if not ultima_cita:
        fecha_base = hoy + timedelta(days=2)
        while fecha_base.weekday() >= 5:  # Saltar sábados y domingos
            fecha_base += timedelta(days=1)
        return timezone.make_aware(datetime.combine(fecha_base, horarios[0]))

    # === Caso 2: Ya hay una cita registrada ===
    fecha_ultima = timezone.localtime(ultima_cita.fecha_cita)
    fecha_ultima_dia = fecha_ultima.date()
    hora_ultima = fecha_ultima.time()

    # Si la última cita ya ocurrió o es el mismo día que hoy, reiniciar ciclo
    if fecha_ultima_dia <= hoy:
        nueva_fecha = hoy + timedelta(days=2)
        while nueva_fecha.weekday() >= 5:
            nueva_fecha += timedelta(days=1)
        return timezone.make_aware(datetime.combine(nueva_fecha, horarios[0]))

    # Si la última cita está en el futuro, continuar con el siguiente horario
    for h in horarios:
        if h > hora_ultima:
            return timezone.make_aware(datetime.combine(fecha_ultima_dia, h))

    # Si ya fue la última hora (4:00 PM), pasar al siguiente día hábil
    siguiente_dia = fecha_ultima_dia + timedelta(days=1)
    while siguiente_dia.weekday() >= 5:
        siguiente_dia += timedelta(days=1)
    return timezone.make_aware(datetime.combine(siguiente_dia, horarios[0]))

@require_http_methods(["POST"])
def post_ticket(request):
    if request.method == "POST":
        try:
            # Tomar datos del formulario
            nivel_id = request.POST.get('level')
            municipio_id = request.POST.get('city')
            asunto_id = request.POST.get('issue')
            nombre = request.POST.get('student_name')
            apellido_paterno = request.POST.get('last_name1')
            apellido_materno = request.POST.get('last_name2')
            telefono = request.POST.get('telephone')
            celular = request.POST.get('cellphone')
            correo = request.POST.get('email')
            curp = request.POST.get('curp')
            curp = curp.upper()
            full_name_request = request.POST.get('full_name_request')

            # Validación del lado del servidor
            if not all([nivel_id, municipio_id, asunto_id, nombre, apellido_paterno, telefono, correo, curp, full_name_request]):
                print("Faltan campos requeridos")
                return JsonResponse({'status': 'error', 'message': 'Faltan campos requeridos'}, status=400)
            
            # Revisar si el alumno ya ha sido anteriormente registrado
            alumno_cita = AlumnoCita.objects.filter(curp=curp).first()

            # Obtener últimos 2 objetos de cita para evitar spam de citas por el mismo alumno
            recent_citas = Cita.objects.order_by('-fecha_cita')[:2]
            if len(recent_citas) == 2 and recent_citas[0].alumno_cita.curp == curp and recent_citas[1].alumno_cita.curp == curp:
                return JsonResponse({'status': 'error', 'message': 'Ya has solicitado dos citas recientemente. Por favor espera antes de solicitar otra.'}, status=400)

            # Si no existe, insertarlo
            if not alumno_cita:
                alumno_cita = AlumnoCita(
                    nombre=nombre,
                    apellido_paterno=apellido_paterno,
                    apellido_materno=apellido_materno,
                    curp=curp,
                    telefono=telefono,
                    celular=celular,
                    email=correo
                )
                alumno_cita.save()

            nivel_educativo = NivelEducativo.objects.get(id=nivel_id)
            municipio = Municipio.objects.get(id=municipio_id)
            asunto = Asuntos.objects.get(id=asunto_id)
            status = Status.objects.get(id=1)  # Asignar un estado por defecto (PENDIENTE)
            # Obtener contador de turno del municipio y asignar nuevo turno
            turno = municipio.contador + 1
            municipio.contador = turno
            # Actualizar el contador en el municipio
            municipio.save()

            chars_curp = ''.join(random.sample(curp, 2)).upper()
            turnoStr = f"{turno}{municipio.cve_municipio}{chars_curp}"

            # Obtener fecha y hora de la última cita registrada
            fecha_cita = obtener_siguiente_fecha_cita()
            
            cita = Cita(
                turno=turnoStr,
                nombre_interesado=full_name_request,
                alumno_cita=alumno_cita,
                asunto=asunto,
                municipio=municipio,
                nivel_educativo=nivel_educativo,
                status=status,
                fecha_cita=fecha_cita
            )
            cita.save()
            return JsonResponse({'status': 'success', 'ticket_id': cita.id, 'message': 'Ticket creado exitosamente'}, status=200)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Petición inválida'}, status=400)

@require_http_methods(["GET"])
def get_ticket(request, ticket_turno, curp):
    try:
        ticket = Cita.objects.get(turno=ticket_turno, alumno_cita__curp=curp)
        return render(request, 'ticket_detail.html', {'ticket': ticket})
    except Cita.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Ticket not found'}, status=404)
    
@require_http_methods(["GET"])
def get_ticket_id(request, ticket_id):
    try:
        ticket = Cita.objects.get(id=ticket_id)
        return render(request, 'ticket_detail.html', {'ticket': ticket})
    except Cita.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Ticket not found'}, status=404)
    
@require_http_methods(["GET"])
def search_ticket(request, ticket_turno, curp):
    try:
        print(ticket_turno)
        searched_ticket = Cita.objects.filter(turno=ticket_turno, alumno_cita__curp=curp).exists()
        if searched_ticket:
            return JsonResponse({'status': 'found'}, status=200)
        else:
            return JsonResponse({'status': 'not found'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
@require_http_methods(["GET"])  
def get_edit_ticket(request, ticket_turno, curp):
    try:
        ticket = Cita.objects.get(turno=ticket_turno, alumno_cita__curp=curp)
        niveles = NivelEducativo.objects.all()
        asuntos = Asuntos.objects.all()
        municipios = Municipio.objects.all()
        
        context = {
            'ticket': ticket,
            'niveles': niveles,
            'asuntos': asuntos,
            'municipios': municipios
        }
        return render(request, 'edit_ticket.html', context)
    except Cita.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Ticket not found'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@require_http_methods(["POST"])
def update_ticket(request, ticket_id):
    try:
        cita = Cita.objects.get(id=ticket_id)
        alumno_cita = cita.alumno_cita
        nivel_id = request.POST.get('level')
        municipio_id = request.POST.get('city')
        asunto_id = request.POST.get('issue')
        nombre = request.POST.get('student_name')
        apellido_paterno = request.POST.get('last_name1')
        apellido_materno = request.POST.get('last_name2')
        telefono = request.POST.get('telephone')
        celular = request.POST.get('cellphone')
        correo = request.POST.get('email')
        curp = request.POST.get('curp')
        full_name_request = request.POST.get('full_name_request')

        alumno_cita.nombre = nombre
        alumno_cita.apellido_paterno = apellido_paterno
        alumno_cita.apellido_materno = apellido_materno
        alumno_cita.curp = curp
        alumno_cita.telefono = telefono
        alumno_cita.celular = celular
        alumno_cita.email = correo
        alumno_cita.save()

        nivel_educativo = NivelEducativo.objects.get(id=nivel_id)
        municipio = Municipio.objects.get(id=municipio_id)
        asunto = Asuntos.objects.get(id=asunto_id)

        cita.nombre_interesado = full_name_request
        cita.asunto = asunto
        cita.municipio = municipio
        cita.nivel_educativo = nivel_educativo
        cita.save()
        return redirect('get_ticket_id', ticket_id=ticket_id)
        
    except Cita.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Ticket not found'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


# Crea un formulario simple con captcha
class LoginFormWithCaptcha(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    captcha = CaptchaField()

def custom_login(request):
    if request.method == 'POST':
        form = LoginFormWithCaptcha(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/admin/')  # redirige al admin
            else:
                form.add_error(None, 'Usuario o contraseña incorrectos')
    else:
        form = LoginFormWithCaptcha()      
    return render(request, 'admin/login.html', {'form': form})