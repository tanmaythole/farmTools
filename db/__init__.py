from sqlobject.mysql import builder
from config import app_config

conn = builder()
conn = conn(
    user=app_config.DB_USER,
    password=app_config.DB_PASSWORD,
    host=app_config.DB_HOST,
    db=app_config.DB_NAME
)