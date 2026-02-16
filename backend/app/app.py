from fastapi.responses import JSONResponse
import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from core.exceptions import PortfolioException
from routes.portfolio_routes import router as portfolio_router
from core.database import init_db
from core.logger import setup_logger

logger = setup_logger(__name__)

init_db()  # Inizializza il database all'avvio dell'app

app = FastAPI(title="Stock Portfolio API")

# Configurazione CORS
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrazione dei router
app.include_router(portfolio_router)

@app.get("/")
async def root():
    return {"status": "API is running"}

# Gestione globale delle eccezioni personalizzate
@app.exception_handler(PortfolioException)
async def portfolio_exception_handler(request: Request, exc: PortfolioException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": True, "message": exc.message},
    )

if __name__ == "__main__":
    logger.info("Starting the API server...")
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)