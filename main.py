from fastapi import FastAPI
from routes import auth, items

app = FastAPI(
    title="Vitibrasil Scraper API",
    description="API for retrieving viticulture data from Embrapa's Vitibrasil website.",
    version="1.0.0"
)

# Incluindo as rotas
app.include_router(auth.router, tags=["Auth"])
app.include_router(items.router, tags=["Items"])
