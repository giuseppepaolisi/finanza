class PortfolioException(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code

class AssetNotFoundError(PortfolioException):
    def __init__(self, symbol: str):
        super().__init__(f"L'asset '{symbol}' non è presente nel tuo portafoglio.", 404)