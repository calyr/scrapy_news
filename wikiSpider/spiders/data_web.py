ALLOWED_DOMAINS = ["thenextweb.com", "www.wired.com"]

# 6, 2
BASE_URLS = [
    { "URL": "https://thenextweb.com/latest", "MAX_PAGE_LOAD": 6 },   
    { "URL": "https://www.wired.com/category/politics", "MAX_PAGE_LOAD": 2 }
]


# Configurar un User-Agent para evitar bloqueos
HEADERS =  {
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }