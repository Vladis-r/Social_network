import json


class PostsDAO:

    def __init__(self, path):
        """Путь для загрузки постов"""
        self.path = path

    def get_posts_all(self):
        """Преобразуем посты из json в словарь"""
        with open(self.path, encoding="utf-8") as file:
            posts = json.load(file)
        return posts

    def get_posts_by_user(self, user_name):
        """Получаем пост по имени пользователя.
        Если такого поста нет - вызываем ошибку"""
        posts = self.get_posts_all()
        posts_by_user = []
        user_count = 0
        for post in posts:
            if post["poster_name"] == user_name:
                user_count += 1
                posts_by_user.append(post)
        if user_count == 0:
            raise ValueError
        return posts_by_user

    def get_comments_by_post_pk(self, post_pk):
        """Получаем комментарии к посту по его номеру.
        Если такого поста нет - вызываем ошибку"""
        with open("data/comments.json", encoding="utf-8") as file:
            comments = json.load(file)
        comments_by_post = []
        post_count = 0
        for comment in comments:
            if comment["post_pk"] == post_pk:
                comments_by_post.append(comment)
                post_count += 1
        if post_count == 0:
            raise ValueError
        else:
            return comments_by_post

    def search_for_posts(self, query):
        """Ищем посты по вхождению слова в текст поста"""
        posts = self.get_posts_all()
        posts_by_search = []
        for post in posts:
            if query.lower() in post["content"].lower():
                posts_by_search.append(post)
        return posts_by_search

    def get_post_by_pk(self, pk):
        """Получаем пост по номеру"""
        posts = self.get_posts_all()
        for post in posts:
            if post["pk"] == pk:
                return self.get_hashtags(post)

    def get_hashtags(self, post):
        """
        Ищем хештеги в поле content.
        Возвращаем пост с тегированным контентом.
        """
        content = post["content"].split()
        for word in content:
            if word[0] == '#':
                new_word = f"""<a href="/tag/{word[1:]}">{word}</a>"""
                content[content.index(word)] = new_word
        post["content"] = " ".join(content)
        return post

    def get_posts_by_hashtags(self, tag):
        """Получаем посты по хештегу"""
        posts = self.get_posts_all()
        posts_by_tag = []
        tag_count = 0
        for post in posts:
            if tag in post["content"]:
                tag_count += 1
                posts_by_tag.append(self.get_hashtags(post))
        if tag_count == 0:
            raise ValueError
        return posts_by_tag
