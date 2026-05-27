import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from infrastructure.adapters.input.valuation_router import router as valuation_router
from infrastructure.adapters.input.discovery_router import router as discovery_router

app = FastAPI(
    title="Equity Valuation Engine API",
    description="API for the Equity Valuation Engine, focused on Value Investing fundamentals and advanced analysis.",
    version="1.0.0"
)

app.include_router(valuation_router)
app.include_router(discovery_router)

@app.get("/", include_in_schema=False)
def root():
    """
    Redirects the main page (/) directly to the Swagger UI (/docs).
    """
    return RedirectResponse(url="/docs")

if __name__ == "__main__":
    import uvicorn
    from infrastructure.config.settings import settings
    
    print(f"Starting FastAPI server on {settings.host}:{settings.port}...")
    uvicorn.run("api_main:app", host=settings.host, port=settings.port, reload=True)
