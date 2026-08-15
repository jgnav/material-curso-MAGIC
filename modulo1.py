"""Autocorrección de 1.1. Primeros pasos con Python."""

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

    def __init__(self, numero, entorno, validar, pista, solucion):
        self.numero = numero
        self._entorno = entorno
        self._validar = validar
        self._pista = pista
        self._solucion = solucion
        self.completado = False
        self.pista_consultada = False
        self.solucion_consultada = False

    def comprobar(self):
        try:
            resultado = self._validar(self._entorno, self)
        except NameError as error:
            _mostrar_comprobacion(
                f"Falta crear o corregir una variable: {error}", False
            )
            return
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
        if self._pista is None:
            return
        self.pista_consultada = True
        print(f"Pista: {self._pista}")

    def solucion(self):
        if self._solucion is None:
            return
        self.solucion_consultada = True
        print("Una posible solución es:\n")
        print(self._solucion)


def _faltan(entorno, *nombres):
    return [nombre for nombre in nombres if nombre not in entorno]


def _casi_igual(valor, esperado):
    es_numero = isinstance(valor, (int, float)) and not isinstance(valor, bool)
    return es_numero and isclose(
        float(valor), esperado, rel_tol=1e-9, abs_tol=1e-9
    )


def _validar_q1(entorno, ejercicio):
    return True


def _validar_q2(entorno, ejercicio):
    if "mensaje" not in entorno:
        return "crea una variable llamada mensaje."
    mensaje = entorno["mensaje"]
    if not isinstance(mensaje, str):
        return "mensaje debe contener texto escrito entre comillas."
    if not mensaje.strip() or mensaje.strip() == "Escribe aquí tu mensaje":
        return "sustituye el texto de ejemplo por un mensaje propio."
    return True


def _validar_q3(entorno, ejercicio):
    if not ejercicio.pista_consultada:
        return "descomenta y ejecuta primero q3.pista()."
    if not ejercicio.solucion_consultada:
        return "ahora descomenta y ejecuta q3.solucion()."
    return True


def _validar_q4(entorno, ejercicio):
    nombres = (
        "precio_compra",
        "numero_acciones",
        "comision_compra",
        "capital_invertido",
    )
    faltan = _faltan(entorno, *nombres)
    if faltan:
        return "faltan estas variables: " + ", ".join(faltan)

    esperado = (
        entorno["precio_compra"] * entorno["numero_acciones"]
        + entorno["comision_compra"]
    )
    if not _casi_igual(entorno["capital_invertido"], esperado):
        return "multiplica el precio por las acciones y suma la comisión."
    return True


def _validar_q5(entorno, ejercicio):
    nombres = ("ingreso_venta", "beneficio", "rentabilidad_pct")
    faltan = _faltan(entorno, *nombres)
    if faltan:
        return "faltan estas variables: " + ", ".join(faltan)

    ingreso_esperado = (
        entorno["precio_venta"] * entorno["numero_acciones"]
        - entorno["comision_venta"]
    )
    beneficio_esperado = ingreso_esperado - entorno["capital_invertido"]
    rentabilidad_esperada = beneficio_esperado / entorno["capital_invertido"] * 100

    if not _casi_igual(entorno["ingreso_venta"], ingreso_esperado):
        return "al importe de la venta debes restarle la comisión de venta."
    if not _casi_igual(entorno["beneficio"], beneficio_esperado):
        return "el beneficio es el ingreso de venta menos el capital invertido."
    if not _casi_igual(entorno["rentabilidad_pct"], rentabilidad_esperada):
        return "divide el beneficio entre el capital invertido y multiplica por 100."
    return True


def _validar_q6(entorno, ejercicio):
    nombres = ("ticker", "cantidad_acciones", "precio_actual", "mercado_abierto")
    faltan = _faltan(entorno, *nombres)
    if faltan:
        return "faltan estas variables: " + ", ".join(faltan)

    tipos_correctos = (
        type(entorno["ticker"]) is str
        and type(entorno["cantidad_acciones"]) is int
        and type(entorno["precio_actual"]) is float
        and type(entorno["mercado_abierto"]) is bool
    )
    if not tipos_correctos:
        return "revisa los tipos: str, int, float y bool, en ese orden."

    valores_correctos = (
        entorno["ticker"] == "SAN"
        and entorno["cantidad_acciones"] == 25
        and isclose(entorno["precio_actual"], 4.58)
        and entorno["mercado_abierto"] is True
    )
    if not valores_correctos:
        return "algún valor no coincide con el enunciado."
    return True


