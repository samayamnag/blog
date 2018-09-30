import factory
from .models import Post
from django.contrib.auth import get_user_model
from faker import Factory


User = get_user_model()
faker = Factory.create()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username',)

    username = factory.Sequence(lambda n: f'username_{n}')
    email = factory.LazyAttribute(
        lambda obj: f'{obj.username}@example.com')
    password = factory.PostGenerationMethodCall('set_password', 'secret')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    title = factory.Sequence(lambda n: "Test title - %01d" % n)
    body = faker.paragraph(nb_sentences=5)


"""
from posts.factories import PostFactory
post = PostFactory()
post = PostFactory.create_batch(100)
"""
