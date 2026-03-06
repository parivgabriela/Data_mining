# #english

# Punctuality and Cancellation Analysis: Flybondi vs. Jetsmart

## Context
This project stems from the need to integrate and apply various Data Science disciplines. 

The inspiration came after purchasing a flight from one of the analyzed companies and encountering news reports regarding their reputation for high cancellation rates during peak seasons. 
The analysis focuses on flight cancellations, identifying periods with the highest cancellation-to-flight ratios.

The goal is to demonstrate proficiency in **Web Scraping**, **Data Cleaning (Wrangling)**, and **EDA**, followed by the generation of data-driven visual reports. Both companies are Argentine low-cost carriers that compete in the same price segment with a "base fare + add-ons" business model.

## Hypothesis
It is postulated that the cancellation rate has a positive correlation with seasonal demand volume.

## Notebooks

### 1. [Scraping and Extraction](notebooks/01_scraping_y_extraccion.ipynb)
Data was extracted from [failbondi.fail](https://failbondi.fail/). This process was designed to handle request throttling and avoid IP blocking, implementing a progressive storage strategy to save information month-by-month.

**Project Walkthrough:**
[![YouTube](https://img.shields.io/badge/-YouTube-red?style=flat&logo=youtube&logoColor=white)](https://youtu.be/fiamnXitfxI)

**Tech Stack:**
* Pandas
* BeautifulSoup

### 2. [Cleaning and Transformation](notebooks/02_limpieza_transformacion.ipynb)
In this stage, raw data is processed. Key features are extracted from the "Departure Delay" column to determine total delay time, flight status, and delay levels. The output is a consolidated **Parquet** file containing cleaned data from both airlines.

**Tech Stack:**
* Pandas
* RegEx (Regular Expressions)

### 3. [EDA Report](notebooks/03_EDA_reporte.ipynb)
Exploratory analysis to uncover patterns, seasonal trends, and comparative performance between both carriers.

**Tech Stack:**
* Pandas
* Matplotlib
* Seaborn

---

# #spanish

# Análisis de Puntualidad y Cancelaciones: Aerolínea Flybondi y Jetsmart

## Contexto
La idea de este proyecto parte de la necesidad de implementar varias áreas de ciencias de datos que fui aprendiendo. 

El motivo de elegir el tema viene luego de comprar mi pasaje áereo de una de las empresas analizadas y ver una noticia en la que se le adjudica una mala reputación sobre las cancelaciones de vuelos en temporada alta. 
Procederemos con el análisis sobre los vuelos cancelados, identificando cuándo tienen mayor cantidad de cancelaciones respecto a la proporción de vuelos.

El objetivo de este proyecto es repasar los temas de **Web Scraping**, **Data Cleaning** y **EDA**, para luego proceder a realizar reportes visuales. Se utilizan datos de dos empresas low-cost del mercado argentino que compiten en la misma gama de precios.

## Hipótesis
Se postula que la tasa de cancelación tiene una correlación positiva con el volumen de demanda estacional.

## Notebooks

### 1. [Scraping y extracción](notebooks/01_scraping_y_extraccion.ipynb)
Para la extracción de datos se utilizó la página [failbondi.fail](https://failbondi.fail/). Se tomó en cuenta el uso de peticiones controladas para evitar bloqueos y se implementó un guardado de datos progresivo mes a mes.

**Explicación del proyecto:**
[![YouTube](https://img.shields.io/badge/-YouTube-red?style=flat&logo=youtube&logoColor=white)](https://www.youtube.com/watch?v=gWwsnjePJjo)

**Tecnologías Utilizadas:**
* Pandas
* BeautifulSoup

### 2. [Limpieza y transformación](notebooks/02_limpieza_transformacion.ipynb)
Se analizan los datos obtenidos y se extrae información de la columna "Demora en despegar", definiendo el tiempo de demora total, el estado del vuelo y niveles de demora. Al finalizar, se obtiene un archivo **Parquet** unificado con los datos de ambas empresas.

**Tecnologías Utilizadas:**
* Pandas
* RegEx

### 3. [Reporte EDA](notebooks/03_EDA_reporte.ipynb)
Análisis exploratorio para descubrir patrones, tendencias estacionales y rendimiento comparativo entre las aerolíneas.

**Tecnologías Utilizadas:**
* Pandas
* Matplotlib
* Seaborn