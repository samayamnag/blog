import itertools
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    title = models.CharField(max_length=50)
    slug = models.CharField(max_length=60)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        ordering = ('title',)

    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    body = models.TextField()
    meta_keywords = models.CharField(max_length=255, null=True, blank=True)
    meta_desc = models.CharField(max_length=255, null=True, blank=True)
    archived = models.BooleanField(default=False)
    categories = models.ManyToManyField(
        Category, related_name='categories', related_query_name='category'
    )
    source_url = models.CharField(max_length=255, null=True, blank=True)
    published_at = models.DateTimeField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'posts'
        verbose_name = 'post'
        verbose_name_plural = 'posts'
        ordering = ("published_at",)
        indexes = [
            models.Index(fields=['slug'], name='posts_slug_idx'),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.title = self.title.capitalize()
        self.body = self.body.capitalize()
        self.slug = self.unique_slug()
        if self.source_url is not None:
            self.source_url = self.source_url.lower()

        super().save(*args, **kwargs)

    def unique_slug(self):
        max_length = Post._meta.get_field('slug').max_length
        original_slug = slugify(self.title)[:max_length]
        for x in itertools.count(1):
            if not Post.objects.filter(slug=original_slug).exists():
                break
            return f'{original_slug[:max_length - len(str(x)) - 1]}-{x}'
        return original_slug

    def get_absolut_url(self):
        return reverse('posts:post-detail', kwargs={'pk': self.id})
