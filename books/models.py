from django.conf import settings
from django.db import models

class Book(models.Model):
    STATUS_CHOICES = [
        ('reading', 'Reading'),
        ('completed', 'Completed'),
        ('plan_to_read', 'Plan to Read'),
    ]

    GENRE_CHOICES = [
        ('Business', 'Business'),
        ('Poetry', 'Poetry'),
        ('Romance', 'Romance'),
        ('Fantasy', 'Fantasy'),
        ('Fiction', 'Fiction'),
        ('Self-Help', 'Self-Help'),
        ('Science', 'Science'),
        ('Classic', 'Classic'),
        ('Science-Fiction', 'Science-Fiction'),
        ('Drama', 'Drama'),
    ]

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='books'
    )
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=150)
    genre = models.CharField(max_length=100, choices=GENRE_CHOICES)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='plan_to_read'
    )
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    cover_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def _str_(self):
        return f'{self.title} - {self.owner.username}'