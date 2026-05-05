import pymysql


DB_CONFIG = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "CYoEw5SaBv1kIk",
    "database": "starloco_game",
    "charset": "utf8mb4",
    "use_unicode": True,
    "init_command": "SET NAMES utf8mb4",
    "cursorclass": pymysql.cursors.DictCursor,
}
