import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

year = "2025"

months_max_days = { "01": 31, "02": 28, "03": 31, "04": 30, "05": 31, "06": 30, "07": 31, "08": 31, "09": 30, "10": 31, "11": 30, "12": 31 }
month_days = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11","12","13","14","15","16","17","18","19","20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31"]


def generate_url(date, company):
    return f"https://failbondi.fail/?date={date}&aerolinea={company}"

def get_html_from_url(url, headers):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        return soup

    return None

def scraping_vuelos(html, date, company):
    """
    Extracts flight data from an HTML table and structures it into a DataFrame.

    Args:
        html (bs4.BeautifulSoup): The BeautifulSoup object containing the parsed HTML.
        date (str or datetime): The reference date to be associated with the scraped data.

    Returns:
        pd.DataFrame: A cleaned DataFrame containing flight records, including
                      standardized dates and month extraction for grouping.
    """
    # 1. Extract headers
    headers = [th.text.strip() for th in html.find('thead').find_all('th')]

    # 2. Extraer filas
    rows = []
    table_body = html.find('tbody')
    for tr in table_body.find_all('tr'):
        cells = [td.text.strip() for td in tr.find_all('td')]
        rows.append(cells)

    # 3. Crear DataFrame
    df = pd.DataFrame(rows, columns=headers)
    df['fecha'] = date
    df['fecha'] = pd.to_datetime(df['fecha'])
    df['mes'] = df['fecha'].dt.month
    df['empresa'] = company

    return df


def get_report_by_month(year_month, max_days, company):
    lista_dfs = []
    for i in range(max_days):
        date = f"{year_month}-{month_days[i]}"
        url_link = generate_url(date, company=company)

        time.sleep(random.uniform(1.5, 3.5))

        main_content = get_html_from_url(url_link, headers)

        try:
            df_iteracion = scraping_vuelos(main_content, date, company)
            if not df_iteracion.empty:
                lista_dfs.append(df_iteracion)
        except Exception as e:
            print(f"Error en fecha {date}: {e}")
            time.sleep(10)

    if not lista_dfs: return pd.DataFrame()

    df_month = pd.concat(lista_dfs, ignore_index=True)
    print(f"[{year_month}] - Filas obtenidas: {len(df_month)}")
    return df_month
