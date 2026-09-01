"""Autocorrección de 1.6. Strings y diccionarios."""

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


def _validar_diccionario(entorno, nombre, esperado):
    if nombre not in entorno:
        return f"crea la variable {nombre}."
    if type(entorno[nombre]) is not dict:
        return f"{nombre} debe ser un diccionario."
    if entorno[nombre] != esperado:
        return f"{nombre} debería valer {esperado!r}."
    return True


def _validar_q1(entorno):
    if entorno.get("codigo") != "SAN.MC":
        return "no modifiques el string codigo."

    esperados = {
        "primer_caracter": "S",
        "ticker": "SAN",
        "mercado": "MC",
        "longitud_codigo": 6,
    }
    for nombre, esperado in esperados.items():
        if nombre not in entorno:
            return f"crea la variable {nombre}."
        if entorno[nombre] != esperado:
            return f"{nombre} debe valer {esperado!r}."
    return True


def _validar_q2(entorno):
    if entorno.get("codigo_usuario") != "  san.mc  ":
        return "no modifiques el string codigo_usuario."

    esperados = {
        "codigo_limpio": "SAN.MC",
        "ticker": "SAN",
    }
    for nombre, esperado in esperados.items():
        if nombre not in entorno:
            return f"crea la variable {nombre}."
        if entorno[nombre] != esperado:
            return f"{nombre} debe valer {esperado!r}."

    obtenido = entorno.get("es_mercado_continuo")
    if type(obtenido) is not bool or obtenido is not True:
        return "es_mercado_continuo debe ser el booleano True."
    return True


def _validar_q3(entorno):
    if entorno.get("registro") != "SAN,4.58,25":
        return "no modifiques el string registro."

    resultado = _validar_lista(entorno, "campos", ["SAN", "4.58", "25"])
    if resultado is not True:
        return resultado
    if entorno.get("resumen") != "SAN | 4.58 | 25":
        return "resumen debe unir los campos con el separador ' | '."
    return True


def _validar_q4(entorno):
    esperado = "SAN: 4.58 € | retorno: 1.37%"
    if entorno.get("mensaje") != esperado:
        return f"mensaje debería valer {esperado!r}."
    return True


def _validar_q5(entorno):
    esperado = {"SAN": 4.58, "IBE": 12.40, "ITX": 47.20}
    resultado = _validar_diccionario(entorno, "precios", esperado)
    if resultado is not True:
        return resultado

    if not _casi_igual(entorno.get("precio_san"), 4.58):
        return "precio_san debe obtenerse mediante la clave 'SAN'."
    obtenido = entorno.get("incluye_ibe")
    if type(obtenido) is not bool or obtenido is not True:
        return "incluye_ibe debe ser el booleano True."
    if entorno.get("precio_bbva") != "No disponible":
        return "utiliza get() para obtener 'No disponible' cuando falte BBVA."
    return True


def _validar_q6(entorno):
    esperado = {"SAN": 4.62, "IBE": 12.40, "REP": 13.85}
    resultado = _validar_diccionario(entorno, "precios", esperado)
    if resultado is not True:
        return resultado

    resultado = _validar_lista(entorno, "tickers", ["SAN", "IBE", "REP"])
    if resultado is not True:
        return resultado
    return _validar_lista(entorno, "valores", [4.62, 12.40, 13.85])


def _validar_q7(entorno):
    esperado = {"SAN": 25, "IBE": 10, "ITX": 5}
    resultado = _validar_diccionario(entorno, "cantidades", esperado)
    if resultado is not True:
        return "no modifiques el diccionario cantidades."
    return _validar_lista(
        entorno,
        "resumen",
        ["SAN: 25 acciones", "IBE: 10 acciones", "ITX: 5 acciones"],
    )


def _validar_q8(entorno):
    cartera_esperada = {
        "SAN": {"cantidad": 25, "precio_compra": 4.58},
        "IBE": {"cantidad": 10, "precio_compra": 12.40},
        "ITX": {"cantidad": 5, "precio_compra": 47.20},
    }
    resultado = _validar_diccionario(entorno, "cartera", cartera_esperada)
    if resultado is not True:
        return "no modifiques el diccionario anidado cartera."

    valores_esperados = {"SAN": 114.50, "IBE": 124.00, "ITX": 236.00}
    resultado = _validar_diccionario(
        entorno, "valores_posicion", valores_esperados
    )
    if resultado is not True:
        return resultado

    if not _casi_igual(entorno.get("valor_total"), 474.50):
        return "valor_total debe acumular el valor de las tres posiciones."
    return True


def cargar(entorno):
    """Carga en el notebook las preguntas de la lección."""

    ejercicios = [
        Ejercicio(1, entorno, _validar_q1),
        Ejercicio(
            2,
            entorno,
            _validar_q2,
            "Aplica strip() y upper() para limpiar el código. Después usa "
            "replace() y endswith() sobre el resultado.",
            "codigo_limpio = codigo_usuario.strip().upper()\n"
            "ticker = codigo_limpio.replace(\".MC\", \"\")\n"
            "es_mercado_continuo = codigo_limpio.endswith(\".MC\")",
        ),
        Ejercicio(
            3,
            entorno,
            _validar_q3,
            "Divide registro por las comas con split(). Después llama a join() "
            "sobre el string que servirá como separador.",
            "campos = registro.split(\",\")\n"
            "resumen = \" | \".join(campos)",
        ),
        Ejercicio(
            4,
            entorno,
            _validar_q4,
            "Escribe una f-string. Utiliza :.2f para precio y :.2% para retorno.",
            "mensaje = f\"{ticker}: {precio:.2f} € | retorno: {retorno:.2%}\"",
        ),
        Ejercicio(
            5,
            entorno,
            _validar_q5,
            "Crea las tres parejas entre llaves. Accede a SAN con corchetes, "
            "comprueba IBE con in y busca BBVA con get().",
            "precios = {\"SAN\": 4.58, \"IBE\": 12.40, \"ITX\": 47.20}\n"
            "precio_san = precios[\"SAN\"]\n"
            "incluye_ibe = \"IBE\" in precios\n"
            "precio_bbva = precios.get(\"BBVA\", \"No disponible\")",
        ),
        Ejercicio(
            6,
            entorno,
            _validar_q6,
            "Asigna el nuevo precio a precios['SAN'] y añade REP del mismo modo. "
            "Convierte keys() y values() a listas.",
            "precios[\"SAN\"] = 4.62\n"
            "precios[\"REP\"] = 13.85\n"
            "tickers = list(precios.keys())\n"
            "valores = list(precios.values())",
        ),
        Ejercicio(
            7,
            entorno,
            _validar_q7,
            "Recorre cantidades.items() con dos variables y añade una f-string "
            "a resumen en cada vuelta.",
            "for ticker, cantidad in cantidades.items():\n"
            "    resumen.append(f\"{ticker}: {cantidad} acciones\")",
        ),
        Ejercicio(
            8,
            entorno,
            _validar_q8,
            "Recorre cartera.items(). Calcula cantidad por precio_compra, guarda "
            "el resultado redondeado bajo la clave ticker y súmalo a valor_total.",
            "for ticker, datos in cartera.items():\n"
            "    valor = datos[\"cantidad\"] * datos[\"precio_compra\"]\n"
            "    valores_posicion[ticker] = round(valor, 2)\n"
            "    valor_total += valor",
        ),
    ]

    for ejercicio in ejercicios:
        entorno[f"q{ejercicio.numero}"] = ejercicio

    print("Preparación completada.")


__all__ = ["cargar"]
