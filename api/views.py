from flask import jsonify, Blueprint
import logging
import logger
from posts_blueprint.dao.posts_dao import PostsDAO

logger_api = logging.getLogger("logs_api")

api_blueprint = Blueprint("api_blueprint", __name__)
api_posts_dao = PostsDAO("data/data.json")


@api_blueprint.route("/api/posts")
def get_all_posts_json():
    """Функция для передачи всех постов в json"""
    logger_api.info(f"Запрос api/posts")
    json_posts = jsonify(api_posts_dao.get_posts_all())
    return json_posts


@api_blueprint.route("/api/posts/<int:post_pk>")
def get_post_by_pk_json(post_pk):
    """Функция для передачи одного поста в json"""
    logger_api.info(f"Запрос api/posts/{post_pk}")
    json_post_by_pk = jsonify(api_posts_dao.get_post_by_pk(post_pk))
    return json_post_by_pk

