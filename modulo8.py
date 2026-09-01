"""Autocorrección de 2.1. Pandas para análisis de datos."""

from html import escape
from math import isclose
from numbers import Real
from pathlib import Path


_DATOS_CSV = """Date,Open,High,Low,Close,Volume
2026-01-02,100.0,102.0,99.5,101.5,120000
2026-01-05,101.5,103.0,100.8,102.4,135000
2026-01-06,102.4,103.2,101.0,101.7,
2026-01-07,101.7,104.0,101.4,103.6,150000
2026-01-08,103.6,105.1,103.2,104.8,142000
2026-01-09,104.8,106.0,104.1,105.4,158000
"""

_COLUMNAS = ["Date", "Open", "High", "Low", "Close", "Volume"]
_FECHAS = [
    "2026-01-02",
    "2026-01-05",
    "2026-01-06",
    "2026-01-07",
    "2026-01-08",
    "2026-01-09",
]
_APERTURAS = [100.0, 101.5, 102.4, 101.7, 103.6, 104.8]
_MAXIMOS = [102.0, 103.0, 103.2, 104.0, 105.1, 106.0]
_MINIMOS = [99.5, 100.8, 101.0, 101.4, 103.2, 104.1]
_CIERRES = [101.5, 102.4, 101.7, 103.6, 104.8, 105.4]
_VOLUMENES = [120000.0, 135000.0, None, 150000.0, 142000.0, 158000.0]


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


def _preparar_datos():
    Path("historico.csv").write_text(_DATOS_CSV, encoding="utf-8")


def _es_modulo_pandas(objeto):
    return getattr(objeto, "__name__", None) == "pandas"


def _es_dataframe(objeto):
    tipo = type(objeto)
    return tipo.__name__ == "DataFrame" and tipo.__module__.startswith("pandas.")


def _es_serie(objeto):
    tipo = type(objeto)
    return tipo.__name__ == "Series" and tipo.__module__.startswith("pandas.")


def _es_ausente(valor):
    try:
        return bool(valor != valor)
    except Exception:
        return False


def _casi_igual(valor, esperado):
    if not isinstance(valor, Real) or isinstance(valor, bool):
        return False
    return isclose(float(valor), float(esperado), rel_tol=1e-9, abs_tol=1e-9)


def _lista_numerica_igual(obtenida, esperada):
    try:
        valores = list(obtenida)
    except TypeError:
        return False
    if len(valores) != len(esperada):
        return False

    for valor, objetivo in zip(valores, esperada):
        if objetivo is None:
            if not _es_ausente(valor):
                return False
        elif not _casi_igual(valor, objetivo):
            return False
    return True


def _fechas_igual(obtenidas, esperadas=_FECHAS):
    try:
        valores = list(obtenidas)
    except TypeError:
        return False

    normalizadas = []
    for valor in valores:
        if hasattr(valor, "strftime"):
            normalizadas.append(valor.strftime("%Y-%m-%d"))
        else:
            normalizadas.append(str(valor))
    return normalizadas == esperadas


def _columnas_iguales(dataframe, esperadas):
    try:
        return list(dataframe.columns) == esperadas
    except Exception:
        return False


def _indice_igual(objeto, esperado):
    try:
        return list(objeto.index) == esperado
    except Exception:
        return False


def _validar_mercado(objeto):
    if not _es_dataframe(objeto):
        return "mercado debe ser un DataFrame de Pandas."
    if objeto.shape != (6, 6) or not _columnas_iguales(objeto, _COLUMNAS):
        return "carga las seis filas y las seis columnas de historico.csv."
    if not _fechas_igual(objeto["Date"]):
        return "la columna Date no coincide con el archivo original."
    if not _lista_numerica_igual(objeto["Open"], _APERTURAS):
        return "la columna Open no coincide con el archivo original."
    if not _lista_numerica_igual(objeto["High"], _MAXIMOS):
        return "la columna High no coincide con el archivo original."
    if not _lista_numerica_igual(objeto["Low"], _MINIMOS):
        return "la columna Low no coincide con el archivo original."
    if not _lista_numerica_igual(objeto["Close"], _CIERRES):
        return "la columna Close no coincide con el archivo original."
    if not _lista_numerica_igual(objeto["Volume"], _VOLUMENES):
        return "la columna Volume no coincide con el archivo original."
    return True


