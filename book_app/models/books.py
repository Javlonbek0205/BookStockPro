from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator
from django.db import models
from django_resized import ResizedImageField
from book_app.models.categories import Category


class Book(models.Model):
    title = models.CharField(max_length=225)
    author = models.CharField(max_length=225)
    cover = ResizedImageField(size=[600, 840], upload_to='books/',  validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])])
    category = models.ManyToManyField(Category, related_name='books', blank=True)
    price = models.IntegerField()
    short_description = models.CharField(max_length=512, null=True, blank=True)
    long_description = models.TextField(null=True, blank=True)
    quantity = models.IntegerField(default=0)
    isbn = models.CharField(max_length=225)
    sku = models.CharField(max_length=225)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books')

    @property
    def average_rating(self):
        reviews = self.review_set.all()
        if reviews.exists():
            return round(sum(review.rating for review in reviews) / reviews.count(), 1)
        return 0

    def __str__(self):
        return self.title



class AdditionalInfo(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    name = models.CharField(max_length=225)
    desc = models.CharField(max_length=225)



class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    text = models.CharField(max_length=1024)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}: {self.text}"