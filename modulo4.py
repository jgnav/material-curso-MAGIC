"""Autocorrección de 1.4. Listas."""

from html import escape
from math import isclose


def _mostrar_comprobacion(mensaje, correcta):
    """Muestra una comprobación coloreada en Colab y texto normal como respaldo."""

    color = "#137333" if correcta else "#c5221f"
    try:
        from IPython.display import HTML, display
    except ImportError:
        print(mensaje)
    else:
        display(
            HTML(
                f'<p style="color: {color}; font-weight: 600; margin: 8px 0;">'
                f"{escape(mensaje)}</p>"
            )
        )


class Ejercicio:
    """Pregunta con comprobación y ayuda opcional."""

    def __init__(self, numero, entorno, validar, pista=None, solucion=None):
        self.numero = numero
        self._entorno = entorno
        self._validar = validar
        self._pista = pista
        self._solucion = solucion
        self.completado = False

    def comprobar(self):
        try:
            resultado = self._validar(self._entorno)
        except Exception as error:
            _mostrar_comprobacion(
                f"El código ha producido {type(error).__name__}: {error}", False
            )
            return

        if resultado is True:
            self.completado = True
            _mostrar_comprobacion("Correcto. Puedes continuar.", True)
            return

        _mostrar_comprobacion(f"Revisa tu respuesta: {resultado}", False)

    def pista(self):
        if self._pista is not None:
            print(f"Pista: {self._pista}")

    def solucion(self):
        if self._solucion is not None:
            print("Una posible solución es:\n")
            print(self._solucion)


def _casi_igual(valor, esperado):
    es_numero = isinstance(valor, (int, float)) and not isinstance(valor, bool)
    return es_numero and isclose(
        float(valor), float(esperado), rel_tol=1e-9, abs_tol=1e-9
    )


def _validar_lista(entorno, nombre, esperado):
    if nombre not in entorno:
        return f"crea la variable {nombre}."
    if type(entorno[nombre]) is not list:
        return f"{nombre} debe ser una lista."
    if entorno[nombre] != esperado:
        return f"{nombre} debería valer {esperado!r}."
    return True


def _validar_q1(entorno):
    resultado = _validar_lista(entorno, "tickers", ["SAN", "BBVA", "IBE", "ITX"])
    if resultado is not True:
        return resultado

    esperados = {
        "primer_ticker": "SAN",
        "ultimo_ticker": "ITX",
    }
    for nombre, esperado in esperados.items():
        if nombre not in entorno:
            return f"crea la variable {nombre}."
        if entorno[nombre] != esperado:
            return f"{nombre} debe valer {esperado!r}."
    return True


def _validar_q2(entorno):
    precios_esperados = [101.20, 102.45, 100.80, 103.10, 104.25]
    resultado = _validar_lista(entorno, "precios_cierre", precios_esperados)
    if resultado is not True:
        return "no modifiques la lista precios_cierre."

    selecciones = {
        "primeras_tres": precios_esperados[:3],
        "ultimas_tres": precios_esperados[-3:],
        "sesiones_centrales": precios_esperados[1:4],
    }
    for nombre, esperado in selecciones.items():
        resultado = _validar_lista(entorno, nombre, esperado)
        if resultado is not True:
            return resultado
    return True


def _validar_q3(entorno):
    resultado = _validar_lista(entorno, "cartera", ["SAN", "ITX"])
    if resultado is not True:
        return (
            "aplica las cuatro operaciones en el orden indicado; "
            "cartera debe terminar como ['SAN', 'ITX']."
        )

    if "ticker_extraido" not in entorno:
        return "guarda en ticker_extraido el valor devuelto por pop()."
    if entorno["ticker_extraido"] != "REP":
        return "ticker_extraido debe guardar el elemento eliminado con pop()."
    return True


def _validar_q4(entorno):
    resultado = _validar_lista(entorno, "cartera", ["SAN", "IBE"])
    if resultado is not True:
        return "no modifiques la lista cartera."

    esperados = {
        "incluye_san": True,
        "incluye_bbva": False,
        "falta_itx": True,
    }
    for nombre, esperado in esperados.items():
        if nombre not in entorno:
            return f"crea la variable {nombre}."
        obtenido = entorno[nombre]
        if type(obtenido) is not bool or obtenido is not esperado:
            return f"{nombre} debe ser el booleano {esperado}."
    return True