def _validar_q7(entorno, ejercicio):
    nombres = ("precio", "acciones", "valor_posicion", "valor_redondeado")
    faltan = _faltan(entorno, *nombres)
    if faltan:
        return "faltan estas variables: " + ", ".join(faltan)

    if type(entorno["precio"]) is not float or not isclose(entorno["precio"], 98.756):
        return "convierte precio_texto con float()."
    if type(entorno["acciones"]) is not int or entorno["acciones"] != 20:
        return "convierte acciones_texto con int()."

    valor_esperado = 98.756 * 20
    if not _casi_igual(entorno["valor_posicion"], valor_esperado):
        return "multiplica el precio convertido por el número de acciones."
    if not _casi_igual(entorno["valor_redondeado"], round(valor_esperado, 2)):
        return "redondea valor_posicion a dos decimales con round()."
    return True


def _validar_q8(entorno, ejercicio):
    if "rentabilidad" not in entorno:
        return "todavía no existe rentabilidad; revisa el nombre mal escrito."
    esperado = (entorno["precio_cierre"] / entorno["precio_apertura"] - 1) * 100
    if not _casi_igual(entorno["rentabilidad"], esperado):
        return "el nombre ya está corregido, pero revisa el cálculo."
    return True


def _validar_q9(entorno, ejercicio):
    nombres = (
        "coste_total",
        "ingreso_total",
        "beneficio_neto",
        "rentabilidad_neta_pct",
    )
    faltan = _faltan(entorno, *nombres)
    if faltan:
        return "faltan estas variables: " + ", ".join(faltan)

    coste_esperado = (
        entorno["precio_entrada"] * entorno["cantidad"]
        + entorno["comision_entrada"]
    )
    ingreso_esperado = (
        entorno["precio_salida"] * entorno["cantidad"]
        - entorno["comision_salida"]
    )
    beneficio_esperado = ingreso_esperado - coste_esperado
    rentabilidad_esperada = beneficio_esperado / coste_esperado * 100
    comprobaciones = (
        _casi_igual(entorno["coste_total"], coste_esperado),
        _casi_igual(entorno["ingreso_total"], ingreso_esperado),
        _casi_igual(entorno["beneficio_neto"], beneficio_esperado),
        _casi_igual(entorno["rentabilidad_neta_pct"], rentabilidad_esperada),
    )
    if not all(comprobaciones):
        return "revisa el coste, el ingreso, el beneficio y la rentabilidad."
    return True


def cargar(entorno):
    """Carga en el notebook las preguntas de la lección."""

    ejercicios = [
        Ejercicio(
            1,
            entorno,
            _validar_q1,
            None,
            None,
        ),
        Ejercicio(
            2,
            entorno,
            _validar_q2,
            None,
            None,
        ),
        Ejercicio(
            3,
            entorno,
            _validar_q3,
            "Elimina el símbolo # situado delante de la llamada.",
            "Al quitar #, la línea deja de ser un comentario y Python la ejecuta.",
        ),
        Ejercicio(
            4,
            entorno,
            _validar_q4,
            "Multiplica el precio por las acciones y suma después la comisión.",
            "capital_invertido = precio_compra * numero_acciones + comision_compra",
        ),
        Ejercicio(
            5,
            entorno,
            _validar_q5,
            "Calcula primero el ingreso, después el beneficio y el porcentaje.",
            "ingreso_venta = precio_venta * numero_acciones - comision_venta\n"
            "beneficio = ingreso_venta - capital_invertido\n"
            "rentabilidad_pct = beneficio / capital_invertido * 100",
        ),
        Ejercicio(
            6,
            entorno,
            _validar_q6,
            "Los textos llevan comillas y True se escribe sin comillas.",
            'ticker = "SAN"\ncantidad_acciones = 25\n'
            "precio_actual = 4.58\nmercado_abierto = True",
        ),
        Ejercicio(
            7,
            entorno,
            _validar_q7,
            "Utiliza float(), int() y después round(..., 2).",
            "precio = float(precio_texto)\nacciones = int(acciones_texto)\n"
            "valor_posicion = precio * acciones\n"
            "valor_redondeado = round(valor_posicion, 2)",
        ),
        Ejercicio(
            8,
            entorno,
            _validar_q8,
            "Compara precio_ciere con el nombre definido en la línea anterior.",
            "rentabilidad = (precio_cierre / precio_apertura - 1) * 100",
        ),
        Ejercicio(
            9,
            entorno,
            _validar_q9,
            "Suma la comisión al coste y resta la comisión del ingreso.",
            "coste_total = precio_entrada * cantidad + comision_entrada\n"
            "ingreso_total = precio_salida * cantidad - comision_salida\n"
            "beneficio_neto = ingreso_total - coste_total\n"
            "rentabilidad_neta_pct = beneficio_neto / coste_total * 100",
        ),
    ]

    for ejercicio in ejercicios:
        entorno[f"q{ejercicio.numero}"] = ejercicio
    print("Preparación completada.")


__all__ = ["cargar"]
