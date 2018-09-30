from rest_framework import status
from rest_framework.test import APITestCase
from posts.models import Post
from posts.factories import PostFactory
from rest_framework.reverse import reverse


class TestPostView(APITestCase):

    def test_empty_post_list(self):
        Post.objects.all().delete()
        url = reverse('api-posts:post-list')
        response = self.client.get(url, format="json")

        self.assertEqual(len(response.data['results']), 0)

    def test_post_list(self):
        PostFactory.create_batch(20)
        url = reverse('api-posts:post-list')
        response = self.client.get(url, {'page_size': 15}, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 15)

    def test_post_detail(self):
        PostFactory.create(title="My first entry", body="Test descritpion")
        url = reverse('api-posts:post-detail', args=[1])
        response = self.client.get(url, {}, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
                "id": 1,
                "title": "My first entry",
                "body": "Test descritpion",
                "slug": "my-first-entry",
                "source_url": None
            }
        )
