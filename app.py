from flask import Flask
import logging
import logger
from posts_blueprint.views import posts_blueprint
from api.views import api_blueprint

logger_posts = logging.getLogger("logs_posts")

app = Flask(__name__)


@app.errorhandler(404)
def page_not_found(error):
    logger_posts.debug(f"Обращение к несуществующей странице, {error}")
    return f'Такой страницы не существует {error}', 404


@app.errorhandler(500)
def server_error(error):
    logger_posts.debug(f"Ошибка соединения с сервером: {error}")
    return f'Ошибка при попытке соединения с сервером {error}', 500


app.register_blueprint(posts_blueprint)
app.register_blueprint(api_blueprint)

if __name__ == '__main__':
    app.run(debug=True)
