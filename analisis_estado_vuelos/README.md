
# Análisis de Puntualidad y Cancelaciones: Aerolínea Flybondi y Jetsmart

## Contexto

La idea de este proyecto parte de la necesidad de implementar varias áreas de ciencias de datos que fui aprendiendo. 

El motivo de elegir el tema viene luego de comprar mi pasaje áereo de una de las empresas analizadas y ver una noticia en la que se le adjudica que tiene un mala reputación sobre las cancelaciones de vuelos en temporada alta.
Vamos a proceder con el analísis sobre los vuelos cancelados, cuando tiene mayor cantidad de cancelaciones respecto a la proporción de vuelos. 

El objetivo con este proyecto quiero repasar los temas de web scrapping, data cleaning y EDA, para luego proceder a realizar reportes visuales.

Se utilizaran los datos de dos empresas low cost que tienen como finalidad vender los boletos en tarifa base y luego para cada cosa cobran como adicional. Dentro del mercado argentino se manejan dentro de la misma gama de precios.

## Hipótesis

Se postula que la tasa de cancelación tiene una correlación positiva con el volumen de demanda estacional.


## Notebooks
[**Scraping y extracción**](notebooks/01_scraping_y_extraccion.ipynb): Para la extracción de datos de los vuelos se utilizó la página https://failbondi.fail/ para esta operación se tomo en cuenta el uso excesivo de las peticiones y evitar el bloqueo, asi también el guardado de datos progresivo para ir guardando la información mes a mes.

### Tecnologías Utilizadas
- Pandas
- BeautifulSoup

[**Limpieza y transformación**](notebooks/02_limpieza_transformacion.ipynb): Se analizan los datos obtenidos en el paso anterior, y se extrae data extra que hay en la columna de "Demora en despegar", donde podemos encontrar el tiempo de demora total de un vuelo o si se cancelo, así definir un nivel de demora, o el estado del vuelo. Al finalizar este notebook se obtiene un archivo parquet con todos los datos de ambas enpresas en un solo archivo.

### Tecnologías Utilizadas
- Pandas
- RegEx

[**Reporte EDA**](notebooks/03_EDA_reporte.ipynb):

### Tecnologías Utilizadas
- Pandas
- Matplot
- Seaborn