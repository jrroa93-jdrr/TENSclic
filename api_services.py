import webbrowser
import datetime
import urllib.parse

def llamar_emergencia(): # <--- ASEGÚRATE QUE SE LLAME ASÍ
    """Abre el marcador con el número del SAMU (131)"""
    webbrowser.open("tel:131")

def obtener_saludo_segun_hora(): # <--- Y ESTA TAMBIÉN
    """Retorna un saludo dinámico según la hora del sistema"""
    hora = datetime.datetime.now().hour
    if hora < 12:
        return "Buenos días"
    elif hora < 20:
        return "Buenas tardes"
    else:
        return "Buenas noches"

def abrir_mapa_sector(sector):
    """Abre Google Maps centrado en el sector de San Bernardo"""
    busqueda = f"{sector}, San Bernardo, Chile"
    url = f"https://www.google.com/maps/search/{urllib.parse.quote(busqueda)}"
    webbrowser.open(url)