def _validar_q1(entorno):
    if not _es_modulo_pandas(entorno.get("pd")):
        return "importa pandas utilizando el alias pd."

    cartera = entorno.get("cartera")
    if not _es_dataframe(cartera):
        return "cartera debe ser un DataFrame."
    if cartera.shape != (3, 2):
        return "cartera debe tener tres filas y dos columnas."
    if not _columnas_iguales(cartera, ["Ticker", "Cantidad"]):
        return "las columnas deben llamarse Ticker y Cantidad, en ese orden."
    if list(cartera["Ticker"]) != ["SAN", "IBE", "ITX"]:
        return "revisa los valores de la columna Ticker."
    if list(cartera["Cantidad"]) != [25, 10, 5]:
        return "revisa los valores de la columna Cantidad."
    return True


def _validar_q2(entorno):
    if not _es_modulo_pandas(entorno.get("pd")):
        return "importa pandas utilizando el alias pd."
    return _validar_mercado(entorno.get("mercado"))


def _validar_q3(entorno):
    mercado = entorno.get("mercado")
    resultado = _validar_mercado(mercado)
    if resultado is not True:
        return "ejecuta correctamente la pregunta anterior antes de continuar."
    if entorno.get("dimensiones") != (6, 6):
        return "guarda mercado.shape en dimensiones."

    primeras = entorno.get("primeras_tres")
    if not _es_dataframe(primeras) or primeras.shape != (3, 6):
        return "primeras_tres debe contener las tres primeras filas."
    if not _indice_igual(primeras, [0, 1, 2]):
        return "utiliza head(3) para conservar las primeras tres filas."
    if not _lista_numerica_igual(primeras["Close"], _CIERRES[:3]):
        return "primeras_tres no contiene los cierres esperados."

    ultimas = entorno.get("ultimas_dos")
    if not _es_dataframe(ultimas) or ultimas.shape != (2, 6):
        return "ultimas_dos debe contener las dos últimas filas."
    if not _indice_igual(ultimas, [4, 5]):
        return "utiliza tail(2) para conservar las dos últimas filas."

    resumen = entorno.get("resumen_numerico")
    if not _es_dataframe(resumen) or resumen.shape != (8, 5):
        return "resumen_numerico debe ser el resultado de mercado.describe()."
    if not _columnas_iguales(resumen, ["Open", "High", "Low", "Close", "Volume"]):
        return "resumen_numerico debe describir las cinco columnas numéricas."
    if list(resumen.index) != ["count", "mean", "std", "min", "25%", "50%", "75%", "max"]:
        return "guarda el resultado completo de describe()."
    if not _casi_igual(resumen.loc["count", "Close"], 6):
        return "el resumen debe incluir los seis cierres."
    if not _casi_igual(resumen.loc["count", "Volume"], 5):
        return "el resumen debe reflejar que falta un valor de Volume."
    return True


def _validar_q4(entorno):
    mercado = entorno.get("mercado")
    resultado = _validar_mercado(mercado)
    if resultado is not True:
        return "no modifiques el DataFrame mercado."

    cierres = entorno.get("cierres")
    if not _es_serie(cierres) or getattr(cierres, "name", None) != "Close":
        return "cierres debe ser la Series obtenida al seleccionar Close."
    if not _lista_numerica_igual(cierres, _CIERRES):
        return "cierres no contiene todos los precios de cierre."

    seleccion = entorno.get("fecha_y_cierre")
    if not _es_dataframe(seleccion):
        return "fecha_y_cierre debe ser un DataFrame."
    if not _columnas_iguales(seleccion, ["Date", "Close"]):
        return "selecciona Date y Close, en ese orden."
    if seleccion.shape != (6, 2) or not _fechas_igual(seleccion["Date"]):
        return "fecha_y_cierre debe conservar las seis filas."
    return True


