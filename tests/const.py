from pydantic import AnyHttpUrl

PROJECT_NAME = "family_budget"
LOG_LEVEL = "local"
ENVIRONMENT = "test"
HOST: str = "0.0.0.0"
PORT: int = 8080
DB_NAME = "test_family_budget"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_USER = "test_family_budget"
DB_PASSWORD = "test_family_budget"
DB_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
BACKEND_CORS_ORIGINS = ["*"]

JWT_SECRET_KEY = "test"
JWT_REFRESH_SECRET_KEY = "test"
