"""Autocorrección de 1.2. Funciones y obtención de ayuda."""

from contextlib import redirect_stdout
from html import escape
from io import StringIO
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


def _validar_funcion_numerica(entorno, nombre, casos):
    if nombre not in entorno:
        return f"define una función llamada {nombre}()."

    funcion = entorno[nombre]
    if not callable(funcion):
        return f"{nombre} debe ser una función."

    for argumentos, argumentos_con_nombre, esperado in casos:
        try:
            with redirect_stdout(StringIO()):
                obtenido = funcion(*argumentos, **argumentos_con_nombre)
        except TypeError as error:
            return f"no puedo llamar a {nombre} con los argumentos pedidos: {error}"
        except Exception as error:
            return f"{nombre} produce {type(error).__name__}: {error}"

        if obtenido is None:
            return f"{nombre} no devuelve ningún valor; revisa la instrucción return."
        if not _casi_igual(obtenido, esperado):
            return (
                f"{nombre}{argumentos} debería devolver {esperado}, "
                f"pero devuelve {obtenido}."
            )

    return True


def _validar_q1(entorno):
    if "precio_redondeado" not in entorno:
        return "crea la variable precio_redondeado."
    if not _casi_igual(entorno["precio_redondeado"], 51.16):
        return "utiliza round() para redondear precio a dos decimales."
    return True


def _validar_q2(entorno):
    return _validar_funcion_numerica(
        entorno,
        "redondear_precio",
        [
            ((3.14159,), {}, 3.14),
            ((51.157,), {}, 51.16),
            ((100,), {}, 100),
        ],
    )


def _validar_q3(entorno):
    return _validar_funcion_numerica(
        entorno,
        "calcular_comision",
        [
            ((5000,), {}, 5),
            ((12500,), {}, 12.5),
            ((0,), {}, 0),
        ],
    )


def _validar_q4(entorno):
    faltan = [
        nombre
        for nombre in ("comision_compra", "comision_venta")
        if nombre not in entorno
    ]
    if faltan:
        return "faltan estas variables: " + ", ".join(faltan)
    if not _casi_igual(entorno["comision_compra"], 5):
        return "calcula comision_compra llamando a calcular_comision() con 5000."
    if not _casi_igual(entorno["comision_venta"], 12.5):
        return "calcula comision_venta llamando a calcular_comision() con 12500."
    return True


def _validar_q5(entorno):
    return _validar_funcion_numerica(
        entorno,
        "calcular_beneficio",
        [
            ((48.60, 51.15, 80), {}, 204),
            ((100, 95, 10), {}, -50),
            ((25, 25, 40), {}, 0),
        ],
    )


def _validar_q6(entorno):
    return _validar_funcion_numerica(
        entorno,
        "calcular_valor_final",
        [
            ((10000, 3.5), {}, 10350),
            ((2500, -2), {}, 2450),
            ((1000, 0), {}, 1000),
        ],
    )


def _validar_q7(entorno):
    if "calcular_comision" not in entorno:
        return "define una función llamada calcular_comision()."

    docstring = getattr(entorno["calcular_comision"], "__doc__", None)
    if not docstring or not any(
        palabra in docstring.lower()
        for palabra in ("porcentaje", "opcional", "modific")
    ):
        return "actualiza la docstring para explicar que el porcentaje puede modificarse."

    return _validar_funcion_numerica(
        entorno,
        "calcular_comision",
        [
            ((5000,), {}, 5),
            ((5000, 0.002), {}, 10),
            ((5000,), {"porcentaje": 0.0025}, 12.5),
        ],
    )


def _validar_q8(entorno):
    if "calcular_rentabilidad" not in entorno:
        return "define una función llamada calcular_rentabilidad()."

    funcion = entorno["calcular_rentabilidad"]
    docstring = getattr(funcion, "__doc__", None)
    if not docstring or "escribe aquí" in docstring.lower():
        return "sustituye el texto de ejemplo por una docstring que describa la función."

    return _validar_funcion_numerica(
        entorno,
        "calcular_rentabilidad",
        [
            ((100, 105), {}, 5),
            ((80, 76), {}, -5),
            ((50, 50), {}, 0),
        ],
    )


