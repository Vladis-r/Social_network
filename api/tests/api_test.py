import pytest

from Social_network.posts_blueprint.dao.posts_dao import PostsDAO


class TestApi:

    @pytest.fixture
    def api_posts_dao(self):
        return PostsDAO("data/data.json")

    @pytest.fixture
    def data_json_keys(self):
        return ["poster_name", "poster_avatar", "pic", "content", "views_count", "likes_count", "pk"]

    def test_type_api_posts(self, api_posts_dao):
        assert type(api_posts_dao.get_posts_all()) == list, "Посты должны передаваться списком"

    def test_keys_by_post(self, api_posts_dao, data_json_keys):
        posts = api_posts_dao.get_posts_all()
        for post in posts:
            post_keys = list(post.keys())
            assert post_keys == data_json_keys, "У элемента нет нужных ключей"

    def test_type_api_post(self, api_posts_dao):
        posts = api_posts_dao.get_posts_all()
        for post in posts:
            assert type(post) == dict, "Должен возвращаться словарь"
