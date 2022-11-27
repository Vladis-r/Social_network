import pytest
import json

from ..dao.posts_dao import PostsDAO


class TestPostsDAO:

    @pytest.fixture
    def posts_dao(self):
        return PostsDAO("data/data.json")

    @pytest.fixture
    def data_json_keys(self):
        return ["poster_name", "poster_avatar", "pic", "content", "views_count", "likes_count", "pk"]

    @pytest.fixture
    def comments_json_keys(self):
        return ["post_pk", "commenter_name", "comment", "pk"]

    def test_get_posts_all(self, posts_dao, data_json_keys):
        """Проверяет, что данные постов верны"""
        posts = posts_dao.get_posts_all()
        assert type(posts) == list, "Тип всех постов должен быть список"
        for post in posts:
            assert type(post) == dict, "Тип каждого поста должен быть словарь"
            post_keys = list(post.keys())
            assert post_keys == data_json_keys, "Ключи в файле data.json должны соответствовать принятому образцу"

    def test_get_comments(self, comments_json_keys):
        """Проверяет, что данные комментариев верны"""
        with open("data/comments.json", encoding="utf-8") as file:
            comments = json.load(file)
        assert type(comments) == list, "Тип файлов в комментариях должен быть список"
        for comment in comments:
            assert type(comment) == dict, "Тип каждого комментария должен быть словарь"
            comment_keys = list(comment.keys())
            assert comment_keys == comments_json_keys, "Ключи в файле comments.json должны соответствовать принятому образцу"
