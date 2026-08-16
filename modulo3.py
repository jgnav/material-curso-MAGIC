"""Autocorrección de 1.3. Booleanos y estructuras condicionales."""

from contextlib import redirect_stdout
from html import escape
from io import StringIO


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
    """Pregunta con comprobación, pista y solución."""

    def __init__(self, numero, entorno, validar, pista, solucion):
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
        print(f"Pista: {self._pista}")

    def solucion(self):
        print("Una posible solución es:\n")
        print(self._solucion)


def _coincide(obtenido, esperado):
    if type(esperado) is bool:
        return type(obtenido) is bool and obtenido is esperado
    return type(obtenido) is type(esperado) and obtenido == esperado


def _validar_funcion(entorno, nombre, casos):
    if nombre not in entorno:
        return f"define una función llamada {nombre}()."

    funcion = entorno[nombre]
    if not callable(funcion):
        return f"{nombre} debe ser una función."

    for argumentos, esperado in casos:
        try:
            with redirect_stdout(StringIO()):
                obtenido = funcion(*argumentos)
        except TypeError as error:
            return f"no puedo llamar a {nombre} con los argumentos pedidos: {error}"
        except Exception as error:
            return f"{nombre} produce {type(error).__name__}: {error}"

        if obtenido is None:
            return f"{nombre} no devuelve ningún valor; revisa la instrucción return."
        if not _coincide(obtenido, esperado):
            return (
                f"{nombre}{argumentos} debería devolver {esperado!r}, "
                f"pero devuelve {obtenido!r}."
            )

    return True


def _validar_q1(entorno):
    esperados = {
        "supera_nivel": True,
        "mismo_precio": False,
        "precio_distinto": True,
    }
    for nombre, esperado in esperados.items():
        if nombre not in entorno:
            return f"crea la variable {nombre}."
        if not _coincide(entorno[nombre], esperado):
            return f"{nombre} debe valer {esperado}."
    return True


def _validar_q2(entorno):
    return _validar_funcion(
        entorno,
        "supera_nivel",
        [
            ((105.20, 103.00), True),
            ((101.50, 103.00), False),
            ((103.00, 103.00), True),
        ],
    )


def _validar_q3(entorno):
    return _validar_funcion(
        entorno,
        "puede_enviar_orden",
        [
            ((True, True, False), True),
            ((False, True, False), False),
            ((True, False, False), False),
            ((True, True, True), False),
        ],
    )


def _validar_q4(entorno):
    return _validar_funcion(
        entorno,
        "puede_operar",
        [
            ((True, True, False, False), True),
            ((True, False, True, False), True),
            ((True, False, False, False), False),
            ((False, True, False, False), False),
            ((True, True, False, True), False),
        ],
    )


def _validar_q5(entorno):
    if "mensaje" not in entorno:
        return "crea o actualiza la variable mensaje."
    if entorno["mensaje"] != "El precio ha superado el nivel":
        return "el bloque if debe actualizar mensaje cuando el precio supera el nivel."
    return True


def _validar_q6(entorno):
    return _validar_funcion(
        entorno,
        "estado_mercado",
        [
            ((True,), "Mercado abierto"),
            ((False,), "Mercado cerrado"),
        ],
    )


def _validar_q7(entorno):
    return _validar_funcion(
        entorno,
        "clasificar_senal",
        [
            ((1.8,), "Comprar"),
            ((-1.4,), "Vender"),
            ((0.3,), "Mantener"),
            ((1,), "Comprar"),
            ((-1,), "Vender"),
            ((1.5, 2), "Mantener"),
        ],
    )


def _validar_q8(entorno):
    return _validar_funcion(
        entorno,
        "estado_operacion",
        [
            ((125.40,), "Con beneficio"),
            ((-32.50,), "Sin beneficio"),
            ((0,), "Sin beneficio"),
        ],
    )


def _validar_q9(entorno):
    return _validar_funcion(
        entorno,
        "evaluar_operacion",
        [
            ((10000, 2000, 150, True), "Operación permitida"),
            ((10000, 3500, 150, True), "Posición demasiado grande"),
            ((10000, 2000, 250, True), "Riesgo demasiado alto"),
            ((10000, 2000, 150, False), "Mercado cerrado"),
            ((10000, 2500, 200, True), "Operación permitida"),
        ],
    )


