# ==========================================
# ARCHIVO: geolocalizacion.py
# Propósito: Gestión de sectores en San Bernardo
# ==========================================

def obtener_sectores():
    """
    Retorna la lista oficial de sectores para los Dropdowns.
    Esto asegura que tanto el TENS como el Paciente usen los mismos nombres.
    """
    return [
        "San Bernardo Centro",
        "Sector Nos",
        "El Mariscal",
        "Lo Blanco / Padre Hurtado",
        "Portales / Estación",
        "Valle de Cóndores",
        "Lo Herrera"
    ]

def calcular_distancia_texto(sector_paciente, sector_tens):
    """
    Compara dos sectores y retorna un indicador de proximidad.
    Útil para mostrar en las tarjetas de búsqueda.
    """
    if not sector_paciente or not sector_tens:
        return "Ubicación no especificada"
        
    if sector_paciente == sector_tens:
        return "📍 En tu mismo sector"
    else:
        return "🚗 Sector cercano (San Bernardo)"

def validar_cobertura(sector):
    """
    Verifica si un sector está dentro del radio de TENSclic.
    """
    sectores_validos = obtener_sectores()
    if sector in sectores_validos:
        return True
    return False