def _validar_q5(entorno):
    precios_esperados = [101.20, 102.45, 100.80, 103.10, 104.25]
    resultado = _validar_lista(entorno, "precios_cierre", precios_esperados)
    if resultado is not True:
        return "no modifiques la lista precios_cierre."

    valores = {
        "precio_minimo": 100.80,
        "precio_maximo": 104.25,
        "precio_total": 511.80,
        "precio_medio": 102.36,
    }
    for nombre, esperado in valores.items():
        if nombre not in entorno:
            return f"crea la variable {nombre}."
        if not _casi_igual(entorno[nombre], esperado):
            return f"revisa el cálculo de {nombre}."

    return _validar_lista(
        entorno,
        "precios_ordenados",
        [100.80, 101.20, 102.45, 103.10, 104.25],
    )


def _validar_q6(entorno):
    cartera_esperada = [
        ["SAN", 25, 4.58],
        ["IBE", 10, 12.40],
        ["ITX", 5, 47.20],
    ]
    resultado = _validar_lista(entorno, "cartera", cartera_esperada)
    if resultado is not True:
        return "no modifiques la lista anidada cartera."

    resultado = _validar_lista(entorno, "primer_activo", ["SAN", 25, 4.58])
    if resultado is not True:
        return resultado

    if entorno.get("ticker_segundo") != "IBE":
        return "ticker_segundo debe contener el ticker del segundo activo."
    if entorno.get("acciones_tercero") != 5:
        return "acciones_tercero debe contener el número de acciones de ITX."
    if not _casi_igual(entorno.get("valor_tercer_activo"), 236.0):
        return "multiplica las acciones del tercer activo por su precio de compra."
    return True


def cargar(entorno):
    """Carga en el notebook las preguntas de la lección."""

    ejercicios = [
        Ejercicio(1, entorno, _validar_q1),
        Ejercicio(
            2,
            entorno,
            _validar_q2,
            "Utiliza [:3] para comenzar desde el principio, [-3:] para contar "
            "desde el final y [1:4] para las posiciones centrales.",
            "primeras_tres = precios_cierre[:3]\n"
            "ultimas_tres = precios_cierre[-3:]\n"
            "sesiones_centrales = precios_cierre[1:4]",
        ),
        Ejercicio(
            3,
            entorno,
            _validar_q3,
            "Cambia el índice 1, usa append() y remove(), y guarda el resultado "
            "de pop() en ticker_extraido.",
            "cartera[1] = \"ITX\"\n"
            "cartera.append(\"REP\")\n"
            "cartera.remove(\"IBE\")\n"
            "ticker_extraido = cartera.pop()",
        ),
        Ejercicio(4, entorno, _validar_q4),
        Ejercicio(
            5,
            entorno,
            _validar_q5,
            "Utiliza min(), max(), sum(), len() y sorted(). Para la media, "
            "divide la suma entre la longitud.",
            "precio_minimo = min(precios_cierre)\n"
            "precio_maximo = max(precios_cierre)\n"
            "precio_total = sum(precios_cierre)\n"
            "precio_medio = sum(precios_cierre) / len(precios_cierre)\n"
            "precios_ordenados = sorted(precios_cierre)",
        ),
        Ejercicio(
            6,
            entorno,
            _validar_q6,
            "El primer índice selecciona el activo y el segundo, uno de sus "
            "datos. En el tercer activo, las acciones están en [1] y el precio en [2].",
            "primer_activo = cartera[0]\n"
            "ticker_segundo = cartera[1][0]\n"
            "acciones_tercero = cartera[2][1]\n"
            "valor_tercer_activo = cartera[2][1] * cartera[2][2]",
        ),
    ]

    for ejercicio in ejercicios:
        entorno[f"q{ejercicio.numero}"] = ejercicio

    print("Preparación completada.")


__all__ = ["cargar"]
