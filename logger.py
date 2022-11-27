import logging

# создаём логгер logger_posts и устанавливаем уровень
logger_posts = logging.getLogger("logs_posts")
logger_posts.setLevel("DEBUG")

# создаём логгер logger_api и устанавливаем уровень
logger_api = logging.getLogger("logs_api")
logger_api.setLevel("DEBUG")

# создаем файл-хендлер
handler_posts = logging.FileHandler("logs/logs_posts.log", "a", "utf-8")
handler_api = logging.FileHandler("logs/logs_api.log", "a", "utf-8")

# добавляем файл-хендлер к логгеру
logger_posts.addHandler(handler_posts)
logger_api.addHandler(handler_api)

# создаем форматтер
formatter_posts = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
formatter_api = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

# добавляем форматтер к логгеру
handler_posts.setFormatter(formatter_posts)
handler_api.setFormatter(formatter_api)
