import pandas as pd
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
