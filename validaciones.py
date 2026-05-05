def validar_rut(rut):
    rut = rut.replace(".", "").replace("-", "").upper()
    if len(rut) < 8: return False
    cuerpo = rut[:-1]
    dv = rut[-1]
    try:
        reversa = map(int, reversed(cuerpo))
        factores = [2, 3, 4, 5, 6, 7]
        suma = sum(d * f for d, f in zip(reversa, factores * 2))
        res = 11 - (suma % 11)
        esperado = str(res) if res < 10 else "K" if res == 11 else "0"
        return dv == esperado
    except:
        return False