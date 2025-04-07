import pandas as pd
from pandas import Timestamp
import codecs
import re


def clean_date(date_str):
    """
    Función para uniformizar fechas a formato yyyy-MM-dd HH:mm:ss
    """
    return pd.to_datetime(date_str)

def clean_body(body_str):
    """
    Unir el texto extraído y limpiar saltos de línea
    """
    
    clean_text = "".join(body_str).replace("\n", " ").strip()
    return clean_text

def convert_timestamps(obj):
    if isinstance(obj, dict):
        return {k: convert_timestamps(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_timestamps(elem) for elem in obj]
    elif isinstance(obj, Timestamp):
        return obj.strftime('%Y-%m-%d %H:%M:%S')
    return obj

def decode_text(text):
    """
    Decodifica caracteres unicode escapados (\u2019, etc.) a texto legible.
    """
    try:
        return codecs.decode(text, 'unicode_escape')
    except Exception:
        return text  # si falla, devuelve el texto original sin modificar
    
def fix_encoding_issues(text):
    try:
        return text.encode('latin1').decode('utf-8')
    except (UnicodeEncodeError, UnicodeDecodeError):
        return text
def remove_links(text):
    """Remove URLs from text"""
    if not text:
        return text

    # Common URL pattern
    url_pattern = r'https[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    # remove URL
    text = re.sub(url_pattern, '', text)

    text = re.sub(r'www\.[^\s]+','', text)

    return text.strip()

def remove_spaces(text):
   # Reemplazar secuencias de espacios múltiples por un solo espacio
    text_cleaned = re.sub(r'\s+', ' ', text)

    # Eliminar los espacios al principio y al final
    text_cleaned = text_cleaned.strip()
    return text_cleaned