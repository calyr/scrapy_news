#!/bin/bash

# Ejecutar Scrapy en segundo plano
scrapy runspider wikiSpider/spiders/newsmergeSpid.py &

# Ejecutar Streamlit
streamlit run layers.py --server.address=0.0.0.0