def cargar(entorno):
    """Carga en el notebook las preguntas de la lección."""

    ejercicios = [
        Ejercicio(
            1,
            entorno,
            _validar_q1,
            "Utiliza > para la primera comparación, == para la segunda y != para la tercera.",
            "supera_nivel = precio_actual > nivel\n"
            "mismo_precio = precio_actual == nivel\n"
            "precio_distinto = precio_actual != nivel",
        ),
        Ejercicio(
            2,
            entorno,
            _validar_q2,
            "La comparación precio >= nivel ya produce True o False; devuélvela directamente.",
            "def supera_nivel(precio, nivel):\n"
            "    return precio >= nivel",
        ),
        Ejercicio(
            3,
            entorno,
            _validar_q3,
            "Las dos primeras condiciones deben ser verdaderas y orden_bloqueada debe ser falsa.",
            "def puede_enviar_orden(mercado_abierto, riesgo_aceptable, orden_bloqueada):\n"
            "    return mercado_abierto and riesgo_aceptable and not orden_bloqueada",
        ),
        Ejercicio(
            4,
            entorno,
            _validar_q4,
            "Agrupa senal_compra or senal_venta entre paréntesis.",
            "def puede_operar(mercado_abierto, senal_compra, senal_venta, riesgo_superado):\n"
            "    return (\n"
            "        mercado_abierto\n"
            "        and (senal_compra or senal_venta)\n"
            "        and not riesgo_superado\n"
            "    )",
        ),
        Ejercicio(
            5,
            entorno,
            _validar_q5,
            "Dentro del if, asigna el texto indicado a la variable mensaje.",
            "mensaje = \"El precio no ha superado el nivel\"\n"
            "if precio_actual > nivel:\n"
            "    mensaje = \"El precio ha superado el nivel\"",
        ),
        Ejercicio(
            6,
            entorno,
            _validar_q6,
            "Utiliza la condición mercado_abierto en el if y devuelve un texto distinto en cada rama.",
            "def estado_mercado(mercado_abierto):\n"
            "    if mercado_abierto:\n"
            "        return \"Mercado abierto\"\n"
            "    else:\n"
            "        return \"Mercado cerrado\"",
        ),
        Ejercicio(
            7,
            entorno,
            _validar_q7,
            "Comprueba primero >= umbral, después <= -umbral y utiliza else para el resto.",
            "def clasificar_senal(variacion_pct, umbral=1):\n"
            "    if variacion_pct >= umbral:\n"
            "        return \"Comprar\"\n"
            "    elif variacion_pct <= -umbral:\n"
            "        return \"Vender\"\n"
            "    else:\n"
            "        return \"Mantener\"",
        ),
        Ejercicio(
            8,
            entorno,
            _validar_q8,
            "Escribe primero el valor para el caso verdadero, después if, la condición y el caso de else.",
            "def estado_operacion(beneficio):\n"
            "    return \"Con beneficio\" if beneficio > 0 else \"Sin beneficio\"",
        ),
        Ejercicio(
            9,
            entorno,
            _validar_q9,
            "Calcula los dos límites y comprueba en orden: mercado, tamaño, pérdida y caso permitido.",
            "def evaluar_operacion(capital, valor_posicion, perdida_maxima, mercado_abierto):\n"
            "    limite_posicion = capital * 0.25\n"
            "    limite_perdida = capital * 0.02\n"
            "\n"
            "    if not mercado_abierto:\n"
            "        return \"Mercado cerrado\"\n"
            "    elif valor_posicion > limite_posicion:\n"
            "        return \"Posición demasiado grande\"\n"
            "    elif perdida_maxima > limite_perdida:\n"
            "        return \"Riesgo demasiado alto\"\n"
            "    else:\n"
            "        return \"Operación permitida\"",
        ),
    ]

    for ejercicio in ejercicios:
        entorno[f"q{ejercicio.numero}"] = ejercicio

    print("Preparación completada.")


__all__ = ["cargar"]
