import json
from flask import Blueprint, render_template, request, redirect
import logging
import logger

from .dao.posts_dao import PostsDAO

logger_posts = logging.getLogger("logs_posts")

posts_blueprint = Blueprint("posts_blueprint", __name__, template_folder="templates")
posts_dao = PostsDAO("data/data.json")


@posts_blueprint.route("/")
def posts_page():
    """Главная страница со всеми постами"""
    try:
        logger_posts.debug(f"Получаем все посты на странице /")
        posts = posts_dao.get_posts_all()
        with open("data/bookmarks.json", 'r', encoding='utf-8') as file_read:
            data = json.load(file_read)
            len_bookmarks = len(data)
        return render_template("index.html", posts=posts, len_bookmarks=len_bookmarks)
    except Exception:
        return logger_posts.debug(f"Произошла ошибка при запросе к главной /")


@posts_blueprint.route("/post/<int:post_pk>")
def post_page(post_pk):
    """Страница поста по его номеру"""
    logger_posts.debug(f"Получаем пост {post_pk} на странице /post/{post_pk}")
    post = posts_dao.get_post_by_pk(post_pk)
    try:
        logger_posts.debug(f"Получаем комментарии для поста {post_pk} на странице /post/{post_pk}")
        comments = posts_dao.get_comments_by_post_pk(post_pk)
        len_comments = len(comments)
    except ValueError:
        comments = []
        len_comments = 0
    except Exception as e:
        logger_posts.error(e, exc_info=True)
        return e, 500
    return render_template("post.html", post=post, comments=comments, len_comments=len_comments)


@posts_blueprint.route("/search/")
def search_page():
    """Страница с постами по поиску"""
    try:
        query = request.args.get("s")
        logger_posts.debug(f"Получаем посты по поиску: {query} на странице /search/{query}")
        posts_by_search = posts_dao.search_for_posts(query)
        len_posts = len(posts_by_search)
    except Exception as e:
        logger_posts.error(e, exc_info=True)
        return e, 500
    return render_template("search.html", posts_by_search=posts_by_search, len_posts=len_posts)


@posts_blueprint.route("/user/<user_name>")
def user_page(user_name):
    """Страница с постами по имени пользователя"""
    try:
        logger_posts.debug(f"Получаем посты по имени пользователя: {user_name} на странице /user/{user_name}")
        posts_by_user = posts_dao.get_posts_by_user(user_name)
    except Exception as e:
        logger_posts.error(e, exc_info=True)
        return e, 500
    return render_template("user-feed.html", posts_by_user=posts_by_user)


@posts_blueprint.route("/tag/<tag_name>")
def tags_page(tag_name):
    """Страница с постами по хештегу"""
    logger_posts.debug(f"Получаем посты по тегу: #{tag_name} на странице /tag/{tag_name}")
    try:
        logger_posts.debug(f"Получаем посты по тегу: {tag_name} на странице /tag/{tag_name}")
        posts_by_tag = posts_dao.get_posts_by_hashtags(f"#{tag_name}")
    except Exception as e:
        logger_posts.error(e, exc_info=True)
        return e, 500
    return render_template("tag.html", posts_by_tag=posts_by_tag, tag_name=tag_name)


@posts_blueprint.route("/bookmarks/add/<int:post_pk>")
def add_bookmark(post_pk):
    """
    Добавить пост в закладку.
    Перенаправление на главную.
    """
    logger_posts.debug(f"Добавляем пост {post_pk} в закладки")
    post = posts_dao.get_post_by_pk(post_pk)

    with open("data/bookmarks.json", 'r', encoding='utf-8') as file_read:
        data = json.load(file_read)
        if post not in data:
            data.append(post)
        with open("data/bookmarks.json", 'w', encoding='utf-8') as file_write:
            json.dump(data, file_write)
    return redirect("/", code=302)


@posts_blueprint.route("/bookmarks/remove/<int:post_pk>")
def remove_bookmark(post_pk):
    """
    Удалить пост из закладок.
    Перенаправление на главную.
    """
    logger_posts.debug(f"Удаляем пост {post_pk} из закладок")
    post = posts_dao.get_post_by_pk(post_pk)

    with open("data/bookmarks.json", 'r', encoding='utf-8') as file_read:
        data = json.load(file_read)
        if post in data:
            data.remove(post)
        with open("data/bookmarks.json", 'w', encoding='utf-8') as file_write:
            json.dump(data, file_write)
    return redirect("/", code=302)


@posts_blueprint.route("/bookmarks/")
def bookmarks_page():
    """
    Посмотреть все закладки
    """
    logger_posts.debug(f"Открываем страницу /bookmarks/")
    with open("data/bookmarks.json", 'r', encoding='utf-8') as file:
        bookmarks = json.load(file)
    return render_template("bookmarks.html", bookmarks=bookmarks)
