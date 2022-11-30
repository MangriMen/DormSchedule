import os
import tempfile

DB_TYPE = "sqlite"
DB_NAME = "schedule"
DB_EXTENSION = "sqlite3"
# PATH_TO_DB = os.path.join(tempfile.gettempdir(), f"{DB_NAME}.{DB_EXTENSION}")
PATH_TO_DB = f"{DB_NAME}.{DB_EXTENSION}"

SQLITE_ENGINE_CONNECTION = f"{DB_TYPE}:///{PATH_TO_DB}"