"""Autocorrección de 1.7. Módulos y bibliotecas externas."""

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


def _es_modulo(objeto, nombre):
    return getattr(objeto, "__name__", None) == nombre


def _lista_numerica_igual(obtenida, esperada):
    try:
        valores = obtenida.tolist()
    except (AttributeError, TypeError):
        return False

    if not isinstance(valores, list) or len(valores) != len(esperada):
        return False
    return all(_casi_igual(valor, objetivo) for valor, objetivo in zip(valores, esperada))


def _validar_q1(entorno):
    if not _es_modulo(entorno.get("math"), "math"):
        return "importa el módulo math con su nombre original."
    if entorno.get("capital") != 1000 or entorno.get("precio_accion") != 37.50:
        return "no modifiques capital ni precio_accion."

    acciones = entorno.get("acciones")
    if type(acciones) is not int or acciones != 26:
        return "acciones debe ser el número entero de acciones que se pueden comprar."
    if not _casi_igual(entorno.get("efectivo_restante"), 25.0):
        return "calcula el efectivo restante después de comprar las acciones."
    return True


def _validar_q2(entorno):
    if not _es_modulo(entorno.get("stats"), "statistics"):
        return "importa statistics utilizando el alias stats."

    esperado = [101.20, 102.45, 100.80, 103.10, 104.25]
    if entorno.get("precios_cierre") != esperado:
        return "no modifiques la lista precios_cierre."
    if not _casi_igual(entorno.get("media"), 102.36):
        return "calcula media con la función mean() del módulo importado."
    if not _casi_igual(entorno.get("mediana"), 102.45):
        return "calcula mediana con la función median() del módulo importado."
    return True


def _validar_q3(entorno):
    funcion = entorno.get("sqrt")
    if (
        not callable(funcion)
        or getattr(funcion, "__module__", None) != "math"
        or getattr(funcion, "__name__", None) != "sqrt"
    ):
        return "importa sqrt directamente desde el módulo math."
    if entorno.get("sesiones") != 252 or entorno.get("volatilidad_diaria") != 0.012:
        return "no modifiques sesiones ni volatilidad_diaria."

    factor = 252 ** 0.5
    if not _casi_igual(entorno.get("factor_anualizacion"), factor):
        return "factor_anualizacion debe ser la raíz cuadrada de sesiones."
    if not _casi_igual(entorno.get("volatilidad_anual"), 0.012 * factor):
        return "multiplica volatilidad_diaria por factor_anualizacion."
    return True


def _validar_q4(entorno):
    stats = entorno.get("stats")
    if not _es_modulo(stats, "statistics"):
        return "importa statistics utilizando el alias stats."
    if entorno.get("tipo_stats") is not type(stats):
        return "guarda el resultado de type(stats) en tipo_stats."
    if entorno.get("nombres_stats") != dir(stats):
        return "guarda el resultado completo de dir(stats) en nombres_stats."
    if entorno.get("funcion_elegida") is not stats.mean:
        return "asigna stats.mean, sin paréntesis, a funcion_elegida."
    return True


def _validar_q5(entorno):
    if not _es_modulo(entorno.get("np"), "numpy"):
        return "importa numpy utilizando el alias np."
    if not _es_modulo(entorno.get("pd"), "pandas"):
        return "importa pandas utilizando el alias pd."
    if not _es_modulo(entorno.get("plt"), "matplotlib.pyplot"):
        return "importa matplotlib.pyplot utilizando el alias plt."

    esperado = {
        "arrays": "numpy",
        "datos_tabulares": "pandas",
        "graficos": "matplotlib.pyplot",
    }
    if entorno.get("bibliotecas") != esperado:
        return "completa bibliotecas con el atributo __name__ de cada alias."
    return True


def _validar_q6(entorno):
    esperado = {
        "modulo_inexistente": "ModuleNotFoundError",
        "nombre_sin_importar": "NameError",
        "atributo_inexistente": "AttributeError",
        "argumento_incompatible": "TypeError",
    }
    if entorno.get("tipos_error") != esperado:
        return "revisa qué tipo de error corresponde a cada fragmento."
    return True


