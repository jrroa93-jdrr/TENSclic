import webbrowser
import urllib.parse

def enviar_notificacion_whatsapp(telefono, mensaje):
    """
    Abre WhatsApp Web o la App con un mensaje pre-escrito.
    El teléfono debe ir con formato internacional (ej: 56912345678)
    """
    # Limpiamos el mensaje para que sea válido en una URL
    mensaje_codificado = urllib.parse.quote(mensaje)
    url = f"https://wa.me/{telefono}?text={mensaje_codificado}"
    webbrowser.open(url)

def formatear_mensaje_emergencia(nombre_paciente, sector):
    return f"¡ALERTA TENSclic! El paciente {nombre_paciente} en el sector {sector} necesita asistencia urgente."