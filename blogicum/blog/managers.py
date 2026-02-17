from django.db import models
from django.db.models import Count
from django.utils import timezone


class PublishedPostQuerySet(models.QuerySet):
    def published(self):
        return self.filter(
            pub_date__lte=timezone.now(),
            is_published=True,
            category__is_published=True
        )

    def with_comment_count(self):
        return self.annotate(
            comment_count=Count('comments')
        ).order_by('-pub_date',)

    def with_related(self):
        return self.select_related('author', 'location', 'category')
