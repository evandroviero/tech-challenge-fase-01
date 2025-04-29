from pydantic import BaseModel, Field
from typing import Optional

class Viticultura(BaseModel):
    """
    Schema for viticulture data query.

    Represents the required parameters to request viticulture data from Embrapa's Vitibrasil website.
    """

    year: int = Field(..., example=2023, description="The year of the data to be retrieved")
    suboption: Optional[str] = Field(None, example="STRING", description="Specific data category depending on the selected endpoint (e.g., grape type or product class).")

    class Config:
        schema_extra = {
            "example": {
                "year": 2023,
                "suboption": "VINHOS DE MESA"
            }
        }
