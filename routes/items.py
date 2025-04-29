from fastapi import APIRouter, HTTPException, Depends, status
from models.item import Viticultura
from core.security import verify_token
from scraping.site_collector import get_infos

router = APIRouter()

@router.get("/")
async def home(username: str = Depends(verify_token)):
    """
    Returns a welcome message for authenticated users.

    - Requires a valid authentication token.
    - Responds with a personalized greeting.
    """
    return f"Hello, {username}! You are authenticated."

@router.post("/producao")
async def post_producao_info(item: Viticultura, username: str = Depends(verify_token)):
    """
    Retrieves grape production data from the Embrapa Vitibrasil website.

    - **Valid year range:** 1970 to 2023
    - Requires a valid authentication token.
    - Returns tabular data for grape production.
    """
    if item.year < 1970 or item.year > 2023:
        raise HTTPException(status_code=400, detail="Invalid year. The valid period is between 1970 and 2023.")
    return get_infos(
        year=item.year,
        option="02",
        suboption=item.suboption
    )

@router.post("/processamento")
async def post_processamento_info(item: Viticultura, username: str = Depends(verify_token)):
    """
    Retrieves grape processing data from the Embrapa Vitibrasil website.

    - **Valid year range:** 1970 to 2023
    - **Allowed suboptions:** "VINIFERAS", "AMERICANAS E HIBRIDAS", "UVAS DE MESA", "SEM CLASSIFICACAO"
    - Requires a valid authentication token.
    - Returns processed grape quantity by type.
    """
    if item.year < 1970 or item.year > 2023:
        raise HTTPException(status_code=400, detail="Invalid year. The valid period is between 1970 and 2023.")
    suboption = ["VINIFERAS", "AMERICANAS E HIBRIDAS", "UVAS DE MESA", "SEM CLASSIFICACAO"]
    if item.suboption is None or item.suboption.upper() not in suboption:
        raise HTTPException(status_code=400, detail=f"Invalid suboption '{suboption}' for option 'processamento'. ")
    return get_infos(
        year=item.year,
        option="03",
        suboption=item.suboption.upper()
    )

@router.post("/comercializacao")
async def post_comercializacao_info(item: Viticultura, username: str = Depends(verify_token)):
    """
    Retrieves commercialization data for grapes and derivatives.

    - **Valid year range:** 1970 to 2023
    - Requires a valid authentication token.
    - Returns commercialization data segmented by type or region.
    """
    if item.year < 1970 or item.year > 2023:
        raise HTTPException(status_code=400, detail="Invalid year. The valid period is between 1970 and 2023.")
    return get_infos(
        year=item.year,
        option="04",
        suboption=item.suboption
    )

@router.post("/importacao")
async def post_importacao_info(item: Viticultura, username: str = Depends(verify_token)):
    """
    Retrieves import data for grapes and grape-related products.

    - **Valid year range:** 1970 to 2024
    - **Allowed suboptions:** "VINHOS DE MESA", "ESPUMANTES", "UVAS FRESCAS", "UVAS PASSAS", "SUCO DE UVA"
    - Requires a valid authentication token.
    - Returns import statistics by product category.
    """
    if item.year < 1970 or item.year > 2024:
        raise HTTPException(status_code=400, detail="Invalid year. The valid period is between 1970 and 2024.")
    suboption = ["VINHOS DE MESA", "ESPUMANTES", "UVAS FRESCAS", "UVAS PASSAS",  "SUCO DE UVA"]
    if item.suboption is None or item.suboption.upper() not in suboption:
        raise HTTPException(status_code=400, detail=f"Invalid suboption '{suboption}' for option 'importacao'. ")
    return get_infos(
        year=item.year,
        option="05",
        suboption=item.suboption.upper()
    )

@router.post("/exportacao")
async def post_exportacao_info(item: Viticultura, username: str = Depends(verify_token)):
    """
    Retrieves export data for grapes and grape-related products.

    - **Valid year range:** 1970 to 2024
    - **Allowed suboptions:** "VINHOS DE MESA", "ESPUMANTES", "UVAS FRESCAS", "SUCO DE UVA"
    - Requires a valid authentication token.
    - Returns export statistics by product category.
    """
    if item.year < 1970 or item.year > 2024:
        raise HTTPException(status_code=400, detail="Invalid year. The valid period is between 1970 and 2024.")
    suboption = ["VINHOS DE MESA", "ESPUMANTES", "UVAS FRESCAS",  "SUCO DE UVA"]
    if item.suboption is None or item.suboption.upper() not in suboption:
        raise HTTPException(status_code=400, detail=f"Invalid suboption '{suboption}' for option 'processamento'. ")
    return get_infos(
        year=item.year,
        option="06",
        suboption=item.suboption.upper()
    )