def _validar_q9(entorno):
    return _validar_funcion_numerica(
        entorno,
        "calcular_beneficio_neto",
        [
            ((48.60, 51.15, 80), {}, 201),
            ((25.40, 26.10, 100), {"comision": 2}, 66),
            ((100, 99, 10), {"comision": 1}, -12),
        ],
    )


def cargar(entorno):
    """Carga en el notebook las preguntas de la lección."""

    ejercicios = [
        Ejercicio(1, entorno, _validar_q1),
        Ejercicio(
            2,
            entorno,
            _validar_q2,
            "Utiliza round() con precio y el número de decimales que necesitas.",
            "def redondear_precio(precio):\n"
            "    \"\"\"Devuelve un precio redondeado a dos decimales.\"\"\"\n"
            "    return round(precio, 2)",
        ),
        Ejercicio(
            3,
            entorno,
            _validar_q3,
            "Multiplica importe por 0.001 y devuelve el resultado.",
            "def calcular_comision(importe):\n"
            "    comision = importe * 0.001\n"
            "    return comision",
        ),
        Ejercicio(
            4,
            entorno,
            _validar_q4,
            "Llama a calcular_comision() una vez con 5000 y otra con 12500.",
            "comision_compra = calcular_comision(5000)\n"
            "comision_venta = calcular_comision(12500)",
        ),
        Ejercicio(
            5,
            entorno,
            _validar_q5,
            "Calcula primero el coste y el ingreso; después resta el coste al ingreso.",
            "def calcular_beneficio(precio_compra, precio_venta, cantidad):\n"
            "    coste = precio_compra * cantidad\n"
            "    ingreso = precio_venta * cantidad\n"
            "    beneficio = ingreso - coste\n"
            "    return beneficio",
        ),
        Ejercicio(
            6,
            entorno,
            _validar_q6,
            "Sustituye print(valor_final) por una instrucción return.",
            "def calcular_valor_final(capital, rentabilidad_pct):\n"
            "    incremento = capital * rentabilidad_pct / 100\n"
            "    valor_final = capital + incremento\n"
            "    return valor_final",
        ),
        Ejercicio(
            7,
            entorno,
            _validar_q7,
            "Añade porcentaje=0.001 en la cabecera y utiliza porcentaje en el cálculo.",
            "def calcular_comision(importe, porcentaje=0.001):\n"
            "    \"\"\"Calcula una comisión con un porcentaje modificable.\"\"\"\n"
            "    return importe * porcentaje",
        ),
        Ejercicio(
            8,
            entorno,
            _validar_q8,
            "La docstring va entre comillas triples justo debajo de la cabecera.",
            "def calcular_rentabilidad(precio_inicial, precio_final):\n"
            "    \"\"\"Calcula la rentabilidad porcentual entre dos precios.\"\"\"\n"
            "    rentabilidad = (precio_final / precio_inicial - 1) * 100\n"
            "    return rentabilidad",
        ),
        Ejercicio(
            9,
            entorno,
            _validar_q9,
            "Suma la comisión al coste, réstala del ingreso y devuelve la diferencia.",
            "def calcular_beneficio_neto(precio_compra, precio_venta, cantidad, "
            "comision=1.50):\n"
            "    coste_total = precio_compra * cantidad + comision\n"
            "    ingreso_total = precio_venta * cantidad - comision\n"
            "    beneficio_neto = ingreso_total - coste_total\n"
            "    return beneficio_neto",
        ),
    ]

    for ejercicio in ejercicios:
        entorno[f"q{ejercicio.numero}"] = ejercicio

    print("Preparación completada.")


__all__ = ["cargar"]