def _validar_q5(entorno):
    primera = entorno.get("primera_fila")
    if not _es_serie(primera) or getattr(primera, "name", None) != 0:
        return "primera_fila debe obtenerse con iloc[0]."
    if not _casi_igual(primera["Close"], 101.5):
        return "primera_fila no contiene el primer cierre."

    primeros = entorno.get("primeros_cierres")
    if not _es_dataframe(primeros):
        return "primeros_cierres debe ser un DataFrame."
    if not _columnas_iguales(primeros, ["Date", "Close"]):
        return "primeros_cierres debe contener Date y Close."
    if not _indice_igual(primeros, [0, 1, 2]):
        return "selecciona las tres primeras filas por posición."
    if not _lista_numerica_igual(primeros["Close"], _CIERRES[:3]):
        return "revisa la selección de los tres primeros cierres."

    if not _casi_igual(entorno.get("primer_cierre"), 101.5):
        return "utiliza loc para obtener Close en la etiqueta de fila 0."
    return True


def _validar_q6(entorno):
    sesiones = entorno.get("sesiones_alcistas")
    if not _es_dataframe(sesiones):
        return "sesiones_alcistas debe ser un DataFrame."
    if not _columnas_iguales(sesiones, ["Date", "Open", "Close"]):
        return "selecciona únicamente Date, Open y Close."
    if not _indice_igual(sesiones, [0, 1, 3, 4, 5]):
        return "la condición debe conservar las sesiones con Close mayor que Open."
    if not _lista_numerica_igual(
        sesiones["Close"], [101.5, 102.4, 103.6, 104.8, 105.4]
    ):
        return "revisa los cierres seleccionados por la condición."
    return True


def _validar_q7(entorno):
    mercado_fechas = entorno.get("mercado_fechas")
    if not _es_dataframe(mercado_fechas):
        return "mercado_fechas debe ser una copia de mercado."
    if mercado_fechas.shape != (6, 6):
        return "mercado_fechas debe conservar todas las filas y columnas."
    if not _fechas_igual(mercado_fechas["Date"]):
        return "la columna Date debe conservar las seis fechas."
    if not str(mercado_fechas["Date"].dtype).startswith("datetime64"):
        return "convierte Date mediante pd.to_datetime()."
    if str(entorno.get("tipo_fecha")) != str(mercado_fechas["Date"].dtype):
        return "guarda el dtype de la columna Date en tipo_fecha."
    return True


def _validar_q8(entorno):
    mercado = entorno.get("mercado")
    resultado = _validar_mercado(mercado)
    if resultado is not True:
        return "no modifiques mercado; realiza la limpieza sobre una copia."

    ausentes = entorno.get("ausentes_por_columna")
    if not _es_serie(ausentes) or list(ausentes.index) != _COLUMNAS:
        return "ausentes_por_columna debe ser una Series con todas las columnas."
    if list(ausentes) != [0, 0, 0, 0, 0, 1]:
        return "cuenta los valores ausentes con isna().sum()."
    if not _casi_igual(entorno.get("volumen_mediano"), 142000.0):
        return "calcula la mediana de Volume antes de sustituir el valor."

    limpio = entorno.get("mercado_limpio")
    if not _es_dataframe(limpio) or limpio.shape != (6, 6):
        return "mercado_limpio debe conservar las seis filas."
    esperado = [120000, 135000, 142000, 150000, 142000, 158000]
    if not _lista_numerica_igual(limpio["Volume"], esperado):
        return "sustituye el volumen ausente por volumen_mediano."
    return True


