import re
from typing import Dict, Optional, Tuple
import pandas as pd


class CSVReader:
    """
    A class to manage reading multiple CSV files with custom delimiters,
    and extracting option parameters from URLs using regex.
    """

    def __init__(self) -> None:
        self.csv_path: Dict[str, Tuple[str, str]] = {
            "comercio": ("datasets/Comercio.csv", ";"),
            "exp_espumantes": ("datasets/ExpEspumantes.csv", "\t"),
            "exp_suco": ("datasets/ExpSuco.csv", "\t"),
            "exp_uva": ("datasets/ExpUva.csv", "\t"),
            "exp_vinho": ("datasets/ExpVinho.csv", "\t"),
            "imp_espumante": ("datasets/ImpEspumantes.csv", "\t"),
            "imp_frescas": ("datasets/ImpFrescas.csv", "\t"),
            "imp_passas": ("datasets/ImpPassas.csv", "\t"),
            "imp_suco": ("datasets/ImpSuco.csv", ";"),
            "imp_vinhos": ("datasets/ImpVinhos.csv", "\t"),
            "processa_americanas": ("datasets/ProcessaAmericanas.csv", "\t"),
            "processa_mesa": ("datasets/ProcessaMesa.csv", "\t"),
            "processa_sem_class": ("datasets/ProcessaSemclass.csv", "\t"),
            "processa_viniferas": ("datasets/ProcessaViniferas.csv", ";"),
            "producao": ("datasets/Producao.csv", ";"),
        }

    def read_file(self, url: str) -> str:
        """
        Reads a CSV file based on URL parameters and returns the content as a JSON string.

        Parameters:
        - url (str): The URL containing 'opcao' and 'subopcao' parameters.

        Returns:
        - str: JSON string representation of the CSV content.

        Raises:
        - ValueError: If the URL or extracted options are invalid.
        - FileNotFoundError: If the file path does not exist.
        - RuntimeError: For other read failures.
        """
        filepath, delimiter = self._extract_path_from_url(url)
        try:
            df = pd.read_csv(filepath, sep=delimiter)
            return df.to_json(orient="records", force_ascii=False)
        except FileNotFoundError as fnf_error:
            raise FileNotFoundError(f"File not found: {filepath}") from fnf_error
        except Exception as e:
            raise RuntimeError(f"Failed to read CSV from {filepath}: {e}") from e

    def _extract_path_from_url(self, url: str) -> Tuple[str, str]:
        """
        Extracts the CSV path and delimiter from the URL.

        Parameters:
        - url (str): URL containing 'opcao' and 'subopcao'.

        Returns:
        - Tuple[str, str]: (file path, delimiter)

        Raises:
        - ValueError: If the URL or parameters are invalid.
        """
        opcao, subopcao = self._parse_url(url)
        path_info = self._resolve_path(opcao, subopcao)

        if not path_info:
            raise ValueError(f"Invalid opcao/subopcao combination: {opcao}, {subopcao}")
        return path_info

    def _parse_url(self, url: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Uses regex to parse 'opcao' and 'subopcao' from a URL.

        Parameters:
        - url (str): The URL to parse.

        Returns:
        - Tuple[Optional[str], Optional[str]]: Extracted opcao and subopcao.
        """
        opcao_match = re.search(r'opcao=(opt_0[1-6])', url)
        subopcao_match = re.search(r'subopcao=(subopt_0[1-6])', url)

        opcao = opcao_match.group(1) if opcao_match else None
        subopcao = subopcao_match.group(1) if subopcao_match else None
        return opcao, subopcao

    def _resolve_path(self, opcao: Optional[str], subopcao: Optional[str]) -> Optional[Tuple[str, str]]:
        """
        Maps opcao/subopcao combination to the corresponding CSV path and delimiter.

        Parameters:
        - opcao (Optional[str])
        - subopcao (Optional[str])

        Returns:
        - Optional[Tuple[str, str]]: Corresponding CSV path and delimiter.
        """
        if opcao == "opt_02":
            return self.csv_path.get("producao")

        if opcao == "opt_03":
            return {
                "subopt_01": self.csv_path.get("processa_viniferas"),
                "subopt_02": self.csv_path.get("processa_americanas"),
                "subopt_03": self.csv_path.get("processa_mesa"),
                "subopt_04": self.csv_path.get("processa_sem_class"),
            }.get(subopcao)

        if opcao == "opt_04":
            return self.csv_path.get("comercio")

        if opcao == "opt_05":
            return {
                "subopt_01": self.csv_path.get("imp_vinhos"),
                "subopt_02": self.csv_path.get("imp_espumante"),
                "subopt_03": self.csv_path.get("imp_frescas"),
                "subopt_04": self.csv_path.get("imp_passas"),
                "subopt_05": self.csv_path.get("imp_suco"),
            }.get(subopcao)

        if opcao == "opt_06":
            return {
                "subopt_01": self.csv_path.get("exp_vinho"),
                "subopt_02": self.csv_path.get("exp_espumantes"),
                "subopt_03": self.csv_path.get("exp_uva"),
                "subopt_04": self.csv_path.get("exp_suco"),
            }.get(subopcao)

        return None
