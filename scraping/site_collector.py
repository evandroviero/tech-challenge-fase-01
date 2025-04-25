import json
import requests
from bs4 import BeautifulSoup
import pandas as pd
from typing import Dict, Any


def fetch_page(url: str) -> BeautifulSoup:
    """Sends an HTTP request and returns the parsed HTML content."""
    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.content, 'html.parser')


def extract_table_data(soup: BeautifulSoup) -> pd.DataFrame:
    """Extracts data from the HTML table and returns a cleaned DataFrame."""
    table = soup.find('table', class_='tb_base tb_dados')
    rows = table.find_all("tr")

    data = []
    for row in rows:
        cells = row.find_all(["th", "td"])
        cells_text = [cell.get_text(strip=True) for cell in cells]
        data.append(cells_text)

    df = pd.DataFrame(data[1:], columns=data[0])
    df["Quantidade (L.)"] = df["Quantidade (L.)"].replace("-", None)
    df["Quantidade (L.)"] = (
        df["Quantidade (L.)"]
        .str.replace(".", "", regex=False)
        .astype(float)
        .fillna(0)
        .astype(int)
    )
    return df


def is_all_upper(text: str) -> bool:
    """Checks if the text is in all uppercase letters."""
    return text == text.upper()


def organize_data(df: pd.DataFrame) -> Dict[str, Dict[str, int]]:
    """Organizes DataFrame data into a hierarchical dictionary."""
    result: Dict[str, Dict[str, int]] = {}
    current_key = None

    for _, row in df.iterrows():
        product = row["Produto"]
        quantity = row["Quantidade (L.)"]

        if is_all_upper(product):
            current_key = product
            result[current_key] = {}
        elif current_key:
            result[current_key][product] = quantity
    json_result = json.dumps(result, ensure_ascii=False, indent=4)
    return json_result


def main(year: int = 2023, option: str = "02") -> Dict[str, Any]:
    """Main function to orchestrate the data collection."""
    if year < 1970 or year > 2023:
        raise ValueError("Invalid year. The valid period is between 1970 and 2024.")
    url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?ano={year}&opcao=opt_{option}"
    soup = fetch_page(url)
    df = extract_table_data(soup)
    structured_data = organize_data(df)
    return structured_data


if __name__ == "__main__":
    data = main()
    print(data)