def _validar_q9(entorno):
    calculado = entorno.get("mercado_calculado")
    if not _es_dataframe(calculado):
        return "mercado_calculado debe ser un DataFrame."
    columnas = _COLUMNAS + ["Rango", "Variacion"]
    if calculado.shape != (6, 8) or not _columnas_iguales(calculado, columnas):
        return "añade Rango y Variacion sin eliminar las columnas originales."

    rangos = [2.5, 2.2, 2.2, 2.6, 1.9, 1.9]
    variaciones = [1.5, 0.9, -0.7, 1.9, 1.2, 0.6]
    if not _lista_numerica_igual(calculado["Rango"], rangos):
        return "Rango debe ser High menos Low en cada fila."
    if not _lista_numerica_igual(calculado["Variacion"], variaciones):
        return "Variacion debe ser Close menos Open en cada fila."
    return True


def _validar_q10(entorno):
    retornos = entorno.get("mercado_retornos")
    if not _es_dataframe(retornos):
        return "mercado_retornos debe ser un DataFrame."
    if not _columnas_iguales(retornos, _COLUMNAS + ["Retorno"]):
        return "añade Retorno sin eliminar las columnas originales."

    esperados = [
        None,
        102.4 / 101.5 - 1,
        101.7 / 102.4 - 1,
        103.6 / 101.7 - 1,
        104.8 / 103.6 - 1,
        105.4 / 104.8 - 1,
    ]
    if not _lista_numerica_igual(retornos["Retorno"], esperados):
        return "calcula Retorno con pct_change(fill_method=None) sobre Close."
    return True


def _validar_q11(entorno):
    analisis = entorno.get("analisis")
    if not _es_dataframe(analisis):
        return "analisis debe ser un DataFrame."
    if not str(analisis["Date"].dtype).startswith("datetime64"):
        return "convierte Date a un tipo de fecha."
    if not _lista_numerica_igual(
        analisis["Volume"], [120000, 135000, 142000, 150000, 142000, 158000]
    ):
        return "sustituye el volumen ausente por la mediana."

    retornos_esperados = [
        None,
        102.4 / 101.5 - 1,
        101.7 / 102.4 - 1,
        103.6 / 101.7 - 1,
        104.8 / 103.6 - 1,
        105.4 / 104.8 - 1,
    ]
    if not _lista_numerica_igual(analisis["Retorno"], retornos_esperados):
        return "calcula de nuevo la columna Retorno sobre analisis."

    medias = [None, None, 101.8666666667, 102.5666666667, 103.3666666667, 104.6]
    if not _lista_numerica_igual(analisis["Media_movil_3"], medias):
        return "calcula Media_movil_3 con una ventana de tres cierres."

    resultado = entorno.get("resultado")
    if not _es_dataframe(resultado):
        return "resultado debe ser un DataFrame."
    columnas = ["Date", "Close", "Retorno", "Media_movil_3"]
    if resultado.shape != (6, 4) or not _columnas_iguales(resultado, columnas):
        return "selecciona las cuatro columnas indicadas, en ese orden."
    if not _fechas_igual(resultado["Date"]):
        return "resultado debe conservar las seis fechas."
    return True


