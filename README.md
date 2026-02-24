# Finanza - Stock Portfolio App

A full-stack application for managing stock portfolios, built with FastAPI (backend) and React (frontend).

## Repository

[GitHub Repository](https://github.com/giuseppepaolisi/finanza)

## Prerequisites

- Docker and Docker Compose
- Python 3.8+
- Node.js 16+
- PostgreSQL (if running locally without Docker)

## Configuration

### Environment Variables

Create a `.env` file in the root directory of the project with the following variables:

```
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_NAME=your_db_name
```

These variables are used by Docker Compose to configure the PostgreSQL database.

## Running with Docker Compose

To run the entire application (backend, frontend, and database) using Docker Compose:

```bash
docker-compose up -p
```

This will start:
- PostgreSQL database on port 5432 (internal)
- Backend API on port 8000
- Frontend on port 5173 (if configured)

## Manual Setup

### Backend Setup and Run

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   ```
   Activate virtual env
   Windows
   ```bash
   venv\Scripts\activate
   ```
   MacOS/Linux
   ```bash
   source venv/bin/activate
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the FastAPI server:
   ```bash
   python -m app.app
   ```

   The backend will be available at `http://localhost:8000`.

   To deactivate the virtual environment when done:
   ```bash
   deactivate
   ```

### Frontend Run

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install Node.js dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

The frontend will be available at `http://localhost:5173`.

## API Documentation

Once the backend is running, you can access the API documentation at `http://localhost:8000/docs` (Swagger UI) or `http://localhost:8000/redoc` (ReDoc).

## Backend Structure

The backend is built with FastAPI and follows a layered architecture for maintainability and separation of concerns. Here's an overview of the main components:

### Core (`core/`)
- **`database.py`**: Handles database connection and session management using SQLAlchemy with PostgreSQL. Includes database initialization and dependency injection for FastAPI routes.
- **`exceptions.py`**: Custom exception classes for portfolio-specific errors.
- **`logger.py`**: Logging configuration for the application.

### Models (`models/`)
- **`models.py`**: SQLAlchemy ORM models defining the database schema:
  - `Asset`: Represents stock assets with symbol, name, market, currency, current value, and update date.
  - `Transaction`: Represents buy/sell transactions linked to assets with quantity, purchase date, and price.

### Repository (`repository/`)
- **`assets_repository.py`**: Data access layer for Asset entities. Provides methods to query, add, and manage assets in the database.
- **`transaction_repository.py`**: Data access layer for Transaction entities. Handles CRUD operations for transactions.

### Services (`services/`)
- **`portfolio_service.py`**: Business logic layer that orchestrates operations between repositories and external clients. Handles portfolio calculations, transaction validation, and integration with stock market data.

### Routes (`routes/`)
- **`portfolio_routes.py`**: FastAPI route definitions for portfolio endpoints. Includes Pydantic schemas for request/response validation and dependency injection for database sessions.

### Clients (`clients/`)
- **`stock_client.py`**: External API client for fetching real-time stock data. Currently uses Yahoo Finance (yfinance) to retrieve current prices, currency, exchange, and company names.

### Main Application (`app.py`)
- Entry point for the FastAPI application. Configures CORS, registers routers, sets up startup events for database initialization, and defines global exception handlers.

### Architecture Flow
1. **API Requests** → Routes layer validates input and calls service methods
2. **Business Logic** → Services layer processes requests, interacts with repositories and external clients
3. **Data Access** → Repository layer handles database operations
4. **External Data** → Clients layer fetches real-time stock information
5. **Core Services** → Database, logging, and exception handling support all layers

This layered architecture ensures clean separation of concerns, making the codebase easier to test, maintain, and extend.