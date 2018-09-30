from django.test import TestCase
from posts.models import Category, Post


class TestPostModel(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_string_representation(self):
        post = Post(title="My entry title")
        self.assertEqual(str(post), post.title)

    def test_verbose_name_plural(self):
        self.assertEqual(str(Post._meta.verbose_name_plural), 'posts')


class TestCategoryModel(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_string_representation(self):
        category = Category(title="Category entry title")
        self.assertEqual(str(category), category.title)

    def test_verbose_name_plural(self):
        self.assertEqual(str(Category._meta.verbose_name_plural), 'categories')