def cargar(entorno):
    """Prepara los datos y carga en el notebook las preguntas de la lección."""

    _preparar_datos()
    ejercicios = [
        Ejercicio(1, entorno, _validar_q1),
        Ejercicio(2, entorno, _validar_q2),
        Ejercicio(
            3,
            entorno,
            _validar_q3,
            "shape es un atributo. Para las filas, llama a head(3) y tail(2) "
            "sobre mercado. El resumen se obtiene con describe().",
            "dimensiones = mercado.shape\n"
            "primeras_tres = mercado.head(3)\n"
            "ultimas_dos = mercado.tail(2)\n"
            "resumen_numerico = mercado.describe()",
        ),
        Ejercicio(
            4,
            entorno,
            _validar_q4,
            "Un nombre entre corchetes devuelve una Series. Una lista de nombres "
            "entre los corchetes devuelve un DataFrame.",
            "cierres = mercado[\"Close\"]\n"
            "fecha_y_cierre = mercado[[\"Date\", \"Close\"]]",
        ),
        Ejercicio(
            5,
            entorno,
            _validar_q5,
            "Utiliza iloc para las posiciones y loc[0, 'Close'] para la etiqueta "
            "y el nombre de columna.",
            "primera_fila = mercado.iloc[0]\n"
            "primeros_cierres = mercado.iloc[:3, [0, 4]]\n"
            "primer_cierre = mercado.loc[0, \"Close\"]",
        ),
        Ejercicio(
            6,
            entorno,
            _validar_q6,
            "Coloca la comparación entre Close y Open como primer argumento de "
            "loc y la lista de columnas como segundo argumento.",
            "sesiones_alcistas = mercado.loc[\n"
            "    mercado[\"Close\"] > mercado[\"Open\"],\n"
            "    [\"Date\", \"Open\", \"Close\"],\n"
            "]",
        ),
        Ejercicio(
            7,
            entorno,
            _validar_q7,
            "Copia mercado, asigna pd.to_datetime(mercado_fechas['Date']) a la "
            "misma columna y consulta después su dtype.",
            "mercado_fechas = mercado.copy()\n"
            "mercado_fechas[\"Date\"] = pd.to_datetime(mercado_fechas[\"Date\"])\n"
            "tipo_fecha = mercado_fechas[\"Date\"].dtype",
        ),
        Ejercicio(
            8,
            entorno,
            _validar_q8,
            "Cuenta los ausentes con isna().sum(). Trabaja sobre mercado.copy(), "
            "calcula la mediana de Volume y pásala a fillna().",
            "ausentes_por_columna = mercado.isna().sum()\n"
            "mercado_limpio = mercado.copy()\n"
            "volumen_mediano = mercado_limpio[\"Volume\"].median()\n"
            "mercado_limpio[\"Volume\"] = (\n"
            "    mercado_limpio[\"Volume\"].fillna(volumen_mediano)\n"
            ")",
        ),
        Ejercicio(
            9,
            entorno,
            _validar_q9,
            "Crea una copia y asigna a cada nueva columna la resta entre las dos "
            "Series correspondientes.",
            "mercado_calculado = mercado.copy()\n"
            "mercado_calculado[\"Rango\"] = (\n"
            "    mercado_calculado[\"High\"] - mercado_calculado[\"Low\"]\n"
            ")\n"
            "mercado_calculado[\"Variacion\"] = (\n"
            "    mercado_calculado[\"Close\"] - mercado_calculado[\"Open\"]\n"
            ")",
        ),
        Ejercicio(
            10,
            entorno,
            _validar_q10,
            "Crea una copia y llama a pct_change(fill_method=None) sobre su "
            "columna Close.",
            "mercado_retornos = mercado.copy()\n"
            "mercado_retornos[\"Retorno\"] = (\n"
            "    mercado_retornos[\"Close\"].pct_change(fill_method=None)\n"
            ")",
        ),
        Ejercicio(
            11,
            entorno,
            _validar_q11,
            "Repite la conversión y la limpieza sobre analisis. Para la media "
            "móvil encadena rolling(window=3).mean() sobre Close.",
            "analisis = mercado.copy()\n"
            "analisis[\"Date\"] = pd.to_datetime(analisis[\"Date\"])\n"
            "analisis[\"Volume\"] = analisis[\"Volume\"].fillna(\n"
            "    analisis[\"Volume\"].median()\n"
            ")\n"
            "analisis[\"Retorno\"] = analisis[\"Close\"].pct_change(\n"
            "    fill_method=None\n"
            ")\n"
            "analisis[\"Media_movil_3\"] = (\n"
            "    analisis[\"Close\"].rolling(window=3).mean()\n"
            ")\n"
            "resultado = analisis[[\n"
            "    \"Date\", \"Close\", \"Retorno\", \"Media_movil_3\"\n"
            "]]",
        ),
    ]

    for ejercicio in ejercicios:
        entorno[f"q{ejercicio.numero}"] = ejercicio

    print("Preparación completada.")


__all__ = ["cargar"]
