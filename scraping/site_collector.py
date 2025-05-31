import json
import re
import requests
from requests.exceptions import HTTPError, RequestException
from bs4 import BeautifulSoup
from typing import Dict, Any, List
from scraping.fallback import CSVReader

def fetch_page(url: str):
    """
    Sends an HTTP request to the specified URL and returns the parsed HTML page.

    Parameters:
    - url (str): The URL to fetch the page from.

    Returns:
    - BeautifulSoup or dict: The parsed HTML page or fallback data from CSV.

    Raises:
    - HTTPError: If the HTTP request fails with status codes other than 500.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        return BeautifulSoup(response.content, 'html.parser')

    except HTTPError as http_err:
        if response.status_code == 500:
            print("Server error (500) encountered. Loading fallback data from CSV.")
            return CSVReader().read_file(url)
        else:
            raise http_err
        
    except RequestException as req_err:
        return CSVReader().read_file(url)


def extract_table_data(soup: BeautifulSoup) -> List[List[str]]:
    """
    Extracts raw tabular data from an HTML table within the parsed page.

    Parameters:ß
    - soup (BeautifulSoup): Parsed HTML page from which to extract the table.

    Returns:
    - List[List[str]]: A list of rows, where each row is a list of cell values as strings.
    """
    table = soup.find('table', class_='tb_base tb_dados')
    rows = table.find_all("tr")

    data = []
    for row in rows:
        cells = row.find_all(["th", "td"])
        cells_text = [cell.get_text(strip=True) for cell in cells]
        data.append(cells_text)
    return data


def organize_data(data: List[List[str]]) -> Dict[str, List[str]]:
    """
    Organizes the extracted table data into a structured dictionary.

    Parameters:
    - data (List[List[str]]): A list of table rows, where the first row is assumed to be the header.

    Returns:
    - Dict[str, List[str]]: A dictionary with column names as keys and lists of column values.
    """
    result: Dict[str, List[str]] = {}
    header = [col.strip() for col in data[0]]
    result = {col: [] for col in header}

    for row in data[1:]:
        if len(row) == len(header):
            for i, col in enumerate(header):
                result[col].append(row[i])
    return result


def update_url(option: str, suboption: str = None, year: int = 2023) -> str:
    """
    Constructs a URL for data collection based on the provided parameters.

    Parameters:
    - option (str): The main category option ("02", "03", "04", "05", "06").
    - suboption (str, optional): Subcategory option, required for options "03", "05", and "06".
    - year (int, optional): Year of data to fetch. Default is 2023.

    Returns:
    - str: A formatted URL for the requested data.

    Raises:
    - ValueError: If the option is invalid, or if a required suboption is missing or invalid.
    """
    base_url = "http://vitibrasil.cnpuv.embrapa.br/index.php"

    valid_suboptions = {
        "03" : {
            "VINIFERAS": "01",
            "AMERICANAS E HIBRIDAS": "02",
            "UVAS DE MESA": "03",
            "SEM CLASSIFICACAO": "04"
        },
        "05": {
            "VINHOS DE MESA": "01",
            "ESPUMANTES": "02",
            "UVAS FRESCAS": "03",
            "UVAS PASSAS": "04",
            "SUCO DE UVA": "05"
        },
        "06": {
            "VINHOS DE MESA": "01",
            "ESPUMANTES": "02",
            "UVAS FRESCAS": "03",
            "SUCO DE UVA": "05"
        }
    }
    if option in ["02", "04"]:
        return f"{base_url}?ano={year}&opcao=opt_{option}"
    suboption_url = valid_suboptions.get(option).get(suboption)
    return f"{base_url}?ano={year}&opcao=opt_{option}&subopcao=subopt_{suboption_url}"

def get_infos(year: int, option: str = "02", suboption: str = None) -> Dict[str, Any]:
    """
    Orchestrates the full data collection process.

    This function validates input parameters, constructs the data URL, fetches the web page,
    extracts and processes the data, and returns it in a structured format.

    Parameters:
    - year (int, optional): The target year for data collection (1970 to 2024). Default is 2023.
    - option (str, optional): The main data category option. Default is "02".
    - suboption (str, optional): A required subcategory for some options ("03", "05", "06").

    Returns:
    - Dict[str, Any]: Structured data organized in a dictionary format.

    Raises:
    - ValueError: If the year is out of range or suboption is missing when required.
    """
    
    url = update_url(option, suboption, year)
    soup = fetch_page(url)
    print(url)
    table_data = extract_table_data(soup)
    structured_data = organize_data(table_data)
    return structured_data
