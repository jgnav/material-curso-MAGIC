"""Autocorrección de 1.5. Bucles."""

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
    precios = [101.237, 102.456, 100.804]
    resultado = _validar_lista(entorno, "precios", precios)
    if resultado is not True:
        return "no modifiques la lista precios."
    return _validar_lista(
        entorno, "precios_redondeados", [101.24, 102.46, 100.80]
    )


def _validar_q2(entorno):
    variaciones = [0.8, -0.4, 0.0, 1.2, -0.7]
    resultado = _validar_lista(entorno, "variaciones_pct", variaciones)
    if resultado is not True:
        return "no modifiques la lista variaciones_pct."

    esperados = {
        "sesiones_positivas": 2,
        "sesiones_negativas": 2,
        "sesiones_sin_cambios": 1,
    }
    for nombre, esperado in esperados.items():
        if nombre not in entorno:
            return f"crea la variable {nombre}."
        if type(entorno[nombre]) is not int or entorno[nombre] != esperado:
            return f"{nombre} debe valer {esperado}."
    return True


def _validar_q3(entorno):
    precios = [100.00, 102.00, 101.00, 104.00]
    resultado = _validar_lista(entorno, "precios_cierre", precios)
    if resultado is not True:
        return "no modifiques la lista precios_cierre."
    return _validar_lista(entorno, "retornos_pct", [2.0, -0.98, 2.97])


def _validar_q4(entorno):
    precios = [101.20, 102.45, 100.80]
    resultado = _validar_lista(entorno, "precios_cierre", precios)
    if resultado is not True:
        return "no modifiques la lista precios_cierre."
    return _validar_lista(
        entorno,
        "sesiones_numeradas",
        [[1, 101.20], [2, 102.45], [3, 100.80]],
    )


def _validar_q5(entorno):
    if "dias" not in entorno:
        return "crea y actualiza la variable dias."
    if type(entorno["dias"]) is not int or entorno["dias"] != 5:
        return "el bucle debe terminar después de 5 días."
    if "capital" not in entorno:
        return "crea y actualiza la variable capital."
    if not _casi_igual(entorno["capital"], 1104.0808032):
        return "actualiza capital en cada vuelta aplicando la rentabilidad diaria."
    return True


def _validar_q6(entorno):
    variaciones = [0.0, 0.8, 0.0, 1.2, -0.6, -1.0]
    resultado = _validar_lista(entorno, "variaciones_pct", variaciones)
    if resultado is not True:
        return "no modifiques la lista variaciones_pct."

    resultado = _validar_lista(
        entorno, "variaciones_revisadas", [0.8, 1.2, -0.6]
    )
    if resultado is not True:
        return (
            "variaciones_revisadas debe omitir los ceros y detenerse "
            "después de la primera variación negativa."
        )
    if not _casi_igual(entorno.get("primera_caida"), -0.6):
        return "primera_caida debe guardar la primera variación negativa."
    return True


def _validar_q7(entorno):
    decimales = [0.008, -0.004, 0.012]
    resultado = _validar_lista(entorno, "variaciones_decimales", decimales)
    if resultado is not True:
        return "no modifiques la lista variaciones_decimales."
    return _validar_lista(entorno, "variaciones_pct", [0.8, -0.4, 1.2])


def _validar_q8(entorno):
    activos = [
        ["SAN", 1.4],
        ["IBE", -0.6],
        ["ITX", 0.9],
        ["REP", -1.2],
    ]
    resultado = _validar_lista(entorno, "activos", activos)
    if resultado is not True:
        return "no modifiques la lista anidada activos."

    resultado = _validar_lista(entorno, "tickers_positivos", ["SAN", "ITX"])
    if resultado is not True:
        return resultado
    return _validar_lista(entorno, "variaciones_negativas", [-0.6, -1.2])


def cargar(entorno):
    """Carga en el notebook las preguntas de la lección."""

    ejercicios = [
        Ejercicio(
            1,
            entorno,
            _validar_q1,
            "Recorre precios con for y añade round(precio, 2) a la nueva lista.",
            "precios_redondeados = []\n"
            "for precio in precios:\n"
            "    precios_redondeados.append(round(precio, 2))",
        ),
        Ejercicio(
            2,
            entorno,
            _validar_q2,
            "Inicializa los tres contadores a cero. Dentro del for, utiliza "
            "if, elif y else, y aumenta el contador correspondiente con += 1.",
            "sesiones_positivas = 0\n"
            "sesiones_negativas = 0\n"
            "sesiones_sin_cambios = 0\n"
            "\n"
            "for variacion in variaciones_pct:\n"
            "    if variacion > 0:\n"
            "        sesiones_positivas += 1\n"
            "    elif variacion < 0:\n"
            "        sesiones_negativas += 1\n"
            "    else:\n"
            "        sesiones_sin_cambios += 1",
        ),
        Ejercicio(
            3,
            entorno,
            _validar_q3,
            "Recorre range(1, len(precios_cierre)). El precio actual está en "
            "indice y el anterior en indice - 1.",
            "retornos_pct = []\n"
            "for indice in range(1, len(precios_cierre)):\n"
            "    precio_anterior = precios_cierre[indice - 1]\n"
            "    precio_actual = precios_cierre[indice]\n"
            "    retorno = (precio_actual / precio_anterior - 1) * 100\n"
            "    retornos_pct.append(round(retorno, 2))",
        ),
        Ejercicio(
            4,
            entorno,
            _validar_q4,
            "Utiliza enumerate(precios_cierre, start=1). En cada vuelta, añade "
            "[numero_sesion, precio] a sesiones_numeradas.",
            "sesiones_numeradas = []\n"
            "for numero_sesion, precio in enumerate(precios_cierre, start=1):\n"
            "    sesiones_numeradas.append([numero_sesion, precio])",
        ),
        Ejercicio(
            5,
            entorno,
            _validar_q5,
            "La condición debe ser capital < objetivo. En cada vuelta, multiplica "
            "capital por 1 + rentabilidad_diaria y aumenta dias.",
            "while capital < objetivo:\n"
            "    capital = capital * (1 + rentabilidad_diaria)\n"
            "    dias += 1",
        ),
        Ejercicio(
            6,
            entorno,
            _validar_q6,
            "Si la variación es cero, ejecuta continue. Para los demás valores, "
            "añade la variación y, si es negativa, guárdala y ejecuta break.",
            "for variacion in variaciones_pct:\n"
            "    if variacion == 0:\n"
            "        continue\n"
            "    variaciones_revisadas.append(variacion)\n"
            "    if variacion < 0:\n"
            "        primera_caida = variacion\n"
            "        break",
        ),
        Ejercicio(
            7,
            entorno,
            _validar_q7,
            "La expresión que se guarda es variacion * 100 y la secuencia es "
            "variaciones_decimales.",
            "variaciones_pct = [\n"
            "    variacion * 100\n"
            "    for variacion in variaciones_decimales\n"
            "]",
        ),
        Ejercicio(
            8,
            entorno,
            _validar_q8,
            "En cada lista interior, activo[0] es el ticker y activo[1] es la "
            "variación. Añade una condición al final de cada comprensión.",
            "tickers_positivos = [\n"
            "    activo[0] for activo in activos if activo[1] > 0\n"
            "]\n"
            "variaciones_negativas = [\n"
            "    activo[1] for activo in activos if activo[1] < 0\n"
            "]",
        ),
    ]

    for ejercicio in ejercicios:
        entorno[f"q{ejercicio.numero}"] = ejercicio

    print("Preparación completada.")


__all__ = ["cargar"]
