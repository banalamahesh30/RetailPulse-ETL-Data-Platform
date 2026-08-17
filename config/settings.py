from pathlib import Path



PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
TRANSFORMED_DATA_DIR = DATA_DIR / "Transformed"
WAREHOUSE_DATA_DIR = DATA_DIR / "warehouse"

PYTHON_DIR = PROJECT_ROOT / "python"
DATABRICKS_DIR = PROJECT_ROOT / "databricks"
SNOWFLAKE_DIR = PROJECT_ROOT / "snowflake"
LOG_DIR = PROJECT_ROOT / "logs"
DOCUMENTATION_DIR = PROJECT_ROOT / "documentation"



LOG_DIR.mkdir(parents=True, exist_ok=True)

SOURCE_TABLES = [
    "customers",
    "products",
    "sellers",
    "orders",
    "order_items",
    "payments",
    "shipments",
    "returns",
    "reviews",
    "warehouses"
]




RAW_FILE_FORMAT = "parquet"
TRANSFORMED_FILE_FORMAT = "parquet"