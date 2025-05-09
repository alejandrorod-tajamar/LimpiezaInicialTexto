
"""Módulo para la gestión personalizada de stopwords en análisis de reseñas.

Este módulo contiene funciones para cargar, personalizar y aplicar stopwords
en el contexto de análisis de reseñas de productos, preservando términos
críticos como negaciones y conectores de contraste.
"""

import spacy
import pandas as pd
from collections import Counter

# Cargar modelo de spaCy
try:
    nlp = spacy.load("es_core_news_sm")
except OSError:
    print("El modelo de spaCy para español no está instalado.")
    print("Instálalo con: python -m spacy download es_core_news_sm")
    raise


def cargar_stopwords_personalizadas(ruta_archivo=None):
    """Carga la lista personalizada de stopwords.

    Args:
        ruta_archivo (str, optional): Ruta al archivo con stopwords personalizadas.
            Si es None, retorna la lista predefinida en este módulo.

    Returns:
        set: Conjunto de stopwords personalizadas
    """
    if ruta_archivo:
        try:
            with open(ruta_archivo, "r", encoding="utf-8") as f:
                return set(line.strip() for line in f)
        except FileNotFoundError:
            print(f"Archivo {ruta_archivo} no encontrado. Usando lista predefinida.")

    # Lista predefinida (stopwords de spaCy con modificaciones)
    stopwords_personalizadas = set(nlp.Defaults.stop_words)

    # Términos clave a preservar
    terminos_a_preservar = [
        "no", "nunca", "tampoco",  # Negaciones
        "pero", "aunque", "sin", "embargo"  # Conectores de contraste
    ]

    # Términos genéricos a eliminar
    terminos_genericos = [
        "producto", "cliente", "día",  # Palabras redundantes
        "hacer", "tener", "decir",     # Verbos comunes sin contexto
        "hola", "gracias", "pd"       # Términos no informativos
    ]

    # Modificar la lista
    for termino in terminos_a_preservar:
        if termino in stopwords_personalizadas:
            stopwords_personalizadas.remove(termino)

    for termino in terminos_genericos:
        stopwords_personalizadas.add(termino)

    return stopwords_personalizadas


def procesar_texto(texto, stopwords=None, conservar_stopwords=False):
    """Procesa texto eliminando o conservando stopwords.

    Args:
        texto (str): Texto a procesar
        stopwords (set, optional): Conjunto de stopwords a utilizar.
            Si es None, usa las stopwords por defecto de spaCy.
        conservar_stopwords (bool): Si es True, conserva todas las stopwords.

    Returns:
        list: Lista de tokens procesados
    """
    doc = nlp(texto)

    if conservar_stopwords:
        return [token.text.lower() for token in doc if not token.is_punct]

    if stopwords is None:
        # Usar stopwords por defecto de spaCy
        return [token.text.lower() for token in doc 
                if not token.is_stop and not token.is_punct]
    else:
        # Usar lista personalizada de stopwords
        return [token.text.lower() for token in doc 
                if token.text.lower() not in stopwords and not token.is_punct]


def analizar_frecuencia(textos):
    """Analiza la frecuencia de palabras en un conjunto de textos.

    Args:
        textos (list or Series): Lista o Series de textos a analizar

    Returns:
        Counter: Contador con las frecuencias de palabras
    """
    if isinstance(textos, pd.Series):
        textos = textos.astype(str).values

    # Concatenar todos los textos
    texto_completo = " ".join(textos)
    doc = nlp(texto_completo)

    # Contar palabras (excluyendo puntuación)
    palabras = [token.text.lower() for token in doc if not token.is_punct]
    return Counter(palabras)


def guardar_stopwords(stopwords, ruta_archivo):
    """Guarda la lista de stopwords en un archivo.

    Args:
        stopwords (set): Conjunto de stopwords a guardar
        ruta_archivo (str): Ruta donde guardar el archivo
    """
    with open(ruta_archivo, "w", encoding="utf-8") as f:
        for word in sorted(stopwords):
            f.write(word + "
")
    print(f"Lista de stopwords guardada en {ruta_archivo}")


def evaluar_precision(casos_prueba, stopwords):
    """Evalúa la precisión de la lista de stopwords en casos de prueba.

    Args:
        casos_prueba (list): Lista de diccionarios con casos de prueba.
            Cada diccionario debe tener las claves "texto" y "esperado".
        stopwords (set): Conjunto de stopwords a evaluar

    Returns:
        float: Precisión promedio (0-100)
    """
    resultados = []
    for caso in casos_prueba:
        resultado = procesar_texto(caso["texto"], stopwords)
        precision = len(set(caso["esperado"]) & set(resultado)) / len(set(caso["esperado"])) * 100
        resultados.append(precision)

    return sum(resultados) / len(resultados)


if __name__ == "__main__":
    # Ejemplo de uso
    print("Módulo de procesamiento de stopwords personalizadas")
    print("Ejemplo de uso:")

    texto_ejemplo = "No recomiendo este producto. Aunque es barato, se rompió en dos días."

    # Procesamiento con stopwords por defecto
    print("
Procesamiento con stopwords por defecto:")
    tokens_default = procesar_texto(texto_ejemplo)
    print(tokens_default)

    # Procesamiento con stopwords personalizadas
    print("
Procesamiento con stopwords personalizadas:")
    stopwords_custom = cargar_stopwords_personalizadas()
    tokens_custom = procesar_texto(texto_ejemplo, stopwords_custom)
    print(tokens_custom)