def _validar_q7(entorno):
    if not _es_modulo(entorno.get("np"), "numpy"):
        return "importa numpy utilizando el alias np."

    precios = [101.20, 102.45, 100.80, 103.10, 104.25]
    if entorno.get("precios_cierre") != precios:
        return "no modifiques la lista precios_cierre."

    precios_array = entorno.get("precios_array")
    if type(precios_array).__module__.split(".")[0] != "numpy":
        return "convierte precios_cierre en un array de NumPy."
    if not _lista_numerica_igual(precios_array, precios):
        return "precios_array debe contener los precios originales."
    if entorno.get("tipo_array") is not type(precios_array):
        return "guarda type(precios_array) en tipo_array."
    if entorno.get("nombres_array") != dir(precios_array):
        return "guarda dir(precios_array) en nombres_array."
    if entorno.get("numero_precios") != 5:
        return "obtén el número de precios mediante el atributo size."
    if not _casi_igual(entorno.get("precio_medio"), 102.36):
        return "utiliza el método mean() del array para calcular la media."

    ajustados = entorno.get("precios_ajustados")
    esperado_ajustado = [101.70, 102.95, 101.30, 103.60, 104.75]
    if not _lista_numerica_igual(ajustados, esperado_ajustado):
        return "suma 0.50 al array completo para obtener precios_ajustados."
    return True


def cargar(entorno):
    """Carga en el notebook las preguntas de la lección."""

    ejercicios = [
        Ejercicio(1, entorno, _validar_q1),
        Ejercicio(
            2,
            entorno,
            _validar_q2,
            "Importa statistics as stats. Después llama a stats.mean() y "
            "stats.median() con la lista de precios.",
            "import statistics as stats\n\n"
            "media = stats.mean(precios_cierre)\n"
            "mediana = stats.median(precios_cierre)",
        ),
        Ejercicio(
            3,
            entorno,
            _validar_q3,
            "Utiliza from math import sqrt. Calcula primero sqrt(sesiones) y "
            "multiplica después la volatilidad diaria por ese factor.",
            "from math import sqrt\n\n"
            "factor_anualizacion = sqrt(sesiones)\n"
            "volatilidad_anual = volatilidad_diaria * factor_anualizacion",
        ),
        Ejercicio(4, entorno, _validar_q4),
        Ejercicio(
            5,
            entorno,
            _validar_q5,
            "Utiliza los alias np, pd y plt. El atributo __name__ de cada "
            "alias contiene el nombre que debes guardar en el diccionario.",
            "import numpy as np\n"
            "import pandas as pd\n"
            "import matplotlib.pyplot as plt\n\n"
            "bibliotecas = {\n"
            "    \"arrays\": np.__name__,\n"
            "    \"datos_tabulares\": pd.__name__,\n"
            "    \"graficos\": plt.__name__,\n"
            "}",
        ),
        Ejercicio(
            6,
            entorno,
            _validar_q6,
            "Relaciona, en este orden, un módulo que no se encuentra, un nombre "
            "no definido, un atributo ausente y un argumento del tipo incorrecto.",
            "tipos_error = {\n"
            "    \"modulo_inexistente\": \"ModuleNotFoundError\",\n"
            "    \"nombre_sin_importar\": \"NameError\",\n"
            "    \"atributo_inexistente\": \"AttributeError\",\n"
            "    \"argumento_incompatible\": \"TypeError\",\n"
            "}",
        ),
        Ejercicio(
            7,
            entorno,
            _validar_q7,
            "Crea el array con np.array(). Explóralo con type() y dir(); entre "
            "sus nombres encontrarás el atributo size y el método mean().",
            "import numpy as np\n\n"
            "precios_array = np.array(precios_cierre)\n"
            "tipo_array = type(precios_array)\n"
            "nombres_array = dir(precios_array)\n"
            "numero_precios = precios_array.size\n"
            "precio_medio = precios_array.mean()\n"
            "precios_ajustados = precios_array + 0.50",
        ),
    ]

    for ejercicio in ejercicios:
        entorno[f"q{ejercicio.numero}"] = ejercicio

    print("Preparación completada.")


__all__ = ["cargar"]
