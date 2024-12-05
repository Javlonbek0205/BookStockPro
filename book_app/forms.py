from django.forms import ModelForm
from .models import Book, Review, AdditionalInfo

class BookCreateForm(ModelForm):
    class Meta:
        model = Book
        fields = [
            'title',
            'author',
            'cover',
            'category',
            'price',
            'short_description',
            'long_description',
            'quantity',
            'isbn',
            'sku',
        ]

class ReviewCreateForm(ModelForm):
    class Meta:
        model = Review
        fields = ('rating', 'text')

class AdditionalInfoCreateForm(ModelForm):
    class Meta:
        model = AdditionalInfo
        fields = ('name', 'desc', )
